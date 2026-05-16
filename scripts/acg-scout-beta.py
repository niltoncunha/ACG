#!/usr/bin/env python3
"""ACG Structure Scout v0.4-beta.

Beta scout for import-graph-driven hotpath scoring and formal readiness scoring.

This file is intentionally separate from scripts/acg-scout.py until the beta
contract is merged into the stable .acg/artifacts package generator used by
scripts/acg-v04.py.

Usage:
  python scripts/acg-scout-beta.py --root . --config acg.yaml
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

VERSION = "0.4-beta"

IGNORE_DIRS = {
    ".git", ".svn", "__pycache__", "node_modules", ".venv", "venv", "env",
    "dist", "build", ".build", ".cache", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", "coverage", ".coverage",
}

TERMINAL_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".mp4", ".mp3", ".wav", ".ogg", ".zip", ".tar", ".gz", ".bz2",
    ".xz", ".rar", ".pdf", ".docx", ".xlsx", ".pptx", ".pyc",
    ".pyo", ".class", ".o", ".a", ".so", ".dll", ".exe", ".bin",
    ".wasm", ".lock",
}

SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".rs", ".go"}

FOLDER_FAMILY_RULES: dict[str, list[str]] = {
    "secrets": ["secrets", ".env", "credentials", "keys", "certs"],
    "infra": ["infra", "terraform", "ansible", "k8s", "kubernetes", "docker", "helm"],
    "migrations": ["migrations", "migration", "alembic", "flyway"],
    "tests": ["tests", "test", "spec", "__tests__", "e2e"],
    "docs": ["docs", "doc", "documentation", "wiki", "guides"],
    "logs": ["logs", "log", ".logs"],
    "exports": ["exports", "export", "output", "outputs", "dist"],
    "generated": ["generated", "gen", ".generated", "auto"],
    "legacy": ["legacy", "deprecated", "archive", "old"],
    "reference": ["reference", "ref", "samples", "fixtures"],
    "memory": ["memory", "cache", ".acg", ".context"],
    "canon": ["canon", "core_docs", "spec", "specs"],
    "core": ["src", "lib", "app", "core", "pkg", "cmd", "api", "server"],
    "runtime": ["runtime", "engine", "executor", "runner"],
    "evaluation": ["eval", "evaluation", "benchmark", "evals"],
}

STRATEGY_MAP = {
    "secrets": "human_only", "infra": "human_only", "migrations": "human_only",
    "logs": "terminal_asset", "exports": "terminal_asset", "generated": "index_only",
    "legacy": "index_only", "reference": "search_only", "memory": "search_only",
    "evaluation": "open_later", "tests": "open_later", "docs": "open_later",
    "canon": "open_now", "core": "open_now", "runtime": "open_now",
    "unknown": "open_later",
}

FAMILY_HOTPATH = {
    "core": 20, "canon": 18, "runtime": 16,
    "tests": 10, "docs": 8, "evaluation": 8,
    "reference": 5, "memory": 4, "legacy": 2, "unknown": 6,
    "generated": 0, "logs": 0, "exports": 0, "secrets": 0,
    "infra": 0, "migrations": 0,
}

FAMILY_RISK = {"secrets": 80, "infra": 60, "migrations": 50, "logs": 10, "exports": 5, "generated": 2}

CONTROL_FILE_NAMES = {
    "acg.yaml", "acg.json", "package.json", "pyproject.toml", "cargo.toml",
    "go.mod", "makefile", "dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "requirements.txt", "setup.py", "setup.cfg",
}

ENTRYPOINT_RE = re.compile(
    r"(^|[\\/])(main\.py|main\.go|main\.rs|index\.[jt]sx?|app\.py|server\.py|__main__\.py|cmd[\\/]main\.go|src[\\/]main\.rs|bin[\\/]main\.rs)$",
    re.I,
)

RISK_PATTERNS = [
    (re.compile(r"secret|password|token|api.?key|credential", re.I), 40),
    (re.compile(r"migration|schema.?change|drop.table", re.I), 30),
    (re.compile(r"\.env$"), 50),
    (re.compile(r"infra|terraform|k8s|kubernetes", re.I), 25),
]

JS_RE = re.compile(r"(?:import\s+.*?\s+from\s+|require\s*\(\s*)['\"](\.{1,2}/[^'\"]+)['\"]", re.MULTILINE)
RUST_RE = re.compile(r"^\s*use\s+([\w:]+)", re.MULTILINE)
GO_BLOCK_RE = re.compile(r"import\s*\((.*?)\)", re.DOTALL)
GO_SINGLE_RE = re.compile(r'import\s+"([^"]+)"')
GO_ITEM_RE = re.compile(r'"([^"]+)"')


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_python(path: Path) -> list[str]:
    try:
        tree = ast.parse(read_text(path), filename=str(path))
    except Exception:
        return []
    out: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            out.append(node.module)
    return out


def extract_js(path: Path) -> list[str]:
    try:
        return JS_RE.findall(read_text(path))
    except OSError:
        return []


def extract_rust(path: Path) -> list[str]:
    try:
        return RUST_RE.findall(read_text(path))
    except OSError:
        return []


def extract_go(path: Path) -> list[str]:
    try:
        src = read_text(path)
    except OSError:
        return []
    block = GO_BLOCK_RE.search(src)
    if block:
        return GO_ITEM_RE.findall(block.group(1))
    single = GO_SINGLE_RE.search(src)
    return [single.group(1)] if single else []


def extract_imports(path: Path) -> list[str]:
    ext = path.suffix.lower()
    if ext == ".py":
        return extract_python(path)
    if ext in {".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs"}:
        return extract_js(path)
    if ext == ".rs":
        return extract_rust(path)
    if ext == ".go":
        return extract_go(path)
    return []


def should_skip_dir(name: str) -> bool:
    return name in IGNORE_DIRS or (name.startswith(".") and name != ".acg")


def glob_to_regex(pattern: str) -> str:
    return "^" + re.escape(pattern).replace("\\*\\*", ".*").replace("\\*", "[^/]*") + "$"


def scan(root: Path, forbidden: list[str]) -> list[Path]:
    forbidden_re = [re.compile(glob_to_regex(p.replace("\\", "/"))) for p in forbidden]
    out: list[Path] = []
    for dp, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        for name in names:
            path = Path(dp) / name
            rel = path.relative_to(root).as_posix()
            if any(rx.fullmatch(rel) for rx in forbidden_re):
                continue
            out.append(path)
    return out


def build_import_graph(files: list[Path], root: Path) -> tuple[dict[str, list[str]], dict[str, int]]:
    rel_map: dict[str, Path] = {}
    stem_idx: dict[str, list[str]] = defaultdict(list)
    for f in files:
        if f.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        try:
            rel = f.relative_to(root).as_posix()
        except ValueError:
            continue
        rel_map[rel] = f
        stem_idx[f.stem.lower()].append(rel)

    edges: dict[str, list[str]] = {}
    indegree: dict[str, int] = defaultdict(int)
    for rel, fpath in rel_map.items():
        resolved: list[str] = []
        for imp in extract_imports(fpath):
            found = False
            if imp.startswith("."):
                candidate_base = (fpath.parent / imp).resolve()
                variants = [candidate_base]
            else:
                variants = [(root / imp.replace(".", "/")).resolve()]
            for base in variants:
                for ext in ("", ".py", ".ts", ".js", ".tsx", ".jsx", ".rs", ".go"):
                    cand = Path(str(base) + ext)
                    try:
                        crel = cand.relative_to(root).as_posix()
                    except ValueError:
                        continue
                    if crel in rel_map and crel != rel:
                        resolved.append(crel)
                        indegree[crel] += 1
                        found = True
                        break
                if found:
                    break
            if not found:
                stem = imp.split(".")[-1].split("/")[-1].lower()
                for match in stem_idx.get(stem, []):
                    if match != rel:
                        resolved.append(match)
                        indegree[match] += 1
                        break
        edges[rel] = sorted(set(resolved))
    for rel in rel_map:
        indegree.setdefault(rel, 0)
    return edges, dict(indegree)


def classify_family(rel: str) -> str:
    parts = Path(rel).parts[:-1]
    for part in parts:
        pl = part.lower()
        for family, keywords in FOLDER_FAMILY_RULES.items():
            if any(pl == kw or pl.startswith(kw) for kw in keywords):
                return family
    return "unknown"


def risk_score(rel: str, family: str) -> int:
    score = FAMILY_RISK.get(family, 0)
    score += sum(weight for pattern, weight in RISK_PATTERNS if pattern.search(rel))
    return min(100, score)


def hotpath_score(rel: str, indegree: dict[str, int], size_bytes: int, family: str, max_indegree: int) -> int:
    topology = int(60 * (indegree.get(rel, 0) / max(max_indegree, 1)))
    if size_bytes < 50_000:
        size_score = 20
    elif size_bytes < 200_000:
        size_score = 12
    elif size_bytes < 500_000:
        size_score = 5
    else:
        size_score = 0
    family_score = FAMILY_HOTPATH.get(family, 6)
    return min(100, topology + size_score + family_score)


def assign_strategy(family: str, size: int, ext: str, risk: int) -> str:
    if ext in TERMINAL_EXTENSIONS:
        return "terminal_asset"
    if risk >= 60:
        return "human_only"
    if size > 500_000:
        return "search_only"
    return STRATEGY_MAP.get(family, "open_later")


def readiness_score(records: list[dict[str, Any]], has_entrypoint: bool, has_control: bool, broken_count: int) -> float:
    total = max(len(records), 1)
    w1 = 0.30 if has_entrypoint else 0.0
    w2 = 0.25 if has_control else 0.0
    open_now = sum(1 for r in records if r["strategy"] == "open_now")
    w3 = 0.25 * min((open_now / total) * 4.0, 1.0)
    w4 = 0.20 * max(0.0, 1.0 - broken_count / total)
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


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}


def run_scout(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    forbidden = config.get("task", {}).get("scope", {}).get("forbidden", []) or config.get("scope", {}).get("forbidden", []) or []
    all_files = scan(root, forbidden)
    edges, indegree = build_import_graph(all_files, root)
    max_indegree = max(indegree.values(), default=1)
    edge_count = sum(len(v) for v in edges.values())

    has_entrypoint = False
    has_control = False
    records: list[dict[str, Any]] = []

    for fp in all_files:
        try:
            rel = fp.relative_to(root).as_posix()
            stat = fp.stat()
        except OSError:
            continue
        ext = fp.suffix.lower()
        family = classify_family(rel)
        risk = risk_score(rel, family)
        strategy = assign_strategy(family, stat.st_size, ext, risk)
        hp = hotpath_score(rel, indegree, stat.st_size, family, max_indegree)
        if fp.name.lower() in CONTROL_FILE_NAMES:
            has_control = True
        if ENTRYPOINT_RE.search(rel):
            has_entrypoint = True
        records.append({
            "relative_path": rel,
            "absolute_path": str(fp.resolve()),
            "size_bytes": stat.st_size,
            "modified": dt.datetime.fromtimestamp(stat.st_mtime, tz=dt.timezone.utc).isoformat(),
            "extension": ext,
            "folder_family": family,
            "role": "source_code" if ext in SOURCE_EXTENSIONS else "other",
            "hotpath_score": hp,
            "risk_score": risk,
            "in_degree": indegree.get(rel, 0),
            "strategy": strategy,
            "allowed_to_open": strategy not in {"human_only", "ignore", "terminal_asset"},
            "allowed_to_edit": strategy in {"open_now", "open_later"} and risk < 40,
            "requires_human_approval": strategy == "human_only",
        })

    records.sort(key=lambda r: (-int(r["hotpath_score"]), int(r["risk_score"]), r["relative_path"]))
    rel_set = {r["relative_path"] for r in records}
    broken = [{"source": src, "missing": tgt} for src, targets in edges.items() for tgt in targets if tgt not in rel_set]
    score = readiness_score(records, has_entrypoint, has_control, len(broken))
    mode = guardrail_mode(score)
    attention = [r for r in records if r["strategy"] == "open_now"][:20]
    phase1 = attention[:10]
    phase2 = [r for r in records if r["strategy"] == "open_later"][:15]
    phase3 = [r for r in records if r["strategy"] == "search_only"][:10]
    language_map: dict[str, int] = defaultdict(int)
    for r in records:
        if r["extension"]:
            language_map[str(r["extension"])] += 1

    brief = {
        "task_id": config.get("task", {}).get("id", "unset"),
        "root": str(root),
        "total_files": len(records),
        "readiness_score": score,
        "guardrail_mode": mode,
        "readiness_components": {
            "W1_entrypoint_detected": has_entrypoint,
            "W2_control_files_present": has_control,
            "W3_open_now_count": sum(1 for r in records if r["strategy"] == "open_now"),
            "W4_broken_refs_count": len(broken),
        },
        "import_graph": {
            "total_edges": edge_count,
            "max_in_degree": max_indegree,
            "hotpath_score_basis": "topology(60)+size(20)+family(20)",
        },
        "instruction": "Read Phase 1 attention_queue files only. Reply ACG-UNDERSTOOD, SCOPE, RISKS, QUESTIONS before any edit.",
    }
    return {
        "acg_version": VERSION,
        "generated_at": dt.datetime.now(tz=dt.timezone.utc).isoformat(),
        "root": str(root),
        "system_profile": {
            "total_files": len(records),
            "language_map": dict(language_map),
            "has_entrypoint": has_entrypoint,
            "has_control_files": has_control,
        },
        "readiness_score": score,
        "guardrail_mode": mode,
        "attention_queue": attention,
        "phased_reading_plan": {"phase1": phase1, "phase2": phase2, "phase3": phase3},
        "broken_refs": broken,
        "execution_brief": brief,
        "context_manifest": records,
    }


def write_outputs(report: dict[str, Any], root: Path) -> None:
    out = root / ".acg-beta"
    out.mkdir(exist_ok=True)
    (out / "scout_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (out / "context_manifest.jsonl").open("w", encoding="utf-8") as handle:
        for row in report["context_manifest"]:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    lines = [
        f"# ACG Structure Map v{report['acg_version']}",
        "",
        f"Root: `{report['root']}`",
        f"Readiness: {report['readiness_score']} [{report['guardrail_mode'].upper()}]",
        "",
        "## Attention Queue",
        "",
        "| # | File | hotpath | in_degree | family | strategy |",
        "|---:|---|---:|---:|---|---|",
    ]
    for i, row in enumerate(report["attention_queue"], 1):
        lines.append(f"| {i} | `{row['relative_path']}` | {row['hotpath_score']} | {row['in_degree']} | {row['folder_family']} | {row['strategy']} |")
    lines += ["", "## Import Graph", ""]
    graph = report["execution_brief"]["import_graph"]
    lines.append(f"- total_edges: {graph['total_edges']}")
    lines.append(f"- max_in_degree: {graph['max_in_degree']}")
    lines.append(f"- score_basis: {graph['hotpath_score_basis']}")
    (out / "structure_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "execution_brief.md").write_text(json.dumps(report["execution_brief"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[acg-scout-beta] Outputs: {out}")
    print(f"readiness_score: {report['readiness_score']} mode={report['guardrail_mode']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="ACG Structure Scout v0.4-beta")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--config", type=Path, default=Path("acg.yaml"))
    args = parser.parse_args()
    root = args.root.resolve()
    report = run_scout(root, load_config(args.config))
    write_outputs(report, root)
    mode = report["guardrail_mode"]
    if mode == "halt":
        raise SystemExit(2)
    if mode == "warn":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
