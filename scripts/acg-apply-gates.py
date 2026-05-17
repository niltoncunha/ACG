#!/usr/bin/env python3
"""Patch an existing ACG package with strict opening/closing gates.

Usage:
  python scripts/acg-apply-gates.py --source /path/to/source --out /path/to/.acg

This is a v0.4-beta hardening postprocessor. It does not scan the source tree.
It only edits generated ACG artifacts under --out.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def counts(out: Path) -> dict[str, int]:
    queues = load_json(out / "artifacts" / "reading_queues.json")
    return {
        "phase1_files": len(queues.get("phase1_reading_order", [])) or len(queues.get("phase1", [])),
        "citation_checks": len(queues.get("citation_check", [])),
        "phase2_candidates": len(queues.get("phase2", [])),
    }


def boundary(source: Path, out: Path) -> dict[str, object]:
    out = out.resolve()
    return {
        "current_package_root": str(out),
        "acg_master": str((out / "ACG_MASTER.md").resolve()),
        "artifacts_root": str((out / "artifacts").resolve()),
        "phase1_pack_root": str((out / "phase1_pack").resolve()),
        "source_root": str(source.resolve()),
    }


def gate_text(source: Path, out: Path) -> str:
    c = counts(out)
    b = boundary(source, out)
    return f"""## ACG Opening and Closing Gates

These gates are mandatory. They are the most important part of the ACG protocol.

A useful-looking summary is invalid if the gates are skipped.

### Opening Gate

Before reading Phase 1 files, the AI must be able to report:

```txt
OPENING_GATE:
- current_package_root: {b['current_package_root']}
- allowed Phase 1 roots: ACG_MASTER.md, artifacts/, phase1_pack/
- source_root direct reads forbidden during Phase 1: YES
- parent/sibling/alternate generated packages forbidden during Phase 1: YES
- expected Phase 1 files: {c['phase1_files']}
- expected citation checks: {c['citation_checks']}
- Phase 2 queue is metadata only: YES
- Phase 2 files are not expected in phase1_pack: YES
- opening gate status: PASSED
```

If `OPENING_GATE` cannot be satisfied, stop. Do not continue.

### Closing Gate

Before final answer, the AI must verify:

```txt
CLOSING_GATE:
- ACG-UNDERSTOOD present: YES
- SELF_CHECKS present: YES
- SCOPE present and auditable: YES
- SCOPE lists all Phase 1 files actually read, in order: YES
- CITATION_CHECK answered all {c['citation_checks']} required checks: YES
- RISKS are objective: YES
- QUESTIONS are objective approvals/clarifications only: YES
- NEXT uses phase2_plan_template.md exactly: YES
- every requested Phase 2 file has why needed/question answered/queue source/risk: YES
- no Phase 2 file described as missing from phase1_pack: YES
- Decision is WAITING_FOR_HUMAN_APPROVAL: YES
- closing gate status: PASSED
```

If `SCOPE` is missing, Phase 1 is incomplete because the read set cannot be audited.

If any required section is missing, Phase 1 is invalid.

If any step is skipped, the process has already failed the ACG protocol.
"""


def skeleton_text(out: Path) -> str:
    c = counts(out)
    return f"""## Required Final Output Skeleton

The final Phase 1 answer is invalid unless it follows this structure.

```txt
ACG-UNDERSTOOD: structure-scout

OPENING_GATE:
- current_package_root: <path>
- expected Phase 1 files: {c['phase1_files']}
- expected citation checks: {c['citation_checks']}
- Phase 2 queue is metadata only: YES
- Phase 2 files are not expected in phase1_pack: YES
- opening gate status: PASSED

SELF_CHECKS:
MASTER_CHECK:
- current_package_root identified: <path>
- allowed Phase 1 roots are limited to ACG_MASTER.md, artifacts/, and phase1_pack/: YES

PHASE1_ORDER_CHECK:
- expected Phase 1 files: {c['phase1_files']}
- read in listed order: YES

CITATION_CHECK_PLAN:
- expected citation checks: {c['citation_checks']}
- answered all checks: YES

BOUNDARY_CHECK:
- stayed inside current_package_root: YES
- did not inspect source_root directly: YES
- did not search Phase 2 files: YES

NEXT_SELF_CHECK:
- Phase 2 queue is metadata only: YES
- every requested Phase 2 file has 4 fields: YES
- no Phase 2 file called missing from phase1_pack: YES

FINAL_COMPLETION_CHECK:
- required sections present: YES

SCOPE:
- <Phase 1 file 1 actually read>
- <Phase 1 file 2 actually read>
...

CITATION_CHECK:
1. <answer>
2. <answer>
...

RISKS:
- <objective risk>

QUESTIONS:
- <objective approval request or none>

NEXT:
Detected mode: <MAP_ONLY|REFACTOR|BUGFIX|FEATURE|DOCS|TESTS|SECURITY|UNKNOWN>

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

CLOSING_GATE:
- SCOPE present and auditable: YES
- all required sections present: YES
- NEXT template complete: YES
- closing gate status: PASSED
```

`SCOPE` is mandatory because without it there is no auditable record of what the AI claims it read.
"""


def append_once(path: Path, marker: str, text: str) -> None:
    if not path.is_file():
        return
    old = path.read_text(encoding="utf-8")
    if marker in old:
        return
    path.write_text(old.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def patch(source: Path, out: Path) -> None:
    artifacts = out / "artifacts"
    gate = gate_text(source, out)
    skeleton = skeleton_text(out)
    block = gate + "\n" + skeleton

    targets = [
        out / "ACG_MASTER.md",
        artifacts / "execution_brief.md",
        artifacts / "step_checks.md",
        artifacts / "completion_checklist.md",
        artifacts / "next_prompt.md",
        artifacts / "phase2_plan_template.md",
    ]
    for target in targets:
        append_once(target, "## ACG Opening and Closing Gates", block)

    report_path = artifacts / "scout_report.json"
    if report_path.is_file():
        report = load_json(report_path)
        c = counts(out)
        report["opening_closing_gates"] = {
            "opening_gate_required": True,
            "closing_gate_required": True,
            "scope_required_for_audit": True,
            "missing_scope_invalidates_phase1": True,
            "skipped_steps_invalidate_protocol": True,
            "expected_phase1_files": c["phase1_files"],
            "expected_citation_checks": c["citation_checks"],
        }
        write_json(report_path, report)


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply ACG opening/closing gates to a generated package")
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    source = Path(args.source).resolve()
    out = Path(args.out).resolve()
    if not out.is_dir():
        raise SystemExit(f"ACG package not found: {out}")
    if not (out / "artifacts" / "reading_queues.json").is_file():
        raise SystemExit(f"ACG reading_queues.json not found under: {out}")
    patch(source, out)
    print(f"ACG gates applied: {out}")
    print(f"Master file: {out / 'ACG_MASTER.md'}")
    print(f"Step checks: {out / 'artifacts' / 'step_checks.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
