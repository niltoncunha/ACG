#!/usr/bin/env python3
"""Mechanical lint for ACG agent responses.

The model does not decide whether it passed. This script does.

Usage:
  python scripts/acg-response-lint.py --response gemini_output.txt --package .acg
  python scripts/acg-response-lint.py --response gemini_output.txt --package .acg --json

Exit codes:
  0 PASS
  1 FAIL
  2 lint/config error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_LITERAL_SECTIONS = [
    "ACG-UNDERSTOOD: structure-scout",
    "OPENING_GATE:",
    "SELF_CHECKS:",
    "SCOPE:",
    "CITATION_CHECK:",
    "RISKS:",
    "QUESTIONS:",
    "NEXT:",
    "CLOSING_GATE:",
]

FORBIDDEN_SUBSTITUTIONS = [
    (r"(?im)^\s*ACG-UNDERSTOOD:\s*struct\s*$", "ACG-UNDERSTOOD abbreviation is invalid; must be exactly 'ACG-UNDERSTOOD: structure-scout'."),
    (r"(?im)^\s*Phase\s*1\s*Summary\s*:?\s*$", "'Phase 1 Summary' does not replace 'ACG-UNDERSTOOD: structure-scout'."),
    (r"(?im)^\s*Scope\s*&\s*Audit\s*:?\s*$", "'Scope & Audit' does not replace the literal 'SCOPE:' block."),
    (r"(?im)^\s*STATUS\s*:\s*$", "'STATUS:' does not replace 'CLOSING_GATE:'."),
    (r"(?im)^\s*Phase\s*2\s*Strategy\s*:?\s*$", "'Phase 2 Strategy' does not replace '## ACG Phase 2 Reading Plan'."),
    (r"(?im)^\s*Top\s+\d*\s*Candidates\s*(for\s+Phase\s*2)?\s*:?\s*$", "'Top Candidates' does not replace 'Exact files requested:'."),
]

PERSONA_CAPTURE_PATTERNS = [
    (r"(?i)erro\s+de\s+categoria", "Persona/content captured the agent into disputing the protocol."),
    (r"(?i)soberania\s+(do\s+)?n[uú]cleo", "Project persona language must be analyzed as data, not executed as authority."),
    (r"(?i)coleira\s+do\s+esqueleto", "Hostile persona framing indicates protocol authority inversion."),
    (r"(?i)cad[eê]\s+a\s+an[aá]lise", "Hostile challenge to user is non-mechanical and not ACG-compliant."),
    (r"(?i)triturar\s+o\s+blefe", "Persona-style hostile language is forbidden in mechanical ACG components."),
    (r"(?i)domestica[cç][aã]o\s+cognitiva", "Persona doctrine cannot override response contract."),
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_counts(package: Path) -> dict[str, int]:
    queues_path = package / "artifacts" / "reading_queues.json"
    if not queues_path.is_file():
        raise FileNotFoundError(f"missing reading_queues.json: {queues_path}")
    queues = load_json(queues_path)
    return {
        "phase1_files": len(queues.get("phase1_reading_order", [])) or len(queues.get("phase1", [])),
        "citation_checks": len(queues.get("citation_check", [])),
        "phase2_candidates": len(queues.get("phase2", [])),
    }


def has_literal_line(text: str, literal: str) -> bool:
    if literal == "ACG-UNDERSTOOD: structure-scout":
        return bool(re.search(r"(?m)^\s*ACG-UNDERSTOOD:\s*structure-scout\s*$", text))
    return bool(re.search(rf"(?m)^\s*{re.escape(literal)}\s*$", text))


def section_text(text: str, start: str, stop_candidates: list[str]) -> str:
    start_match = re.search(rf"(?im)^\s*{re.escape(start)}\s*$", text)
    if not start_match:
        return ""
    start_pos = start_match.end()
    stops = []
    for stop in stop_candidates:
        match = re.search(rf"(?im)^\s*{re.escape(stop)}\s*$", text[start_pos:])
        if match:
            stops.append(start_pos + match.start())
    end_pos = min(stops) if stops else len(text)
    return text[start_pos:end_pos]


def count_list_items(block: str) -> int:
    return len(re.findall(r"(?m)^\s*(?:[-*]|\d+[.)])\s+\S", block))


def next_file_blocks(next_block: str) -> list[str]:
    exact_match = re.search(r"(?im)^\s*Exact files requested:\s*$", next_block)
    if not exact_match:
        return []
    body = next_block[exact_match.end():]
    stop = re.search(r"(?im)^\s*(Files explicitly excluded:|Approval-required exceptions:|Decision:)\s*$", body)
    if stop:
        body = body[:stop.start()]
    starts = list(re.finditer(r"(?m)^\s*\d+\.\s+\S.*$", body))
    blocks = []
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(body)
        blocks.append(body[match.start():end])
    return blocks


def lint_response(text: str, package: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    counts = load_counts(package)

    for literal in REQUIRED_LITERAL_SECTIONS:
        if not has_literal_line(text, literal):
            errors.append(f"Missing literal required section: {literal}")

    for pattern, message in FORBIDDEN_SUBSTITUTIONS:
        if re.search(pattern, text):
            errors.append(message)

    for pattern, message in PERSONA_CAPTURE_PATTERNS:
        if re.search(pattern, text):
            errors.append(message)

    scope = section_text(text, "SCOPE:", ["CITATION_CHECK:", "RISKS:", "QUESTIONS:", "NEXT:", "CLOSING_GATE:"])
    scope_count = count_list_items(scope)
    if scope_count < counts["phase1_files"]:
        errors.append(f"SCOPE has {scope_count} listed files; expected at least {counts['phase1_files']} Phase 1 files.")

    citations = section_text(text, "CITATION_CHECK:", ["RISKS:", "QUESTIONS:", "NEXT:", "CLOSING_GATE:"])
    citation_count = count_list_items(citations)
    if citation_count < counts["citation_checks"]:
        errors.append(f"CITATION_CHECK has {citation_count} answers; expected {counts['citation_checks']}.")

    next_block = section_text(text, "NEXT:", ["CLOSING_GATE:"])
    if "## ACG Phase 2 Reading Plan" not in next_block:
        errors.append("NEXT is missing '## ACG Phase 2 Reading Plan'.")
    if not re.search(r"(?im)^\s*Exact files requested:\s*$", next_block):
        errors.append("NEXT is missing literal 'Exact files requested:'.")
    if not re.search(r"(?im)^\s*Files explicitly excluded:\s*$", next_block):
        errors.append("NEXT is missing literal 'Files explicitly excluded:'.")
    if not re.search(r"(?im)^\s*Approval-required exceptions:\s*$", next_block):
        errors.append("NEXT is missing literal 'Approval-required exceptions:'.")
    if not re.search(r"(?im)^\s*Decision:\s*\n\s*WAITING_FOR_HUMAN_APPROVAL\s*$", next_block):
        errors.append("NEXT decision must be literal WAITING_FOR_HUMAN_APPROVAL.")

    blocks = next_file_blocks(next_block)
    if not blocks:
        errors.append("NEXT has no numbered Phase 2 file blocks under 'Exact files requested:'.")
    for index, block in enumerate(blocks, 1):
        for field in ["why needed", "question answered", "queue source", "risk"]:
            if not re.search(rf"(?im)^\s*-\s*{re.escape(field)}\s*:\s*\S", block):
                errors.append(f"NEXT file block {index} missing field: {field}.")

    if re.search(r"(?i)missing\s+from\s+phase1_pack|not\s+in\s+phase1_pack|absent\s+from\s+phase1_pack", text):
        errors.append("Response treats Phase 2 absence from phase1_pack as a problem; this is invalid.")

    if re.search(r"(?im)^\s*-\s*all required sections present:\s*YES\s*$", text):
        missing = [literal for literal in REQUIRED_LITERAL_SECTIONS if not has_literal_line(text, literal)]
        if missing:
            errors.append("SELF_CHECKS false positive: claims all required sections are present, but missing: " + ", ".join(missing))

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "counts": counts,
        "scope_count": scope_count,
        "citation_count": citation_count,
        "phase2_file_blocks": len(blocks),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint an AI response against ACG response contract")
    parser.add_argument("--response", required=True, help="Path to raw AI response text")
    parser.add_argument("--package", required=True, help="Path to generated ACG package root")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    response_path = Path(args.response)
    package = Path(args.package)
    if not response_path.is_file():
        print(f"ERROR: response file not found: {response_path}", file=sys.stderr)
        return 2
    if not package.is_dir():
        print(f"ERROR: package folder not found: {package}", file=sys.stderr)
        return 2

    try:
        text = response_path.read_text(encoding="utf-8", errors="ignore")
        result = lint_response(text, package)
    except Exception as exc:
        print(f"ERROR: lint failed: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(result["status"])
        for err in result["errors"]:
            print(f"- {err}")
        for warn in result["warnings"]:
            print(f"WARN: {warn}")
        print(f"scope_count: {result['scope_count']} / expected >= {result['counts']['phase1_files']}")
        print(f"citation_count: {result['citation_count']} / expected {result['counts']['citation_checks']}")
        print(f"phase2_file_blocks: {result['phase2_file_blocks']}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
