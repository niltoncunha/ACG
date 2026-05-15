#!/usr/bin/env python3
"""ACG-Core v0.2 enforcement runner.

No external dependencies. Designed for CI.

Checks:
- branch is not the configured default branch;
- changed files stay inside task.scope.allowed;
- changed files do not touch task.scope.forbidden;
- configured verification commands run externally;
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
import sys
from pathlib import Path
from typing import Any

EVIDENCE_FILE = Path("acg-evidence.jsonl")
LOG_DIR = Path("acg-logs")
DEFAULT_SCAN_EXCLUDES = {
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


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def run_process(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def git(args: list[str], cwd: Path | None = None, allow_fail: bool = False) -> str:
    cp = run_process(["git", *args], cwd=cwd)
    if cp.returncode != 0:
        if allow_fail:
            return ""
        raise RuntimeError(cp.stdout.strip())
    return cp.stdout.strip()


def clean_value(value: str) -> Any:
    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
        cleaned = cleaned[1:-1]

    lower = cleaned.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    return cleaned


def parse_yaml_subset(path: Path) -> dict[str, Any]:
    """Parse the small YAML subset used by ACG-Core."""
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    cfg: dict[str, Any] = {
        "project": {},
        "task": {"scope": {"allowed": [], "forbidden": []}, "done_when": []},
        "verify": {"commands": []},
        "promotion": {},
    }

    section: str | None = None
    sub: str | None = None
    last_done: dict[str, Any] | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = line.strip()

        if indent == 0 and stripped.endswith(":"):
            section = stripped[:-1]
            sub = None
            last_done = None
            continue

        if section in {"project", "promotion"} and indent >= 2 and ":" in stripped:
            key, value = stripped.split(":", 1)
            cfg[section][key.strip()] = clean_value(value)
            continue

        if section == "task":
            if indent == 2 and stripped == "scope:":
                sub = "scope"
                continue
            if indent == 2 and stripped == "done_when:":
                sub = "done_when"
                continue
            if indent == 2 and ":" in stripped and sub is None:
                key, value = stripped.split(":", 1)
                cfg["task"][key.strip()] = clean_value(value)
                continue
            if sub in {"scope", "scope.allowed", "scope.forbidden"} and indent == 4 and stripped.endswith(":"):
                sub = f"scope.{stripped[:-1]}"
                continue
            if sub in {"scope.allowed", "scope.forbidden"} and indent >= 6 and stripped.startswith("-"):
                target = sub.split(".", 1)[1]
                cfg["task"]["scope"].setdefault(target, []).append(clean_value(stripped[1:]))
                continue
            if sub == "done_when" and indent >= 4:
                if stripped.startswith("-") and ":" in stripped:
                    key, value = stripped[1:].strip().split(":", 1)
                    last_done = {key.strip(): clean_value(value)}
                    cfg["task"]["done_when"].append(last_done)
                    continue
                if last_done is not None and ":" in stripped:
                    key, value = stripped.split(":", 1)
                    last_done[key.strip()] = clean_value(value)
                    continue

        if section == "verify":
            if indent == 2 and stripped == "commands:":
                sub = "commands"
                continue
            if sub == "commands" and indent >= 4 and stripped.startswith("-"):
                cfg["verify"].setdefault("commands", []).append(clean_value(stripped[1:]))
                continue

    return cfg


def current_branch(repo_root: Path) -> str:
    return os.environ.get("GITHUB_HEAD_REF") or git(
        ["rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_root,
        allow_fail=True,
    ) or "unknown"


def append_evidence(
    cfg: dict[str, Any],
    repo_root: Path,
    step: str,
    status: str,
    extra: dict[str, Any] | None = None,
) -> None:
    event = {
        "task_id": cfg.get("task", {}).get("id", "unknown-task"),
        "timestamp": now(),
        "step": step,
        "status": status,
        "branch": current_branch(repo_root),
        "commit": git(["rev-parse", "HEAD"], cwd=repo_root, allow_fail=True) or None,
    }
    if extra:
        event.update(extra)
    with (repo_root / EVIDENCE_FILE).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def tracked_files(root: Path, config_path: Path) -> list[str]:
    files: list[str] = []
    skip_names = {
        EVIDENCE_FILE.name,
        config_path.name,
    }
    skip_dirs = set(DEFAULT_SCAN_EXCLUDES)
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel in skip_names:
            continue
        files.append(rel)
    return sorted(files)


def ref_exists(repo_root: Path, ref: str) -> bool:
    cp = run_process(["git", "rev-parse", "--verify", ref], cwd=repo_root)
    return cp.returncode == 0


def changed_files_from_merge_base(repo_root: Path, base_ref: str) -> list[str]:
    if not ref_exists(repo_root, base_ref):
        return []
    merge_base = git(["merge-base", base_ref, "HEAD"], cwd=repo_root, allow_fail=True)
    if not merge_base:
        return []
    out = git(["diff", "--name-only", f"{merge_base}..HEAD"], cwd=repo_root, allow_fail=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def changed_files(repo_root: Path, default_branch: str, config_path: Path) -> list[str]:
    base = os.environ.get("GITHUB_BASE_REF") or default_branch
    for ref in (f"origin/{base}", base):
        files = changed_files_from_merge_base(repo_root, ref)
        if files:
            return files
    candidates = [
        ["diff", "--name-only", f"origin/{base}...HEAD"],
        ["diff", "--name-only", f"{base}...HEAD"],
        ["diff", "--name-only", "HEAD~1...HEAD"],
        ["diff", "--name-only"],
    ]
    for args in candidates:
        out = git(args, cwd=repo_root, allow_fail=True)
        if out:
            return [line.strip() for line in out.splitlines() if line.strip()]
    return tracked_files(repo_root, config_path)


def normalize_repo_path(path: str) -> str | None:
    normalized = str(path).strip().replace("\\", "/")
    if not normalized:
        return None
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:/", normalized):
        return None

    parts = normalized.split("/")
    if any(not part or part in {".", ".."} for part in parts):
        return None
    return "/".join(parts)


def matches(path: str, patterns: list[str]) -> bool:
    normalized = normalize_repo_path(path)
    if normalized is None:
        return False
    for pattern in patterns or []:
        normalized_pattern = str(pattern).strip().replace(os.sep, "/").replace("\\", "/")
        if normalized_pattern.startswith("./"):
            normalized_pattern = normalized_pattern[2:]
        if normalized_pattern in {"*", "**"}:
            return True
        if normalized_pattern.endswith("/**") and normalized.startswith(normalized_pattern[:-3].rstrip("/") + "/"):
            return True
        if fnmatch.fnmatch(normalized, normalized_pattern):
            return True
    return False


def check_branch(cfg: dict[str, Any], repo_root: Path) -> None:
    default = str(cfg.get("project", {}).get("default_branch", "main"))
    branch = current_branch(repo_root)
    ok = branch != default
    append_evidence(
        cfg,
        repo_root,
        "branch",
        "passed" if ok else "failed",
        {"branch": branch, "default_branch": default},
    )
    if not ok:
        raise SystemExit(f"ACG BLOCKED: current branch is default branch '{default}'")
    print(f"ACG branch passed: {branch}")


def check_scope(cfg: dict[str, Any], repo_root: Path, config_path: Path) -> None:
    scope = cfg.get("task", {}).get("scope", {})
    allowed = [str(item) for item in scope.get("allowed", [])]
    forbidden = [str(item) for item in scope.get("forbidden", [])]
    raw_files = changed_files(
        repo_root,
        str(cfg.get("project", {}).get("default_branch", "main")),
        config_path,
    )
    invalid = [path for path in raw_files if normalize_repo_path(path) is None]
    files = [normalized for path in raw_files if (normalized := normalize_repo_path(path)) is not None]
    outside = [path for path in files if allowed and not matches(path, allowed)]
    blocked = [path for path in files if matches(path, forbidden)]
    ok = not invalid and not outside and not blocked
    append_evidence(
        cfg,
        repo_root,
        "scope",
        "passed" if ok else "failed",
        {
            "changed_files": files,
            "invalid_paths": invalid,
            "outside_scope": outside,
            "forbidden_touched": blocked,
        },
    )
    if not ok:
        print("ACG SCOPE FAILED")
        for item in invalid:
            print(f"invalid path: {item}")
        for item in outside:
            print(f"outside allowed scope: {item}")
        for item in blocked:
            print(f"forbidden touched: {item}")
        raise SystemExit(1)
    print("ACG scope passed")


def run_command(cfg: dict[str, Any], repo_root: Path, step: str, command: str) -> int:
    (repo_root / LOG_DIR).mkdir(exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{step}_{command}")[:120]
    log_path = repo_root / LOG_DIR / f"{safe_name}.log"
    print(f"ACG running {step}: {command}")
    try:
        args = shlex.split(command)
    except ValueError as exc:
        append_evidence(cfg, repo_root, step, "failed", {"command": command, "error": str(exc)})
        return 1

    cp = run_process(args, cwd=repo_root)
    log_path.write_text(cp.stdout, encoding="utf-8")
    append_evidence(
        cfg,
        repo_root,
        step,
        "passed" if cp.returncode == 0 else "failed",
        {"command": command, "exit_code": cp.returncode, "log_path": str(log_path.relative_to(repo_root))},
    )
    if cp.stdout:
        print(cp.stdout[-4000:])
    return cp.returncode


def check_verify(cfg: dict[str, Any], repo_root: Path) -> None:
    commands = [str(item) for item in cfg.get("verify", {}).get("commands", [])]
    if not commands:
        append_evidence(cfg, repo_root, "verify", "failed", {"reason": "no verify.commands configured"})
        raise SystemExit("ACG BLOCKED: verify.commands is empty")

    failed = [command for command in commands if run_command(cfg, repo_root, "verify", command) != 0]
    append_evidence(
        cfg,
        repo_root,
        "verify_summary",
        "passed" if not failed else "failed",
        {"failed": failed},
    )
    if failed:
        raise SystemExit("ACG BLOCKED: verification failed")
    print("ACG verify passed")


def scan_candidates(repo_root: Path, pattern: str, exclude_dirs: set[str]) -> list[Path]:
    if pattern in {"**", "**/*"}:
        paths = repo_root.rglob("*")
    else:
        paths = repo_root.glob(pattern)

    found: list[Path] = []
    for path in paths:
        if any(part in exclude_dirs for part in path.parts):
            continue
        if path.is_file():
            found.append(path)
    return found


def check_done(cfg: dict[str, Any], repo_root: Path) -> None:
    failed: list[dict[str, Any]] = []
    for item in cfg.get("task", {}).get("done_when", []) or []:
        if "command" in item:
            if run_command(cfg, repo_root, "done_when", str(item["command"])) != 0:
                failed.append(item)
            continue

        if "file_exists" in item:
            target = repo_root / str(item["file_exists"])
            ok = target.exists()
            append_evidence(
                cfg,
                repo_root,
                "done_when",
                "passed" if ok else "failed",
                {"file_exists": str(item["file_exists"])} ,
            )
            if not ok:
                failed.append(item)
            continue

        if "no_pattern" in item:
            paths = str(item.get("paths", "**"))
            pattern = str(item.get("pattern", ""))
            exclude_dirs = set(DEFAULT_SCAN_EXCLUDES)
            raw_excludes = str(item.get("exclude_dirs", "")).strip()
            if raw_excludes:
                exclude_dirs.update(part.strip() for part in raw_excludes.split(",") if part.strip())
            found: list[str] = []
            regex = re.compile(pattern)
            for path in scan_candidates(repo_root, paths, exclude_dirs):
                if regex.search(path.read_text(encoding="utf-8", errors="ignore")):
                    found.append(str(path.relative_to(repo_root)))
            append_evidence(
                cfg,
                repo_root,
                "done_when",
                "passed" if not found else "failed",
                {"pattern": pattern, "matches": found},
            )
            if found:
                failed.append(item)

    append_evidence(
        cfg,
        repo_root,
        "done_when_summary",
        "passed" if not failed else "failed",
        {"failed": failed},
    )
    if failed:
        raise SystemExit("ACG BLOCKED: done_when failed")
    print("ACG done_when passed")


def check_gate(cfg: dict[str, Any], repo_root: Path) -> None:
    promotion = cfg.get("promotion", {})
    evidence_path = repo_root / EVIDENCE_FILE
    if promotion.get("fail_closed", True) is not True:
        append_evidence(cfg, repo_root, "gate", "failed", {"reason": "fail_closed is not true"})
        raise SystemExit("ACG BLOCKED: fail_closed must be true")

    if promotion.get("require_evidence", True) and (
        not evidence_path.exists() or not evidence_path.read_text(encoding="utf-8").strip()
    ):
        raise SystemExit("ACG BLOCKED: evidence missing")

    append_evidence(cfg, repo_root, "gate", "passed", {"evidence": str(EVIDENCE_FILE)})
    print("ACG gate passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG-Core enforcement runner")
    parser.add_argument("--config", default="acg.yaml")
    parser.add_argument(
        "--mode",
        default="all",
        choices=["branch", "scope", "verify", "done", "gate", "all"],
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = Path.cwd() / config_path
    config_path = config_path.resolve()
    repo_root = config_path.parent

    cfg = parse_yaml_subset(config_path)

    if args.mode in {"branch", "all"}:
        check_branch(cfg, repo_root)
    if args.mode in {"scope", "all"}:
        check_scope(cfg, repo_root, config_path)
    if args.mode in {"verify", "all"}:
        check_verify(cfg, repo_root)
    if args.mode in {"done", "all"}:
        check_done(cfg, repo_root)
    if args.mode in {"gate", "all"}:
        check_gate(cfg, repo_root)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
