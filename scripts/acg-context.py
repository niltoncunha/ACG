#!/usr/bin/env python3
"""ACG Guided Context Mode.

Create an intelligent context manifest and a Phase 1 reading pack from a large
folder before sending material to an AI assistant.

No external dependencies.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
from pathlib import Path

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", "dist", "build", ".venv", "venv", "coverage"}
LARGE_LIMIT = 500_000

ORIENTATION_NAMES = {
    "readme.md",
    "agents.md",
    "active-index.md",
    "system_healthcheck.md",
    "environment_contract.md",
    "structure_map.md",
    "memory_contract.md",
    "system_law.md",
}

CONTROL_NAMES = {
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "cargo.toml",
    "go.mod",
    "dockerfile",
    "docker-compose.yml",
    "makefile",
    "acg.yaml",
}

TERMINAL_HINTS = [
    "/refs/ssot/",
    "/chat_exports/",
    "/logs/",
    "/legacy/",
    "/archive/",
    ".sqlite",
    ".sqlite3",
]


def utc(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def relpath(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def classify(relative_path: str, size: int) -> dict[str, object]:
    rp = relative_path.replace("\\", "/")
    low = rp.lower()
    name = Path(rp).name.lower()
    ext = Path(rp).suffix.lower()

    terminal = size >= LARGE_LIMIT or any(hint in low for hint in TERMINAL_HINTS)
    if terminal:
        return {
            "role": "reference_or_terminal_asset",
            "phase": "terminal",
            "strategy": "search_only" if ext in {".txt", ".md", ".json", ".yml", ".yaml"} else "ignore",
            "risk": "context_exhaustion" if size >= LARGE_LIMIT else "history_or_reference_noise",
            "allowed_to_open": False,
            "allowed_to_edit": False,
            "requires_human_approval": True,
            "public_safe": False,
        }

    if name in ORIENTATION_NAMES or (rp.startswith("00_core/") and ext in {".md", ".txt", ".yml", ".yaml"}):
        return {
            "role": "orientation",
            "phase": "phase1",
            "strategy": "open",
            "risk": "low",
            "allowed_to_open": True,
            "allowed_to_edit": False,
            "requires_human_approval": False,
            "public_safe": False,
        }

    if name in CONTROL_NAMES or "schema" in name:
        return {
            "role": "control_or_schema",
            "phase": "phase1",
            "strategy": "open",
            "risk": "medium_control_file",
            "allowed_to_open": True,
            "allowed_to_edit": False,
            "requires_human_approval": False,
            "public_safe": False,
        }

    if rp.startswith(("01_canon/", "02_memory/", "06_runtime_guides/")) and ext in {".md", ".txt", ".yml", ".yaml"}:
        return {
            "role": "governance_or_memory",
            "phase": "phase2",
            "strategy": "open",
            "risk": "medium_dense_rules",
            "allowed_to_open": True,
            "allowed_to_edit": False,
            "requires_human_approval": False,
            "public_safe": False,
        }

    if rp.startswith(("04_eval/", "05_lab/", "tests/")):
        return {
            "role": "evaluation_or_test",
            "phase": "phase3",
            "strategy": "open_later",
            "risk": "medium_validation_context",
            "allowed_to_open": False,
            "allowed_to_edit": False,
            "requires_human_approval": True,
            "public_safe": False,
        }

    return {
        "role": "unknown_or_supporting_file",
        "phase": "phase2",
        "strategy": "open_later",
        "risk": "unknown",
        "allowed_to_open": False,
        "allowed_to_edit": False,
        "requires_human_approval": True,
        "public_safe": False,
    }


def scan(source: Path, limit: int) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in source.rglob("*"):
        if should_skip(path):
            continue
        if not path.is_file():
            continue
        rp = relpath(source, path)
        stat = path.stat()
        meta = classify(rp, stat.st_size)
        records.append({
            "relative_path": rp,
            "absolute_path": str(path.resolve()).replace("\\", "/"),
            "size": stat.st_size,
            "modified": utc(stat.st_mtime),
            "extension": path.suffix.lower(),
            "exists": True,
            **meta,
        })
        if len(records) >= limit:
            break
    return records


def sort_records(records: list[dict[str, object]]) -> list[dict[str, object]]:
    phase_order = {"phase1": 0, "phase2": 1, "phase3": 2, "terminal": 3}
    role_order = {"orientation": 0, "control_or_schema": 1, "governance_or_memory": 2}
    return sorted(
        records,
        key=lambda r: (
            phase_order.get(str(r["phase"]), 9),
            role_order.get(str(r["role"]), 9),
            int(r["size"]),
            str(r["relative_path"]),
        ),
    )


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")


def write_table(path: Path, records: list[dict[str, object]]) -> None:
    lines = ["relative_path | absolute_path | size | phase | strategy | role | risk"]
    for r in records:
        lines.append(f"{r['relative_path']} | {r['absolute_path']} | {r['size']} | {r['phase']} | {r['strategy']} | {r['role']} | {r['risk']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_phase_pack(records: list[dict[str, object]], pack_dir: Path, phase: str, max_files: int) -> list[dict[str, object]]:
    pack_dir.mkdir(parents=True, exist_ok=True)
    selected = [r for r in sort_records(records) if r["phase"] == phase and r["strategy"] == "open" and r["allowed_to_open"]]
    selected = selected[:max_files]
    for r in selected:
        src = Path(str(r["absolute_path"]))
        dst = pack_dir / str(r["relative_path"])
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return selected


def write_prompt(path: Path, selected: list[dict[str, object]]) -> None:
    files = "\n".join(f"- {r['relative_path']}" for r in selected)
    path.write_text(f"""# ACG Phase 1 Orientation Task

