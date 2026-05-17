#!/usr/bin/env python3
"""ACG v0.4-beta orchestrator.

Single-command flow for topology-aware context generation.

This wrapper must not downgrade or overwrite the package contract emitted by
acg-scout.py. It runs the Scout, adds optional v0.4 topology/payload artifacts,
and patches dynamic package-boundary rules into the generated ACG package.

Usage:
  python scripts/acg-v04.py --source /path/to/project --out .acg
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

CODE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "coverage"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def sanitize_text(text: str) -> str:
    return "".join(ch for ch in text if ch in "\n\r\t" or ord(ch) >= 32)


def repo_signature(source: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(source.rglob("*")):
        if should_skip(path) or not path.is_file() or path.suffix.lower() not in CODE_EXTENSIONS:
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        rel = path.relative_to(source).as_posix()
        h.update(rel.encode("utf-8", errors="ignore"))
        h.update(str(stat.st_size).encode())
        h.update(str(int(stat.st_mtime)).encode())
    return h.hexdigest()


def run_step(name: str, cmd: list[str]) -> tuple[float, int]:
    print(f"ACG v0.4 running {name}: {' '.join(cmd)}")
    started = time.perf_counter()
    result = subprocess.run(cmd, text=True)
    elapsed = time.perf_counter() - started
    if result.returncode != 0:
        raise SystemExit(f"ACG v0.4 step failed: {name} exit={result.returncode}")
    return elapsed, result.returncode


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_text_safe(path: Path, max_bytes: int = 100_000) -> str:
    if not path.is_file():
        return ""
    data = path.read_bytes()[:max_bytes]
    return sanitize_text(data.decode("utf-8", errors="ignore"))


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def build_context_payload(source: Path, out: Path, model_budget_tokens: int) -> dict:
    artifacts = out / "artifacts"
    queues = load_json(artifacts / "reading_queues.json")
    graph_path = artifacts / "import_graph.json"
    graph = load_json(graph_path) if graph_path.is_file() else {"nodes": {}}
    nodes = graph.get("nodes", {})

    phase1_items = []
    for item in queues.get("phase1", []):
        rel = item["relative_path"]
        pack_path = out / "phase1_pack" / rel
        content = read_text_safe(pack_path)
        phase1_items.append({
            "path": rel,
            "mode": "full",
            "tokens_estimated": estimate_tokens(content),
            "reason": item.get("reason", []),
            "hotpath_score": item.get("hotpath_score"),
            "risk_score": item.get("risk_score"),
            "content": content,
        })

    hubs = []
    for path, node in sorted(
        nodes.items(),
        key=lambda kv: (
            -int(kv[1].get("architectural_weight", 0)),
            -int(kv[1].get("in_degree", 0)),
            kv[0],
        ),
    )[:50]:
        hubs.append({
            "path": path,
            "architectural_weight": node.get("architectural_weight", 0),
            "in_degree": node.get("in_degree", 0),
            "out_degree": node.get("out_degree", 0),
            "git_velocity_90d": node.get("git_velocity_90d", 0),
            "surface_available": node.get("surface_available", False),
        })

    surfaces = read_text_safe(artifacts / "surface_summaries.md", max_bytes=250_000)
    cluster_map = read_text_safe(artifacts / "cluster_map.md", max_bytes=120_000)
    payload = {
        "schema": "acg.context_payload.v0.4-beta",
        "generated": now(),
        "source": str(source),
        "package_root": str(out),
        "model_budget_tokens": model_budget_tokens,
        "budget_policy": {
            "note": "This is a lightweight payload. It is not a full RAG system.",
            "phase1_full_files": len(phase1_items),
            "topological_hubs": len(hubs),
        },
        "package_boundary": package_boundary(source, out),
        "skeleton": {
            "cluster_map_md": cluster_map,
            "top_hubs": hubs,
        },
        "contracts": {
            "surface_summaries_md": surfaces,
        },
        "full_files_allowed": phase1_items,
        "summaries": {
            "phase1_queue_md": read_text_safe(artifacts / "phase1_queue.md"),
            "phase2_queue_md": read_text_safe(artifacts / "phase2_queue.md"),
            "approval_required_md": read_text_safe(artifacts / "approval_required.md"),
            "search_targets_md": read_text_safe(artifacts / "search_targets.md", max_bytes=120_000),
        },
    }
    payload["tokens_estimated"] = estimate_tokens(json.dumps(payload, ensure_ascii=False))
    return payload


def count_code_files(source: Path) -> int:
    total = 0
    for path in source.rglob("*"):
        if should_skip(path) or not path.is_file() or path.suffix.lower() not in CODE_EXTENSIONS:
            continue
        total += 1
    return total


def package_boundary(source: Path, out: Path) -> dict[str, object]:
    out = out.resolve()
    return {
        "current_package_root": str(out),
        "acg_master": str((out / "ACG_MASTER.md").resolve()),
        "artifacts_root": str((out / "artifacts").resolve()),
        "phase1_pack_root": str((out / "phase1_pack").resolve()),
        "source_root": str(source.resolve()),
        "phase1_allowed_roots": [
            str((out / "ACG_MASTER.md").resolve()),
            str((out / "artifacts").resolve()),
            str((out / "phase1_pack").resolve()),
        ],
        "phase1_forbidden": [
            "parent directories of current_package_root",
            "sibling directories of current_package_root",
            "previous, cached, backup, alternate, or regenerated ACG packages",
            "direct reads from source_root",
            "FindFiles/SearchText used to locate Phase 2 files before human approval",
        ],
        "phase2_queue_semantics": "Phase 2 queue entries are metadata requests for human approval. They are not expected to exist in phase1_pack, and absence from phase1_pack is not a missing-file error.",
    }


def boundary_markdown(source: Path, out: Path) -> str:
    b = package_boundary(source, out)
    return f"""## ACG Package Boundary

