# ACG Structure Scout

**Agentic Code Guidance** for large codebases.

ACG is a guidance and enforcement package for AI-assisted software work.

It exists because the first failure often happens before code is written: the user gives the AI a vague mission, too many files, no reading order, no scope, and no external gate.

ACG turns vague human intent into scoped, verifiable AI work.

It does not replace the developer, reviewer, or CI system. It gives the user and the AI a controlled path through a large codebase.

```txt
vague request
  -> guided task contract
  -> full structural inventory
  -> hotpath scoring
  -> reading queues
  -> scoped AI work
  -> external verify
  -> evidence gate
```

---

## Why this exists

The original failure case is simple:

```txt
"I asked an AI to refactor a large codebase. It spent a long time, burned huge context, and broke the app."
```

The likely failure is not only that the model wrote bad code.

The workflow was wrong:

- the user gave a broad mission;
- the AI opened too much too early;
- there was no full structural map;
- there was no stable reading chain;
- there was no scoped execution path;
- verification depended too much on the AI's own report;
- promotion had no hard evidence gate.

ACG exists to reduce that failure mode.

---

## Core idea

ACG does not solve large codebases by reading every file.

ACG first builds a structural map of the whole codebase:

```txt
all files
  -> folder families
  -> hotpaths
  -> terminal assets
  -> human-only zones
  -> reading queues
  -> controlled phase packs
```

Then the AI reads only the right subset, in the right order, with explicit limits.

---

## What ACG does first

ACG should not start by asking the AI to code.

It should first guide the user through a minimum task contract:

```txt
1. What do you want changed?
2. Which area may the AI inspect first?
3. Which areas are forbidden or sensitive?
4. What should the AI open first?
5. What should wait?
6. How will we know the work passed?
7. What evidence is required before promotion?
```

If the request is too vague, ACG should slow the process down.

Bad request:

```txt
Refactor the whole codebase.
```

Better request:

```txt
Map the repository structure first. Then propose a scoped plan for the auth module. Do not edit payments, migrations, infrastructure, secrets, or environment files. Verification must run outside the AI.
```

---

## ACG has three layers

### 1. Guided Task Contract

Turns vague user intent into a minimal operating contract.

It clarifies:

- goal;
- scope;
- sensitive zones;
- expected verification;
- evidence required before promotion.

### 2. Structure Scout

The Scout runs before deep AI work.

It maps the repository or file bundle structurally before asking the model to interpret everything semantically.

It produces:

- full file inventory;
- folder family classification;
- hotpath score per file;
- risk score per file;
- strategy per file: `open_now`, `open_later`, `search_only`, `index_only`, `human_only`, `terminal_asset`, `ignore`;
- `structure_map.md`;
- `hotpaths.json`;
- `reading_queues.json`;
- `search_targets.md`;
- `phase1_pack/`;
- `execution_brief.md`.

The goal is not to read every file. The goal is to understand the shape of the whole codebase before deciding what the AI should read.

### 3. Enforcement Core

The enforcement core runs around the work.

It provides:

- branch check;
- scope check;
- forbidden path check;
- external verification runner;
- `done_when` checks;
- JSONL evidence;
- fail-closed promotion gate;
- GitHub Actions validation.

---

## System control map

```txt
+======================================================================+
|                                  ACG                                 |
|        User Guidance + Structure Scout + Mechanical Enforcement       |
+======================================================================+

  VAGUE HUMAN INTENT
              |
              v
      [00] GUIDED TASK CONTRACT
              |
              v
      [01] FULL FILE INVENTORY
              |
              v
      [02] FOLDER FAMILY CLASSIFICATION
              |
              v
      [03] HOTPATH + RISK SCORING
              |
              v
      [04] STRUCTURE MAP
              |
              v
      [05] READING QUEUES
              |
              v
      [06] CONTROLLED PHASE PACKS
              |
              v
      [07] EXECUTION BRIEF FOR THE AI
              |
              v
      [08] SCOPED AGENT WORK
              |
              v
      [09] EXTERNAL VERIFY + EVIDENCE
              |
              v
      [10] FAIL-CLOSED PROMOTION GATE

+======================================================================+
|  The AI does the work. ACG maps the codebase, guides the request,     |
|  limits scope, requires evidence, and blocks unsafe promotion.         |
+======================================================================+
```

---

## Structure Scout v0.3

Run:

```bash
python3 scripts/acg-scout.py --source /path/to/project --out .acg
```

On Windows:

```powershell
python scripts\acg-scout.py --source "E:\path\to\project" --out ".acg"
```

Generated output:

```txt
.acg/
  context_manifest.jsonl
  structure_map.md
  hotpaths.json
  reading_queues.json
  search_targets.md
  execution_brief.md
  phase1_pack/
```

The primary artifact is:

```txt
.acg/structure_map.md
```

The `phase1_pack/` is only a controlled reading subset derived from the full structural map. It is not the whole analysis.

---

## Enforcement rules

The enforcement core keeps four hard rules:

| Rule | Purpose |
|---|---|
| Isolated branch | Avoid direct mutation of the default branch. |
| Technical scope fence | Block direct edits outside declared paths. |
| External verification | Do not trust agent self-reports as proof. |
| Fail-closed promotion | Missing or failed evidence blocks promotion. |

---

## What ACG protects against

- vague requests turning into uncontrolled AI work;
- reading too many files too early;
- losing the structural chain of a codebase;
- treating a tiny sample as if it represented the whole codebase;
- direct edits outside declared scope;
- edits to forbidden paths;
- agentic work on the default branch;
- promotion without configured verification;
- treating agent self-report as proof;
- missing minimum audit evidence.

## What ACG does not protect against

- weak or flaky test suites;
- semantic drift in untested behavior;
- bad product or architecture decisions;
- unsafe migrations;
- security bugs not covered by verification;
- side effects caused by executed code;
- humans bypassing CI or branch protection.

See [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md).

---

## Claim

ACG does not make AI-generated code correct.

ACG makes large-codebase AI work structurally mapped, guided, scoped, evidenced, and harder to promote when it goes wrong.

---

## License

Free and open source under the MIT License.

Copyright 2026 Nilton Cunha.