You are working inside a copied Phase 1 context pack.

Only read files inside this folder.
Do not search outside this folder.
Do not open SSOT, logs, chat exports, scripts, legacy archives, or any other file.
Use Portuguese for interaction.

Files included in this pack:
{files}

Important:
Use internal file names only for private analysis.
For public-facing summaries, replace internal project names with generic labels such as:
- core system
- structure map
- memory layer
- runtime contract
- evaluation layer
- legacy archive

Task:
Read only the Phase 1 files included in this folder and produce an orientation report.

Output:

## Phase 1 Orientation Report

1. What this file bundle appears to be
2. Main structural layers
3. Operating rules / constraints found
4. Memory or state rules found
5. What the AI should not do yet
6. What files should be opened in Phase 2
7. Unknowns / questions for the human

Rules:
- Separate explicit facts from inference.
- Do not produce final conclusions.
- Do not propose edits.
- Do not execute anything.
- Do not read beyond this folder.
""", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG Guided Context Mode")
    parser.add_argument("--source", required=True, help="Source folder to scan")
    parser.add_argument("--out", required=True, help="Output folder for ACG context package")
    parser.add_argument("--limit", type=int, default=2000)
    parser.add_argument("--max-phase1", type=int, default=8)
    args = parser.parse_args()

    source = Path(args.source).resolve()
    out = Path(args.out).resolve()
    if not source.exists() or not source.is_dir():
        raise SystemExit(f"Source folder not found: {source}")
    out.mkdir(parents=True, exist_ok=True)

    records = sort_records(scan(source, args.limit))
    write_jsonl(out / "context_manifest.jsonl", records)
    write_table(out / "context_manifest.txt", records)
    selected = copy_phase_pack(records, out / "phase1_pack", "phase1", args.max_phase1)
    write_prompt(out / "phase1_pack" / "ACG_PHASE1_PROMPT.md", selected)

    print(f"ACG context manifest written to: {out / 'context_manifest.jsonl'}")
    print(f"ACG readable manifest written to: {out / 'context_manifest.txt'}")
    print(f"ACG Phase 1 pack written to: {out / 'phase1_pack'}")
    print(f"Phase 1 files copied: {len(selected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
