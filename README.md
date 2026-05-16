# ACG Structure Scout

**Agentic Code Guidance** for large codebases.

ACG is a guidance, context-mapping, and enforcement package for AI-assisted software work.

It exists because the first failure often happens before code is written: the user gives the AI a vague mission, too many files, no reading order, no scope, and no external gate.

ACG turns vague human intent into scoped, phased, verifiable AI work.

It does not replace the developer, reviewer, test suite, or CI system. It gives the user and the AI a controlled path through a large codebase.

```txt
vague request
  -> guided task contract
  -> full structural inventory
  -> topology-aware context package
  -> bounded reading plan
  -> scoped AI work
  -> external verify
  -> evidence gate
```

---

## Current status

Recommended entrypoint:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Windows:

```powershell
python scripts\acg-v04.py --source "E:\path\to\project" --out ".acg"
```

For a faster first run without lexical indexing:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg --skip-lexical-index
```

ACG v0.4-alpha keeps the v0.3 Structure Scout stable and adds topology-aware artifacts, compact queues, an optional context payload, and performance reporting.

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

## What ACG generates

Run v0.4-alpha:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Generated package:

```txt
.acg/
  ACG_MASTER.md
  phase1_pack/
  cache/
    topology.sha256
  artifacts/
    context_manifest.jsonl
    structure_map.md
    hotpaths.json
    reading_queues.json
    phase1_queue.md
    phase2_queue.md
    approval_required.md
    search_targets.md
    execution_brief.md
    next_prompt.md
    phase2_plan_template.md
    import_graph.json
    cluster_map.md
    surface_summaries.md
    context_payload.json
    performance_report.md
```

The AI entrypoint is always:

```txt
Open .acg/ACG_MASTER.md first and follow it exactly.
```

The human should not need to invent the next prompt. `ACG_MASTER.md`, `next_prompt.md`, and `phase2_plan_template.md` drive the next bounded step.

---

## Core idea

ACG does not solve large codebases by asking the AI to read every file.

ACG first builds a structural and topological map of the whole codebase:

```txt
all files
  -> folder families
  -> hotpaths
  -> risks
  -> terminal/search-only assets
  -> import graph, when code exists
  -> cluster map
  -> surface summaries
  -> reading queues
  -> controlled phase packs
```

Then the AI reads only the right subset, in the right order, with explicit limits.

---

## Layers

### 1. Guided Task Contract

Turns vague user intent into a minimal operating contract:

- goal;
- scope;
- sensitive zones;
- expected verification;
- evidence required before promotion.

### 2. Structure Scout

Maps the repository before deep semantic work.

It produces:

- full file inventory;
- folder family classification;
- hotpath score per file;
- risk score per file;
- strategy per file: `open_now`, `open_later`, `search_only`, `index_only`, `human_only`, `terminal_asset`, `ignore`;
- compact phase queues;
- search-only targets;
- controlled Phase 1 pack;
- generated AI instructions.

### 3. Topology Layer v0.4-alpha

Adds code topology when code files exist:

- static import graph;
- in-degree / out-degree;
- architectural hub view;
- surface summaries for high-weight code files;
- lightweight context payload;
- performance report and topology cache.

If the folder is mostly documentation, the topological layer will be small. That is expected.

### 4. Enforcement Core

Runs around the work:

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
|     User Guidance + Structure Scout + Topology + Evidence Gate        |
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
      [04] TOPOLOGY + SURFACE SUMMARIES
              |
              v
      [05] STRUCTURE MAP + CLUSTER MAP
              |
              v
      [06] READING QUEUES
              |
              v
      [07] CONTROLLED PHASE PACKS
              |
              v
      [08] EXECUTION BRIEF FOR THE AI
              |
              v
      [09] SCOPED AGENT WORK
              |
              v
      [10] EXTERNAL VERIFY + EVIDENCE
              |
              v
      [11] FAIL-CLOSED PROMOTION GATE
```

---

## Enforcement rules

The enforcement core keeps four hard rules:

| Rule | Purpose |
|---|---|
| Isolated branch | Avoid direct mutation of the default branch. |
| Technical scope fence | Block direct edits outside declared paths. |
| External verification | Do not trust agent self-reports as proof. |
| Fail-closed promotion | Missing or failed evidence blocks promotion. |

Run enforcement directly:

```bash
python scripts/acg-enforce.py --config acg.yaml --mode all
```

---

## Important limitation

ACG has two different kinds of control:

| Layer | Type |
|---|---|
| `ACG_MASTER.md`, queues, prompts | cooperative guidance |
| `acg-enforce.py`, CI, branch/scope checks | mechanical enforcement |
| `acg-gateway.py` | gateway-style control when the agent uses it |

Markdown instructions are not a sandbox. If an agent has direct filesystem access, ACG can guide and audit its behavior, but it cannot physically prevent reads unless the runtime is configured to force reads through a gateway or restricted environment.

See [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md).

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
- direct filesystem access outside a controlled gateway;
- humans bypassing CI or branch protection.

---

## Claim

ACG does not make AI-generated code correct.

ACG makes large-codebase AI work structurally mapped, topology-aware when possible, guided, scoped, evidenced, and harder to promote when it goes wrong.

---

## License

Free and open source under the MIT License.

Copyright 2026 Nilton Cunha.
