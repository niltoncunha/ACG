#!/usr/bin/env python3
"""ACG Context Gateway v0.4-alpha.

A small local CLI gateway that reads files only when they are present in the
approved ACG queues for the selected phase.

This is not a full sandbox. It is a ready-to-use control point for agents that
agree to access files through this tool. For hard enforcement, run the agent in
an environment where direct filesystem reads are blocked and expose only this
gateway.

Usage:
  python scripts/acg-gateway.py list --acg .acg --phase 1
  python scripts/acg-gateway.py read --acg .acg --phase 1 --path 00_core/README.md
  python scripts/acg-gateway.py read --acg .acg --phase 2 --path 06_runtime_guides/runtime_execution.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def normalize(path: str) -> str:
    return path.replace("\\", "/").strip().lstrip("./")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_path(acg: Path, name: str) -> Path:
    return acg / "artifacts" / name


def load_queue(acg: Path, phase: int) -> dict[str, dict]:
    queues = load_json(artifact_path(acg, "reading_queues.json"))
    key = "phase1" if phase == 1 else "phase2"
    return {normalize(item["relative_path"]): item for item in queues.get(key, [])}


def load_pack_path(acg: Path, rel_path: str) -> Path:
    return acg / "phase1_pack" / rel_path


def log_event(acg: Path, event: dict) -> None:
    event = {"timestamp": now(), **event}
    log_path = acg / "gateway-evidence.jsonl"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def list_allowed(acg: Path, phase: int) -> int:
    queue = load_queue(acg, phase)
    for path in sorted(queue):
        print(path)
    print(f"ACG gateway phase {phase} allowed files: {len(queue)}")
    return 0


def read_allowed(acg: Path, source: Path | None, phase: int, requested: str) -> int:
    rel_path = normalize(requested)
    queue = load_queue(acg, phase)
    if rel_path not in queue:
        log_event(acg, {"event": "blocked_read", "phase": phase, "path": rel_path, "reason": "not_in_phase_queue"})
        print(f"ACG-BLOCKED: {rel_path} is not available in phase {phase}.")
        print("Use the current phase queue or request explicit human approval.")
        return 2

    if phase == 1:
        path = load_pack_path(acg, rel_path)
    else:
        if source is None:
            print("ACG-BLOCKED: --source is required for phase 2 reads.")
            return 2
        path = source / rel_path

    if not path.is_file():
        log_event(acg, {"event": "blocked_read", "phase": phase, "path": rel_path, "reason": "file_not_found"})
        print(f"ACG-BLOCKED: file not found for {rel_path}: {path}")
        return 2

    log_event(acg, {"event": "allowed_read", "phase": phase, "path": rel_path})
    print(path.read_text(encoding="utf-8", errors="ignore"))
    return 0


def status(acg: Path) -> int:
    queues = load_json(artifact_path(acg, "reading_queues.json"))
    for key in ["phase1", "phase2", "approval_required", "search_targets", "human_only", "ignored"]:
        print(f"{key}: {len(queues.get(key, []))}")
    print(f"evidence: {acg / 'gateway-evidence.jsonl'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG Context Gateway v0.4-alpha")
    sub = parser.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--acg", default=".acg", help="ACG output folder")
    common.add_argument("--phase", type=int, default=1, choices=[1, 2])

    p_list = sub.add_parser("list", parents=[common], help="List allowed files for a phase")
    p_list.set_defaults(fn=lambda args: list_allowed(Path(args.acg), args.phase))

    p_read = sub.add_parser("read", parents=[common], help="Read a file through the gateway")
    p_read.add_argument("--source", help="Original source folder, required for phase 2")
    p_read.add_argument("--path", required=True, help="Relative path from the original source")
    p_read.set_defaults(fn=lambda args: read_allowed(Path(args.acg), Path(args.source).resolve() if args.source else None, args.phase, args.path))

    p_status = sub.add_parser("status", help="Print queue counts")
    p_status.add_argument("--acg", default=".acg")
    p_status.set_defaults(fn=lambda args: status(Path(args.acg)))

    args = parser.parse_args()
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
