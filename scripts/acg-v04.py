#!/usr/bin/env python3
"""ACG v0.4-alpha orchestrator.

Single-command alpha flow for topology-aware context generation.

This keeps v0.3 stable while making v0.4 operational:
- runs acg-scout.py
- runs acg-import-graph.py with a simple cache key
- runs acg-lexical-index.py optionally
- exposes v0.4 artifacts in ACG_MASTER.md and execution_brief.md
- writes context_payload.json
- writes performance_report.md

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
TEXT_EXTENSIONS = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "coverage"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def sanitize_text(text: str) -> str:
    """Remove NUL/control chars that poison JSON payloads while keeping whitespace."""
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


def read_text_safe(path: Path, max_bytes: int = 100_000) -> str:
    if not path.is_file():
        return ""
    data = path.read_bytes()[:max_bytes]
    return sanitize_text(data.decode("utf-8", errors="ignore"))


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def queue_count(queues: dict, key: str) -> int:
    value = queues.get(key, [])
    return len(value) if isinstance(value, list) else 0


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
        "schema": "acg.context_payload.v0.4-alpha",
        "generated": now(),
        "source": str(source),
        "model_budget_tokens": model_budget_tokens,
        "budget_policy": {
            "note": "This is a lightweight payload. It is not a full RAG system.",
            "phase1_full_files": len(phase1_items),
            "topological_hubs": len(hubs),
        },
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


def write_v04_master(out: Path, source: Path, queues: dict, indexed_code_files: int) -> None:
    phase1 = queue_count(queues, "phase1")
    phase2 = queue_count(queues, "phase2")
    approval = queue_count(queues, "approval_required")
    search_targets = queue_count(queues, "search_targets")
    human_only = queue_count(queues, "human_only")
    ignored = queue_count(queues, "ignored")
    total = phase1 + phase2 + approval + search_targets + human_only + ignored

    lines = [
        "# ACG Master Context File",
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
        "  cache/",
        "    topology.sha256",
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
        "    import_graph.json",
        "    cluster_map.md",
        "    surface_summaries.md",
        "    context_payload.json",
        "    performance_report.md",
        "```",
        "",
        "## Source",
        "",
        f"`{source}`",
        "",
        "## Inventory Summary",
        "",
        f"- Total queued/indexed files: {total}",
        f"- Phase 1 files: {phase1}",
        f"- Safe Phase 2 candidates: {phase2}",
        f"- Approval-required candidates: {approval}",
        f"- Search-only / terminal assets: {search_targets}",
        f"- Human-only files: {human_only}",
        f"- Ignored files: {ignored}",
        f"- Indexed code files for topology: {indexed_code_files}",
        "",
        "## What the human does",
        "",
        "The human does not need to invent follow-up prompts or copy/paste `next_prompt.md`.",
        "The human gives the AI this file, then approves, rejects, or clarifies the AI's bounded NEXT block.",
        "",
        "## v0.4 Topology Artifacts",
        "",
        "- `artifacts/cluster_map.md`: read before planning Phase 2. It is the human-readable topology layer.",
        "- `artifacts/surface_summaries.md`: read before planning Phase 2. It is allowed summary content for high-weight code surfaces.",
        "- `artifacts/context_payload.json`: optional structured payload mode. Use it instead of manual file loading only when the caller asks for payload mode or context compaction.",
        "- `artifacts/import_graph.json`: machine-readable topology. Do not read fully by default; use only for diagnostics or tool processing.",
        "- `artifacts/performance_report.md`: diagnostics only. Read it when validating v0.4 runtime cost.",
        "",
        "Surface summaries are allowed context. The original files summarized there keep their original queue status and may still be `search_only` or approval-gated.",
        "",
        "## Read Order for AI",
        "",
        "1. Read this file: `ACG_MASTER.md`.",
        "2. Read `artifacts/execution_brief.md`.",
        "3. Read `artifacts/next_prompt.md` before Phase 1; it is the automatic continuation protocol.",
        "4. Read `artifacts/phase2_plan_template.md`; it is the required NEXT output contract.",
        "5. Read `artifacts/structure_map.md` for the structural overview.",
        "6. Read `artifacts/cluster_map.md` for v0.4 topology.",
        "7. Read `artifacts/surface_summaries.md` for allowed code-surface summaries.",
        "8. Read `artifacts/phase1_queue.md` and `artifacts/phase2_queue.md` for human-readable queues.",
        "9. Read `artifacts/approval_required.md` and `artifacts/search_targets.md` to understand what must not be opened directly.",
        "10. Read only files copied inside `phase1_pack/`.",
        "11. Return the Phase 1 confirmation plus a fully formed NEXT block. Do not wait for the human to paste another prompt.",
        "",
        "## Optional Payload Mode",
        "",
        "If the user asks for compact context, payload mode, or single-file handoff, read `artifacts/context_payload.json`.",
        "Otherwise, do not duplicate Phase 1 by reading both `context_payload.json` and all files in `phase1_pack/` unless explicitly useful.",
        "",
        "## Do Not Do",
        "",
        "- Do not read the original source folder blindly.",
        "- Do not open terminal assets directly.",
        "- Do not treat `... N more` summaries as complete lists.",
        "- Do not depend on reading full JSON manually when a compact `.md` queue exists.",
        "- Do not read `import_graph.json` fully unless topology diagnostics are needed.",
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
    (out / "ACG_MASTER.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_v04_execution_brief(out: Path) -> None:
    artifacts = out / "artifacts"
    queues = load_json(artifacts / "reading_queues.json")
    phase1 = queues.get("phase1", [])
    phase2 = queues.get("phase2", [])
    search_targets = queues.get("search_targets", [])

    lines = [
        "# ACG Execution Brief",
        "",
        "You are operating under ACG Structure Scout v0.4-alpha.",
        "",
        "Read `../ACG_MASTER.md` first. It is the only root-level instruction file.",
        "Read `next_prompt.md` before Phase 1. It is your continuation protocol after Phase 1.",
        "Read `phase2_plan_template.md` before Phase 1. It defines the required NEXT format.",
        "Read `cluster_map.md` and `surface_summaries.md` before planning Phase 2.",
        "Use `phase1_queue.md` and `phase2_queue.md` for conversational planning; do not depend on reading the full JSON manually.",
        "Do not read the entire source folder. Read only the Phase 1 pack first.",
        "Do not edit files. This is orientation only.",
        "Do not claim final understanding. Return uncertainties explicitly.",
        "The human should not need to copy/paste a second prompt. You must apply `next_prompt.md` automatically after Phase 1.",
        "",
        "## Required artifacts to inspect first",
        "",
        "- `../ACG_MASTER.md`",
        "- `execution_brief.md`",
        "- `next_prompt.md`",
        "- `phase2_plan_template.md`",
        "- `structure_map.md`",
        "- `cluster_map.md`",
        "- `surface_summaries.md`",
        "- `phase1_queue.md`",
        "- `phase2_queue.md`",
        "- `approval_required.md`",
        "- `search_targets.md`",
        "- `../phase1_pack/`",
        "",
        "## Optional v0.4 diagnostics",
        "",
        "- `performance_report.md`: read only when checking runtime cost.",
        "- `context_payload.json`: read only in payload mode or compact handoff mode.",
        "- `import_graph.json`: machine-readable; do not read fully by default.",
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
        "",
        "## Required Phase 1 Output",
        "",
        "After Phase 1, reply with:",
        "",
        "```txt",
        "ACG-UNDERSTOOD: structure-scout",
        "SCOPE: files you actually read",
        "RISKS: key risks before deeper processing",
        "QUESTIONS: objective questions or approval requests only",
        "NEXT: Phase 2 plan or up to 3 clarification questions, following next_prompt.md and phase2_plan_template.md",
        "```",
    ]
    (artifacts / "execution_brief.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def patch_next_prompt_for_v04(out: Path) -> None:
    path = out / "artifacts" / "next_prompt.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    marker = "## v0.4 Planning Context"
    if marker in text:
        return
    insert = (
        "\n"
        "## v0.4 Planning Context\n\n"
        "Before proposing Phase 2, consider `cluster_map.md` and `surface_summaries.md` if available.\n"
        "Do not request original code files only because they appear in surface summaries. Surface summaries are allowed context; original files keep their queue status.\n"
        "Do not read `import_graph.json` fully unless topology diagnostics are explicitly required.\n"
        "Use `context_payload.json` only in payload mode or compact handoff mode.\n"
    )
    if "## Required NEXT block" in text:
        text = text.replace("## Required NEXT block", insert + "\n## Required NEXT block")
    else:
        text += insert
    path.write_text(text, encoding="utf-8")


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


def count_code_files(source: Path) -> int:
    total = 0
    for path in source.rglob("*"):
        if should_skip(path) or not path.is_file() or path.suffix.lower() not in CODE_EXTENSIONS:
            continue
        total += 1
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG v0.4-alpha orchestrator")
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
    (artifacts / "context_payload.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    timings["context_payload"] = time.perf_counter() - started

    indexed_code_files = count_code_files(source)

    queues = load_json(artifacts / "reading_queues.json")
    write_v04_master(out, source, queues, indexed_code_files)
    write_v04_execution_brief(out)
    patch_next_prompt_for_v04(out)

    write_performance_report(artifacts / "performance_report.md", timings, source, out, cache_hit, indexed_code_files)

    print(f"ACG v0.4 complete: {out}")
    print(f"Master file: {out / 'ACG_MASTER.md'}")
    print(f"Execution brief: {artifacts / 'execution_brief.md'}")
    print(f"Context payload: {artifacts / 'context_payload.json'}")
    print(f"Performance report: {artifacts / 'performance_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
