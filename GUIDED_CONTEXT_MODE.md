# ACG Guided Context Mode

Guided Context Mode is the user-facing layer that turns vague human intent into safe AI navigation through a large codebase.

It should not depend on the user knowing how to prepare a file bundle manually.

The user may start with:

```txt
I have this folder. Help me organize it for AI work.
```

ACG must convert that into:

```txt
full structural inventory
folder family classification
hotpath scoring
reading queues
phase packs
execution brief
human approval points
```

---

## Goal

Convert a large folder into a controlled context system:

- `context_manifest.jsonl` — all indexed files with metadata and strategy;
- `structure_map.md` — human-readable map of the codebase shape;
- `hotpaths.json` — highest-value files by score;
- `reading_queues.json` — ordered reading queues;
- `search_targets.md` — large or terminal assets for targeted search only;
- `phase1_pack/` — copied files for first AI orientation;
- `execution_brief.md` — instructions the AI must follow.

The phase pack is not the analysis.

The structure map is the main artifact.

---

## Why this matters

A plain manifest with only relative paths is not enough.

The AI may see:

```txt
00_core/README.md
```

but fail to open it because the real file lives elsewhere.

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
```

and explains how each file should be handled.

---

## Manifest v0.3 fields

Each file is represented with fields like:

```json
{
  "relative_path": "src/auth/index.ts",
  "absolute_path": "E:/project/src/auth/index.ts",
  "size": 1420,
  "modified": "2026-05-16T11:29:03Z",
  "extension": ".ts",
  "depth": 2,
  "folder_family": "core",
  "family_tier": "priority",
  "role": "source_code",
  "hotpath_score": 87,
  "risk_score": 12,
  "strategy": "open_now",
  "allowed_to_open": true,
  "allowed_to_edit": false,
  "requires_human_approval": false,
  "public_safe": false
}
```

---

## Strategies

| Strategy | Meaning |
|---|---|
| `open_now` | Safe and important enough for early reading. |
| `open_later` | Useful, but not first. |
| `search_only` | Do not open fully; use targeted search. |
| `index_only` | Keep in inventory, but do not read by default. |
| `human_only` | Requires explicit human approval. |
| `terminal_asset` | Large/historical/reference asset; never read blindly. |
| `ignore` | Generated/cache/noise. |

---

## Guided flow

```txt
[00] Human vague intent
       ↓
[01] ACG derives/asks for task contract
       ↓
[02] ACG scans the full source folder
       ↓
[03] ACG classifies folder families
       ↓
[04] ACG scores hotpaths and risks
       ↓
[05] ACG writes structure_map.md
       ↓
[06] ACG writes reading_queues.json
       ↓
[07] ACG creates phase1_pack/
       ↓
[08] ACG writes execution_brief.md
       ↓
[09] AI reads only the allowed pack/brief
       ↓
[10] AI returns orientation + questions
       ↓
[11] Human approves next phase
```

---

## Command

```bash
python3 scripts/acg-scout.py --source /path/to/project --out .acg
```

Windows:

```powershell
python scripts\acg-scout.py --source "E:\path\to\project" --out ".acg"
```

---

## Core rule

The AI should not be asked to read everything.

It should receive:

```txt
structure_map.md
reading_queues.json
execution_brief.md
phase1_pack/
```

and then proceed one phase at a time.

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