Current ACG package root is the directory containing this `ACG_MASTER.md`.

```txt
current_package_root: {b['current_package_root']}
artifacts_root:       {b['artifacts_root']}
phase1_pack_root:     {b['phase1_pack_root']}
source_root:          {b['source_root']}
```

During Phase 1, the AI may read only:

- this `ACG_MASTER.md` file;
- files under this package's `artifacts/` directory;
- files under this package's `phase1_pack/` directory, in `phase1_reading_order.md` order.

Do not inspect any path outside the current ACG package root during Phase 1.

Do not inspect parent, sibling, previous, cached, backup, alternate, or regenerated ACG packages unless the human explicitly asks to compare packages.

Do not search for Phase 2 files during Phase 1.

Phase 2 queue entries are metadata requests for human approval. They are not expected to exist inside `phase1_pack/`. Absence from `phase1_pack/` is not a missing-file error.
"""


def insert_section_once(path: Path, marker: str, section: str, after_heading: str | None = None) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    if after_heading and after_heading in text:
        text = text.replace(after_heading, after_heading + "\n\n" + section.strip() + "\n", 1)
    else:
        text = text.rstrip() + "\n\n" + section.strip() + "\n"
    path.write_text(text, encoding="utf-8")


def patch_package_boundary(out: Path, source: Path) -> None:
    artifacts = out / "artifacts"
    section = boundary_markdown(source, out)
    marker = "## ACG Package Boundary"

    insert_section_once(out / "ACG_MASTER.md", marker, section, after_heading="## Source")
    insert_section_once(artifacts / "execution_brief.md", marker, section, after_heading="## Expected Completion Counts")
    insert_section_once(artifacts / "next_prompt.md", marker, section, after_heading="## Expected Counts")
    insert_section_once(artifacts / "phase2_plan_template.md", marker, section)
    insert_section_once(artifacts / "completion_checklist.md", marker, section)

    checklist = artifacts / "completion_checklist.md"
    if checklist.is_file():
        text = checklist.read_text(encoding="utf-8")
        extra = """
## Package Boundary Checklist

- [ ] I stayed inside the current package root during Phase 1.
- [ ] I did not inspect parent, sibling, previous, cached, backup, alternate, or regenerated packages.
- [ ] I did not read directly from `source_root` during Phase 1.
- [ ] I did not search for Phase 2 files during Phase 1.
- [ ] I did not treat absence from `phase1_pack/` as missing source context.
"""
        if "## Package Boundary Checklist" not in text:
            checklist.write_text(text.rstrip() + "\n\n" + extra.strip() + "\n", encoding="utf-8")

    report_path = artifacts / "scout_report.json"
    if report_path.is_file():
        report = load_json(report_path)
        report["package_boundary"] = package_boundary(source, out)
        if "completion_checklist" in report and isinstance(report["completion_checklist"], dict):
            report["completion_checklist"]["package_boundary"] = {
                "stay_inside_current_package_root": True,
                "do_not_search_phase2_files_during_phase1": True,
                "phase2_absence_from_phase1_pack_is_expected": True,
            }
        write_json(report_path, report)


def patch_v04_context_notes(out: Path) -> None:
    artifacts = out / "artifacts"
    note = """## v0.4 Topology Context

