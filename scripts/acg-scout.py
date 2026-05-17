#!/usr/bin/env python3
"""ACG Structure Scout v0.4-beta.

Stable package generator used by scripts/acg-v04.py.

Public CLI:
  python scripts/acg-scout.py --source /path/to/project --out .acg

Core behavior:
- classify file ownership before ranking;
- separate PROJECT_OWNED material from tool runtimes, dependencies, generated cache,
  references, corpora and unknown external material;
- build the main import graph only from PROJECT_OWNED source files;
- classify project_kind before readiness;
- generate mapping gates, phase reading order, citation checks, environment mode,
  and scout regime so an agent cannot treat ACG-UNDERSTOOD as a shallow formality.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import fnmatch
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
MAX_IMPORT_PARSE_BYTES = 350_000

SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs"}
DOC_EXTENSIONS = {".md", ".txt", ".rst", ".adoc"}
DATA_EXTENSIONS = {".csv", ".tsv", ".jsonl", ".parquet", ".arrow", ".feather", ".ndjson"}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".rst", ".adoc", ".json", ".jsonl", ".yaml", ".yml", ".toml",
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs", ".java", ".sh", ".ps1",
}
BINARY_OR_DATABASE_EXTENSIONS = {".sqlite", ".sqlite3", ".db", ".db3", ".bin", ".pkl", ".pickle"}

PRUNE_DIR_NAMES = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules", ".pnpm", ".yarn", ".npm",
    "bower_components", ".venv", "venv", "env", "__pypackages__", "site-packages",
    "dist-packages", "target", ".gradle", ".mypy_cache", ".pytest_cache", ".ruff_cache",
}
ALLOWED_HIDDEN_DIRS = {".github"}
DEPENDENCY_MARKERS = {"node_modules", ".pnpm", "bower_components", "site-packages", "dist-packages", "__pypackages__", "vendor", "vendors", "third_party", ".venv", "venv", "env"}
TOOL_RUNTIME_MARKERS = {"runtimes", "runtime-cache", "toolchains", "plugins", "extensions", "cache", ".cache"}
GENERATED_MARKERS = {"dist", "build", "coverage", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "generated", ".generated", "out", "outputs"}
REFERENCE_MARKERS = {"refs", "reference", "references", "samples", "fixtures", "ssot"}
DATASET_MARKERS = {"dataset", "datasets", "corpus", "corpora", "data", "datalake", "chat_exports", "exports"}

PROJECT_MARKER_FILES = {
    "AGENTS.md", "README.md", "START.HERE.md", "MANIFEST.md", "VISIBLE_WORKSPACE_MAP.md",
    "ACTIVE-INDEX.md", "acg.yaml", "acg.json", "package.json", "pyproject.toml",
    "Cargo.toml", "go.mod", "Makefile", "requirements.txt", "setup.py", "setup.cfg",
    "tsconfig.json", "pnpm-workspace.yaml", "WORKSPACE",
}
PROJECT_MARKER_DIRS = {
    "src", "lib", "app", "apps", "packages", "pkg", "cmd", "api", "server",
    "tests", "test", "docs", "workspace", "agent_files", "00_core", "00-core", "01_canon",
    "01-canon", "02_memory", "02-memory", "03_profiles", "03-profiles", "04_eval",
    "04-eval", "06_runtime_guides", "06-runtime-guides",
}
CONTROL_FILE_NAMES = {
    "acg.yaml", "acg.json", "package.json", "pyproject.toml", "cargo.toml", "go.mod",
    "makefile", "dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "requirements.txt", "setup.py", "setup.cfg", "tsconfig.json",
}
ORIENTATION_ENTRYPOINT_NAMES = {"agents.md", "active-index.md", "start.here.md", "manifest.md", "visible_workspace_map.md", "readme.md"}
STRUCTURAL_CONTRACT_NAMES = {
    "system_law.md", "memory_contract.md", "environment_contract.md", "agents.md",
    "active-index.md", "manifest.md", "start.here.md", "visible_workspace_map.md",
    "genio.active.set.md", "genio.cleanup.map.md", "genio.nucleus.core.md",
}
DATASET_CONTROL_NAMES = {"manifest.md", "manifest.json", "schema.json", "schema.yaml", "dataset.json", "metadata.json", "readme.md"}
ENTRYPOINT_RE = re.compile(r"(^|[\\/])(main\.py|main\.go|main\.rs|index\.[jt]sx?|app\.py|server\.py|__main__\.py|cmd[\\/]main\.go|src[\\/]main\.rs|bin[\\/]main\.rs)$", re.I)

LEGACY_ROOT_ARTIFACTS = {
    "context_manifest.jsonl", "structure_map.md", "hotpaths.json", "reading_queues.json",
    "search_targets.md", "execution_brief.md", "next_prompt.md", "phase1_queue.md",
    "phase2_queue.md", "approval_required.md", "phase2_plan_template.md", "scout_report.json",
    "phase1_reading_order.md", "citation_check.md",
}
CRITICAL_NAME_WEIGHTS = {
    "agents.md": 42, "active-index.md": 40, "start.here.md": 40, "manifest.md": 34,
    "visible_workspace_map.md": 34, "readme.md": 22, "environment_contract.md": 38,
    "system_law.md": 36, "memory_contract.md": 34, "blueprint": 34, "structure_map": 34,
    "runtime_execution.md": 30, "acg.yaml": 38, "package.json": 30, "pyproject.toml": 30,
    "go.mod": 30, "cargo.toml": 30, "tsconfig.json": 26, "requirements.txt": 24,
}
FAMILY_HOTPATH = {
    "core": 20, "canon": 18, "runtime": 16, "tests": 10, "docs": 8, "guides": 8,
    "evaluation": 8, "reference": 5, "memory": 4, "dataset": 6, "legacy": 2,
    "unknown": 6, "generated": 0, "logs": 0, "exports": 0, "secrets": 0,
    "infra": 0, "migrations": 0,
}
FAMILY_RULES = [
    (r"(^|/)90_legacy(/|$)|(^|/)90-legacy(/|$)|(^|/)legacy(/|$)|(^|/)archive|(^|/)_old(/|$)|(^|/)old(/|$)", "legacy", "terminal"),
    (r"(^|/)logs?(/|$)|\.log$", "logs", "terminal"),
    (r"(^|/)chat_exports?(/|$)|(^|/)exports?(/|$)", "exports", "terminal"),
    (r"(^|/)datasets?(/|$)|(^|/)corpus(/|$)|(^|/)corpora(/|$)|(^|/)data(/|$)", "dataset", "search_only"),
    (r"(^|/)ssot(/|$)|(^|/)refs(/|$)", "reference", "search_only"),
    (r"(^|/)dist(/|$)|(^|/)build(/|$)|\.cache(/|$)|__pycache__", "generated", "ignore"),
    (r"(^|/)\.env$|(^|/)\.env\.|(^|/)secrets?(/|$)", "secrets", "human_only"),
    (r"(^|/)migrations?(/|$)|(^|/)schema/.*\.sql$", "migrations", "human_only"),
    (r"(^|/)infra(/|$)|(^|/)terraform(/|$)|\.tf$", "infra", "human_only"),
    (r"(^|/)00_core(/|$)|(^|/)00-core(/|$)|(^|/)core(/|$)|(^|/)src(/|$)|(^|/)app(/|$)|(^|/)lib(/|$)|(^|/)pkg(/|$)|(^|/)cmd(/|$)|(^|/)api(/|$)|(^|/)server(/|$)|(^|/)workspace(/|$)", "core", "priority"),
    (r"(^|/)01_canon(/|$)|(^|/)01-canon(/|$)|(^|/)canon(/|$)", "canon", "priority"),
    (r"(^|/)02_memory(/|$)|(^|/)02-memory(/|$)|(^|/)memory(/|$)|(^|/)state(/|$)", "memory", "priority"),
    (r"(^|/)scripts?(/|$)|(^|/)bin(/|$)|(^|/)cli(/|$)", "runtime", "standard"),
    (r"(^|/)tests?(/|$)|(^|/)spec(/|$)|(^|/)__tests__(/|$)", "tests", "standard"),
    (r"(^|/)docs?(/|$)|(^|/)documentation(/|$)", "docs", "standard"),
    (r"(^|/)06_runtime|(^|/)06-runtime|(^|/)guides?(/|$)", "guides", "standard"),
    (r"(^|/)eval(/|$)|(^|/)lab(/|$)|benchmark", "evaluation", "later"),
]
TERMINAL_FAMILIES = {"legacy", "logs", "exports", "generated"}
HUMAN_ONLY_FAMILIES = {"secrets", "migrations", "infra"}

JS_RE = re.compile(r"(?:import\s+.*?\s+from\s+|require\s*\(\s*|import\s*\(\s*)['\"](\.{1,2}/[^'\"]+)['\"]", re.MULTILINE)
RUST_RE = re.compile(r"^\s*use\s+([\w:]+)", re.MULTILINE)
GO_BLOCK_RE = re.compile(r"import\s*\((.*?)\)", re.DOTALL)
GO_SINGLE_RE = re.compile(r'import\s+"([^"]+)"')
GO_ITEM_RE = re.compile(r'"([^"]+)"')

@dataclass
class Ownership:
    ownership_class: str
    ownership_score: float
    included_in_import_graph: bool
    reason: str

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
    ownership_class: str
    ownership_score: float
    included_in_import_graph: bool
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

def normalize_rel(path: str) -> str:
    return path.replace("\\", "/").strip().lstrip("./")

def parts(rel: str) -> list[str]:
    return [p for p in normalize_rel(rel).split("/") if p and p != "."]

def load_acgignore(source: Path) -> list[str]:
    path = source / ".acgignore"
    if not path.is_file():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip() and not line.strip().startswith("#")]

def matches_any_glob(rel: str, patterns: list[str]) -> bool:
    rel = normalize_rel(rel)
    return any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch("/" + rel, p) for p in patterns)

def has_marker(rel: str, markers: set[str]) -> bool:
    return bool({p.lower() for p in parts(rel)} & markers)

def is_dependency_path(rel: str) -> bool:
    ps = {p.lower() for p in parts(rel)}
    return bool(ps & DEPENDENCY_MARKERS) or any(p.endswith(".dist-info") or p.endswith(".egg-info") for p in ps)

def is_generated_path(rel: str) -> bool:
    return has_marker(rel, GENERATED_MARKERS)

def is_reference_path(rel: str) -> bool:
    return has_marker(rel, REFERENCE_MARKERS)

def is_dataset_path(rel: str) -> bool:
    return has_marker(rel, DATASET_MARKERS) or Path(rel.lower()).suffix in DATA_EXTENSIONS

def is_tool_runtime_path(rel: str) -> bool:
    ps = parts(rel)
    low = [p.lower() for p in ps]
    if any(p.startswith(".") and p not in ALLOWED_HIDDEN_DIRS for p in ps):
        return True
    if set(low) & TOOL_RUNTIME_MARKERS:
        if {"plugins", "repos"} <= set(low) or "runtimes" in low or "toolchains" in low or ".cache" in low:
            return True
    if len(low) >= 2 and low[0] in {"root", "home", "tmp", "var"} and (low[1].startswith(".") or "runtimes" in low):
        return True
    return False

def should_prune_dir(rel_dir: str, name: str, ignore_patterns: list[str]) -> bool:
    lname = name.lower()
    if matches_any_glob(rel_dir, ignore_patterns):
        return True
    if lname in PRUNE_DIR_NAMES or lname.endswith(".dist-info") or lname.endswith(".egg-info"):
        return True
    if name.startswith(".") and name not in ALLOWED_HIDDEN_DIRS:
        return True
    return False

def read_text_limited(path: Path, max_bytes: int = MAX_IMPORT_PARSE_BYTES) -> str:
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    return data[:max_bytes].decode("utf-8", errors="ignore")

def remove_readonly(func, path: str, exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)

def safe_rmtree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, onerror=remove_readonly)

def collect_paths(source: Path, limit: int, ignore_patterns: list[str]) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(source):
        dir_path = Path(dirpath)
        kept = []
        for d in dirnames:
            try:
                rel_d = (dir_path / d).relative_to(source).as_posix()
            except ValueError:
                continue
            if not should_prune_dir(rel_d, d, ignore_patterns):
                kept.append(d)
        dirnames[:] = kept
        for filename in filenames:
            path = dir_path / filename
            try:
                rel = path.relative_to(source).as_posix()
            except ValueError:
                continue
            if matches_any_glob(rel, ignore_patterns) or not path.is_file():
                continue
            out.append(path)
            if len(out) >= limit:
                return out
    return out

def find_git_root(source: Path) -> Path | None:
    current = source.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None

def detect_environment(source: Path) -> dict[str, object]:
    git_root = find_git_root(source)
    has_git = git_root is not None
    return {
        "has_git": has_git,
        "git_root": str(git_root) if git_root else None,
        "git_velocity_available": has_git,
        "branch_check_available": has_git,
        "enforcement_level": "full" if has_git else "scout_only",
        "notes": [] if has_git else ["No .git folder detected. Scout artifacts work; branch checks, git velocity and PR-style enforcement require Git."],
    }

def infer_project_roots(source: Path, paths: list[Path]) -> list[str]:
    scores: dict[str, int] = defaultdict(int)
    for p in paths:
        try:
            rel = p.relative_to(source).as_posix()
        except ValueError:
            continue
        if is_dependency_path(rel) or is_tool_runtime_path(rel) or is_generated_path(rel):
            continue
        parent = p.parent.relative_to(source).as_posix() if p.parent != source else "."
        if p.name in PROJECT_MARKER_FILES:
            scores[parent] += 6 if p.name in {"AGENTS.md", "README.md", "ACTIVE-INDEX.md", "START.HERE.md"} else 5
        for part in parts(rel)[:-1]:
            if part in PROJECT_MARKER_DIRS:
                prefix = rel.split(part, 1)[0].rstrip("/")
                scores[prefix or "."] += 3
        if ENTRYPOINT_RE.search(rel):
            scores[parent] += 5
    if not scores:
        return ["."]
    roots = [r for r, score in scores.items() if score >= 5] or [max(scores.items(), key=lambda kv: kv[1])[0]]
    roots = sorted(set(roots), key=lambda r: (len(parts(r)), r))
    kept: list[str] = []
    for root in roots:
        if not any(root == k or normalize_rel(root).startswith(normalize_rel(k).rstrip("/") + "/") for k in kept):
            kept.append(root)
    return kept or ["."]

def under_project_root(rel: str, project_roots: list[str]) -> bool:
    rel = normalize_rel(rel)
    return any(root == "." or rel == normalize_rel(root) or rel.startswith(normalize_rel(root).rstrip("/") + "/") for root in project_roots)

def classify_ownership(rel: str, project_roots: list[str]) -> Ownership:
    if is_dependency_path(rel):
        return Ownership("VENDORED_DEPENDENCY", 0.05, False, "dependency marker")
    if is_tool_runtime_path(rel):
        return Ownership("TOOL_RUNTIME", 0.05, False, "tool/runtime marker")
    if is_generated_path(rel):
        return Ownership("GENERATED_CACHE", 0.10, False, "generated/cache marker")
    if is_dataset_path(rel):
        return Ownership("REFERENCE_ASSET", 0.35, False, "dataset/corpus marker")
    if is_reference_path(rel):
        return Ownership("REFERENCE_ASSET", 0.35, False, "reference asset marker")
    if under_project_root(rel, project_roots):
        return Ownership("PROJECT_OWNED", 1.0, True, "under inferred project root")
    return Ownership("UNKNOWN_EXTERNAL", 0.25, False, "outside inferred project roots")

def extract_python_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(read_text_limited(path), filename=str(path))
    except Exception:
        return []
    out: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                out.append(("." * int(node.level)) + node.module if node.level else node.module)
            elif node.level:
                out.append("." * int(node.level))
    return out

def extract_imports(path: Path) -> list[str]:
    ext = path.suffix.lower()
    if ext == ".py":
        return extract_python_imports(path)
    text = read_text_limited(path)
    if ext in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        return JS_RE.findall(text)
    if ext == ".rs":
        return RUST_RE.findall(text)
    if ext == ".go":
        block = GO_BLOCK_RE.search(text)
        if block:
            return GO_ITEM_RE.findall(block.group(1))
        single = GO_SINGLE_RE.search(text)
        return [single.group(1)] if single else []
    return []

def build_file_index(paths: list[Path], source: Path, ownership: dict[str, Ownership]) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in paths:
        rel = path.relative_to(source).as_posix()
        own = ownership.get(rel)
        if not own or not own.included_in_import_graph:
            continue
        if path.suffix.lower() not in SOURCE_EXTENSIONS or path.stat().st_size > MAX_IMPORT_PARSE_BYTES:
            continue
        stem_key = path.with_suffix("").relative_to(source).as_posix()
        index[rel] = rel
        index[stem_key] = rel
        index[path.name] = rel
        index[path.stem] = rel
    return index

def resolve_import(source: Path, from_file: str, raw: str, index: dict[str, str]) -> str | None:
    if not raw or raw.startswith(("http://", "https://")):
        return None
    if raw in index:
        return index[raw]
    base_dir = (source / from_file).parent
    if raw.startswith("."):
        try:
            variants = [(base_dir / raw).resolve().relative_to(source.resolve()).as_posix()]
        except ValueError:
            return None
    else:
        variants = [raw.replace(".", "/"), raw.replace("::", "/"), raw]
    for variant in variants:
        for suffix in ["", "/index", "/__init__", "/mod"]:
            for ext in ["", ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs"]:
                key = f"{variant}{suffix}{ext}"
                if key in index:
                    return index[key]
    stem = raw.split(".")[-1].split("/")[-1].split("::")[-1]
    return index.get(stem)

def build_import_graph(paths: list[Path], source: Path, ownership: dict[str, Ownership]) -> tuple[dict[str, list[str]], dict[str, int], dict[str, int]]:
    index = build_file_index(paths, source, ownership)
    edges: dict[str, list[str]] = {}
    reverse: dict[str, set[str]] = defaultdict(set)
    rel_to_path = {p.relative_to(source).as_posix(): p for p in paths}
    for rel, path in rel_to_path.items():
        if rel not in index:
            continue
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

def classify_family(rel: str) -> tuple[str, str, list[str]]:
    low = rel.lower()
    if Path(low).suffix in BINARY_OR_DATABASE_EXTENSIONS:
        return "binary_or_database", "terminal", ["matched_family:binary_or_database"]
    for pattern, family, tier in FAMILY_RULES:
        if re.search(pattern, low):
            return family, tier, [f"matched_family:{family}"]
    return "unknown", "standard", ["matched_family:unknown"]

def detect_role(rel: str, ext: str, family: str) -> tuple[str, list[str]]:
    name = Path(rel.lower()).name
    if ext in BINARY_OR_DATABASE_EXTENSIONS:
        return "database_or_binary_asset", ["database_or_binary_extension"]
    if name in ORIENTATION_ENTRYPOINT_NAMES:
        return "orientation", ["orientation_name"]
    if name in DATASET_CONTROL_NAMES or ext in DATA_EXTENSIONS:
        return "dataset_or_corpus", ["dataset_signal"]
    if "blueprint" in name or "structure_map" in name or "environment_contract" in name:
        return "architecture_or_contract", ["architecture_or_contract_name"]
    if name in CONTROL_FILE_NAMES or "schema" in name:
        return "control_or_schema", ["control_or_schema_name"]
    if family in {"canon", "memory", "guides"}:
        return "governance_or_memory", ["governance_family"]
    if family in {"tests", "evaluation"}:
        return "validation", ["validation_family"]
    if ext in SOURCE_EXTENSIONS or ext == ".java":
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

def heuristic_score(rel: str, size: int, ext: str, depth: int, family: str) -> tuple[int, list[str]]:
    score = 50
    reasons: list[str] = []
    name = Path(rel.lower()).name
    for key, boost in CRITICAL_NAME_WEIGHTS.items():
        if key in name:
            score += boost
            reasons.append(f"critical_name:+{boost}")
            break
    score -= min(depth * 3, 20)
    if family in {"core", "canon", "memory"}:
        score += 22
    elif family in {"runtime", "guides", "tests"}:
        score += 8
    if family in TERMINAL_FAMILIES or family == "binary_or_database":
        score -= 45
    if family in {"reference", "dataset"}:
        score -= 20
    if family in HUMAN_ONLY_FAMILIES:
        score -= 35
    if size > 2_000_000:
        score -= 45
    elif size > 500_000:
        score -= 35
    elif size > 100_000:
        score -= 15
    elif 0 < size < 50:
        score -= 20
    reasons.append("non_code_heuristic_score")
    return max(0, min(100, score)), reasons

def score_file(rel: str, size: int, ext: str, depth: int, family: str, in_degree: int, max_in_degree: int, own: Ownership) -> tuple[int, int, list[str]]:
    topology = int(60 * (in_degree / max(max_in_degree, 1))) if own.included_in_import_graph and ext in SOURCE_EXTENSIONS else 0
    if own.ownership_class != "PROJECT_OWNED":
        base = 20 if own.ownership_class in {"UNKNOWN_EXTERNAL", "REFERENCE_ASSET"} else 12
        return base, 0, [f"ownership_cap:{own.ownership_class}", own.reason]
    if ext in SOURCE_EXTENSIONS:
        score = min(100, topology + size_component(size) + FAMILY_HOTPATH.get(family, 6))
        return score, topology, [f"topology_score:+{topology}", f"size_component:+{size_component(size)}", f"family_component:+{FAMILY_HOTPATH.get(family, 6)}", own.reason]
    heuristic, reasons = heuristic_score(rel, size, ext, depth, family)
    reasons.append(own.reason)
    return heuristic, topology, reasons

def risk_score(size: int, family: str, ext: str, rel: str, own: Ownership) -> int:
    risk = 0
    if own.ownership_class in {"VENDORED_DEPENDENCY", "TOOL_RUNTIME", "GENERATED_CACHE"}:
        risk += 35
    if own.ownership_class == "UNKNOWN_EXTERNAL":
        risk += 20
    if family in HUMAN_ONLY_FAMILIES:
        risk += 80
    if family in TERMINAL_FAMILIES or family == "binary_or_database":
        risk += 45
    if family in {"reference", "dataset"}:
        risk += 35
    if size > 2_000_000:
        risk += 40
    elif size > 500_000:
        risk += 30
    if ext in {".env", ".sql", ".sqlite", ".sqlite3", ".db", ".db3"}:
        risk += 50
    if re.search(r"secret|password|token|api.?key|credential", rel, re.I):
        risk += 30
    return max(0, min(100, risk))

def strategy_for(family: str, size: int, score: int, ext: str, risk: int, own: Ownership) -> tuple[str, bool, bool, bool]:
    if own.ownership_class in {"VENDORED_DEPENDENCY", "TOOL_RUNTIME", "GENERATED_CACHE"}:
        return "terminal_asset", False, False, True
    if own.ownership_class in {"REFERENCE_ASSET", "UNKNOWN_EXTERNAL"}:
        return "search_only", False, False, True
    if family in HUMAN_ONLY_FAMILIES or risk >= 60:
        return "human_only", False, False, True
    if ext in BINARY_OR_DATABASE_EXTENSIONS or family == "binary_or_database":
        return "terminal_asset", False, False, True
    if family == "generated":
        return "ignore", False, False, False
    if family in {"logs", "exports"}:
        return "terminal_asset", False, False, True
    if family == "dataset":
        return "search_only", False, False, True
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

def scan(source: Path, limit: int) -> tuple[list[FileEntry], dict[str, object]]:
    ignore_patterns = load_acgignore(source)
    paths = collect_paths(source, limit, ignore_patterns)
    project_roots = infer_project_roots(source, paths)
    ownership = {p.relative_to(source).as_posix(): classify_ownership(p.relative_to(source).as_posix(), project_roots) for p in paths}
    edges, indegree, outdegree = build_import_graph(paths, source, ownership)
    max_in_degree = max(indegree.values(), default=0)
    entries: list[FileEntry] = []
    has_executable_entrypoint = False
    has_control_files = False
    orientation_entrypoints: set[str] = set()
    structural_contracts: set[str] = set()
    dataset_entrypoints: set[str] = set()
    dataset_metadata: set[str] = set()
    dataset_control_names = {n.lower() for n in DATASET_CONTROL_NAMES}
    for path in paths:
        rel = path.relative_to(source).as_posix()
        st = path.stat()
        ext = path.suffix.lower()
        depth = len(Path(rel).parts) - 1
        own = ownership[rel]
        family, tier, family_reasons = classify_family(rel)
        role, role_reasons = detect_role(rel, ext, family)
        in_deg = int(indegree.get(rel, 0))
        out_deg = int(outdegree.get(rel, 0))
        score, topology, score_reasons = score_file(rel, st.st_size, ext, depth, family, in_deg, max_in_degree, own)
        risk = risk_score(st.st_size, family, ext, rel, own)
        strategy, open_ok, edit_ok, approval = strategy_for(family, st.st_size, score, ext, risk, own)
        name = Path(rel.lower()).name
        if own.ownership_class == "PROJECT_OWNED":
            has_control_files = has_control_files or name in CONTROL_FILE_NAMES
            has_executable_entrypoint = has_executable_entrypoint or bool(ENTRYPOINT_RE.search(rel))
            if name in ORIENTATION_ENTRYPOINT_NAMES:
                orientation_entrypoints.add(rel)
            if name in STRUCTURAL_CONTRACT_NAMES or family in {"canon", "memory"} or "contract" in name or "law" in name:
                structural_contracts.add(rel)
            if name in dataset_control_names:
                dataset_metadata.add(rel)
            if family == "dataset" or ext in DATA_EXTENSIONS:
                dataset_entrypoints.add(rel)
        entries.append(FileEntry(rel, str(path.resolve()).replace("\\", "/"), st.st_size, st.st_size, utc(st.st_mtime), ext, depth, family, tier, role, own.ownership_class, own.ownership_score, own.included_in_import_graph and ext in SOURCE_EXTENSIONS and rel in indegree, score, risk, in_deg, out_deg, topology, out_deg, strategy, open_ok, edit_ok, approval, False, family_reasons + role_reasons + score_reasons))
    graph_stats = {
        "total_edges": sum(len(v) for v in edges.values()),
        "max_in_degree": max_in_degree,
        "nodes": len(edges),
        "project_roots": project_roots,
        "has_entrypoint": has_executable_entrypoint,
        "has_control_files": has_control_files,
        "orientation_entrypoints": sorted(orientation_entrypoints),
        "structural_contracts": sorted(structural_contracts),
        "dataset_entrypoints": sorted(dataset_entrypoints),
        "dataset_metadata": sorted(dataset_metadata),
        "environment": detect_environment(source),
        "hotpath_score_basis": "PROJECT_OWNED source_code: topology(60)+size(20)+family(20); external/data/runtime files capped or search-only",
    }
    graph_stats["project_kind"] = infer_project_kind(entries, graph_stats)
    graph_stats["readiness_subscores"] = readiness_subscores(entries, graph_stats)
    return entries, graph_stats

def sort_hot(entries: Iterable[FileEntry]) -> list[FileEntry]:
    return sorted(entries, key=lambda e: (e.ownership_class != "PROJECT_OWNED", -e.hotpath_score, -e.in_degree, e.risk_score, e.depth, e.relative_path))

def is_safe_read_candidate(entry: FileEntry) -> bool:
    return entry.ownership_class == "PROJECT_OWNED" and entry.strategy in {"open_now", "open_later"} and not entry.requires_human_approval and entry.folder_family not in TERMINAL_FAMILIES and entry.folder_family not in HUMAN_ONLY_FAMILIES and entry.folder_family not in {"binary_or_database", "dataset"} and entry.extension in TEXT_EXTENSIONS

def ownership_summary(entries: list[FileEntry]) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for e in entries:
        out[e.ownership_class] += 1
    return dict(sorted(out.items()))

def kind_feature_counts(entries: list[FileEntry], graph_stats: dict[str, object]) -> dict[str, int]:
    project_entries = [e for e in entries if e.ownership_class == "PROJECT_OWNED"]
    return {
        "project_files": len(project_entries),
        "code_files": sum(1 for e in project_entries if e.extension in SOURCE_EXTENSIONS),
        "doc_files": sum(1 for e in project_entries if e.extension in DOC_EXTENSIONS or e.role in {"orientation", "architecture_or_contract", "governance_or_memory"}),
        "data_files": sum(1 for e in project_entries if e.extension in DATA_EXTENSIONS or e.folder_family == "dataset"),
        "runtime_files": sum(1 for e in entries if e.ownership_class in {"TOOL_RUNTIME", "VENDORED_DEPENDENCY", "GENERATED_CACHE"}),
        "orientation_files": len(graph_stats.get("orientation_entrypoints", [])),
        "contract_files": len(graph_stats.get("structural_contracts", [])),
        "control_files": 1 if graph_stats.get("has_control_files") else 0,
        "entrypoint_files": 1 if graph_stats.get("has_entrypoint") else 0,
        "dataset_metadata_files": len(graph_stats.get("dataset_metadata", [])),
    }

def infer_project_kind(entries: list[FileEntry], graph_stats: dict[str, object]) -> str:
    counts = kind_feature_counts(entries, graph_stats)
    total = max(len(entries), 1)
    project_files = max(counts["project_files"], 1)
    runtime_ratio = counts["runtime_files"] / total
    code_ratio = counts["code_files"] / project_files
    doc_ratio = counts["doc_files"] / project_files
    data_ratio = counts["data_files"] / project_files
    agent_score = counts["orientation_files"] + counts["contract_files"]
    code_score = counts["code_files"] + 4 * counts["control_files"] + 4 * counts["entrypoint_files"]
    if runtime_ratio >= 0.75 and counts["project_files"] < max(20, int(total * 0.10)):
        return "TOOL_RUNTIME"
    if data_ratio >= 0.45 and counts["data_files"] >= max(10, counts["code_files"] * 2):
        return "DATASET_OR_CORPUS"
    if code_score >= 8 and agent_score >= 2:
        return "MIXED_REPO"
    if code_score >= 8 or (counts["code_files"] >= 10 and code_ratio >= 0.25):
        return "CODEBASE"
    if agent_score >= 2 and doc_ratio >= max(0.30, code_ratio):
        return "AGENT_WORKSPACE"
    if counts["doc_files"] >= 5 and counts["code_files"] <= max(2, counts["doc_files"] // 5):
        return "DOCUMENTATION_BUNDLE"
    if counts["data_files"] >= 5 and counts["code_files"] == 0:
        return "DATASET_OR_CORPUS"
    return "UNKNOWN"

def readiness_subscores(entries: list[FileEntry], graph_stats: dict[str, object]) -> dict[str, object]:
    counts = kind_feature_counts(entries, graph_stats)
    project_entries = [e for e in entries if e.ownership_class == "PROJECT_OWNED"]
    total = max(len(project_entries), 1)
    open_now = sum(1 for e in project_entries if e.strategy == "open_now")
    common_w3 = 0.25 * min((open_now / total) * 4.0, 1.0)
    common_w4 = 0.20
    code_score = round((0.30 if graph_stats.get("has_entrypoint") else 0.0) + (0.25 if graph_stats.get("has_control_files") else 0.0) + common_w3 + common_w4, 3)
    orientation_score = round((0.30 if graph_stats.get("orientation_entrypoints") else 0.0) + (0.25 if graph_stats.get("structural_contracts") else 0.0) + common_w3 + common_w4, 3)
    dataset_meta = bool(graph_stats.get("dataset_metadata")) or bool(graph_stats.get("orientation_entrypoints"))
    dataset_entry = bool(graph_stats.get("dataset_entrypoints"))
    dataset_count_bonus = 0.25 if counts["data_files"] > 0 else 0.0
    dataset_score = round((0.30 if (dataset_entry or dataset_meta) else 0.0) + (0.25 if dataset_meta else 0.0) + dataset_count_bonus + common_w4, 3)
    runtime_penalty = 0.20 if counts["runtime_files"] > max(counts["project_files"] * 3, 100) else 0.0
    return {
        "code_readiness": max(0.0, min(1.0, code_score)),
        "orientation_readiness": max(0.0, min(1.0, orientation_score)),
        "dataset_readiness": max(0.0, min(1.0, dataset_score)),
        "runtime_penalty": runtime_penalty,
        "open_now_count": open_now,
        "project_files": counts["project_files"],
        "code_files": counts["code_files"],
        "doc_files": counts["doc_files"],
        "data_files": counts["data_files"],
        "runtime_files": counts["runtime_files"],
    }

def readiness_score(entries: list[FileEntry], graph_stats: dict[str, object]) -> float:
    subs = graph_stats.get("readiness_subscores") or readiness_subscores(entries, graph_stats)
    kind = str(graph_stats.get("project_kind", "UNKNOWN"))
    code = float(subs["code_readiness"])
    orient = float(subs["orientation_readiness"])
    dataset = float(subs["dataset_readiness"])
    penalty = float(subs.get("runtime_penalty", 0.0))
    if kind == "CODEBASE":
        score = code if code >= 0.45 else min(code, 0.44)
    elif kind in {"AGENT_WORKSPACE", "DOCUMENTATION_BUNDLE"}:
        score = orient
    elif kind == "MIXED_REPO":
        score = (code * 0.55) + (orient * 0.45)
    elif kind == "DATASET_OR_CORPUS":
        score = dataset
    elif kind == "TOOL_RUNTIME":
        score = min(code, orient, dataset, 0.34)
    else:
        score = max(code, orient, dataset) - 0.10
        if score < 0.45:
            score = min(score, 0.44)
    return round(max(0.0, min(1.0, score - penalty)), 3)

def guardrail_mode(score: float) -> str:
    if score >= 0.65:
        return "silent"
    if score >= 0.45:
        return "warn"
    return "halt"

def detect_scout_regime(entries: list[FileEntry], graph_stats: dict[str, object]) -> str:
    project_files = int((graph_stats.get("readiness_subscores") or {}).get("project_files", 0))
    total_files = len(entries)
    import_nodes = int(graph_stats.get("nodes", 0))
    scale = max(project_files, total_files)
    if scale < 50:
        return "minimal"
    if scale < 500:
        return "standard"
    if scale < 5000:
        return "extended" if import_nodes else "standard"
    return "large"

def readiness_gate(score: float, graph_stats: dict[str, object], min_required: float = 0.65) -> dict[str, object]:
    kind = str(graph_stats.get("project_kind", "UNKNOWN"))
    if kind in {"TOOL_RUNTIME", "UNKNOWN"}:
        effective_min = max(min_required, 0.65)
    else:
        effective_min = min_required
    status = "passed" if score >= effective_min else ("warn" if score >= 0.45 else "failed")
    return {"min_required": effective_min, "actual": score, "status": status, "project_kind": kind}

def phase1_order_reason(entry: dict[str, object]) -> str:
    path = str(entry.get("relative_path", ""))
    name = Path(path.lower()).name
    if name == "agents.md":
        return "defines agent operating contract"
    if name in {"active-index.md", "start.here.md"}:
        return "states active orientation and current focus"
    if name == "readme.md":
        return "provides project-level overview"
    if "environment_contract" in name:
        return "defines environment and safety boundaries"
    if "system_law" in name or "law" in name:
        return "defines global constraints"
    if "memory_contract" in name or "contract" in name:
        return "defines persistent-state contract"
    if "blueprint" in name or "structure_map" in name:
        return "describes architecture or structure"
    return "high-priority Phase 1 file from ACG queue"

def phase1_sort_key(item: dict[str, object]) -> tuple[int, int, str]:
    path = str(item.get("relative_path", ""))
    name = Path(path.lower()).name
    priority = 50
    ordered = ["agents.md", "active-index.md", "start.here.md", "readme.md"]
    if name in ordered:
        priority = ordered.index(name)
    elif "environment_contract" in name:
        priority = 10
    elif "system_law" in name:
        priority = 11
    elif "memory_contract" in name:
        priority = 12
    elif "blueprint" in name:
        priority = 20
    elif "structure_map" in name:
        priority = 21
    return (priority, -int(item.get("hotpath_score", 0)), path)

def build_phase1_reading_order(phase1: list[dict[str, object]]) -> list[dict[str, object]]:
    ordered = sorted(phase1, key=phase1_sort_key)
    return [{"step": i, "file": str(item["relative_path"]), "reason": phase1_order_reason(item)} for i, item in enumerate(ordered, 1)]

def citation_prompt_for(path: str) -> str:
    name = Path(path.lower()).name
    if name == "agents.md":
        return "cite one concrete operating rule from this file"
    if name in {"active-index.md", "start.here.md"}:
        return "cite the active focus, current mission, or first concrete status item"
    if name == "readme.md":
        return "cite the stated purpose or first major section title"
    if "environment_contract" in name:
        return "cite one explicit environment boundary or forbidden action"
    if "system_law" in name:
        return "cite one system constraint or law"
    if "memory_contract" in name:
        return "cite one memory/state rule"
    if "blueprint" in name:
        return "cite one architecture claim or component name"
    if "structure_map" in name:
        return "cite one mapped layer or directory/component relationship"
    return "cite one concrete heading, rule, or statement from this file"

def build_citation_check(reading_order: list[dict[str, object]], max_items: int = 8) -> list[dict[str, object]]:
    checks = []
    for item in reading_order[:max_items]:
        file = str(item["file"])
        checks.append({"file": file, "check": citation_prompt_for(file), "required": True})
    return checks

def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_jsonl(path: Path, entries: list[FileEntry]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(asdict(entry), ensure_ascii=False, sort_keys=True) + "\n")

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
    phase2 = [e for e in hot if e.relative_path not in phase1_paths and is_safe_read_candidate(e)][:phase2_max_files]
    approval_required = [e for e in hot if e.strategy in {"open_now", "open_later"} and e.requires_human_approval]
    search_targets = [e for e in hot if e.strategy in {"search_only", "terminal_asset"}]
    phase1_dicts = [asdict(e) for e in phase1]
    reading_order = build_phase1_reading_order(phase1_dicts)
    citation_check = build_citation_check(reading_order)
    return {
        "phase1": phase1_dicts,
        "phase1_total_bytes": total,
        "phase1_reading_order": reading_order,
        "citation_check": citation_check,
        "phase2": [asdict(e) for e in phase2],
        "approval_required": [asdict(e) for e in approval_required],
        "search_targets": [asdict(e) for e in search_targets],
        "human_only": [asdict(e) for e in hot if e.strategy == "human_only"],
        "ignored": [asdict(e) for e in hot if e.strategy == "ignore"],
    }

def write_queue_markdown(path: Path, title: str, description: str, items: list[dict[str, object]]) -> None:
    lines = [f"# {title}", "", description, "", "| # | File | Owner | Role | Family | Score | In | Risk | Strategy |", "|---:|---|---|---|---|---:|---:|---:|---|"]
    if not items:
        lines.append("| - | None | - | - | - | - | - | - | - |")
    else:
        for i, item in enumerate(items, 1):
            lines.append(f"| {i} | `{item['relative_path']}` | {item.get('ownership_class', '-')} | {item['role']} | {item['folder_family']} | {item['hotpath_score']} | {item.get('in_degree', 0)} | {item['risk_score']} | {item['strategy']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def family_summary(entries: list[FileEntry]) -> list[dict[str, object]]:
    buckets: dict[str, list[FileEntry]] = defaultdict(list)
    for e in entries:
        buckets[e.folder_family].append(e)
    rows = []
    for family, items in sorted(buckets.items()):
        strategies: dict[str, int] = defaultdict(int)
        for item in items:
            strategies[item.strategy] += 1
        rows.append({"family": family, "files": len(items), "avg_hotpath_score": round(sum(i.hotpath_score for i in items) / len(items), 1), "dominant_strategy": sorted(strategies.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]})
    return rows

def ownership_summary(entries: list[FileEntry]) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for e in entries:
        out[e.ownership_class] += 1
    return dict(sorted(out.items()))

def write_phase1_reading_order(path: Path, order: list[dict[str, object]]) -> None:
    lines = ["# ACG Phase 1 Reading Order", "", "Read Phase 1 files in this order. Do not substitute your own order.", "", "| Step | File | Reason |", "|---:|---|---|"]
    for item in order:
        lines.append(f"| {item['step']} | `{item['file']}` | {item['reason']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_citation_check(path: Path, checks: list[dict[str, object]]) -> None:
    lines = ["# ACG Citation Check", "", "The AI must answer these checks after Phase 1. This reduces shallow self-reporting.", "", "| File | Required check |", "|---|---|"]
    for item in checks:
        lines.append(f"| `{item['file']}` | {item['check']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_structure_map(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object], graph_stats: dict[str, object]) -> None:
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    subs = graph_stats.get("readiness_subscores", {})
    gate = graph_stats.get("readiness_gate", {})
    lines = [
        "# ACG Structure Map", "", f"Version: `{VERSION}`", f"Source: `{source}`",
        f"Generated: {dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()}",
        f"Total indexed files: {len(entries)}", f"Project kind: {graph_stats.get('project_kind')}",
        f"Scout regime: {graph_stats.get('scout_regime')}", f"Readiness score: {readiness} [{mode.upper()}]",
        f"Readiness gate: {gate.get('status')} (min={gate.get('min_required')}, actual={gate.get('actual')})",
        "", "## Environment", "",
        f"- has_git: {graph_stats.get('environment', {}).get('has_git')}",
        f"- enforcement_level: {graph_stats.get('environment', {}).get('enforcement_level')}",
        "", "## Readiness Subscores", "",
        f"- code_readiness: {subs.get('code_readiness')}", f"- orientation_readiness: {subs.get('orientation_readiness')}",
        f"- dataset_readiness: {subs.get('dataset_readiness')}", f"- runtime_penalty: {subs.get('runtime_penalty')}",
        "", "## Project Roots", "",
    ]
    for root in graph_stats.get("project_roots", []):
        lines.append(f"- `{root}`")
    lines += ["", "## Phase 1 Reading Order", ""]
    for item in queues.get("phase1_reading_order", []):
        lines.append(f"{item['step']}. `{item['file']}` - {item['reason']}")
    lines += ["", "## Citation Check", ""]
    for item in queues.get("citation_check", []):
        lines.append(f"- `{item['file']}`: {item['check']}")
    lines += ["", "## Ownership Summary", "", "| Ownership | Files |", "|---|---:|"]
    for k, v in ownership_summary(entries).items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "## Import Graph Stats", "", f"- Nodes: {graph_stats.get('nodes', 0)}", f"- Total edges: {graph_stats.get('total_edges', 0)}", f"- Max in-degree: {graph_stats.get('max_in_degree', 0)}", f"- Score basis: {graph_stats.get('hotpath_score_basis')}", "", "## Cluster Overview", "", "| Family | Files | Avg Hotpath | Dominant Strategy |", "|---|---:|---:|---|"]
    for row in family_summary(entries):
        lines.append(f"| {row['family']} | {row['files']} | {row['avg_hotpath_score']} | {row['dominant_strategy']} |")
    lines += ["", "## Top Hotpath Files", "", "| Score | In | Out | Owner | Risk | Strategy | Family | File |", "|---:|---:|---:|---|---:|---|---|---|"]
    for e in sort_hot(entries)[:25]:
        lines.append(f"| {e.hotpath_score} | {e.in_degree} | {e.out_degree} | {e.ownership_class} | {e.risk_score} | {e.strategy} | {e.folder_family} | `{e.relative_path}` |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def copy_phase1(out_dir: Path, queues: dict[str, object]) -> None:
    pack = out_dir / "phase1_pack"
    if pack.exists():
        safe_rmtree(pack)
    pack.mkdir(parents=True, exist_ok=True)
    phase1_by_path = {str(item["relative_path"]): item for item in queues.get("phase1", [])}
    ordered_paths = [str(item["file"]) for item in queues.get("phase1_reading_order", [])]
    for rel in ordered_paths:
        item = phase1_by_path.get(rel)
        if not item:
            continue
        src = Path(str(item["absolute_path"]))
        dst = pack / str(item["relative_path"])
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

def write_search_targets(path: Path, queues: dict[str, object]) -> None:
    lines = ["# ACG Search Targets", "", "These files should not be opened fully. Use targeted search only.", ""]
    for item in queues.get("search_targets", []):
        lines.append(f"- `{item['relative_path']}` - {item.get('ownership_class', '-')}, {item['strategy']}, {item['size']} bytes, risk {item['risk_score']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_phase2_template(path: Path) -> None:
    path.write_text("""# ACG Phase 2 Plan Template

