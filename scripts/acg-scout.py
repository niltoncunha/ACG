#!/usr/bin/env python3
"""ACG Structure Scout v0.3.

Build a structural map of a large folder before giving it to an AI agent.

Outputs:
- .acg/context_manifest.jsonl
- .acg/structure_map.md
- .acg/hotpaths.json
- .acg/reading_queues.json
- .acg/search_targets.md
- .acg/execution_brief.md
- .acg/phase1_pack/

No external dependencies.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", "coverage", ".cache", ".pytest_cache", ".mypy_cache",
}

CRITICAL_NAME_WEIGHTS = {
    "agents.md": 42,
    "active-index.md": 40,
    "readme.md": 22,
    "environment_contract.md": 38,
    "system_law.md": 36,
    "memory_contract.md": 34,
    "blueprint": 34,
    "structure_map": 34,
    "runtime_execution.md": 30,
    "acg.yaml": 38,
    "package.json": 30,
    "pyproject.toml": 30,
    "go.mod": 30,
    "cargo.toml": 30,
    "tsconfig.json": 26,
    "requirements.txt": 24,
}

EXTENSION_WEIGHTS = {
    ".py": 15, ".ts": 15, ".tsx": 15, ".js": 12, ".jsx": 12,
    ".go": 15, ".rs": 15, ".java": 12,
    ".yaml": 18, ".yml": 18, ".toml": 16, ".json": 10,
    ".md": 8, ".sh": 12, ".ps1": 12, ".sql": -5,
    ".log": -30, ".csv": -20, ".jsonl": -15, ".lock": -25, ".map": -30,
}

FAMILY_RULES = [
    (r"(^|/)90_legacy(/|$)|(^|/)legacy(/|$)|(^|/)archive|(^|/)_old(/|$)|(^|/)old(/|$)", "legacy", "terminal"),
    (r"(^|/)logs?(/|$)|\.log$", "logs", "terminal"),
    (r"(^|/)chat_exports?(/|$)|(^|/)exports?(/|$)", "exports", "terminal"),
    (r"(^|/)ssot(/|$)|(^|/)refs(/|$)", "reference", "search_only"),
    (r"(^|/)dist(/|$)|(^|/)build(/|$)|\.cache(/|$)|__pycache__", "generated", "ignore"),
    (r"(^|/)\.env$|(^|/)\.env\.|(^|/)secrets?(/|$)", "secrets", "human_only"),
    (r"(^|/)migrations?(/|$)|(^|/)schema/.*\.sql$", "migrations", "human_only"),
    (r"(^|/)infra(/|$)|(^|/)terraform(/|$)|\.tf$", "infra", "human_only"),
    (r"(^|/)00_core(/|$)|(^|/)core(/|$)|(^|/)src(/|$)|(^|/)app(/|$)|(^|/)lib(/|$)", "core", "priority"),
    (r"(^|/)01_canon(/|$)|(^|/)canon(/|$)", "canon", "priority"),
    (r"(^|/)02_memory(/|$)|(^|/)memory(/|$)|(^|/)state(/|$)", "memory", "priority"),
    (r"(^|/)scripts?(/|$)|(^|/)bin(/|$)|(^|/)cli(/|$)", "runtime", "standard"),
    (r"(^|/)tests?(/|$)|(^|/)spec(/|$)|(^|/)__tests__(/|$)", "tests", "standard"),
    (r"(^|/)docs?(/|$)|(^|/)documentation(/|$)", "docs", "standard"),
    (r"(^|/)06_runtime|(^|/)guides?(/|$)", "guides", "standard"),
    (r"(^|/)eval(/|$)|(^|/)lab(/|$)|benchmark", "evaluation", "later"),
]

TERMINAL_FAMILIES = {"legacy", "logs", "exports", "generated"}
HUMAN_ONLY_FAMILIES = {"secrets", "migrations", "infra"}


@dataclass
class FileEntry:
    relative_path: str
    absolute_path: str
    size: int
    modified: str
    extension: str
    depth: int
    folder_family: str
    family_tier: str
    role: str
    hotpath_score: int
    risk_score: int
    strategy: str
    allowed_to_open: bool
    allowed_to_edit: bool
    requires_human_approval: bool
    public_safe: bool
    reason: list[str] = field(default_factory=list)


def utc(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def classify_family(relative_path: str) -> tuple[str, str, list[str]]:
    low = relative_path.lower()
    for pattern, family, tier in FAMILY_RULES:
        if re.search(pattern, low):
            return family, tier, [f"matched_family:{family}"]
    return "unknown", "standard", ["matched_family:unknown"]


def detect_role(relative_path: str, extension: str, family: str) -> tuple[str, list[str]]:
    low = relative_path.lower()
    name = Path(low).name
    if name in {"readme.md", "agents.md", "active-index.md"}:
        return "orientation", ["orientation_name"]
    if "blueprint" in name or "structure_map" in name or "environment_contract" in name:
        return "architecture_or_contract", ["architecture_or_contract_name"]
    if name in {"package.json", "pyproject.toml", "go.mod", "cargo.toml", "requirements.txt", "acg.yaml"} or "schema" in name:
        return "control_or_schema", ["control_or_schema_name"]
    if family in {"canon", "memory", "guides"}:
        return "governance_or_memory", ["governance_family"]
    if family in {"tests", "evaluation"}:
        return "validation", ["validation_family"]
    if extension in {".py", ".ts", ".js", ".go", ".rs", ".java"}:
        return "source_code", ["source_extension"]
    if family in TERMINAL_FAMILIES or family == "reference":
        return "reference_or_terminal_asset", ["terminal_or_reference_family"]
    return "supporting_file", []


def score_file(relative_path: str, size: int, extension: str, depth: int, family: str, modified_ts: float, now_ts: float) -> tuple[int, list[str]]:
    score = 50
    reasons = []
    name = Path(relative_path.lower()).name
    for key, boost in CRITICAL_NAME_WEIGHTS.items():
        if key in name:
            score += boost
            reasons.append(f"critical_name:+{boost}")
            break
    depth_penalty = min(depth * 3, 20)
    score -= depth_penalty
    if depth_penalty:
        reasons.append(f"depth_penalty:-{depth_penalty}")
    if family in {"core", "canon", "memory"}:
        score += 22
        reasons.append("priority_family:+22")
    elif family in {"runtime", "guides", "tests"}:
        score += 8
        reasons.append("standard_structural_family:+8")
    hours = max(0.0, (now_ts - modified_ts) / 3600)
    if hours < 72:
        score += 15
        reasons.append("recent_72h:+15")
    elif hours < 168:
        score += 8
        reasons.append("recent_7d:+8")
    ext_weight = EXTENSION_WEIGHTS.get(extension.lower(), 0)
    score += ext_weight
    if ext_weight:
        reasons.append(f"extension:{ext_weight:+d}")
    if family in TERMINAL_FAMILIES:
        score -= 45
        reasons.append("terminal_family:-45")
    if family == "reference":
        score -= 25
        reasons.append("reference_family:-25")
    if family in HUMAN_ONLY_FAMILIES:
        score -= 35
        reasons.append("human_only_family:-35")
    if size > 2_000_000:
        score -= 45
        reasons.append("huge_file:-45")
    elif size > 500_000:
        score -= 35
        reasons.append("large_file:-35")
    elif size > 100_000:
        score -= 15
        reasons.append("medium_large_file:-15")
    elif 0 < size < 50:
        score -= 20
        reasons.append("tiny_file:-20")
    return max(0, min(100, score)), reasons


def risk_score(size: int, family: str, extension: str) -> int:
    risk = 0
    if family in HUMAN_ONLY_FAMILIES:
        risk += 80
    if family in TERMINAL_FAMILIES:
        risk += 45
    if family == "reference":
        risk += 35
    if size > 2_000_000:
        risk += 40
    elif size > 500_000:
        risk += 30
    if extension in {".env", ".sql", ".sqlite", ".sqlite3"}:
        risk += 50
    return max(0, min(100, risk))


def strategy_for(family: str, size: int, score: int) -> tuple[str, bool, bool, bool]:
    if family in {"secrets", "migrations", "infra"}:
        return "human_only", False, False, True
    if family == "generated":
        return "ignore", False, False, False
    if family in {"logs", "exports"}:
        return "terminal_asset", False, False, True
    if size > 2_000_000:
        return "terminal_asset", False, False, True
    if family == "reference" or size > 500_000:
        return "search_only", False, False, True
    if family == "legacy":
        return "open_later", False, False, True
    if score >= 70:
        return "open_now", True, False, False
    if score >= 40:
        return "open_later", False, False, False
    if score >= 20:
        return "search_only", False, False, True
    return "index_only", False, False, False


def scan(source: Path, limit: int) -> list[FileEntry]:
    now_ts = dt.datetime.now(dt.timezone.utc).timestamp()
    entries = []
    for path in source.rglob("*"):
        if should_skip(path) or not path.is_file():
            continue
        rel = path.relative_to(source).as_posix()
        stat = path.stat()
        ext = path.suffix.lower()
        depth = len(Path(rel).parts) - 1
        family, tier, family_reasons = classify_family(rel)
        role, role_reasons = detect_role(rel, ext, family)
        score, score_reasons = score_file(rel, stat.st_size, ext, depth, family, stat.st_mtime, now_ts)
        risk = risk_score(stat.st_size, family, ext)
        strategy, open_ok, edit_ok, approval = strategy_for(family, stat.st_size, score)
        entries.append(FileEntry(
            relative_path=rel,
            absolute_path=str(path.resolve()).replace("\\", "/"),
            size=stat.st_size,
            modified=utc(stat.st_mtime),
            extension=ext,
            depth=depth,
            folder_family=family,
            family_tier=tier,
            role=role,
            hotpath_score=score,
            risk_score=risk,
            strategy=strategy,
            allowed_to_open=open_ok,
            allowed_to_edit=edit_ok,
            requires_human_approval=approval,
            public_safe=False,
            reason=family_reasons + role_reasons + score_reasons,
        ))
        if len(entries) >= limit:
            break
    return entries


def sort_hot(entries: Iterable[FileEntry]) -> list[FileEntry]:
    return sorted(entries, key=lambda e: (-e.hotpath_score, e.risk_score, e.depth, e.relative_path))


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, entries: list[FileEntry]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(asdict(entry), ensure_ascii=False, sort_keys=True) + "\n")


def family_summary(entries: list[FileEntry]) -> list[dict[str, object]]:
    by_family: dict[str, list[FileEntry]] = {}
    for entry in entries:
        by_family.setdefault(entry.folder_family, []).append(entry)
    rows = []
    for family, items in sorted(by_family.items()):
        avg_score = round(sum(i.hotpath_score for i in items) / len(items), 1)
        strategies: dict[str, int] = {}
        for item in items:
            strategies[item.strategy] = strategies.get(item.strategy, 0) + 1
        dominant = sorted(strategies.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        rows.append({"family": family, "files": len(items), "avg_hotpath_score": avg_score, "dominant_strategy": dominant})
    return rows


def build_queues(entries: list[FileEntry], phase1_max_files: int, phase1_max_bytes: int, phase2_max_files: int) -> dict[str, object]:
    hot = sort_hot(entries)
    phase1 = []
    total = 0
    for entry in hot:
        if entry.strategy != "open_now":
            continue
        if len(phase1) >= phase1_max_files:
            break
        if total + entry.size > phase1_max_bytes and phase1:
            continue
        phase1.append(entry)
        total += entry.size
    phase2 = [e for e in hot if e.strategy == "open_later" and e not in phase1][:phase2_max_files]
    search_targets = [e for e in hot if e.strategy in {"search_only", "terminal_asset"}]
    human_only = [e for e in hot if e.strategy == "human_only"]
    ignored = [e for e in hot if e.strategy == "ignore"]
    return {
        "phase1": [asdict(e) for e in phase1],
        "phase1_total_bytes": total,
        "phase2": [asdict(e) for e in phase2],
        "search_targets": [asdict(e) for e in search_targets],
        "human_only": [asdict(e) for e in human_only],
        "ignored": [asdict(e) for e in ignored],
    }


def write_structure_map(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object]) -> None:
    hot = sort_hot(entries)[:25]
    search_targets = queues.get("search_targets", [])
    human_only = queues.get("human_only", [])
    lines = [
        "# ACG Structure Map",
        "",
        f"Source: `{source}`",
        f"Generated: {dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()}",
        f"Total indexed files: {len(entries)}",
        "",
        "## Cluster Overview",
        "",
        "| Family | Files | Avg Hotpath | Dominant Strategy |",
        "|---|---:|---:|---|",
    ]
    for row in family_summary(entries):
        lines.append(f"| {row['family']} | {row['files']} | {row['avg_hotpath_score']} | {row['dominant_strategy']} |")
    lines += ["", "## Top Hotpath Files", "", "| Score | Risk | Strategy | Family | File |", "|---:|---:|---|---|---|"]
    for entry in hot:
        lines.append(f"| {entry.hotpath_score} | {entry.risk_score} | {entry.strategy} | {entry.folder_family} | `{entry.relative_path}` |")
    lines += ["", "## Phase 1 Reading Queue", ""]
    for item in queues.get("phase1", []):
        lines.append(f"- `{item['relative_path']}` — score {item['hotpath_score']}, {item['role']}")
    lines += ["", "## Search-Only / Terminal Assets", ""]
    for item in search_targets[:25]:
        lines.append(f"- `{item['relative_path']}` — {item['strategy']}, {item['size']} bytes")
    if len(search_targets) > 25:
        lines.append(f"- ... {len(search_targets) - 25} more")
    lines += ["", "## Human-Only Files", ""]
    if human_only:
        for item in human_only[:25]:
            lines.append(f"- `{item['relative_path']}` — {item['folder_family']}")
    else:
        lines.append("- None detected.")
    lines += ["", "## Rule", "", "Do not ask an AI to read the whole folder. Use the reading queues and search targets."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_phase1(out_dir: Path, queues: dict[str, object]) -> None:
    pack = out_dir / "phase1_pack"
    if pack.exists():
        shutil.rmtree(pack)
    pack.mkdir(parents=True, exist_ok=True)
    for item in queues.get("phase1", []):
        src = Path(str(item["absolute_path"]))
        dst = pack / str(item["relative_path"])
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def write_search_targets(path: Path, queues: dict[str, object]) -> None:
    lines = ["# ACG Search Targets", "", "These files should not be opened fully. Use targeted search only.", ""]
    for item in queues.get("search_targets", []):
        lines.append(f"- `{item['relative_path']}` — {item['strategy']}, {item['size']} bytes, risk {item['risk_score']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_execution_brief(path: Path, queues: dict[str, object]) -> None:
    phase1 = queues.get("phase1", [])
    phase2 = queues.get("phase2", [])
    search_targets = queues.get("search_targets", [])
    lines = [
        "# ACG Execution Brief",
        "",
        "You are operating under ACG Structure Scout.",
        "",
        "Do not read the entire source folder. Read only the Phase 1 pack first.",
        "Do not edit files. This is orientation only.",
        "Do not claim final understanding. Return uncertainties explicitly.",
        "",
        "## You may read now",
    ]
    for item in phase1:
        lines.append(f"- `{item['relative_path']}`")
    lines += ["", "## You may request later"]
    for item in phase2[:20]:
        lines.append(f"- `{item['relative_path']}`")
    lines += ["", "## Search-only targets"]
    for item in search_targets[:20]:
        lines.append(f"- `{item['relative_path']}`")
    lines += [
        "", "## Required confirmation", "", "Reply with:", "",
        "```txt", "ACG-UNDERSTOOD: structure-scout", "SCOPE: files you actually read",
        "RISKS: key risks before deeper processing", "QUESTIONS: what needs human approval", "```",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG Structure Scout v0.3")
    parser.add_argument("--source", required=True, help="Folder to scan")
    parser.add_argument("--out", default=".acg", help="Output folder")
    parser.add_argument("--limit", type=int, default=100000, help="Maximum files to index")
    parser.add_argument("--phase1-max-files", type=int, default=12)
    parser.add_argument("--phase1-max-bytes", type=int, default=51200)
    parser.add_argument("--phase2-max-files", type=int, default=25)
    args = parser.parse_args()

    source = Path(args.source).resolve()
    out = Path(args.out).resolve()
    if not source.is_dir():
        raise SystemExit(f"Source folder not found: {source}")
    out.mkdir(parents=True, exist_ok=True)

    entries = scan(source, args.limit)
    queues = build_queues(entries, args.phase1_max_files, args.phase1_max_bytes, args.phase2_max_files)

    write_jsonl(out / "context_manifest.jsonl", entries)
    write_json(out / "hotpaths.json", [asdict(e) for e in sort_hot(entries)[:100]])
    write_json(out / "reading_queues.json", queues)
    write_structure_map(out / "structure_map.md", source, entries, queues)
    write_search_targets(out / "search_targets.md", queues)
    write_execution_brief(out / "execution_brief.md", queues)
    copy_phase1(out, queues)

    print(f"ACG Structure Scout indexed files: {len(entries)}")
    print(f"ACG output folder: {out}")
    print(f"Structure map: {out / 'structure_map.md'}")
    print(f"Reading queues: {out / 'reading_queues.json'}")
    print(f"Phase 1 pack: {out / 'phase1_pack'}")
    print(f"Execution brief: {out / 'execution_brief.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