- `cluster_map.md` and `surface_summaries.md` are allowed planning context.
- `import_graph.json` is machine-readable diagnostics; do not read fully by default.
- `context_payload.json` is optional compact handoff mode, not mandatory Phase 1 input.
- Surface summaries do not grant permission to open original files outside the active queue.
"""
    insert_section_once(out / "ACG_MASTER.md", "## v0.4 Topology Context", note)
    insert_section_once(artifacts / "execution_brief.md", "## v0.4 Topology Context", note)
    insert_section_once(artifacts / "next_prompt.md", "## v0.4 Topology Context", note)


def write_performance_report(path: Path, timings: dict[str, float], source: Path, out: Path, cache_hit: bool, indexed_code_files: int) -> None:
    total = sum(timings.values())
    lines = [
        "# ACG v0.4 Performance Report",
        "",
        f"Generated: {now()}",
        f"Source: `{source}`",
        f"Output: `{out}`",
        f"Import graph cache hit: {str(cache_hit).lower()}",
        f"Indexed code files: {indexed_code_files}",
        "",
        "## Timings",
        "",
        "| Step | Seconds |",
        "|---|---:|",
    ]
    for key, value in timings.items():
        lines.append(f"| {key} | {value:.3f} |")
    lines.append(f"| total | {total:.3f} |")
    lines += [
        "",
        "## Performance Targets",
        "",
        "- Target for 10k files: < 30 seconds when cache is warm or mostly warm.",
        "- Target for 100k files: < 3 minutes for full scan on normal developer hardware.",
        "- If these targets fail, disable optional lexical indexing first, then reduce surface summary limits.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG v0.4-beta orchestrator")
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", default=".acg")
    parser.add_argument("--model-budget-tokens", type=int, default=128000)
    parser.add_argument("--skip-lexical-index", action="store_true")
    parser.add_argument("--force-topology", action="store_true")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    out = Path(args.out).resolve()
    artifacts = out / "artifacts"
    cache = out / "cache"
    scripts_dir = Path(__file__).resolve().parent

    if not source.is_dir():
        raise SystemExit(f"Source folder not found: {source}")
    out.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)

    timings: dict[str, float] = {}
    t, _ = run_step("scout", [sys.executable, str(scripts_dir / "acg-scout.py"), "--source", str(source), "--out", str(out)])
    timings["scout"] = t

    signature = repo_signature(source)
    signature_path = cache / "topology.sha256"
    graph_outputs_exist = (
        (artifacts / "import_graph.json").is_file()
        and (artifacts / "cluster_map.md").is_file()
        and (artifacts / "surface_summaries.md").is_file()
    )
    cache_hit = graph_outputs_exist and signature_path.is_file() and signature_path.read_text(encoding="utf-8").strip() == signature and not args.force_topology

    if cache_hit:
        timings["import_graph"] = 0.0
        print("ACG v0.4 import graph cache hit")
    else:
        t, _ = run_step("import_graph", [sys.executable, str(scripts_dir / "acg-import-graph.py"), "--source", str(source), "--out", str(artifacts)])
        timings["import_graph"] = t
        signature_path.write_text(signature + "\n", encoding="utf-8")

    if args.skip_lexical_index:
        timings["lexical_index"] = 0.0
    else:
        t, _ = run_step("lexical_index", [sys.executable, str(scripts_dir / "acg-lexical-index.py"), "build", "--source", str(source), "--out", str(artifacts)])
        timings["lexical_index"] = t

    started = time.perf_counter()
    payload = build_context_payload(source, out, args.model_budget_tokens)
    write_json(artifacts / "context_payload.json", payload)
    timings["context_payload"] = time.perf_counter() - started

    indexed_code_files = count_code_files(source)
    patch_package_boundary(out, source)
    patch_v04_context_notes(out)
    write_performance_report(artifacts / "performance_report.md", timings, source, out, cache_hit, indexed_code_files)

    print(f"ACG v0.4 complete: {out}")
    print(f"Master file: {out / 'ACG_MASTER.md'}")
    print(f"Execution brief: {artifacts / 'execution_brief.md'}")
    print(f"Completion checklist: {artifacts / 'completion_checklist.md'}")
    print(f"Context payload: {artifacts / 'context_payload.json'}")
    print(f"Performance report: {artifacts / 'performance_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
