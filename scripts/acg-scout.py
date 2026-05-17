#!/usr/bin/env python3
"""ACG Structure Scout v0.4-beta.

Stable package generator used by scripts/acg-v04.py.

Keeps the public CLI:
  python scripts/acg-scout.py --source /path/to/project --out .acg

Adds ownership-aware topology:
- infer project-owned roots from repository markers;
- classify external/runtime/dependency/cache files;
- build the main import graph only from PROJECT_OWNED source files;
- cap external hotpath scores so tool runtimes cannot outrank the target codebase.
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
TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml",
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs", ".java", ".sh", ".ps1",
}
BINARY_OR_DATABASE_EXTENSIONS = {".sqlite", ".sqlite3", ".db", ".db3", ".bin", ".pkl", ".pickle"}

PRUNE_DIR_NAMES = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules", ".pnpm", ".yarn", ".npm",
    "bower_components", ".venv", "venv", "env", "__pypackages__", "site-packages",
    "dist-packages", "target", ".gradle", ".mypy_cache", ".pytest_cache", ".ruff_cache",
}
ALLOWED_HIDDEN_DIRS = {".github"}

DEPENDENCY_MARKERS = {
    "node_modules", ".pnpm", "bower_components", "site-packages", "dist-packages",
    "__pypackages__", "vendor", "vendors", "third_party", ".venv", "venv", "env",
}
TOOL_RUNTIME_MARKERS = {"runtimes", "runtime-cache", "toolchains", "plugins", "extensions", "cache", ".cache"}
GENERATED_MARKERS = {"dist", "build", "coverage", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "generated", ".generated", "out", "outputs"}
REFERENCE_MARKERS = {"refs", "reference", "references", "samples", "fixtures", "ssot"}

PROJECT_MARKER_FILES = {
    "AGENTS.md", "README.md", "acg.yaml", "acg.json", "package.json", "pyproject.toml",
    "Cargo.toml", "go.mod", "Makefile", "requirements.txt", "setup.py", "setup.cfg",
    "tsconfig.json", "pnpm-workspace.yaml", "WORKSPACE",
}
PROJECT_MARKER_DIRS = {
    "src", "lib", "app", "apps", "packages", "pkg", "cmd", "api", "server",
    "tests", "test", "docs", "workspace", "agent_files", "00_core", "01_canon",
    "02_memory", "03_profiles", "04_eval", "06_runtime_guides",
}
CONTROL_FILE_NAMES = {
    "acg.yaml", "acg.json", "package.json", "pyproject.toml", "cargo.toml", "go.mod",
    "makefile", "dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "requirements.txt", "setup.py", "setup.cfg",
}
ENTRYPOINT_RE = re.compile(
    r"(^|[\\/])(main\.py|main\.go|main\.rs|index\.[jt]sx?|app\.py|server\.py|__main__\.py|cmd[\\/]main\.go|src[\\/]main\.rs|bin[\\/]main\.rs)$",
    re.I,
)

LEGACY_ROOT_ARTIFACTS = {
    "context_manifest.jsonl", "structure_map.md", "hotpaths.json", "reading_queues.json",
    "search_targets.md", "execution_brief.md", "next_prompt.md", "phase1_queue.md",
    "phase2_queue.md", "approval_required.md", "phase2_plan_template.md", "scout_report.json",
}

CRITICAL_NAME_WEIGHTS = {
    "agents.md": 42, "active-index.md": 40, "readme.md": 22,
    "environment_contract.md": 38, "system_law.md": 36, "memory_contract.md": 34,
    "blueprint": 34, "structure_map": 34, "runtime_execution.md": 30,
    "acg.yaml": 38, "package.json": 30, "pyproject.toml": 30, "go.mod": 30,
    "cargo.toml": 30, "tsconfig.json": 26, "requirements.txt": 24,
}
FAMILY_HOTPATH = {
    "core": 20, "canon": 18, "runtime": 16, "tests": 10, "docs": 8, "guides": 8,
    "evaluation": 8, "reference": 5, "memory": 4, "legacy": 2, "unknown": 6,
    "generated": 0, "logs": 0, "exports": 0, "secrets": 0, "infra": 0, "migrations": 0,
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
    (r"(^|/)00_core(/|$)|(^|/)core(/|$)|(^|/)src(/|$)|(^|/)app(/|$)|(^|/)lib(/|$)|(^|/)pkg(/|$)|(^|/)cmd(/|$)|(^|/)api(/|$)|(^|/)server(/|$)|(^|/)workspace(/|$)", "core", "priority"),
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
    patterns: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def matches_any_glob(rel: str, patterns: list[str]) -> bool:
    rel = normalize_rel(rel)
    return any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch("/" + rel, p) for p in patterns)


def is_dependency_path(rel: str) -> bool:
    ps = {p.lower() for p in parts(rel)}
    return bool(ps & DEPENDENCY_MARKERS) or any(p.endswith(".dist-info") or p.endswith(".egg-info") for p in ps)


def is_generated_path(rel: str) -> bool:
    return bool({p.lower() for p in parts(rel)} & GENERATED_MARKERS)


def is_reference_path(rel: str) -> bool:
    return bool({p.lower() for p in parts(rel)} & REFERENCE_MARKERS)


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
    rel = normalize_rel(rel_dir)
    lname = name.lower()
    if matches_any_glob(rel, ignore_patterns):
        return True
    if lname in PRUNE_DIR_NAMES:
        return True
    if name.startswith(".") and name not in ALLOWED_HIDDEN_DIRS:
        return True
    if lname.endswith(".dist-info") or lname.endswith(".egg-info"):
        return True
    return False


def read_text_limited(path: Path, max_bytes: int = MAX_IMPORT_PARSE_BYTES) -> str:
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    if len(data) > max_bytes:
        data = data[:max_bytes]
    return data.decode("utf-8", errors="ignore")


def remove_readonly(func, path: str, exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def safe_rmtree(path: Path) -> None:
    if not path.exists():
        return
    try:
        shutil.rmtree(path, onerror=remove_readonly)
    except PermissionError as exc:
        raise RuntimeError("ACG could not replace phase1_pack. Close programs using .acg/phase1_pack, delete it manually, and rerun.") from exc


def collect_paths(source: Path, limit: int, ignore_patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(source):
        dir_path = Path(dirpath)
        new_dirs: list[str] = []
        for d in dirnames:
            try:
                rel_d = (dir_path / d).relative_to(source).as_posix()
            except ValueError:
                continue
            if not should_prune_dir(rel_d, d, ignore_patterns):
                new_dirs.append(d)
        dirnames[:] = new_dirs
        for filename in filenames:
            path = dir_path / filename
            try:
                rel = path.relative_to(source).as_posix()
            except ValueError:
                continue
            if matches_any_glob(rel, ignore_patterns) or not path.is_file():
                continue
            paths.append(path)
            if len(paths) >= limit:
                return paths
    return paths


def infer_project_roots(source: Path, paths: list[Path]) -> list[str]:
    scores: dict[str, int] = defaultdict(int)
    for p in paths:
        try:
            rel = p.relative_to(source).as_posix()
        except ValueError:
            continue
        if is_dependency_path(rel) or is_tool_runtime_path(rel) or is_generated_path(rel):
            continue
        pp = p.parent.relative_to(source).as_posix() if p.parent != source else "."
        name = p.name
        if name in PROJECT_MARKER_FILES:
            scores[pp] += 6 if name in {"AGENTS.md", "README.md"} else 5
        for part in parts(rel)[:-1]:
            if part in PROJECT_MARKER_DIRS:
                prefix = rel.split(part, 1)[0].rstrip("/")
                scores[prefix or "."] += 3
        if ENTRYPOINT_RE.search(rel):
            scores[pp] += 5
    if not scores:
        return ["."]
    roots = [r for r, s in scores.items() if s >= 5] or [max(scores.items(), key=lambda kv: kv[1])[0]]
    roots = sorted(set(roots), key=lambda r: (len(parts(r)), r))
    kept: list[str] = []
    for r in roots:
        if not any(r == k or normalize_rel(r).startswith(normalize_rel(k).rstrip("/") + "/") for k in kept):
            kept.append(r)
    return kept or ["."]


def under_project_root(rel: str, project_roots: list[str]) -> bool:
    rel = normalize_rel(rel)
    for root in project_roots:
        root = normalize_rel(root)
        if root == "." or rel == root or rel.startswith(root.rstrip("/") + "/"):
            return True
    return False


def classify_ownership(rel: str, project_roots: list[str]) -> Ownership:
    if is_dependency_path(rel):
        return Ownership("VENDORED_DEPENDENCY", 0.05, False, "dependency marker")
    if is_tool_runtime_path(rel):
        return Ownership("TOOL_RUNTIME", 0.05, False, "tool/runtime marker")
    if is_generated_path(rel):
        return Ownership("GENERATED_CACHE", 0.10, False, "generated/cache marker")
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
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(("." * int(node.level)) + node.module if node.level else node.module)
            elif node.level:
                imports.append("." * int(node.level))
    return imports


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


def resolve_import(source: Path, from_file: str, raw_import: str, index: dict[str, str]) -> str | None:
    if not raw_import or raw_import.startswith(("http://", "https://")):
        return None
    if raw_import in index:
        return index[raw_import]
    base_dir = (source / from_file).parent
    if raw_import.startswith("."):
        try:
            variants = [(base_dir / raw_import).resolve().relative_to(source.resolve()).as_posix()]
        except ValueError:
            return None
    else:
        variants = [raw_import.replace(".", "/"), raw_import.replace("::", "/"), raw_import]
    for variant in variants:
        for suffix in ["", "/index", "/__init__", "/mod"]:
            for ext in ["", ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs"]:
                key = f"{variant}{suffix}{ext}"
                if key in index:
                    return index[key]
    stem = raw_import.split(".")[-1].split("/")[-1].split("::")[-1]
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


def classify_family(relative_path: str) -> tuple[str, str, list[str]]:
    low = relative_path.lower()
    if Path(low).suffix in BINARY_OR_DATABASE_EXTENSIONS:
        return "binary_or_database", "terminal", ["matched_family:binary_or_database"]
    for pattern, family, tier in FAMILY_RULES:
        if re.search(pattern, low):
            return family, tier, [f"matched_family:{family}"]
    return "unknown", "standard", ["matched_family:unknown"]


def detect_role(relative_path: str, extension: str, family: str) -> tuple[str, list[str]]:
    name = Path(relative_path.lower()).name
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


def heuristic_score(relative_path: str, size: int, extension: str, depth: int, family: str) -> tuple[int, list[str]]:
    score = 50
    reasons: list[str] = []
    name = Path(relative_path.lower()).name
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
    if family == "reference":
        score -= 25
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


def score_file(relative_path: str, size: int, extension: str, depth: int, family: str, in_degree: int, max_in_degree: int, own: Ownership) -> tuple[int, int, list[str]]:
    topology = int(60 * (in_degree / max(max_in_degree, 1))) if own.included_in_import_graph and extension in SOURCE_EXTENSIONS else 0
    if own.ownership_class != "PROJECT_OWNED":
        base = 20 if own.ownership_class in {"UNKNOWN_EXTERNAL", "REFERENCE_ASSET"} else 12
        return base, 0, [f"ownership_cap:{own.ownership_class}", own.reason]
    if extension in SOURCE_EXTENSIONS:
        score = min(100, topology + size_component(size) + FAMILY_HOTPATH.get(family, 6))
        return score, topology, [f"topology_score:+{topology}", f"size_component:+{size_component(size)}", f"family_component:+{FAMILY_HOTPATH.get(family, 6)}", own.reason]
    heuristic, reasons = heuristic_score(relative_path, size, extension, depth, family)
    reasons.append(own.reason)
    return heuristic, topology, reasons


def risk_score(size: int, family: str, extension: str, relative_path: str, own: Ownership) -> int:
    risk = 0
    if own.ownership_class in {"VENDORED_DEPENDENCY", "TOOL_RUNTIME", "GENERATED_CACHE"}:
        risk += 35
    if own.ownership_class == "UNKNOWN_EXTERNAL":
        risk += 20
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


def strategy_for(family: str, size: int, score: int, extension: str, risk: int, own: Ownership) -> tuple[str, bool, bool, bool]:
    if own.ownership_class in {"VENDORED_DEPENDENCY", "TOOL_RUNTIME", "GENERATED_CACHE"}:
        return "terminal_asset", False, False, True
    if own.ownership_class in {"REFERENCE_ASSET", "UNKNOWN_EXTERNAL"}:
        return "search_only", False, False, True
    if family in HUMAN_ONLY_FAMILIES or risk >= 60:
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


def scan(source: Path, limit: int) -> tuple[list[FileEntry], dict[str, object]]:
    ignore_patterns = load_acgignore(source)
    paths = collect_paths(source, limit, ignore_patterns)
    project_roots = infer_project_roots(source, paths)
    ownership = {p.relative_to(source).as_posix(): classify_ownership(p.relative_to(source).as_posix(), project_roots) for p in paths}
    edges, indegree, outdegree = build_import_graph(paths, source, ownership)
    max_in_degree = max(indegree.values(), default=0)
    entries: list[FileEntry] = []
    has_entrypoint = False
    has_control = False
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
        if own.ownership_class == "PROJECT_OWNED":
            has_control = has_control or path.name.lower() in CONTROL_FILE_NAMES
            has_entrypoint = has_entrypoint or bool(ENTRYPOINT_RE.search(rel))
        entries.append(FileEntry(rel, str(path.resolve()).replace("\\", "/"), st.st_size, st.st_size, utc(st.st_mtime), ext, depth, family, tier, role, own.ownership_class, own.ownership_score, own.included_in_import_graph and ext in SOURCE_EXTENSIONS and rel in indegree, score, risk, in_deg, out_deg, topology, out_deg, strategy, open_ok, edit_ok, approval, False, family_reasons + role_reasons + score_reasons))
    graph_stats = {"total_edges": sum(len(v) for v in edges.values()), "max_in_degree": max_in_degree, "nodes": len(edges), "project_roots": project_roots, "has_entrypoint": has_entrypoint, "has_control_files": has_control, "hotpath_score_basis": "PROJECT_OWNED source_code: topology(60)+size(20)+family(20); external files capped"}
    return entries, graph_stats


def sort_hot(entries: Iterable[FileEntry]) -> list[FileEntry]:
    return sorted(entries, key=lambda e: (e.ownership_class != "PROJECT_OWNED", -e.hotpath_score, -e.in_degree, e.risk_score, e.depth, e.relative_path))


def is_safe_read_candidate(entry: FileEntry) -> bool:
    return entry.ownership_class == "PROJECT_OWNED" and entry.strategy in {"open_now", "open_later"} and not entry.requires_human_approval and entry.folder_family not in TERMINAL_FAMILIES and entry.folder_family not in HUMAN_ONLY_FAMILIES and entry.folder_family != "binary_or_database" and entry.extension in TEXT_EXTENSIONS


def readiness_score(entries: list[FileEntry], graph_stats: dict[str, object]) -> float:
    project_entries = [e for e in entries if e.ownership_class == "PROJECT_OWNED"]
    total = max(len(project_entries), 1)
    w1 = 0.30 if graph_stats.get("has_entrypoint") else 0.0
    w2 = 0.25 if graph_stats.get("has_control_files") else 0.0
    open_now = sum(1 for entry in project_entries if entry.strategy == "open_now")
    w3 = 0.25 * min((open_now / total) * 4.0, 1.0)
    w4 = 0.20
    score = w1 + w2 + w3 + w4
    if not graph_stats.get("has_entrypoint") and not graph_stats.get("has_control_files"):
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
    return {"phase1": [asdict(e) for e in phase1], "phase1_total_bytes": total, "phase2": [asdict(e) for e in phase2], "approval_required": [asdict(e) for e in approval_required], "search_targets": [asdict(e) for e in search_targets], "human_only": [asdict(e) for e in hot if e.strategy == "human_only"], "ignored": [asdict(e) for e in hot if e.strategy == "ignore"]}


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
    for entry in entries:
        buckets[entry.folder_family].append(entry)
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


def write_structure_map(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object], graph_stats: dict[str, object]) -> None:
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    lines = ["# ACG Structure Map", "", f"Version: `{VERSION}`", f"Source: `{source}`", f"Generated: {dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()}", f"Total indexed files: {len(entries)}", f"Readiness score: {readiness} [{mode.upper()}]", "", "## Project Roots", ""]
    for root in graph_stats.get("project_roots", []):
        lines.append(f"- `{root}`")
    lines += ["", "## Ownership Summary", "", "| Ownership | Files |", "|---|---:|"]
    for k, v in ownership_summary(entries).items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "## Import Graph Stats", "", f"- Nodes: {graph_stats.get('nodes', 0)}", f"- Total edges: {graph_stats.get('total_edges', 0)}", f"- Max in-degree: {graph_stats.get('max_in_degree', 0)}", f"- Score basis: {graph_stats.get('hotpath_score_basis')}", "", "## Cluster Overview", "", "| Family | Files | Avg Hotpath | Dominant Strategy |", "|---|---:|---:|---|"]
    for row in family_summary(entries):
        lines.append(f"| {row['family']} | {row['files']} | {row['avg_hotpath_score']} | {row['dominant_strategy']} |")
    lines += ["", "## Top Hotpath Files", "", "| Score | In | Out | Owner | Risk | Strategy | Family | File |", "|---:|---:|---:|---|---:|---|---|---|"]
    for entry in sort_hot(entries)[:25]:
        lines.append(f"| {entry.hotpath_score} | {entry.in_degree} | {entry.out_degree} | {entry.ownership_class} | {entry.risk_score} | {entry.strategy} | {entry.folder_family} | `{entry.relative_path}` |")
    lines += ["", "## Rule", "", "Only PROJECT_OWNED files can compete in the main hotpath queue. External/runtime/dependency files are capped and excluded from the main import graph."]
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
    lines = ["# ACG Execution Brief", "", f"You are operating under ACG Structure Scout v{VERSION}.", "", f"Readiness: {readiness} [{mode.upper()}]", "", "Ownership-aware import graph scoring is active.", "Only PROJECT_OWNED source files are included in the main import graph.", "External runtime/dependency/cache files cannot win the main attention queue.", "", "## Import Graph Stats", "", f"- total_edges: {graph_stats.get('total_edges', 0)}", f"- max_in_degree: {graph_stats.get('max_in_degree', 0)}", f"- score_basis: {graph_stats.get('hotpath_score_basis')}", "", "## Project Roots", ""]
    for root in graph_stats.get("project_roots", []):
        lines.append(f"- `{root}`")
    lines += ["", "## Required artifacts to inspect first", "", "- `../ACG_MASTER.md`", "- `execution_brief.md`", "- `next_prompt.md`", "- `phase2_plan_template.md`", "- `structure_map.md`", "- `phase1_queue.md`", "- `phase2_queue.md`", "- `approval_required.md`", "- `search_targets.md`", "- `../phase1_pack/`", "", "## You may read now"]
    for item in queues.get("phase1", []):
        lines.append(f"- `{item['relative_path']}`")
    lines += ["", "## Required Phase 1 Output", "", "```txt", "ACG-UNDERSTOOD: structure-scout", "SCOPE: files you actually read", "RISKS: key risks before deeper processing", "QUESTIONS: objective questions or approval requests only", "NEXT: Phase 2 plan or up to 3 clarification questions", "```"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_next_prompt(path: Path, queues: dict[str, object]) -> None:
    lines = ["# ACG Continuation Protocol", "", "This file is not a human copy/paste prompt.", "The AI must read this file before Phase 1 and apply it automatically after Phase 1.", "", "## Current safe Phase 2 candidates", ""]
    for item in queues.get("phase2", []):
        lines.append(f"- `{item['relative_path']}` - {item.get('ownership_class', '-')}, {item['role']}, score {item['hotpath_score']}, in_degree {item.get('in_degree', 0)}")
    lines += ["", "Return NEXT using `phase2_plan_template.md` exactly."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_master(path: Path, source: Path, entries: list[FileEntry], queues: dict[str, object], graph_stats: dict[str, object]) -> None:
    readiness = readiness_score(entries, graph_stats)
    mode = guardrail_mode(readiness)
    lines = ["# ACG Master Context File", "", f"Generated by ACG Structure Scout v{VERSION}.", "", "This is the root instruction file for the generated ACG context package.", "", "## Source", "", f"`{source}`", "", "## Inventory Summary", "", f"- Total indexed files: {len(entries)}", f"- Phase 1 files: {len(queues.get('phase1', []))}", f"- Safe Phase 2 candidates: {len(queues.get('phase2', []))}", f"- Search-only / terminal assets: {len(queues.get('search_targets', []))}", f"- Import graph nodes: {graph_stats.get('nodes', 0)}", f"- Import graph edges: {graph_stats.get('total_edges', 0)}", f"- Max in-degree: {graph_stats.get('max_in_degree', 0)}", f"- Readiness score: {readiness} [{mode.upper()}]", "", "## Project Roots", ""]
    for root in graph_stats.get("project_roots", []):
        lines.append(f"- `{root}`")
    lines += ["", "## Read Order for AI", "", "1. Read this file: `ACG_MASTER.md`.", "2. Read `artifacts/execution_brief.md`.", "3. Read `artifacts/next_prompt.md`.", "4. Read `artifacts/phase2_plan_template.md`.", "5. Read `artifacts/structure_map.md`.", "6. Read `artifacts/phase1_queue.md` and `artifacts/phase2_queue.md`.", "7. Read `artifacts/approval_required.md` and `artifacts/search_targets.md`.", "8. Read only files copied inside `phase1_pack/`.", "", "## Do Not Do", "", "- Do not read the original source folder blindly.", "- Do not open terminal assets directly.", "- Do not read non-PROJECT_OWNED files unless explicitly approved.", "- Do not edit files during orientation.", "- Do not ask vague questions such as 'what next?'."]
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
    for entry in entries:
        if entry.extension:
            extensions[entry.extension] += 1
    report = {"acg_version": VERSION, "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(), "root": str(source), "system_profile": {"total_files": len(entries), "language_map": dict(extensions), "ownership_summary": ownership_summary(entries), "project_roots": graph_stats.get("project_roots", []), "has_entrypoint": bool(graph_stats.get("has_entrypoint")), "has_control_files": bool(graph_stats.get("has_control_files"))}, "readiness_score": readiness, "guardrail_mode": mode, "attention_queue": queues.get("phase1", [])[:20], "phased_reading_plan": {"phase1": queues.get("phase1", []), "phase2": queues.get("phase2", []), "phase3": queues.get("search_targets", [])[:10]}, "broken_refs": [], "execution_brief": {"task_id": "structure-scout", "root": str(source), "total_files": len(entries), "readiness_score": readiness, "guardrail_mode": mode, "readiness_components": {"W1_entrypoint_detected": bool(graph_stats.get("has_entrypoint")), "W2_control_files_present": bool(graph_stats.get("has_control_files")), "W3_open_now_count": len(queues.get("phase1", [])), "W4_broken_refs_count": 0}, "import_graph": {"total_edges": graph_stats.get("total_edges", 0), "max_in_degree": graph_stats.get("max_in_degree", 0), "hotpath_score_basis": graph_stats.get("hotpath_score_basis")}, "instruction": "Read Phase 1 files only. Return ACG-UNDERSTOOD, SCOPE, RISKS, QUESTIONS, NEXT before any edit."}, "context_manifest_ref": "context_manifest.jsonl"}
    write_json(path, report)


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG Structure Scout v0.4-beta")
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
    print(f"Project roots: {', '.join(str(x) for x in graph_stats.get('project_roots', []))}")
    print(f"Ownership summary: {ownership_summary(entries)}")
    print(f"Import graph nodes: {graph_stats.get('nodes', 0)}")
    print(f"Import graph edges: {graph_stats.get('total_edges', 0)}")
    print(f"Max in-degree: {graph_stats.get('max_in_degree', 0)}")
    print(f"ACG output folder: {out}")
    print(f"Scout report: {artifacts / 'scout_report.json'}")
    print(f"Phase 1 pack: {out / 'phase1_pack'}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        raise SystemExit(f"ACG ERROR: {exc}")
