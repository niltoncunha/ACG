# ACG Structure Scout

**Agentic Code Guidance** for large codebases, agent workspaces, documentation bundles and corpus-style folders.

ACG is a guidance, context-mapping, topology-aware scouting and enforcement package for AI-assisted software work.

It exists because the first failure often happens before code is written: the user gives the AI a vague mission, too many files, no reading order, no scope, and no external gate.

ACG turns vague human intent into scoped, phased, verifiable AI work.

It does not replace the developer, reviewer, test suite, sandbox, or CI system. It gives the user and the AI a controlled path through a large folder or repository.

```txt
vague request
  -> guided task contract
  -> full structural inventory
  -> ownership classification
  -> project_kind detection
  -> topology-aware context package when code exists
  -> readiness gate
  -> ordered Phase 1 reading
  -> citation check
  -> bounded Phase 2 plan
  -> scoped AI work
  -> external verify
  -> evidence gate
```

---

## Current status

Current line: **v0.4-beta experimental**.

Recommended entrypoint:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Windows:

```powershell
python scripts\acg-v04.py --source "E:\path\to\project" --out ".acg"
```

Fast first run without lexical indexing:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg --skip-lexical-index
```

Direct Structure Scout run:

```bash
python scripts/acg-scout.py --source /path/to/project --out .acg
```

ACG v0.4-beta keeps the v0.3/v0.4 package layout usable while adding ownership-aware hotpath ranking, adaptive project kind detection, readiness subscores, mapping gates, explicit Phase 1 reading order and citation checks.

---

## What ACG generates

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
    phase1_reading_order.md
    citation_check.md
    phase2_queue.md
    approval_required.md
    search_targets.md
    execution_brief.md
    next_prompt.md
    phase2_plan_template.md
    scout_report.json
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

The human should not need to invent the next prompt. `ACG_MASTER.md`, `phase1_reading_order.md`, `citation_check.md`, `next_prompt.md`, and `phase2_plan_template.md` drive the next bounded step.

---

## Core idea

ACG does not solve large folders by asking the AI to read every file.

ACG first builds a structural map:

```txt
all files
  -> ownership_class
  -> project_kind
  -> folder families
  -> hotpaths
  -> risks
  -> terminal/search-only assets
  -> import graph, when PROJECT_OWNED code exists
  -> readiness_subscores
  -> readiness_gate
  -> scout_regime
  -> reading queues
  -> citation checks
  -> controlled phase packs
```

Then the AI reads only the right subset, in the right order, with explicit limits.

---

## Package kinds

ACG does not assume every folder is a classic executable codebase.

`project_kind` may be:

| project_kind | Meaning |
|---|---|
| `CODEBASE` | Classic source repository with code, control files, tests or entrypoints. |
| `AGENT_WORKSPACE` | Agent/corpus workspace with `AGENTS.md`, indexes, contracts, memory/canon/core layers. |
| `DOCUMENTATION_BUNDLE` | Documentation-first package with README/spec/index structure and little or no code. |
| `MIXED_REPO` | Code plus significant agent/documentation layer. |
| `DATASET_OR_CORPUS` | Data/corpus/export package where search, schema and metadata matter more than source imports. |
| `TOOL_RUNTIME` | Environment, dependency, runtime, plugin or toolchain folder; not a project target by default. |
| `UNKNOWN` | Insufficient structural evidence; should not silently proceed. |

The detected package kind controls readiness scoring.

---

## Ownership classes

Every file receives `ownership_class`:

| ownership_class | Meaning |
|---|---|
| `PROJECT_OWNED` | Belongs to the inferred target project or workspace. |
| `VENDORED_DEPENDENCY` | Dependency bundle, package install, third-party vendored tree. |
| `TOOL_RUNTIME` | Tool/runtime/cache/plugin environment around the project. |
| `GENERATED_CACHE` | Generated or cache artifact. |
| `REFERENCE_ASSET` | Reference, corpus, dataset, fixture or search-only material. |
| `UNKNOWN_EXTERNAL` | Outside inferred project roots. |

Only `PROJECT_OWNED` source files are allowed into the main import graph and primary hotpath competition. Runtime/dependency files are capped and classified as `terminal_asset` or `search_only`.

---

## Readiness and mapping gates

The Scout now emits:

```json
{
  "project_kind": "AGENT_WORKSPACE",
  "scout_regime": "standard",
  "readiness_score": 0.771,
  "readiness_gate": {
    "min_required": 0.65,
    "actual": 0.771,
    "status": "passed"
  },
  "readiness_subscores": {
    "code_readiness": 0.22,
    "orientation_readiness": 0.77,
    "dataset_readiness": 0.50,
    "runtime_penalty": 0.0
  }
}
```

For `CODEBASE`, code entrypoints and control/build files matter most.

For `AGENT_WORKSPACE` and `DOCUMENTATION_BUNDLE`, orientation entrypoints and structural contracts matter most.

For `DATASET_OR_CORPUS`, manifest/schema/metadata and search-only discipline matter most.

For `TOOL_RUNTIME`, readiness is capped and should not silently promote the folder as a target project.

---

## Phase 1 proof of reading

ACG no longer relies only on an agent saying it understood.

The generated package includes:

```txt
artifacts/phase1_reading_order.md
artifacts/citation_check.md
```

The AI must return:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files actually read, in order
CITATION_CHECK: one answer per required citation check
RISKS: key risks before deeper processing
QUESTIONS: objective questions or approval requests only
NEXT: bounded Phase 2 plan or clarification questions
```

This does not prove perfect understanding, but it reduces shallow self-reporting.

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

Maps the repository or folder before deep semantic work.

It produces:

- full file inventory;
- ownership classification;
- project kind classification;
- folder family classification;
- hotpath score per file;
- risk score per file;
- strategy per file: `open_now`, `open_later`, `search_only`, `index_only`, `human_only`, `terminal_asset`, `ignore`;
- compact phase queues;
- ordered Phase 1 reading plan;
- citation checks;
- search-only targets;
- controlled Phase 1 pack;
- generated AI instructions.

### 3. Topology Layer

Adds code topology when `PROJECT_OWNED` code files exist:

- static import graph;
- in-degree / out-degree;
- topology score;
- architectural hub view;
- surface summaries for high-weight code files;
- lightweight context payload;
- performance report and topology cache.

If the folder is mostly documentation, corpus, or agent workspace material, the topological layer may be small. That is expected.

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

## Environment detection

The Scout emits:

```json
{
  "environment": {
    "has_git": true,
    "git_root": "...",
    "git_velocity_available": true,
    "branch_check_available": true,
    "enforcement_level": "full"
  }
}
```

If no `.git` folder is found, ACG still generates the context package, but reports:

```txt
enforcement_level = scout_only
```

That means branch checks, git velocity and PR-style enforcement require a Git repository.

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
| `phase1_reading_order.md`, `citation_check.md` | cooperative proof-of-reading friction |
| `acg-enforce.py`, CI, branch/scope checks | mechanical enforcement |
| `acg-gateway.py` | advisory gateway when the agent uses it |

Markdown instructions are not a sandbox. If an agent has direct filesystem access, ACG can guide and audit its behavior, but it cannot physically prevent reads unless the runtime is configured to force reads through a gateway or restricted environment.

See [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md).

---

## Claim

ACG does not make AI-generated code correct.

ACG makes large-folder AI work structurally mapped, ownership-aware, topology-aware when code exists, guided, scoped, evidenced, and harder to promote when it goes wrong.

---

## License

Free and open source under the MIT License.

Copyright 2026 Nilton Cunha.