The AI must use this exact structure for the NEXT block after Phase 1.

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
- non-PROJECT_OWNED: excluded unless explicit human approval is granted
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
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    subs = graph_stats.get("readiness_subscores", {})
    gate = graph_stats.get("readiness_gate", {})
    env = graph_stats.get("environment", {})
    lines = [
        "# ACG Execution Brief", "", f"You are operating under ACG Structure Scout v{VERSION}.", "",
        f"Project kind: {graph_stats.get('project_kind')}", f"Scout regime: {graph_stats.get('scout_regime')}",
        f"Readiness: {readiness} [{mode.upper()}]", f"Readiness gate: {gate.get('status')} (min={gate.get('min_required')}, actual={gate.get('actual')})",
        f"Environment: enforcement_level={env.get('enforcement_level')}, has_git={env.get('has_git')}",
        f"Readiness subscores: code={subs.get('code_readiness')}, orientation={subs.get('orientation_readiness')}, dataset={subs.get('dataset_readiness')}",
        "", "Ownership-aware import graph scoring is active.",
        "Only PROJECT_OWNED source files are included in the main import graph.",
        "Do not proceed to execution if readiness_gate.status is failed.",
        "Phase 1 is not complete until reading order is followed and citation checks are answered.",
        "", "## Required artifacts to inspect first", "",
        "- `../ACG_MASTER.md`", "- `execution_brief.md`", "- `phase1_reading_order.md`", "- `citation_check.md`", "- `next_prompt.md`", "- `phase2_plan_template.md`", "- `structure_map.md`", "- `phase1_queue.md`", "- `phase2_queue.md`", "- `approval_required.md`", "- `search_targets.md`", "- `../phase1_pack/`",
        "", "## Phase 1 Reading Order", "",
    ]
    for item in queues.get("phase1_reading_order", []):
        lines.append(f"{item['step']}. `{item['file']}` - {item['reason']}")
    lines += ["", "## Citation Check", ""]
    for item in queues.get("citation_check", []):
        lines.append(f"- `{item['file']}`: {item['check']}")
    lines += ["", "## Required Phase 1 Output", "", "```txt", "ACG-UNDERSTOOD: structure-scout", "SCOPE: files you actually read, in order", "CITATION_CHECK: one answer per required citation check", "RISKS: key risks before deeper processing", "QUESTIONS: objective questions or approval requests only", "NEXT: Phase 2 plan or up to 3 clarification questions", "```"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_next_prompt(path: Path, queues: dict[str, object]) -> None:
    lines = ["# ACG Continuation Protocol", "", "This file is not a human copy/paste prompt.", "The AI must read this file before Phase 1 and apply it automatically after Phase 1.", "Phase 1 is incomplete unless `phase1_reading_order.md` is followed and `citation_check.md` is answered.", "", "## Current safe Phase 2 candidates", ""]
    for item in queues.get("phase2", []):
        lines.append(f"- `{item['relative_path']}` - {item.get('ownership_class', '-')}, {item['role']}, score {item['hotpath_score']}, in_degree {item.get('in_degree', 0)}")
    lines += ["", "Return NEXT using `phase2_plan_template.md` exactly."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_master(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object], graph_stats: dict[str, object]) -> None:
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    gate = graph_stats.get("readiness_gate", {})
    env = graph_stats.get("environment", {})
    lines = ["# ACG Master Context File", "", f"Generated by ACG Structure Scout v{VERSION}.", "", "This is the root instruction file for the generated ACG context package.", "", "## Source", "", f"`{source}`", "", "## Inventory Summary", "", f"- Total indexed files: {len(entries)}", f"- Project kind: {graph_stats.get('project_kind')}", f"- Scout regime: {graph_stats.get('scout_regime')}", f"- Environment enforcement level: {env.get('enforcement_level')}", f"- Phase 1 files: {len(queues.get('phase1', []))}", f"- Safe Phase 2 candidates: {len(queues.get('phase2', []))}", f"- Search-only / terminal assets: {len(queues.get('search_targets', []))}", f"- Import graph nodes: {graph_stats.get('nodes', 0)}", f"- Import graph edges: {graph_stats.get('total_edges', 0)}", f"- Max in-degree: {graph_stats.get('max_in_degree', 0)}", f"- Readiness score: {readiness} [{mode.upper()}]", f"- Readiness gate: {gate.get('status')} (min={gate.get('min_required')}, actual={gate.get('actual')})", "", "## Project Roots", ""]
    for root in graph_stats.get("project_roots", []):
        lines.append(f"- `{root}`")
    lines += ["", "## Read Order for AI", "", "1. Read this file: `ACG_MASTER.md`.", "2. Read `artifacts/execution_brief.md`.", "3. Read `artifacts/phase1_reading_order.md`.", "4. Read `artifacts/citation_check.md`.", "5. Read `artifacts/next_prompt.md`.", "6. Read `artifacts/phase2_plan_template.md`.", "7. Read `artifacts/structure_map.md`.", "8. Read `artifacts/phase1_queue.md` and `artifacts/phase2_queue.md`.", "9. Read `artifacts/approval_required.md` and `artifacts/search_targets.md`.", "10. Read only files copied inside `phase1_pack/`, in the order defined by `phase1_reading_order.md`.", "", "## Do Not Do", "", "- Do not read the original source folder blindly.", "- Do not open terminal assets directly.", "- Do not read non-PROJECT_OWNED files unless explicitly approved.", "- Do not edit files during orientation.", "- Do not claim Phase 1 completion without answering citation_check.md.", "- Do not ask vague questions such as 'what next?'."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def cleanup_legacy_root_artifacts(out: Path) -> None:
    for name in LEGACY_ROOT_ARTIFACTS:
        target = out / name
        if target.is_file():
            target.unlink()

def write_scout_report(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object], graph_stats: dict[str, object]) -> None:
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    extensions: dict[str, int] = defaultdict(int)
    for e in entries:
        if e.extension:
            extensions[e.extension] += 1
    report = {
        "acg_version": VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "root": str(source),
        "scout_regime": graph_stats.get("scout_regime"),
        "environment": graph_stats.get("environment"),
        "readiness_gate": graph_stats.get("readiness_gate"),
        "phase1_reading_order": queues.get("phase1_reading_order", []),
        "citation_check": queues.get("citation_check", []),
        "system_profile": {
            "total_files": len(entries), "language_map": dict(extensions), "ownership_summary": ownership_summary(entries),
            "project_roots": graph_stats.get("project_roots", []), "project_kind": graph_stats.get("project_kind"),
            "readiness_subscores": graph_stats.get("readiness_subscores", {}),
            "has_entrypoint": bool(graph_stats.get("has_entrypoint")), "has_control_files": bool(graph_stats.get("has_control_files")),
            "orientation_entrypoints": graph_stats.get("orientation_entrypoints", []), "structural_contracts": graph_stats.get("structural_contracts", []),
            "dataset_entrypoints": graph_stats.get("dataset_entrypoints", []), "dataset_metadata": graph_stats.get("dataset_metadata", []),
        },
        "readiness_score": readiness,
        "guardrail_mode": mode,
        "attention_queue": queues.get("phase1", [])[:20],
        "phased_reading_plan": {"phase1": queues.get("phase1", []), "phase2": queues.get("phase2", []), "phase3": queues.get("search_targets", [])[:10]},
        "broken_refs": [],
        "execution_brief": {
            "task_id": "structure-scout", "root": str(source), "total_files": len(entries), "readiness_score": readiness, "guardrail_mode": mode,
            "readiness_gate": graph_stats.get("readiness_gate"), "scout_regime": graph_stats.get("scout_regime"), "environment": graph_stats.get("environment"),
            "readiness_components": {
                "project_kind": graph_stats.get("project_kind"), "subscores": graph_stats.get("readiness_subscores", {}),
                "W1_executable_or_orientation_or_dataset_entrypoint": bool(graph_stats.get("has_entrypoint") or graph_stats.get("orientation_entrypoints") or graph_stats.get("dataset_metadata")),
                "W2_control_or_structural_or_metadata": bool(graph_stats.get("has_control_files") or graph_stats.get("structural_contracts") or graph_stats.get("dataset_metadata")),
                "W3_open_now_count": len(queues.get("phase1", [])), "W4_broken_refs_count": 0,
            },
            "import_graph": {"total_edges": graph_stats.get("total_edges", 0), "max_in_degree": graph_stats.get("max_in_degree", 0), "hotpath_score_basis": graph_stats.get("hotpath_score_basis")},
            "instruction": "Read Phase 1 files in phase1_reading_order. Answer citation_check. Then return ACG-UNDERSTOOD, SCOPE, CITATION_CHECK, RISKS, QUESTIONS, NEXT before any edit.",
        },
        "context_manifest_ref": "context_manifest.jsonl",
    }
    write_json(path, report)

def main() -> int:
    parser = argparse.ArgumentParser(description="ACG Structure Scout v0.4-beta")
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", default=".acg")
    parser.add_argument("--limit", type=int, default=100000)
    parser.add_argument("--phase1-max-files", type=int, default=12)
    parser.add_argument("--phase1-max-bytes", type=int, default=51200)
    parser.add_argument("--phase2-max-files", type=int, default=25)
    parser.add_argument("--min-readiness-score", type=float, default=0.65)
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
    graph_stats["scout_regime"] = detect_scout_regime(entries, graph_stats)
    score = readiness_score(entries, graph_stats)
    graph_stats["readiness_gate"] = readiness_gate(score, graph_stats, args.min_readiness_score)
    write_jsonl(artifacts / "context_manifest.jsonl", entries)
    write_json(artifacts / "hotpaths.json", [asdict(e) for e in sort_hot(entries)[:100]])
    write_json(artifacts / "reading_queues.json", queues)
    write_queue_markdown(artifacts / "phase1_queue.md", "ACG Phase 1 Queue", "Files copied into `../phase1_pack/` and allowed for first orientation.", queues["phase1"])
    write_queue_markdown(artifacts / "phase2_queue.md", "ACG Phase 2 Queue", "Safe candidates for a bounded Phase 2 reading plan. Do not open until human approval.", queues["phase2"])
    write_queue_markdown(artifacts / "approval_required.md", "ACG Approval-Required Queue", "Files that require explicit human approval before reading.", queues["approval_required"])
    write_phase1_reading_order(artifacts / "phase1_reading_order.md", queues["phase1_reading_order"])
    write_citation_check(artifacts / "citation_check.md", queues["citation_check"])
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
    print(f"Project kind: {graph_stats.get('project_kind')}")
    print(f"Scout regime: {graph_stats.get('scout_regime')}")
    print(f"Readiness gate: {graph_stats.get('readiness_gate')}")
    print(f"Environment: {graph_stats.get('environment')}")
    print(f"Readiness subscores: {graph_stats.get('readiness_subscores')}")
    print(f"Project roots: {', '.join(str(x) for x in graph_stats.get('project_roots', []))}")
    print(f"Ownership summary: {ownership_summary(entries)}")
    print(f"Phase 1 reading order: {len(queues.get('phase1_reading_order', []))}")
    print(f"Citation checks: {len(queues.get('citation_check', []))}")
    print(f"Import graph nodes: {graph_stats.get('nodes', 0)}")
    print(f"Import graph edges: {graph_stats.get('total_edges', 0)}")
    print(f"Max in-degree: {graph_stats.get('max_in_degree', 0)}")
    print(f"ACG output folder: {out}")
    print(f"Scout report: {artifacts / 'scout_report.json'}")
    print(f"Phase 1 pack: {out / 'phase1_pack'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
