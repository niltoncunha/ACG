#!/usr/bin/env python3
"""ACG Structure Scout v0.4-beta-compatible.

Build a structural and topology-aware context package before giving a large
folder or repository to an AI agent.

This is the stable package generator used by scripts/acg-v04.py.
It preserves the v0.3 CLI and generated .acg/artifacts layout while adding
import-graph-driven hotpath scoring for source-code files.

Generated layout:

.acg/
  ACG_MASTER.md
  phase1_pack/
  artifacts/
    context_manifest.jsonl
    structure_map.md
    hotpaths.json
    reading_queues.json
    phase1_queue.md
    phase2_queue.md
    approval_required.md
    search_targets.md
    execution_brief.md
    next_prompt.md
    phase2_plan_template.md
    scout_report.json

No external dependencies.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import os
import re
import shutil
import stat
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

VERSION = "0.4-beta"

EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", "coverage", ".cache", ".pytest_cache", ".mypy_cache",
}

BINARY_OR_DATABASE_EXTENSIONS = {".sqlite", ".sqlite3", ".db", ".db3", ".bin", ".pkl", ".pickle"}
SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs"}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml",
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs", ".java", ".sh", ".ps1",
}

LEGACY_ROOT_ARTIFACTS = {
    "context_manifest.jsonl", "structure_map.md", "hotpaths.json", "reading_queues.json",
    "search_targets.md", "execution_brief.md", "next_prompt.md", "phase1_queue.md",
    "phase2_queue.md", "approval_required.md", "phase2_plan_template.md", "scout_report.json",
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
    ".py": 15, ".ts": 15, ".tsx": 15, ".js": 12, ".jsx": 12, ".mjs": 12, ".cjs": 12,
    ".go": 15, ".rs": 15, ".java": 12,
    ".yaml": 18, ".yml": 18, ".toml": 16, ".json": 10,
    ".md": 8, ".sh": 12, ".ps1": 12, ".sql": -5,
    ".log": -30, ".csv": -20, ".jsonl": -15, ".lock": -25, ".map": -30,
    ".sqlite": -60, ".sqlite3": -60, ".db": -60, ".db3": -60,
}

FAMILY_HOTPATH = {
    "core": 20, "canon": 18, "runtime": 16,
    "tests": 10, "docs": 8, "guides": 8, "evaluation": 8,
    "reference": 5, "memory": 4, "legacy": 2, "unknown": 6,
    "generated": 0, "logs": 0, "exports": 0,
    "secrets": 0, "infra": 0, "migrations": 0,
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
    (r"(^|/)00_core(/|$)|(^|/)core(/|$)|(^|/)src(/|$)|(^|/)app(/|$)|(^|/)lib(/|$)|(^|/)pkg(/|$)|(^|/)cmd(/|$)|(^|/)api(/|$)|(^|/)server(/|$)", "core", "priority"),
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

CONTROL_FILE_NAMES = {
    "acg.yaml", "acg.json", "package.json", "pyproject.toml",
    "cargo.toml", "go.mod", "makefile", "dockerfile",
    "docker-compose.yml", "docker-compose.yaml", "requirements.txt",
    "setup.py", "setup.cfg",
}

ENTRYPOINT_RE = re.compile(
    r"(^|[\\/])(main\.py|main\.go|main\.rs|index\.[jt]sx?|app\.py|server\.py|__main__\.py|cmd[\\/]main\.go|src[\\/]main\.rs|bin[\\/]main\.rs)$",
    re.I,
)

JS_RE = re.compile(r"(?:import\s+.*?\s+from\s+|require\s*\(\s*|import\s*\(\s*)['\"](\.{1,2}/[^'\"]+)['\"]", re.MULTILINE)
RUST_RE = re.compile(r"^\s*use\s+([\w:]+)", re.MULTILINE)
GO_BLOCK_RE = re.compile(r"import\s*\((.*?)\)", re.DOTALL)
GO_SINGLE_RE = re.compile(r'import\s+"([^"]+)"')
GO_ITEM_RE = re.compile(r'"([^"]+)"')


@dataclass
class FileEntry:
    relative_path: str
    absolute_path: str
    size: int
    size_bytes: int
    modified: str
    extension: str
    depth: int
    folder_family: str
    family_tier: str
    role: str
    hotpath_score: int
    risk_score: int
    in_degree: int
    out_degree: int
    topology_score: int
    import_count: int
    strategy: str
    allowed_to_open: bool
    allowed_to_edit: bool
    requires_human_approval: bool
    public_safe: bool
    reason: list[str] = field(default_factory=list)


def utc(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def remove_readonly(func, path: str, exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def safe_rmtree(path: Path) -> None:
    if not path.exists():
        return
    try:
        shutil.rmtree(path, onerror=remove_readonly)
    except PermissionError as exc:
        raise RuntimeError(
            "ACG could not replace phase1_pack because Windows is holding a file or folder open. "
            "Close Explorer, editors, Gemini/Codex/Claude sessions, terminals inside .acg/phase1_pack, "
            "then delete .acg/phase1_pack manually and rerun."
        ) from exc
    except OSError as exc:
        raise RuntimeError(
            f"ACG could not remove old folder: {path}. Close programs using it, delete it manually, and rerun."
        ) from exc


def extract_python_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(read_text(path), filename=str(path))
    except Exception:
        return []
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                if node.level:
                    imports.append("." * int(node.level) + node.module)
                else:
                    imports.append(node.module)
            elif node.level:
                imports.append("." * int(node.level))
    return imports


def extract_js_imports(path: Path) -> list[str]:
    try:
        return JS_RE.findall(read_text(path))
    except OSError:
        return []


def extract_rust_imports(path: Path) -> list[str]:
    try:
        return RUST_RE.findall(read_text(path))
    except OSError:
        return []


def extract_go_imports(path: Path) -> list[str]:
    try:
        text = read_text(path)
    except OSError:
        return []
    block = GO_BLOCK_RE.search(text)
    if block:
        return GO_ITEM_RE.findall(block.group(1))
    single = GO_SINGLE_RE.search(text)
    return [single.group(1)] if single else []


def extract_imports(path: Path) -> list[str]:
    ext = path.suffix.lower()
    if ext == ".py":
        return extract_python_imports(path)
    if ext in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        return extract_js_imports(path)
    if ext == ".rs":
        return extract_rust_imports(path)
    if ext == ".go":
        return extract_go_imports(path)
    return []


def build_file_index(paths: list[Path], source: Path) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in paths:
        if path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        rel = path.relative_to(source).as_posix()
        stem_key = path.with_suffix("").relative_to(source).as_posix()
        index[rel] = rel
        index[stem_key] = rel
        index[path.name] = rel
        index[path.stem] = rel
    return index


def resolve_import(source: Path, from_file: str, raw_import: str, index: dict[str, str]) -> str | None:
    if not raw_import or raw_import.startswith(("http://", "https://")):
        return None
    if raw_import in index:
        return index[raw_import]

    from_path = source / from_file
    base_dir = from_path.parent

    if raw_import.startswith("."):
        candidate = (base_dir / raw_import).resolve()
        try:
            rel_candidate = candidate.relative_to(source.resolve()).as_posix()
        except ValueError:
            return None
        variants = [rel_candidate]
    else:
        variants = [raw_import.replace(".", "/"), raw_import.replace("::", "/"), raw_import]

    extensions = ["", ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs"]
    suffixes = ["", "/index", "/__init__", "/mod"]
    for variant in variants:
        for suffix in suffixes:
            for ext in extensions:
                key = f"{variant}{suffix}{ext}"
                if key in index:
                    return index[key]

    stem = raw_import.split(".")[-1].split("/")[-1].split("::")[-1]
    if stem in index:
        return index[stem]
    return None


def build_import_graph(paths: list[Path], source: Path) -> tuple[dict[str, list[str]], dict[str, int], dict[str, int]]:
    source_paths = [p for p in paths if p.suffix.lower() in SOURCE_EXTENSIONS]
    index = build_file_index(source_paths, source)
    edges: dict[str, list[str]] = {}
    reverse: dict[str, set[str]] = defaultdict(set)

    for path in source_paths:
        rel = path.relative_to(source).as_posix()
        targets: set[str] = set()
        for raw in extract_imports(path):
            target = resolve_import(source, rel, raw, index)
            if target and target != rel:
                targets.add(target)
        edges[rel] = sorted(targets)
        for target in targets:
            reverse[target].add(rel)

    indegree = {rel: len(reverse.get(rel, set())) for rel in index.values()}
    outdegree = {rel: len(edges.get(rel, [])) for rel in index.values()}
    return edges, indegree, outdegree


def classify_family(relative_path: str) -> tuple[str, str, list[str]]:
    low = relative_path.lower()
    if Path(low).suffix in BINARY_OR_DATABASE_EXTENSIONS:
        return "binary_or_database", "terminal", ["matched_family:binary_or_database"]
    for pattern, family, tier in FAMILY_RULES:
        if re.search(pattern, low):
            return family, tier, [f"matched_family:{family}"]
    return "unknown", "standard", ["matched_family:unknown"]


def detect_role(relative_path: str, extension: str, family: str) -> tuple[str, list[str]]:
    low = relative_path.lower()
    name = Path(low).name
    if extension in BINARY_OR_DATABASE_EXTENSIONS:
        return "database_or_binary_asset", ["database_or_binary_extension"]
    if name in {"readme.md", "agents.md", "active-index.md"}:
        return "orientation", ["orientation_name"]
    if "blueprint" in name or "structure_map" in name or "environment_contract" in name:
        return "architecture_or_contract", ["architecture_or_contract_name"]
    if name in CONTROL_FILE_NAMES or "schema" in name:
        return "control_or_schema", ["control_or_schema_name"]
    if family in {"canon", "memory", "guides"}:
        return "governance_or_memory", ["governance_family"]
    if family in {"tests", "evaluation"}:
        return "validation", ["validation_family"]
    if extension in SOURCE_EXTENSIONS or extension == ".java":
        return "source_code", ["source_extension"]
    if family in TERMINAL_FAMILIES or family == "reference":
        return "reference_or_terminal_asset", ["terminal_or_reference_family"]
    return "supporting_file", []


def size_component(size: int) -> int:
    if size < 50_000:
        return 20
    if size < 200_000:
        return 12
    if size < 500_000:
        return 5
    return 0


def heuristic_score(relative_path: str, size: int, extension: str, depth: int, family: str, modified_ts: float, now_ts: float) -> tuple[int, list[str]]:
    score = 50
    reasons: list[str] = []
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
    if family in TERMINAL_FAMILIES or family == "binary_or_database":
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


def score_file(relative_path: str, size: int, extension: str, depth: int, family: str, role: str, modified_ts: float, now_ts: float, in_degree: int, max_in_degree: int) -> tuple[int, int, list[str]]:
    topology = int(60 * (in_degree / max(max_in_degree, 1))) if extension in SOURCE_EXTENSIONS else 0
    reasons: list[str] = []
    if extension in SOURCE_EXTENSIONS:
        score = topology + size_component(size) + FAMILY_HOTPATH.get(family, 6)
        reasons.extend([
            f"topology_score:+{topology}",
            f"size_component:+{size_component(size)}",
            f"family_component:+{FAMILY_HOTPATH.get(family, 6)}",
        ])
        name = Path(relative_path.lower()).name
        if name in CONTROL_FILE_NAMES or ENTRYPOINT_RE.search(relative_path):
            score += 10
            reasons.append("control_or_entrypoint:+10")
        return min(100, score), topology, reasons

    heuristic, heuristic_reasons = heuristic_score(relative_path, size, extension, depth, family, modified_ts, now_ts)
    reasons.extend(heuristic_reasons)
    reasons.append("non_code_heuristic_score")
    return heuristic, topology, reasons


def risk_score(size: int, family: str, extension: str, relative_path: str = "") -> int:
    risk = 0
    if family in HUMAN_ONLY_FAMILIES:
        risk += 80
    if family in TERMINAL_FAMILIES or family == "binary_or_database":
        risk += 45
    if family == "reference":
        risk += 35
    if size > 2_000_000:
        risk += 40
    elif size > 500_000:
        risk += 30
    if extension in {".env", ".sql", ".sqlite", ".sqlite3", ".db", ".db3"}:
        risk += 50
    if re.search(r"secret|password|token|api.?key|credential", relative_path, re.I):
        risk += 30
    return max(0, min(100, risk))


def strategy_for(family: str, size: int, score: int, extension: str, risk: int) -> tuple[str, bool, bool, bool]:
    if family in {"secrets", "migrations", "infra"} or risk >= 60:
        return "human_only", False, False, True
    if extension in BINARY_OR_DATABASE_EXTENSIONS or family == "binary_or_database":
        return "terminal_asset", False, False, True
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


def collect_paths(source: Path, limit: int) -> list[Path]:
    paths: list[Path] = []
    for path in source.rglob("*"):
        if should_skip(path) or not path.is_file():
            continue
        paths.append(path)
        if len(paths) >= limit:
            break
    return paths


def scan(source: Path, limit: int) -> tuple[list[FileEntry], dict[str, object]]:
    now_ts = dt.datetime.now(dt.timezone.utc).timestamp()
    paths = collect_paths(source, limit)
    edges, indegree, outdegree = build_import_graph(paths, source)
    max_in_degree = max(indegree.values(), default=0)
    entries: list[FileEntry] = []
    has_entrypoint = False
    has_control = False

    for path in paths:
        rel = path.relative_to(source).as_posix()
        st = path.stat()
        ext = path.suffix.lower()
        depth = len(Path(rel).parts) - 1
        family, tier, family_reasons = classify_family(rel)
        role, role_reasons = detect_role(rel, ext, family)
        in_deg = int(indegree.get(rel, 0))
        out_deg = int(outdegree.get(rel, 0))
        score, topology, score_reasons = score_file(rel, st.st_size, ext, depth, family, role, st.st_mtime, now_ts, in_deg, max_in_degree)
        risk = risk_score(st.st_size, family, ext, rel)
        strategy, open_ok, edit_ok, approval = strategy_for(family, st.st_size, score, ext, risk)
        if path.name.lower() in CONTROL_FILE_NAMES:
            has_control = True
        if ENTRYPOINT_RE.search(rel):
            has_entrypoint = True
        entries.append(FileEntry(
            relative_path=rel,
            absolute_path=str(path.resolve()).replace("\\", "/"),
            size=st.st_size,
            size_bytes=st.st_size,
            modified=utc(st.st_mtime),
            extension=ext,
            depth=depth,
            folder_family=family,
            family_tier=tier,
            role=role,
            hotpath_score=score,
            risk_score=risk,
            in_degree=in_deg,
            out_degree=out_deg,
            topology_score=topology,
            import_count=out_deg,
            strategy=strategy,
            allowed_to_open=open_ok,
            allowed_to_edit=edit_ok,
            requires_human_approval=approval,
            public_safe=False,
            reason=family_reasons + role_reasons + score_reasons,
        ))

    graph_stats = {
        "total_edges": sum(len(v) for v in edges.values()),
        "max_in_degree": max_in_degree,
        "nodes": len(edges),
        "has_entrypoint": has_entrypoint,
        "has_control_files": has_control,
        "hotpath_score_basis": "source_code: topology(60)+size(20)+family(20); non_code: structural heuristic",
    }
    return entries, graph_stats


def sort_hot(entries: Iterable[FileEntry]) -> list[FileEntry]:
    return sorted(entries, key=lambda e: (-e.hotpath_score, -e.in_degree, e.risk_score, e.depth, e.relative_path))


def is_safe_read_candidate(entry: FileEntry) -> bool:
    return (
        entry.strategy in {"open_now", "open_later"}
        and not entry.requires_human_approval
        and entry.folder_family not in TERMINAL_FAMILIES
        and entry.folder_family not in HUMAN_ONLY_FAMILIES
        and entry.folder_family != "binary_or_database"
        and entry.extension in TEXT_EXTENSIONS
    )


def readiness_score(entries: list[FileEntry], graph_stats: dict[str, object]) -> float:
    total = max(len(entries), 1)
    has_entrypoint = bool(graph_stats.get("has_entrypoint"))
    has_control = bool(graph_stats.get("has_control_files"))
    w1 = 0.30 if has_entrypoint else 0.0
    w2 = 0.25 if has_control else 0.0
    open_now = sum(1 for entry in entries if entry.strategy == "open_now")
    w3 = 0.25 * min((open_now / total) * 4.0, 1.0)
    # Broken refs are not included in stable package generation yet.
    broken_refs = 0
    w4 = 0.20 * max(0.0, 1.0 - broken_refs / total)
    score = w1 + w2 + w3 + w4
    if not has_entrypoint and not has_control:
        score = min(score, 0.44)
    return round(score, 3)


def guardrail_mode(score: float) -> str:
    if score >= 0.65:
        return "silent"
    if score >= 0.45:
        return "warn"
    return "halt"


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
    phase1: list[FileEntry] = []
    total = 0
    for entry in hot:
        if entry.strategy != "open_now" or not is_safe_read_candidate(entry):
            continue
        if len(phase1) >= phase1_max_files:
            break
        if total + entry.size > phase1_max_bytes and phase1:
            continue
        phase1.append(entry)
        total += entry.size

    phase1_paths = {e.relative_path for e in phase1}
    phase2_candidates = [e for e in hot if e.relative_path not in phase1_paths and is_safe_read_candidate(e)]
    phase2 = phase2_candidates[:phase2_max_files]
    approval_required = [e for e in hot if e.strategy in {"open_now", "open_later"} and e.requires_human_approval]
    search_targets = [e for e in hot if e.strategy in {"search_only", "terminal_asset"}]
    human_only = [e for e in hot if e.strategy == "human_only"]
    ignored = [e for e in hot if e.strategy == "ignore"]
    return {
        "phase1": [asdict(e) for e in phase1],
        "phase1_total_bytes": total,
        "phase2": [asdict(e) for e in phase2],
        "approval_required": [asdict(e) for e in approval_required],
        "search_targets": [asdict(e) for e in search_targets],
        "human_only": [asdict(e) for e in human_only],
        "ignored": [asdict(e) for e in ignored],
    }


def write_queue_markdown(path: Path, title: str, description: str, items: list[dict[str, object]]) -> None:
    lines = [f"# {title}", "", description, "", "| # | File | Role | Family | Score | In | Risk | Strategy |", "|---:|---|---|---|---:|---:|---:|---|"]
    if not items:
        lines.append("| - | None | - | - | - | - | - | - |")
    else:
        for i, item in enumerate(items, 1):
            lines.append(
                f"| {i} | `{item['relative_path']}` | {item['role']} | {item['folder_family']} | "
                f"{item['hotpath_score']} | {item.get('in_degree', 0)} | {item['risk_score']} | {item['strategy']} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_structure_map(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object], graph_stats: dict[str, object]) -> None:
    hot = sort_hot(entries)[:25]
    search_targets = queues.get("search_targets", [])
    human_only = queues.get("human_only", [])
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    lines = [
        "# ACG Structure Map",
        "",
        f"Version: `{VERSION}`",
        f"Source: `{source}`",
        f"Generated: {dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()}",
        f"Total indexed files: {len(entries)}",
        f"Readiness score: {readiness} [{mode.upper()}]",
        "",
        "## Import Graph Stats",
        "",
        f"- Nodes: {graph_stats.get('nodes', 0)}",
        f"- Total edges: {graph_stats.get('total_edges', 0)}",
        f"- Max in-degree: {graph_stats.get('max_in_degree', 0)}",
        f"- Score basis: {graph_stats.get('hotpath_score_basis')}",
        "",
        "## Companion Artifacts",
        "",
        "- Master file: `../ACG_MASTER.md`",
        "- Full manifest: `context_manifest.jsonl`",
        "- Scout report: `scout_report.json`",
        "- Machine-readable queues: `reading_queues.json`",
        "- Human-readable Phase 1 queue: `phase1_queue.md`",
        "- Human-readable Phase 2 queue: `phase2_queue.md`",
        "- Phase 2 response contract: `phase2_plan_template.md`",
        "- Full search-only list: `search_targets.md`",
        "- Continuation protocol: `next_prompt.md`",
        "- AI handoff: `execution_brief.md`",
        "- Controlled initial files: `../phase1_pack/`",
        "",
        "## Cluster Overview",
        "",
        "| Family | Files | Avg Hotpath | Dominant Strategy |",
        "|---|---:|---:|---|",
    ]
    for row in family_summary(entries):
        lines.append(f"| {row['family']} | {row['files']} | {row['avg_hotpath_score']} | {row['dominant_strategy']} |")
    lines += ["", "## Top Hotpath Files", "", "| Score | In | Out | Risk | Strategy | Family | File |", "|---:|---:|---:|---:|---|---|---|"]
    for entry in hot:
        lines.append(f"| {entry.hotpath_score} | {entry.in_degree} | {entry.out_degree} | {entry.risk_score} | {entry.strategy} | {entry.folder_family} | `{entry.relative_path}` |")
    lines += ["", "## Phase 1 Reading Queue", "", "See `phase1_queue.md` for the complete human-readable queue.", ""]
    for item in queues.get("phase1", []):
        lines.append(f"- `{item['relative_path']}` - score {item['hotpath_score']}, in_degree {item.get('in_degree', 0)}, {item['role']}")
    lines += ["", "## Search-Only / Terminal Assets", "", "Summary only. See `search_targets.md` for the full list.", ""]
    for item in search_targets[:25]:
        lines.append(f"- `{item['relative_path']}` - {item['strategy']}, {item['size']} bytes")
    if len(search_targets) > 25:
        lines.append(f"- ... {len(search_targets) - 25} more. Full list: `search_targets.md`; machine-readable queue: `reading_queues.json`.")
    lines += ["", "## Human-Only Files", ""]
    if human_only:
        for item in human_only[:25]:
            lines.append(f"- `{item['relative_path']}` - {item['folder_family']}")
        if len(human_only) > 25:
            lines.append(f"- ... {len(human_only) - 25} more. Full list: `reading_queues.json` under `human_only`.")
    else:
        lines.append("- None detected.")
    lines += ["", "## Rule", "", "Do not ask an AI to read the whole folder. Use the reading queues and search targets."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_phase1(out_dir: Path, queues: dict[str, object]) -> None:
    pack = out_dir / "phase1_pack"
    if pack.exists():
        safe_rmtree(pack)
    pack.mkdir(parents=True, exist_ok=True)
    for item in queues.get("phase1", []):
        src = Path(str(item["absolute_path"]))
        dst = pack / str(item["relative_path"])
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def write_search_targets(path: Path, queues: dict[str, object]) -> None:
    lines = ["# ACG Search Targets", "", "These files should not be opened fully. Use targeted search only.", ""]
    for item in queues.get("search_targets", []):
        lines.append(f"- `{item['relative_path']}` - {item['strategy']}, {item['size']} bytes, risk {item['risk_score']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_phase2_template(path: Path) -> None:
    path.write_text("""# ACG Phase 2 Plan Template

