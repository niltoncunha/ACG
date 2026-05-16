#!/usr/bin/env python3
"""ACG enforcement runner.

No external dependencies. Designed for local use and CI.

Core checks:
- branch is not the configured default branch;
- changed files stay inside task.scope.allowed;
- changed files do not touch task.scope.forbidden;
- verification commands run outside the agent;
- evidence is written to acg-evidence.jsonl;
- promotion fails closed when evidence is missing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any

EVIDENCE_FILE = Path("acg-evidence.jsonl")
LOG_DIR = Path("acg-logs")
DEFAULT_EXCLUDES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "coverage",
    LOG_DIR.name,
}
GENERATED_FILES = {EVIDENCE_FILE.name}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def run_process(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def git(args: list[str], cwd: Path, allow_fail: bool = False) -> str:
    cp = run_process(["git", *args], cwd=cwd)
    if cp.returncode != 0:
        if allow_fail:
            return ""
        raise RuntimeError(cp.stdout.strip())
    return cp.stdout.strip()


def clean_value(value: str) -> Any:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    low = value.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    return value


def parse_yaml_subset(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    cfg: dict[str, Any] = {
        "project": {},
        "task": {"scope": {"allowed": [], "forbidden": []}, "done_when": []},
        "verify": {"commands": []},
        "promotion": {},
    }
    section = None
    sub = None
    last_done = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        text = line.strip()
        if indent == 0 and text.endswith(":"):
            section = text[:-1]
            sub = None
            last_done = None
            continue
        if section in {"project", "promotion"} and indent >= 2 and ":" in text:
            key, value = text.split(":", 1)
            cfg[section][key.strip()] = clean_value(value)
            continue
        if section == "task":
            if indent == 2 and text == "scope:":
                sub = "scope"
                continue
            if indent == 2 and text == "done_when:":
                sub = "done_when"
                continue
            if indent == 2 and ":" in text and sub is None:
                key, value = text.split(":", 1)
                cfg["task"][key.strip()] = clean_value(value)
                continue
            if sub in {"scope", "scope.allowed", "scope.forbidden"} and indent == 4 and text.endswith(":"):
                sub = "scope." + text[:-1]
                continue
            if sub in {"scope.allowed", "scope.forbidden"} and indent >= 6 and text.startswith("-"):
                target = sub.split(".", 1)[1]
                cfg["task"]["scope"].setdefault(target, []).append(clean_value(text[1:]))
                continue
            if sub == "done_when" and indent >= 4:
                if text.startswith("-") and ":" in text:
                    key, value = text[1:].strip().split(":", 1)
                    last_done = {key.strip(): clean_value(value)}
                    cfg["task"]["done_when"].append(last_done)
                    continue
                if last_done is not None and ":" in text:
                    key, value = text.split(":", 1)
                    last_done[key.strip()] = clean_value(value)
                    continue
        if section == "verify":
            if indent == 2 and text == "commands:":
                sub = "commands"
                continue
            if sub == "commands" and indent >= 4 and text.startswith("-"):
                cfg["verify"].setdefault("commands", []).append(clean_value(text[1:]))
                continue
    return cfg


def current_branch(root: Path) -> str:
    return os.environ.get("GITHUB_HEAD_REF") or git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=root, allow_fail=True) or "unknown"


def append_evidence(cfg: dict[str, Any], root: Path, step: str, status: str, extra: dict[str, Any] | None = None) -> None:
    event = {
        "task_id": cfg.get("task", {}).get("id", "unknown-task"),
        "timestamp": now(),
        "step": step,
        "status": status,
        "branch": current_branch(root),
        "commit": git(["rev-parse", "HEAD"], cwd=root, allow_fail=True) or None,
    }
    if extra:
        event.update(extra)
    with (root / EVIDENCE_FILE).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def ref_exists(root: Path, ref: str) -> bool:
    return run_process(["git", "rev-parse", "--verify", ref], cwd=root).returncode == 0


def list_from_git(root: Path, args: list[str]) -> list[str]:
    out = git(args, cwd=root, allow_fail=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def normalize_repo_path(path: str) -> str | None:
    path = str(path).strip().replace("\\", "/")
    if not path or path.startswith("/") or re.match(r"^[A-Za-z]:/", path):
        return None
    parts = path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return None
    if any(part in DEFAULT_EXCLUDES for part in parts):
        return None
    if path in GENERATED_FILES:
        return None
    return "/".join(parts)


def changed_files(root: Path, default_branch: str) -> list[str]:
    paths: set[str] = set()
    base = os.environ.get("GITHUB_BASE_REF") or default_branch
    for ref in (f"origin/{base}", base):
        if ref_exists(root, ref):
            merge_base = git(["merge-base", ref, "HEAD"], cwd=root, allow_fail=True)
            if merge_base:
                paths.update(list_from_git(root, ["diff", "--name-only", f"{merge_base}..HEAD"]))
    paths.update(list_from_git(root, ["diff", "--name-only"]))
    paths.update(list_from_git(root, ["diff", "--cached", "--name-only"]))
    paths.update(list_from_git(root, ["ls-files", "--others", "--exclude-standard"]))
    normalized = [item for p in paths if (item := normalize_repo_path(p)) is not None]
    return sorted(set(normalized))


def matches(path: str, patterns: list[str]) -> bool:
    for pattern in patterns or []:
        p = str(pattern).replace(os.sep, "/").replace("\\", "/").strip()
        if p.startswith("./"):
            p = p[2:]
        if p in {"*", "**"}:
            return True
        if p.endswith("/**") and path.startswith(p[:-3].rstrip("/") + "/"):
            return True
        if fnmatch.fnmatch(path, p):
            return True
    return False


def check_branch(cfg: dict[str, Any], root: Path) -> None:
    default = str(cfg.get("project", {}).get("default_branch", "main"))
    branch = current_branch(root)
    ok = branch != default
    append_evidence(cfg, root, "branch", "passed" if ok else "failed", {"branch": branch, "default_branch": default})
    if not ok:
        raise SystemExit(f"ACG BLOCKED: current branch is default branch '{default}'")
    print(f"ACG branch passed: {branch}")


def check_scope(cfg: dict[str, Any], root: Path) -> None:
    scope = cfg.get("task", {}).get("scope", {})
    allowed = [str(x) for x in scope.get("allowed", [])]
    forbidden = [str(x) for x in scope.get("forbidden", [])]
    files = changed_files(root, str(cfg.get("project", {}).get("default_branch", "main")))
    outside = [path for path in files if allowed and not matches(path, allowed)]
    blocked = [path for path in files if matches(path, forbidden)]
    ok = not outside and not blocked
    append_evidence(cfg, root, "scope", "passed" if ok else "failed", {"changed_files": files, "outside_scope": outside, "forbidden_touched": blocked})
    if not ok:
        print("ACG SCOPE FAILED")
        for item in outside:
            print(f"outside allowed scope: {item}")
        for item in blocked:
            print(f"forbidden touched: {item}")
        raise SystemExit(1)
    print("ACG scope passed")


def run_command(cfg: dict[str, Any], root: Path, step: str, command: str) -> int:
    (root / LOG_DIR).mkdir(exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{step}_{command}")[:120]
    log_path = root / LOG_DIR / f"{safe}.log"
    print(f"ACG running {step}: {command}")
    try:
        args = shlex.split(command)
    except ValueError as exc:
        append_evidence(cfg, root, step, "failed", {"command": command, "error": str(exc)})
        return 1
    cp = run_process(args, cwd=root)
    log_path.write_text(cp.stdout, encoding="utf-8")
    append_evidence(cfg, root, step, "passed" if cp.returncode == 0 else "failed", {"command": command, "exit_code": cp.returncode, "log_path": str(log_path.relative_to(root))})
    if cp.stdout:
        print(cp.stdout[-4000:])
    return cp.returncode


def check_verify(cfg: dict[str, Any], root: Path) -> None:
    commands = [str(x) for x in cfg.get("verify", {}).get("commands", [])]
    if not commands:
        append_evidence(cfg, root, "verify", "failed", {"reason": "no verify.commands configured"})
        raise SystemExit("ACG BLOCKED: verify.commands is empty")
    failed = [cmd for cmd in commands if run_command(cfg, root, "verify", cmd) != 0]
    append_evidence(cfg, root, "verify_summary", "passed" if not failed else "failed", {"failed": failed})
    if failed:
        raise SystemExit("ACG BLOCKED: verification failed")
    print("ACG verify passed")


def check_done(cfg: dict[str, Any], root: Path) -> None:
    failed = []
    for item in cfg.get("task", {}).get("done_when", []) or []:
        if "command" in item:
            if run_command(cfg, root, "done_when", str(item["command"])) != 0:
                failed.append(item)
        elif "file_exists" in item:
            target = root / str(item["file_exists"])
            ok = target.exists()
            append_evidence(cfg, root, "done_when", "passed" if ok else "failed", {"file_exists": str(item["file_exists"])})
            if not ok:
                failed.append(item)
        elif "no_pattern" in item:
            pattern = str(item.get("pattern", ""))
            paths = str(item.get("paths", "**"))
            rx = re.compile(pattern)
            found = []
            for path in root.glob(paths):
                if path.is_file() and rx.search(path.read_text(encoding="utf-8", errors="ignore")):
                    found.append(str(path.relative_to(root)))
            append_evidence(cfg, root, "done_when", "passed" if not found else "failed", {"pattern": pattern, "matches": found})
            if found:
                failed.append(item)
    append_evidence(cfg, root, "done_when_summary", "passed" if not failed else "failed", {"failed": failed})
    if failed:
        raise SystemExit("ACG BLOCKED: done_when failed")
    print("ACG done_when passed")


def check_gate(cfg: dict[str, Any], root: Path) -> None:
    promotion = cfg.get("promotion", {})
    evidence = root / EVIDENCE_FILE
    if promotion.get("fail_closed", True) is not True:
        append_evidence(cfg, root, "gate", "failed", {"reason": "fail_closed is not true"})
        raise SystemExit("ACG BLOCKED: fail_closed must be true")
    if promotion.get("require_evidence", True) and (not evidence.exists() or not evidence.read_text(encoding="utf-8").strip()):
        raise SystemExit("ACG BLOCKED: evidence missing")
    append_evidence(cfg, root, "gate", "passed", {"evidence": str(EVIDENCE_FILE)})
    print("ACG gate passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG enforcement runner")
    parser.add_argument("--config", default="acg.yaml")
    parser.add_argument("--mode", default="all", choices=["branch", "scope", "verify", "done", "gate", "all"])
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    root = config_path.parent
    cfg = parse_yaml_subset(config_path)
    if args.mode in {"branch", "all"}:
        check_branch(cfg, root)
    if args.mode in {"scope", "all"}:
        check_scope(cfg, root)
    if args.mode in {"verify", "all"}:
        check_verify(cfg, root)
    if args.mode in {"done", "all"}:
        check_done(cfg, root)
    if args.mode in {"gate", "all"}:
        check_gate(cfg, root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
