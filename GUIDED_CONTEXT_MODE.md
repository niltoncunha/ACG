# ACG Guided Context Mode

Guided Context Mode is the user-facing layer that turns vague human intent into safe AI navigation through a large codebase, agent workspace, documentation bundle or corpus-style folder.

It should not depend on the user knowing how to prepare a file bundle manually.

The user may start with:

```txt
I have this folder. Help me organize it for AI work.
```

ACG converts that into:

```txt
full structural inventory
ownership classification
project_kind classification
folder family classification
hotpath scoring
topology artifacts when PROJECT_OWNED code exists
readiness_subscores
readiness_gate
scout_regime
environment/enforcement_level
phase queues
phase1_reading_order
citation_check
phase packs
execution brief
human approval points
```

---

## Current command

Recommended v0.4-beta entrypoint:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Fast first run:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg --skip-lexical-index
```

Direct Scout run:

```bash
python scripts/acg-scout.py --source /path/to/project --out .acg
```

---

## Goal

Convert a large folder into a controlled context system:

- `ACG_MASTER.md` — single AI entrypoint;
- `context_manifest.jsonl` — all indexed files with metadata and strategy;
- `scout_report.json` — compact machine-readable run summary;
- `structure_map.md` — human-readable map of folder shape, ownership, regime and gates;
- `cluster_map.md` — topology map when code exists;
- `surface_summaries.md` — allowed summaries of high-weight code surfaces;
- `hotpaths.json` — highest-value files by score;
- `phase1_queue.md` — first allowed reading queue;
- `phase1_reading_order.md` — exact order for Phase 1 reading;
- `citation_check.md` — required proof-of-reading prompts;
- `phase2_queue.md` — next safe candidates, not opened until approved;
- `approval_required.md` — files requiring explicit human approval;
- `search_targets.md` — large, terminal, reference, dataset or external assets for targeted search only;
- `phase1_pack/` — copied files for first AI orientation;
- `execution_brief.md` — instructions the AI must follow;
- `next_prompt.md` — automatic continuation protocol;
- `phase2_plan_template.md` — strict NEXT format;
- `context_payload.json` — optional compact handoff format.

The phase pack is not the analysis.

The structure map plus queues plus reading order plus citation checks are the operating map.

---

## Why this matters

A plain manifest with only relative paths is not enough.

The AI may see:

```txt
00_core/README.md
```

but fail to understand whether it is an entrypoint, support file, terminal asset, runtime artifact, external reference, dataset file or risky historical artifact.

ACG therefore preserves:

```txt
relative_path
absolute_path
ownership_class
included_in_import_graph
project_kind
folder_family
role
hotpath_score
risk_score
in_degree
out_degree
topology_score
strategy
allowed_to_open
requires_human_approval
```

and explains how each file should be handled.

---

## Guided flow

```txt
[00] Human vague intent
       ↓
[01] ACG scans the full source folder
       ↓
[02] ACG classifies ownership
       ↓
[03] ACG classifies project_kind
       ↓
[04] ACG classifies folder families
       ↓
[05] ACG scores hotpaths and risks
       ↓
[06] ACG builds topology/surfaces when PROJECT_OWNED code exists
       ↓
[07] ACG calculates readiness_subscores and readiness_gate
       ↓
[08] ACG writes ACG_MASTER.md
       ↓
[09] AI opens ACG_MASTER.md only
       ↓
[10] AI reads required artifacts
       ↓
[11] AI follows phase1_reading_order.md
       ↓
[12] AI reads only phase1_pack/ in that order
       ↓
[13] AI answers citation_check.md
       ↓
[14] AI returns SCOPE / CITATION_CHECK / RISKS / QUESTIONS / NEXT
       ↓
[15] Human approves, rejects or clarifies Phase 2
```

---

## Required AI read order

The generated package instructs the AI to read:

```txt
.acg/ACG_MASTER.md
.acg/artifacts/execution_brief.md
.acg/artifacts/phase1_reading_order.md
.acg/artifacts/citation_check.md
.acg/artifacts/next_prompt.md
.acg/artifacts/phase2_plan_template.md
.acg/artifacts/structure_map.md
.acg/artifacts/phase1_queue.md
.acg/artifacts/phase2_queue.md
.acg/artifacts/approval_required.md
.acg/artifacts/search_targets.md
.acg/phase1_pack/    # only files listed for Phase 1, in order
```

The user should not need to copy/paste `next_prompt.md`. The AI must apply it automatically after Phase 1.

---

## Required Phase 1 output

The AI should return:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files you actually read, in order
CITATION_CHECK: one answer per required citation check
RISKS: key risks before deeper processing
QUESTIONS: objective questions or approval requests only
NEXT: Phase 2 plan or up to 3 clarification questions
```

If `CITATION_CHECK` is missing, Phase 1 should be treated as incomplete.

---

## Package kinds

ACG supports:

```txt
CODEBASE
AGENT_WORKSPACE
DOCUMENTATION_BUNDLE
MIXED_REPO
DATASET_OR_CORPUS
TOOL_RUNTIME
UNKNOWN
```

This matters because a classic codebase and an agent workspace do not have the same readiness requirements.

A codebase needs executable/control evidence.

An agent workspace needs orientation entrypoints and structural contracts.

A corpus needs manifests, schemas, metadata and search-only discipline.

A runtime/tooling folder should not silently pass as a target project.

---

## Core rule

The AI should not be asked to read everything.

It should receive:

```txt
Open .acg/ACG_MASTER.md first and follow it exactly.
```

Everything else is derived from the generated ACG package.

---

## Public safety

Generated prompts should remind the AI:

```txt
Use internal file names only for private analysis.
For public summaries, replace internal names with generic labels.
```

---

## Status

Guided Context Mode is the bridge between:

```txt
human vague intent
```

and:

```txt
safe AI execution over large folders
```

It exists to make ACG usable for non-experts without forcing them to manually create manifests, copy files, design reading phases, or know how to distinguish a codebase from a runtime bundle or corpus.
