#!/usr/bin/env python3
"""ACG Import Graph v0.4-alpha.

Static, no-dependency topology extractor for large codebases.

It does not execute project code. It scans files, extracts static imports,
computes in_degree/out_degree, detects hubs, writes a cluster map and public
surface summaries for important files.

Usage:
  python scripts/acg-import-graph.py --source /path/to/project --out .acg/artifacts
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

CODE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "coverage"}
SURFACE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs"}


@dataclass
class GraphNode:
    path: str
    extension: str
    size: int
    imports: list[str] = field(default_factory=list)
    resolved_imports: list[str] = field(default_factory=list)
    imported_by: list[str] = field(default_factory=list)
    in_degree: int = 0
    out_degree: int = 0
    git_velocity_90d: int = 0
    public_surface_count: int = 0
    architectural_weight: int = 0
    surface_available: bool = False


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_python_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(read_text(path))
    except Exception:
        return []
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append("." * int(node.level) + node.module)
            elif node.level:
                imports.append("." * int(node.level))
    return imports


def extract_js_ts_imports(path: Path) -> list[str]:
    text = read_text(path)
    patterns = [
        r"from\s+['\"]([^'\"]+)['\"]",
        r"import\s+['\"]([^'\"]+)['\"]",
        r"require\(['\"]([^'\"]+)['\"]\)",
        r"import\(['\"]([^'\"]+)['\"]\)",
    ]
    imports: list[str] = []
    for pattern in patterns:
        imports.extend(re.findall(pattern, text))
    return imports


def extract_go_imports(path: Path) -> list[str]:
    text = read_text(path)
    imports: list[str] = []
    block = re.search(r"import\s*\((.*?)\)", text, re.DOTALL)
    if block:
        imports.extend(re.findall(r'"([^"]+)"', block.group(1)))
    imports.extend(re.findall(r'import\s+"([^"]+)"', text))
    return imports


def extract_rust_imports(path: Path) -> list[str]:
    text = read_text(path)
    imports = re.findall(r"^\s*use\s+([^;]+);", text, re.MULTILINE)
    imports.extend(re.findall(r"^\s*mod\s+([A-Za-z_][A-Za-z0-9_]*);", text, re.MULTILINE))
    return imports


def extract_imports(path: Path) -> list[str]:
    if path.suffix == ".py":
        return extract_python_imports(path)
    if path.suffix in {".js", ".jsx", ".ts", ".tsx"}:
        return extract_js_ts_imports(path)
    if path.suffix == ".go":
        return extract_go_imports(path)
    if path.suffix == ".rs":
        return extract_rust_imports(path)
    return []


def build_file_index(root: Path) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in root.rglob("*"):
        if should_skip(path) or not path.is_file() or path.suffix not in CODE_EXTENSIONS:
            continue
        rp = rel(root, path)
        stem_key = path.with_suffix("").relative_to(root).as_posix()
        index[rp] = rp
        index[stem_key] = rp
        index[path.name] = rp
        index[path.stem] = rp
    return index


def resolve_import(root: Path, from_file: str, raw_import: str, index: dict[str, str]) -> str | None:
    if not raw_import or raw_import.startswith(("http://", "https://")):
        return None
    if raw_import in index:
        return index[raw_import]

    from_path = root / from_file
    base = from_path.parent

    if raw_import.startswith("."):
        candidate = (base / raw_import).resolve()
        try:
            rel_candidate = candidate.relative_to(root.resolve()).as_posix()
        except ValueError:
            return None
        variants = [rel_candidate, rel_candidate.replace(".", "/")]
    else:
        variants = [raw_import.replace(".", "/"), raw_import]

    extensions = ["", ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs"]
    suffixes = ["", "/index", "/__init__", "/mod"]
    for variant in variants:
        for suffix in suffixes:
            for ext in extensions:
                key = f"{variant}{suffix}{ext}"
                if key in index:
                    return index[key]
    return None


def git_velocity(root: Path, days: int = 90) -> dict[str, int]:
    git_dir = root / ".git"
    if not git_dir.exists():
        return {}
    try:
        result = subprocess.run(
            ["git", "log", f"--since={days} days ago", "--name-only", "--pretty=format:", "--diff-filter=AM"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except Exception:
        return {}
    counts: Counter[str] = Counter()
    for line in result.stdout.splitlines():
        item = line.strip().replace("\\", "/")
        if item:
            counts[item] += 1
    return dict(counts)


def extract_public_surface(path: Path, max_lines: int = 160) -> list[str]:
    text = read_text(path)
    ext = path.suffix
    lines: list[str] = []
    if ext == ".py":
        try:
            tree = ast.parse(text)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    lines.append(f"class {node.name}")
                    for child in node.body:
                        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and not child.name.startswith("_"):
                            args = [a.arg for a in child.args.args]
                            lines.append(f"  def {child.name}({', '.join(args)})")
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                    args = [a.arg for a in node.args.args]
                    lines.append(f"def {node.name}({', '.join(args)})")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            lines.append(target.id)
        except Exception:
            pass
    elif ext in {".ts", ".tsx", ".js", ".jsx"}:
        patterns = [
            r"^\s*export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const|let|var|type|interface|enum)\s+[^\n]+",
            r"^\s*module\.exports\s*=\s*[^\n]+",
            r"^\s*exports\.[A-Za-z0-9_]+\s*=\s*[^\n]+",
        ]
        for pattern in patterns:
            lines.extend(re.findall(pattern, text, flags=re.MULTILINE))
    elif ext == ".go":
        lines.extend(re.findall(r"^\s*func\s+(?:\([^)]*\)\s*)?[A-Z][A-Za-z0-9_]*\s*\([^\n]*", text, re.MULTILINE))
        lines.extend(re.findall(r"^\s*type\s+[A-Z][A-Za-z0-9_]*\s+[^\n]+", text, re.MULTILINE))
    elif ext == ".rs":
        lines.extend(re.findall(r"^\s*pub\s+(?:async\s+)?(?:fn|struct|enum|trait|type)\s+[^\n{;]+", text, re.MULTILINE))
    if not lines:
        lines = text.splitlines()[:80]
    return lines[:max_lines]


def calculate_weight(node: GraphNode) -> int:
    score = 0
    score += min(node.in_degree * 5, 45)
    score += min(node.out_degree * 2, 15)
    score += min(node.git_velocity_90d * 4, 25)
    score += min(node.public_surface_count * 2, 20)
    if re.search(r"(schema|contract|types?|interface|model|api|router|auth|payment|security)", node.path, re.IGNORECASE):
        score += 15
    return min(score, 100)


def build_graph(root: Path) -> tuple[dict[str, GraphNode], dict[str, list[str]]]:
    index = build_file_index(root)
    velocity = git_velocity(root)
    nodes: dict[str, GraphNode] = {}

    for path in root.rglob("*"):
        if should_skip(path) or not path.is_file() or path.suffix not in CODE_EXTENSIONS:
            continue
        rp = rel(root, path)
        raw_imports = extract_imports(path)
        resolved = []
        for raw in raw_imports:
            target = resolve_import(root, rp, raw, index)
            if target and target != rp:
                resolved.append(target)
        surface = extract_public_surface(path)
        nodes[rp] = GraphNode(
            path=rp,
            extension=path.suffix,
            size=path.stat().st_size,
            imports=raw_imports,
            resolved_imports=sorted(set(resolved)),
            out_degree=len(set(resolved)),
            git_velocity_90d=velocity.get(rp, 0),
            public_surface_count=len(surface),
            surface_available=bool(surface),
        )

    reverse: dict[str, list[str]] = defaultdict(list)
    for source, node in nodes.items():
        for target in node.resolved_imports:
            if target in nodes:
                reverse[target].append(source)

    for path, node in nodes.items():
        node.imported_by = sorted(set(reverse.get(path, [])))
        node.in_degree = len(node.imported_by)
        node.architectural_weight = calculate_weight(node)

    return nodes, dict(reverse)


def macro_family(path: str) -> str:
    parts = path.split("/")
    if not parts:
        return "root"
    if parts[0] in {"src", "app", "lib", "packages", "services", "apps"} and len(parts) > 1:
        return "/".join(parts[:2])
    return parts[0]


def write_cluster_map(path: Path, nodes: dict[str, GraphNode]) -> None:
    by_family: dict[str, list[GraphNode]] = defaultdict(list)
    for node in nodes.values():
        by_family[macro_family(node.path)].append(node)

    lines = ["# ACG Cluster Map", "", "Topological view generated from static imports.", "", "## Macro Clusters", "", "| Cluster | Files | Avg Weight | Top Hubs |", "|---|---:|---:|---|"]
    for family, items in sorted(by_family.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        avg = round(sum(i.architectural_weight for i in items) / max(len(items), 1), 1)
        hubs = sorted(items, key=lambda n: (-n.in_degree, -n.architectural_weight, n.path))[:3]
        hub_text = ", ".join(f"`{h.path}` (in:{h.in_degree}, w:{h.architectural_weight})" for h in hubs) or "-"
        lines.append(f"| `{family}` | {len(items)} | {avg} | {hub_text} |")

    lines += ["", "## Top Architectural Hubs", "", "| Weight | In | Out | Velocity | Surface | File |", "|---:|---:|---:|---:|---:|---|"]
    for node in sorted(nodes.values(), key=lambda n: (-n.architectural_weight, -n.in_degree, n.path))[:50]:
        lines.append(f"| {node.architectural_weight} | {node.in_degree} | {node.out_degree} | {node.git_velocity_90d} | {node.public_surface_count} | `{node.path}` |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_surface_summaries(path: Path, root: Path, nodes: dict[str, GraphNode], max_files: int = 30) -> None:
    selected = sorted(nodes.values(), key=lambda n: (-n.architectural_weight, -n.in_degree, n.path))[:max_files]
    lines = ["# ACG Surface Summaries", "", "Public surfaces for high-weight files. These are not full file contents.", ""]
    for node in selected:
        file_path = root / node.path
        lines.append(f"## `{node.path}`")
        lines.append("")
        lines.append(f"weight: {node.architectural_weight} | in_degree: {node.in_degree} | out_degree: {node.out_degree} | velocity_90d: {node.git_velocity_90d}")
        lines.append("")
        lines.append("```txt")
        lines.extend(extract_public_surface(file_path, max_lines=120))
        lines.append("```")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG Import Graph v0.4-alpha")
    parser.add_argument("--source", required=True, help="Source repository/folder")
    parser.add_argument("--out", default=".acg/artifacts", help="Output artifact folder")
    args = parser.parse_args()

    root = Path(args.source).resolve()
    out = Path(args.out).resolve()
    if not root.is_dir():
        raise SystemExit(f"Source folder not found: {root}")
    out.mkdir(parents=True, exist_ok=True)

    nodes, reverse = build_graph(root)
    payload = {
        "generated": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": str(root),
        "nodes": {path: asdict(node) for path, node in sorted(nodes.items())},
        "reverse": {path: sorted(set(items)) for path, items in sorted(reverse.items())},
    }
    (out / "import_graph.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_cluster_map(out / "cluster_map.md", nodes)
    write_surface_summaries(out / "surface_summaries.md", root, nodes)

    print(f"ACG import graph nodes: {len(nodes)}")
    print(f"Import graph: {out / 'import_graph.json'}")
    print(f"Cluster map: {out / 'cluster_map.md'}")
    print(f"Surface summaries: {out / 'surface_summaries.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
