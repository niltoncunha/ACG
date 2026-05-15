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


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def run_process(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def git(args: list[str], allow_fail: bool = False) -> str:
    cp = run_process(["git", *args])
    if cp.returncode != 0:
        if allow_fail:
            return ""
        raise RuntimeError(cp.stdout.strip())
    return cp.stdout.strip()


def clean_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_yaml_subset(path: Path) -> dict[str, Any]:
    """Tiny parser for the acg.yaml subset used by ACG-Core.

    Supported shape:
    project.name/default_branch
    task.id/description
    task.scope.allowed/forbidden
    task.done_when list with command/file_exists/no_pattern entries
    verify.commands
    promotion.fail_closed/require_evidence
    """
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
        s = line.strip()

        if indent == 0 and s.endswith(":"):
            section = s[:-1]
            sub = None
            last_done = None
            continue

        if section in {"project", "promotion"} and indent >= 2 and ":" in s:
            key, value = s.split(":", 1)
            val: Any = clean_value(value)
            if str(val).lower() == "true":
                val = True
            elif str(val).lower() == "false":
                val = False
            cfg[section][key.strip()] = val
            continue

        if section == "task":
            if indent == 2 and s == "scope:":
                sub = "scope"
                continue
            if indent == 2 and s == "done_when:":
                sub = "done_when"
                continue
            if indent == 2 and ":" in s and sub is None:
                key, value = s.split(":", 1)
                cfg["task"][key.strip()] = clean_value(value)
                continue
            if sub == "scope" and indent == 4 and s.endswith(":"):
                sub = "scope." + s[:-1]
                continue
            if sub in {"scope.allowed", "scope.forbidden"} and indent >= 6 and s.startswith("-"):
                target = sub.split(".", 1)[1]
                cfg["task"]["scope"].setdefault(target, []).append(clean_value(s[1:]))
                continue
            if sub == "done_when" and indent >= 4:
                if s.startswith("-") and ":" in s:
                    key, value = s[1:].strip().split(":", 1)
                    last_done = {key.strip(): clean_value(value)}
                    cfg["task"]["done_when"].append(last_done)
                    continue
                if last_done is not None and ":" in s:
                    key, value = s.split(":", 1)
                    last_done[key.strip()] = clean_value(value)
                    continue

        if section == "verify":
            if indent == 2 and s == "commands:":
                sub = "commands"
                continue
            if sub == "commands" and indent >= 4 and s.startswith("-"):
                cfg["verify"].setdefault("commands", []).append(clean_value(s[1:]))
                continue

    return cfg


def current_branch() -> str:
    return os.environ.get("GITHUB_HEAD_REF") or git(["rev-parse", "--abbrev-ref", "HEAD"], allow_fail=True) or "unknown"


def append_evidence(cfg: dict[str, Any], step: str, status: str, extra: dict[str, Any] | None = None) -> None:
    event = {
        "task_id": cfg.get("task", {}).get("id", "unknown-task"),
        "timestamp": now(),
        "step": step,
        "status": status,
        "branch": current_branch(),
        "commit": git(["rev-parse", "HEAD"], allow_fail=True) or None,
    }
    if extra:
        event.update(extra)
    with EVIDENCE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def changed_files(default_branch: str) -> list[str]:
    base = os.environ.get("GITHUB_BASE_REF") or default_branch
    candidates = [
        ["diff", "--name-only", f"origin/{base}...HEAD"],
        ["diff", "--name-only", f"{base}...HEAD"],
        ["diff", "--name-only", "HEAD~1...HEAD"],
        ["diff", "--name-only"],
    ]
    for args in candidates:
        out = git(args, allow_fail=True)
        if out:
            return [x.strip() for x in out.splitlines() if x.strip()]
    return []


def matches(path: str, patterns: list[str]) -> bool:
    norm = path.replace(os.sep, "/")
    for pattern in patterns or []:
        p = str(pattern).replace(os.sep, "/")
        if p in {"*", "**"}:
            return True
        if p.endswith("/**") and norm.startswith(p[:-3].rstrip("/") + "/"):
            return True
        if fnmatch.fnmatch(norm, p):
            return True
    return False


def check_branch(cfg: dict[str, Any]) -> None:
    default = cfg.get("project", {}).get("default_branch", "main")
    branch = current_branch()
    ok = branch != default
    append_evidence(cfg, "branch", "passed" if ok else "failed", {"branch": branch, "default_branch": default})
    if not ok:
        raise SystemExit(f"ACG BLOCKED: current branch is default branch '{default}'")
    print(f"ACG branch passed: {branch}")


def check_scope(cfg: dict[str, Any]) -> None:
    files = changed_files(cfg.get("project", {}).get("default_branch", "main"))
    scope = cfg.get("task", {}).get("scope", {})
    allowed = scope.get("allowed", [])
    forbidden = scope.get("forbidden", [])
    outside = [f for f in files if allowed and not matches(f, allowed)]
    blocked = [f for f in files if matches(f, forbidden)]
    ok = not outside and not blocked
    append_evidence(cfg, "scope", "passed" if ok else "failed", {"changed_files": files, "outside_scope": outside, "forbidden_touched": blocked})
    if not ok:
        print("ACG SCOPE FAILED")
        for f in outside:
            print(f"outside allowed scope: {f}")
        for f in blocked:
            print(f"forbidden touched: {f}")
        raise SystemExit(1)
    print("ACG scope passed")


def run_command(cfg: dict[str, Any], step: str, command: str) -> int:
    LOG_DIR.mkdir(exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{step}_{command}")[:120]
    log_path = LOG_DIR / f"{safe_name}.log"
    print(f"ACG running {step}: {command}")
    try:
        args = shlex.split(command)
    except ValueError as exc:
        append_evidence(cfg, step, "failed", {"command": command, "error": str(exc)})
        return 1
    cp = run_process(args)
    log_path.write_text(cp.stdout, encoding="utf-8")
    append_evidence(cfg, step, "passed" if cp.returncode == 0 else "failed", {"command": command, "exit_code": cp.returncode, "log_path": str(log_path)})
    if cp.stdout:
        print(cp.stdout[-4000:])
    return cp.returncode


def check_verify(cfg: dict[str, Any]) -> None:
    commands = cfg.get("verify", {}).get("commands", [])
    if not commands:
        append_evidence(cfg, "verify", "failed", {"reason": "no verify.commands configured"})
        raise SystemExit("ACG BLOCKED: verify.commands is empty")
    failed = [cmd for cmd in commands if run_command(cfg, "verify", cmd) != 0]
    append_evidence(cfg, "verify_summary", "passed" if not failed else "failed", {"failed": failed})
    if failed:
        raise SystemExit("ACG BLOCKED: verification failed")
    print("ACG verify passed")


def check_done(cfg: dict[str, Any]) -> None:
    failed = []
    for item in cfg.get("task", {}).get("done_when", []) or []:
        if "command" in item:
            if run_command(cfg, "done_when", str(item["command"])) != 0:
                failed.append(item)
        elif "file_exists" in item:
            ok = Path(str(item["file_exists"])).exists()
            append_evidence(cfg, "done_when", "passed" if ok else "failed", {"file_exists": item["file_exists"]})
            if not ok:
                failed.append(item)
        elif "no_pattern" in item:
            paths = str(item.get("paths", "**"))
            pattern = str(item.get("pattern", ""))
            found = []
            rx = re.compile(pattern)
            for p in Path.cwd().glob(paths):
                if p.is_file() and rx.search(p.read_text(encoding="utf-8", errors="ignore")):
                    found.append(str(p))
            append_evidence(cfg, "done_when", "passed" if not found else "failed", {"pattern": pattern, "matches": found})
            if found:
                failed.append(item)
    append_evidence(cfg, "done_when_summary", "passed" if not failed else "failed", {"failed": failed})
    if failed:
        raise SystemExit("ACG BLOCKED: done_when failed")
    print("ACG done_when passed")


def check_gate(cfg: dict[str, Any]) -> None:
    promotion = cfg.get("promotion", {})
    if promotion.get("fail_closed", True) is not True:
        append_evidence(cfg, "gate", "failed", {"reason": "fail_closed is not true"})
        raise SystemExit("ACG BLOCKED: fail_closed must be true")
    if promotion.get("require_evidence", True) and (not EVIDENCE_FILE.exists() or not EVIDENCE_FILE.read_text(encoding="utf-8").strip()):
        raise SystemExit("ACG BLOCKED: evidence missing")
    append_evidence(cfg, "gate", "passed", {"evidence": str(EVIDENCE_FILE)})
    print("ACG gate passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG-Core enforcement runner")
    parser.add_argument("--config", default="acg.yaml")
    parser.add_argument("--mode", default="all", choices=["branch", "scope", "verify", "done", "gate", "all"])
    args = parser.parse_args()
    cfg = parse_yaml_subset(Path(args.config))
    if args.mode in {"branch", "all"}:
        check_branch(cfg)
    if args.mode in {"scope", "all"}:
        check_scope(cfg)
    if args.mode in {"verify", "all"}:
        check_verify(cfg)
    if args.mode in {"done", "all"}:
        check_done(cfg)
    if args.mode in {"gate", "all"}:
        check_gate(cfg)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
