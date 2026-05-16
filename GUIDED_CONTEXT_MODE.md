# ACG Guided Context Mode

ACG should not depend on users knowing how to prepare a large file bundle for an AI.

The user usually starts with a vague intent:

```txt
I want the AI to organize this project.
```

That is not enough.

Guided Context Mode turns vague intent into a controlled context package.

## Goal

Convert a large folder into:

- an intelligent context manifest;
- a phase 1 reading pack;
- an AI handoff prompt;
- explicit open/search/ignore strategies;
- human questions before deeper processing.

## Why this matters

A plain manifest with only relative paths is not enough.

The AI may see:

```txt
00_core/README.md
```

but fail to open it because the real file lives elsewhere.

ACG must therefore preserve both:

```txt
relative_path
absolute_path
```

and also explain how each file should be handled.

## Context Manifest v2

Each file should be represented with fields like:

```json
{
  "relative_path": "00_core/README.md",
  "absolute_path": "E:/repo/00_core/README.md",
  "size": 362,
  "modified": "2026-05-16T11:29:03Z",
  "extension": ".md",
  "role": "orientation",
  "phase": "phase1",
  "strategy": "open",
  "risk": "low",
  "allowed_to_open": true,
  "allowed_to_edit": false,
  "requires_human_approval": false,
  "public_safe": false
}
```

## Strategies

| Strategy | Meaning |
|---|---|
| `open` | Safe to open directly in this phase. |
| `search_only` | Too large or too dense; use targeted search only. |
| `ignore` | Not useful for this task. |
| `human_only` | Sensitive; human approval required. |
| `terminal_asset` | Reference data, export, log, archive or large file. |

## Guided flow

```txt
[00] Human vague intent
       ↓
[01] ACG asks/derives task contract
       ↓
[02] ACG scans source folder
       ↓
[03] ACG writes context_manifest.jsonl
       ↓
[04] ACG creates Phase 1 Pack with real files
       ↓
[05] ACG writes AI handoff prompt
       ↓
[06] AI reads only the pack
       ↓
[07] AI returns orientation report
       ↓
[08] Human approves Phase 2
```

## Core rule

The AI should not be asked to read everything.

It should receive:

```txt
manifest + phase pack + handoff prompt
```

and then proceed one phase at a time.

## Public safety

Generated prompts should remind the AI:

```txt
Use internal file names only for private analysis.
For public summaries, replace internal names with generic labels.
```

## Status

Guided Context Mode is the missing bridge between:

```txt
human vague intent
```

and:

```txt
safe AI execution
```

It is the user-facing layer that makes ACG usable for non-experts.