The AI must use this exact structure for the NEXT block after Phase 1.

A Phase 2 plan is invalid if any requested file is missing one of these fields.

```txt
NEXT:
Detected mode: <MAP_ONLY|REFACTOR|BUGFIX|FEATURE|DOCS|TESTS|SECURITY|UNKNOWN>

If UNKNOWN:
1. <concrete question 1>
2. <concrete question 2>
3. <concrete question 3>
STOP: waiting for human clarification.

If known:
## ACG Phase 2 Reading Plan

Exact files requested:
1. <relative path>
   - why needed: <specific reason>
   - question answered: <specific question>
   - queue source: phase2_queue.md
   - risk: <risk or none>

Files explicitly excluded:
- search_only: excluded unless targeted search is approved
- terminal_asset: excluded
- legacy: excluded unless approval_required exception is approved
- logs: excluded
- exports: excluded
- binary/database: excluded
- original source folder: excluded

Approval-required exceptions:
- none OR <exact file + reason + why normal queue is insufficient>

Decision:
WAITING_FOR_HUMAN_APPROVAL
```
""", encoding="utf-8")


def write_execution_brief(path: Path, queues: dict[str, object], entries: list[FileEntry], graph_stats: dict[str, object]) -> None:
    phase1 = queues.get("phase1", [])
    phase2 = queues.get("phase2", [])
    search_targets = queues.get("search_targets", [])
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    lines = [
        "# ACG Execution Brief",
        "",
        f"You are operating under ACG Structure Scout v{VERSION}.",
        "",
        f"Readiness: {readiness} [{mode.upper()}]",
        "",
        "Import graph scoring is active for source-code files. `hotpath_score` includes `in_degree` topology where imports can be resolved.",
        "",
        "Read `../ACG_MASTER.md` first. It is the only root-level instruction file.",
        "Read `next_prompt.md` before Phase 1. It is your continuation protocol after Phase 1.",
        "Read `phase2_plan_template.md` before Phase 1. It defines the required NEXT format.",
        "Use `phase1_queue.md` and `phase2_queue.md` for conversational planning; do not depend on reading the full JSON manually.",
        "Do not read the entire source folder. Read only the Phase 1 pack first.",
        "Do not edit files. This is orientation only.",
        "Do not claim final understanding. Return uncertainties explicitly.",
        "The human should not need to copy/paste a second prompt. You must apply `next_prompt.md` automatically after Phase 1.",
        "",
        "## Import Graph Stats",
        "",
        f"- total_edges: {graph_stats.get('total_edges', 0)}",
        f"- max_in_degree: {graph_stats.get('max_in_degree', 0)}",
        f"- score_basis: {graph_stats.get('hotpath_score_basis')}",
        "",
        "## Required artifacts to inspect first",
        "",
        "- `../ACG_MASTER.md`",
        "- `execution_brief.md`",
        "- `next_prompt.md`",
        "- `phase2_plan_template.md`",
        "- `structure_map.md`",
        "- `phase1_queue.md`",
        "- `phase2_queue.md`",
        "- `approval_required.md`",
        "- `search_targets.md`",
        "- `../phase1_pack/`",
        "",
        "## You may read now",
    ]
    for item in phase1:
        lines.append(f"- `{item['relative_path']}`")
    lines += ["", "## You may request later"]
    for item in phase2[:20]:
        lines.append(f"- `{item['relative_path']}`")
    if len(phase2) > 20:
        lines.append(f"- ... {len(phase2) - 20} more. Full queue: `phase2_queue.md`.")
    lines += ["", "## Search-only targets", "", "Summary only. Do not infer that this is the full list; use `search_targets.md`.", ""]
    for item in search_targets[:20]:
        lines.append(f"- `{item['relative_path']}`")
    if len(search_targets) > 20:
        lines.append(f"- ... {len(search_targets) - 20} more. Full list: `search_targets.md`; machine-readable queue: `reading_queues.json` under `search_targets`.")
    lines += [
        "", "## Required Phase 1 Output", "", "After Phase 1, reply with:", "",
        "```txt", "ACG-UNDERSTOOD: structure-scout", "SCOPE: files you actually read",
        "RISKS: key risks before deeper processing", "QUESTIONS: objective questions or approval requests only",
        "NEXT: Phase 2 plan or up to 3 clarification questions, following next_prompt.md and phase2_plan_template.md", "```",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_next_prompt(path: Path, queues: dict[str, object]) -> None:
    phase2 = queues.get("phase2", [])
    approval_required = queues.get("approval_required", [])
    lines = [
        "# ACG Continuation Protocol",
        "",
        "This file is not a human copy/paste prompt.",
        "The AI must read this file before Phase 1 and apply it automatically after Phase 1.",
        "The AI must also follow `phase2_plan_template.md` exactly when writing NEXT.",
        "",
        "## After Phase 1",
        "",
        "Do not open new files yet.",
        "Do not read the original source folder directly.",
        "Do not open search-only, terminal, legacy, log, export, database or binary files.",
        "Do not ask vague questions such as 'what next?'.",
        "Do not assume a refactor, bugfix, or feature task if the user only requested orientation.",
        "",
        "Classify the user's intent into one of these modes:",
        "",
        "1. MAP_ONLY - understand/organize the codebase without edits",
        "2. REFACTOR - change structure while preserving behavior",
        "3. BUGFIX - investigate a concrete failure",
        "4. FEATURE - add a bounded capability",
        "5. DOCS - improve documentation or onboarding",
        "6. TESTS - improve verification coverage",
        "7. SECURITY - inspect sensitive or risky behavior",
        "8. UNKNOWN - objective not clear enough",
        "",
        "If the user only asked to open ACG_MASTER or run orientation, use MAP_ONLY.",
        "If the mode is UNKNOWN, ask at most 3 concrete questions and stop.",
        "If the mode is known, produce a bounded Phase 2 Reading Plan from `phase2_queue.md` only.",
        "",
        "## Required NEXT block",
        "",
        "Return NEXT using `phase2_plan_template.md` exactly.",
        "A NEXT block is invalid if it does not list exact files, why each is needed, what question each answers, exclusions, approval-required exceptions, and WAITING_FOR_HUMAN_APPROVAL.",
        "",
        "## Current safe Phase 2 candidates",
        "",
    ]
    if phase2:
        for item in phase2:
            lines.append(f"- `{item['relative_path']}` - {item['role']}, score {item['hotpath_score']}, in_degree {item.get('in_degree', 0)}")
    else:
        lines.append("- None generated. Ask for objective clarification or request a human-approved exception.")
    lines += ["", "## Approval-required exceptions", ""]
    if approval_required:
        for item in approval_required[:30]:
            lines.append(f"- `{item['relative_path']}` - {item['folder_family']}, {item['strategy']}, risk {item['risk_score']}")
        if len(approval_required) > 30:
            lines.append(f"- ... {len(approval_required) - 30} more in `approval_required.md`.")
    else:
        lines.append("- None.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_master(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object], graph_stats: dict[str, object]) -> None:
    phase1 = queues.get("phase1", [])
    phase2 = queues.get("phase2", [])
    approval_required = queues.get("approval_required", [])
    search_targets = queues.get("search_targets", [])
    human_only = queues.get("human_only", [])
    ignored = queues.get("ignored", [])
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    lines = [
        "# ACG Master Context File",
        "",
        f"Generated by ACG Structure Scout v{VERSION}.",
        "",
        "This is the root instruction file for the generated ACG context package.",
        "",
        "Start here. Do not treat files in `artifacts/` as separate entrypoints unless this file points to them.",
        "",
        "## Generated Layout",
        "",
        "```txt",
        ".acg/",
        "  ACG_MASTER.md",
        "  phase1_pack/",
        "  artifacts/",
        "    context_manifest.jsonl",
        "    structure_map.md",
        "    hotpaths.json",
        "    reading_queues.json",
        "    phase1_queue.md",
        "    phase2_queue.md",
        "    approval_required.md",
        "    search_targets.md",
        "    execution_brief.md",
        "    next_prompt.md",
        "    phase2_plan_template.md",
        "    scout_report.json",
        "```",
        "",
        "## Source",
        "",
        f"`{source}`",
        "",
        "## Inventory Summary",
        "",
        f"- Total indexed files: {len(entries)}",
        f"- Phase 1 files: {len(phase1)}",
        f"- Safe Phase 2 candidates: {len(phase2)}",
        f"- Approval-required candidates: {len(approval_required)}",
        f"- Search-only / terminal assets: {len(search_targets)}",
        f"- Human-only files: {len(human_only)}",
        f"- Ignored files: {len(ignored)}",
        f"- Import graph nodes: {graph_stats.get('nodes', 0)}",
        f"- Import graph edges: {graph_stats.get('total_edges', 0)}",
        f"- Max in-degree: {graph_stats.get('max_in_degree', 0)}",
        f"- Readiness score: {readiness} [{mode.upper()}]",
        "",
        "## What the human does",
        "",
        "The human does not need to invent follow-up prompts or copy/paste `next_prompt.md`.",
        "The human gives the AI this file, then approves, rejects, or clarifies the AI's bounded NEXT block.",
        "",
        "## Read Order for AI",
        "",
        "1. Read this file: `ACG_MASTER.md`.",
        "2. Read `artifacts/execution_brief.md`.",
        "3. Read `artifacts/next_prompt.md` before Phase 1; it is the automatic continuation protocol.",
        "4. Read `artifacts/phase2_plan_template.md`; it is the required NEXT output contract.",
        "5. Read `artifacts/structure_map.md` for the structural and topology overview.",
        "6. Read `artifacts/phase1_queue.md` and `artifacts/phase2_queue.md` for human-readable queues.",
        "7. Read `artifacts/approval_required.md` and `artifacts/search_targets.md` to understand what must not be opened directly.",
        "8. Read only files copied inside `phase1_pack/`.",
        "9. Return the Phase 1 confirmation plus a fully formed NEXT block. Do not wait for the human to paste another prompt.",
        "",
        "## Do Not Do",
        "",
        "- Do not read the original source folder blindly.",
        "- Do not open terminal assets directly.",
        "- Do not treat `... N more` summaries as complete lists.",
        "- Do not depend on reading full JSON manually when a compact `.md` queue exists.",
        "- Do not edit files during orientation.",
        "- Do not claim final understanding from Phase 1 alone.",
        "- Do not ask the human vague questions such as 'what next?' Use `next_prompt.md`.",
        "",
        "## Required AI Output",
        "",
        "```txt",
        "ACG-UNDERSTOOD: structure-scout",
        "SCOPE: files you actually read",
        "RISKS: key risks before deeper processing",
        "QUESTIONS: objective questions or approval requests only",
        "NEXT: apply artifacts/next_prompt.md and artifacts/phase2_plan_template.md automatically",
        "```",
        "",
        "## Human Next Step",
        "",
        "Approve, reject, or clarify the AI's NEXT block. Do not design a new prompt manually.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cleanup_legacy_root_artifacts(out: Path) -> None:
    for name in LEGACY_ROOT_ARTIFACTS:
        target = out / name
        if target.is_file():
            target.unlink()


def write_scout_report(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object], graph_stats: dict[str, object]) -> None:
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    extensions: dict[str, int] = {}
    for entry in entries:
        if entry.extension:
            extensions[entry.extension] = extensions.get(entry.extension, 0) + 1
    report = {
        "acg_version": VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "root": str(source),
        "system_profile": {
            "total_files": len(entries),
            "language_map": extensions,
            "has_entrypoint": bool(graph_stats.get("has_entrypoint")),
            "has_control_files": bool(graph_stats.get("has_control_files")),
        },
        "readiness_score": readiness,
        "guardrail_mode": mode,
        "attention_queue": queues.get("phase1", [])[:20],
        "phased_reading_plan": {
            "phase1": queues.get("phase1", []),
            "phase2": queues.get("phase2", []),
            "phase3": queues.get("search_targets", [])[:10],
        },
        "broken_refs": [],
        "execution_brief": {
            "task_id": "structure-scout",
            "root": str(source),
            "total_files": len(entries),
            "readiness_score": readiness,
            "guardrail_mode": mode,
            "readiness_components": {
                "W1_entrypoint_detected": bool(graph_stats.get("has_entrypoint")),
                "W2_control_files_present": bool(graph_stats.get("has_control_files")),
                "W3_open_now_count": len(queues.get("phase1", [])),
                "W4_broken_refs_count": 0,
            },
            "import_graph": {
                "total_edges": graph_stats.get("total_edges", 0),
                "max_in_degree": graph_stats.get("max_in_degree", 0),
                "hotpath_score_basis": graph_stats.get("hotpath_score_basis"),
            },
            "instruction": "Read Phase 1 files only. Return ACG-UNDERSTOOD, SCOPE, RISKS, QUESTIONS, NEXT before any edit.",
        },
        "context_manifest": [asdict(entry) for entry in entries],
    }
    write_json(path, report)


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG Structure Scout v0.4-beta-compatible")
    parser.add_argument("--source", required=True, help="Folder to scan")
    parser.add_argument("--out", default=".acg", help="Output folder")
    parser.add_argument("--limit", type=int, default=100000, help="Maximum files to index")
    parser.add_argument("--phase1-max-files", type=int, default=12)
    parser.add_argument("--phase1-max-bytes", type=int, default=51200)
    parser.add_argument("--phase2-max-files", type=int, default=25)
    args = parser.parse_args()

    source = Path(args.source).resolve()
    out = Path(args.out).resolve()
    artifacts = out / "artifacts"
    if not source.is_dir():
        raise SystemExit(f"Source folder not found: {source}")
    out.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir(parents=True, exist_ok=True)
    cleanup_legacy_root_artifacts(out)

    entries, graph_stats = scan(source, args.limit)
    queues = build_queues(entries, args.phase1_max_files, args.phase1_max_bytes, args.phase2_max_files)

    write_jsonl(artifacts / "context_manifest.jsonl", entries)
    write_json(artifacts / "hotpaths.json", [asdict(e) for e in sort_hot(entries)[:100]])
    write_json(artifacts / "reading_queues.json", queues)
    write_queue_markdown(artifacts / "phase1_queue.md", "ACG Phase 1 Queue", "Files copied into `../phase1_pack/` and allowed for first orientation.", queues["phase1"])
    write_queue_markdown(artifacts / "phase2_queue.md", "ACG Phase 2 Queue", "Safe candidates for a bounded Phase 2 reading plan. Do not open until human approval.", queues["phase2"])
    write_queue_markdown(artifacts / "approval_required.md", "ACG Approval-Required Queue", "Files that require explicit human approval before reading.", queues["approval_required"])
    write_phase2_template(artifacts / "phase2_plan_template.md")
    write_structure_map(artifacts / "structure_map.md", source, entries, queues, graph_stats)
    write_search_targets(artifacts / "search_targets.md", queues)
    write_execution_brief(artifacts / "execution_brief.md", queues, entries, graph_stats)
    write_next_prompt(artifacts / "next_prompt.md", queues)
    copy_phase1(out, queues)
    write_master(out / "ACG_MASTER.md", source, entries, queues, graph_stats)
    write_scout_report(artifacts / "scout_report.json", source, entries, queues, graph_stats)

    print(f"ACG Structure Scout indexed files: {len(entries)}")
    print(f"ACG Structure Scout version: {VERSION}")
    print(f"Import graph nodes: {graph_stats.get('nodes', 0)}")
    print(f"Import graph edges: {graph_stats.get('total_edges', 0)}")
    print(f"Max in-degree: {graph_stats.get('max_in_degree', 0)}")
    print(f"ACG output folder: {out}")
    print(f"Master file: {out / 'ACG_MASTER.md'}")
    print(f"Artifacts folder: {artifacts}")
    print(f"Structure map: {artifacts / 'structure_map.md'}")
    print(f"Phase 1 queue: {artifacts / 'phase1_queue.md'}")
    print(f"Phase 2 queue: {artifacts / 'phase2_queue.md'}")
    print(f"Phase 2 template: {artifacts / 'phase2_plan_template.md'}")
    print(f"Scout report: {artifacts / 'scout_report.json'}")
    print(f"Next protocol: {artifacts / 'next_prompt.md'}")
    print(f"Phase 1 pack: {out / 'phase1_pack'}")
    print(f"Execution brief: {artifacts / 'execution_brief.md'}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        raise SystemExit(f"ACG ERROR: {exc}")
