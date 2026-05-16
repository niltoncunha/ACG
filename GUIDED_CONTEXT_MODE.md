# ACG Guided Context Mode

Guided Context Mode is the user-facing layer that turns vague human intent into safe AI navigation through a large codebase.

It should not depend on the user knowing how to prepare a file bundle manually.

The user may start with:

```txt
I have this folder. Help me organize it for AI work.
```

ACG converts that into:

```txt
full structural inventory
folder family classification
hotpath scoring
phase queues
topology artifacts when code exists
surface summaries
phase packs
execution brief
human approval points
```

---

## Current command

Recommended v0.4-alpha entrypoint:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Fast first run:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg --skip-lexical-index
```

---

## Goal

Convert a large folder into a controlled context system:

- `ACG_MASTER.md` — single AI entrypoint;
- `context_manifest.jsonl` — all indexed files with metadata and strategy;
- `structure_map.md` — human-readable map of the repository shape;
- `cluster_map.md` — topology map when code exists;
- `surface_summaries.md` — allowed summaries of high-weight code surfaces;
- `hotpaths.json` — highest-value files by score;
- `phase1_queue.md` — first allowed reading queue;
- `phase2_queue.md` — next safe candidates, not opened until approved;
- `approval_required.md` — files requiring explicit human approval;
- `search_targets.md` — large or terminal assets for targeted search only;
- `phase1_pack/` — copied files for first AI orientation;
- `execution_brief.md` — instructions the AI must follow;
- `next_prompt.md` — automatic continuation protocol;
- `phase2_plan_template.md` — strict NEXT format;
- `context_payload.json` — optional compact handoff format.

The phase pack is not the analysis.

The structure map plus queues plus topology artifacts are the operating map.

---

## Why this matters

A plain manifest with only relative paths is not enough.

The AI may see:

```txt
00_core/README.md
```

but fail to understand whether it is an entrypoint, support file, terminal asset, or risky historical artifact.

ACG therefore preserves:

```txt
relative_path
absolute_path
size
extension
folder_family
hotpath_score
risk_score
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
[02] ACG classifies folder families
       ↓
[03] ACG scores hotpaths and risks
       ↓
[04] ACG builds topology/surfaces when code exists
       ↓
[05] ACG writes ACG_MASTER.md
       ↓
[06] AI opens ACG_MASTER.md only
       ↓
[07] AI reads required artifacts
       ↓
[08] AI reads only phase1_pack/
       ↓
[09] AI returns SCOPE/RISKS/QUESTIONS/NEXT
       ↓
[10] Human approves or rejects Phase 2
```

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
safe AI execution over large codebases
```

It exists to make ACG usable for non-experts without forcing them to manually create manifests, copy files, or design reading phases.
