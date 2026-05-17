# ACG Specification v0.4-beta experimental

ACG (Agentic Code Guidance) is a structural guidance, ownership-aware scouting, topology-aware context, and mechanical enforcement layer for AI-assisted work over large codebases, documentation bundles, agent workspaces and corpus-style folders.

---

## Core Thesis

Large-folder AI failures usually happen because the workflow asks the model to:

- process too much context too early;
- infer repository structure without a map;
- treat a tiny sample as if it represented the whole folder;
- mix target files with runtime/dependency/tooling files;
- modify broad areas without stable scope;
- self-report verification or understanding;
- promote changes without external evidence.

ACG exists to reduce those failure modes.

ACG does not read the whole folder into the model.

ACG maps the shape of the folder first, classifies what belongs to the target project, then gives the AI a controlled reading and execution path.

---

## Layers

ACG has four practical layers.

### 1. Guided Task Contract

Turns vague human intent into a minimal operating contract.

It clarifies:

- objective;
- initial inspection area;
- forbidden or sensitive zones;
- expected verification;
- evidence required before promotion.

### 2. Structure Scout

The Structure Scout runs before deep AI execution.

Its job is to build a structural map of the repository or file bundle before the model attempts broad semantic interpretation.

The Scout indexes the folder, but does not ask the AI to read the folder.

Current package outputs include:

```txt
.acg/ACG_MASTER.md
.acg/phase1_pack/
.acg/artifacts/context_manifest.jsonl
.acg/artifacts/structure_map.md
.acg/artifacts/hotpaths.json
.acg/artifacts/reading_queues.json
.acg/artifacts/phase1_queue.md
.acg/artifacts/phase1_reading_order.md
.acg/artifacts/citation_check.md
.acg/artifacts/phase2_queue.md
.acg/artifacts/approval_required.md
.acg/artifacts/search_targets.md
.acg/artifacts/execution_brief.md
.acg/artifacts/next_prompt.md
.acg/artifacts/phase2_plan_template.md
.acg/artifacts/scout_report.json
```

The primary AI entrypoint is:

```txt
.acg/ACG_MASTER.md
```

The phase pack is derived from the full map. It is not the complete understanding of the codebase.

### 3. Topology and Mapping Layer

The topology/mapping layer adds:

```txt
ownership_class
project_kind
readiness_subscores
readiness_gate
scout_regime
environment/enforcement_level
phase1_reading_order
citation_check
in_degree / out_degree / topology_score when PROJECT_OWNED code exists
```

These artifacts do not replace phase queues.

They help the AI understand what to read, what not to read, what kind of package it is looking at, and whether Phase 1 is sufficiently mapped before moving deeper.

### 4. Enforcement Core

The enforcement layer keeps four hard rules:

1. **Isolated branch** — AI work must not happen directly on the default branch.
2. **Technical scope fence** — changed files must stay inside declared allowed paths and outside forbidden paths.
3. **External verification** — verification is executed by CI/orchestrator, not trusted from agent self-report.
4. **Fail-closed promotion with evidence** — no evidence, no promotion.

---

## Recommended command

Current user entrypoint:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Fast mode:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg --skip-lexical-index
```

Direct scout mode:

```bash
python scripts/acg-scout.py --source /path/to/project --out .acg
```

`acg-scout.py` is the stable package generator used by `acg-v04.py`.

---

## Package kind

ACG classifies the scanned folder before applying readiness.

```txt
CODEBASE
AGENT_WORKSPACE
DOCUMENTATION_BUNDLE
MIXED_REPO
DATASET_OR_CORPUS
TOOL_RUNTIME
UNKNOWN
```

| project_kind | Readiness ruler |
|---|---|
| `CODEBASE` | executable entrypoint + build/control file + code queues |
| `AGENT_WORKSPACE` | orientation entrypoint + structural contract + documentation queues |
| `DOCUMENTATION_BUNDLE` | README/index/start + spec/manifest/docs structure |
| `MIXED_REPO` | weighted combination of code readiness and orientation readiness |
| `DATASET_OR_CORPUS` | manifest/schema/metadata + search/index discipline |
| `TOOL_RUNTIME` | capped; should not silently pass as target project |
| `UNKNOWN` | conservative; should not silently proceed |

---

## Ownership classes

Each indexed file receives `ownership_class`:

```txt
PROJECT_OWNED
VENDORED_DEPENDENCY
TOOL_RUNTIME
GENERATED_CACHE
REFERENCE_ASSET
UNKNOWN_EXTERNAL
```

Only `PROJECT_OWNED` source files are included in the main import graph.

Only `PROJECT_OWNED` files can compete normally in the main hotpath queue.

Runtime, dependency, generated, reference and unknown external files are capped and moved to `search_only` or `terminal_asset` strategies unless explicitly approved.

---

## File strategies

Each indexed file receives fields like:

```json
{
  "relative_path": "src/auth/index.ts",
  "absolute_path": "E:/project/src/auth/index.ts",
  "ownership_class": "PROJECT_OWNED",
  "included_in_import_graph": true,
  "folder_family": "core",
  "role": "source_code",
  "hotpath_score": 87,
  "risk_score": 12,
  "in_degree": 14,
  "out_degree": 3,
  "topology_score": 42,
  "strategy": "open_now",
  "allowed_to_open": true,
  "allowed_to_edit": false,
  "requires_human_approval": false
}
```

Typical families:

```txt
core
canon
memory
runtime
tests
docs
evaluation
reference
dataset
legacy
logs
exports
generated
secrets
infra
migrations
unknown
```

| Strategy | Meaning |
|---|---|
| `open_now` | Safe and important enough for early reading. |
| `open_later` | Useful, but not first. |
| `search_only` | Do not open fully; use targeted search. |
| `index_only` | Keep in inventory, but do not read by default. |
| `human_only` | Requires explicit human approval. |
| `terminal_asset` | Large/historical/reference/runtime asset; never read blindly. |
| `ignore` | Generated/cache/noise. |

---

## Formal Definitions

### hotpath_score

For `PROJECT_OWNED` source files:

```txt
hotpath_score in [0, 100]

hotpath_score = min(100, topology + size_score + family_score)

topology     in [0, 60] = int(60 * in_degree / max(max_in_degree, 1))
size_score   in [0, 20] = 20 if <=50KB | 12 if <=200KB | 5 if <=500KB | 0 otherwise
family_score in [0, 20]
```

For non-source files, ACG uses structural heuristics.

For non-`PROJECT_OWNED` files, ACG caps score and excludes them from main import-graph competition.

Topology is derived from import-graph centrality:

- Python: `ast.parse` -> `ast.Import` + `ast.ImportFrom`.
- JS/TS: relative `import ... from './path'`, `require('./path')`, and dynamic relative import patterns currently handled by regex.
- Rust: `use module::path`.
- Go: import blocks and single-line imports.

External dependencies do not contribute to the main `in_degree`.

### readiness_score

ACG computes readiness subscores and then selects the score based on `project_kind`.

```json
{
  "readiness_subscores": {
    "code_readiness": 0.68,
    "orientation_readiness": 0.82,
    "dataset_readiness": 0.50,
    "runtime_penalty": 0.0,
    "open_now_count": 12,
    "project_files": 948,
    "code_files": 2,
    "doc_files": 120,
    "data_files": 0,
    "runtime_files": 3281
  }
}
```

Selection rules:

| project_kind | readiness_score |
|---|---|
| `CODEBASE` | `code_readiness`, capped below pass if no executable/control evidence |
| `AGENT_WORKSPACE` | `orientation_readiness` |
| `DOCUMENTATION_BUNDLE` | `orientation_readiness` |
| `MIXED_REPO` | `0.55 * code_readiness + 0.45 * orientation_readiness` |
| `DATASET_OR_CORPUS` | `dataset_readiness` |
| `TOOL_RUNTIME` | capped at `0.34` |
| `UNKNOWN` | conservative max subscore minus uncertainty penalty |

### guardrail_mode thresholds

| Mode | Condition | Behavior |
|---|---|---|
| `silent` | score >= 0.65 | Proceed. |
| `warn` | 0.45 <= score < 0.65 | Proceed only with explicit human checkpoint. |
| `halt` | score < 0.45 | Block deeper execution/promotion. |

### readiness_gate

The Scout emits:

```json
{
  "readiness_gate": {
    "min_required": 0.65,
    "actual": 0.771,
    "status": "passed",
    "project_kind": "AGENT_WORKSPACE"
  }
}
```

`TOOL_RUNTIME` and `UNKNOWN` do not receive easier gates.

---

## Scout regime

The Scout emits `scout_regime`:

```txt
minimal
standard
extended
large
```

This is based on scale and import-graph availability. It tells the agent how cautiously to treat the generated map.

---

## Environment mode

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

If no `.git` folder exists, the package remains usable for mapping, but enforcement is reported as:

```txt
enforcement_level = scout_only
```

---

## Phase 1 reading proof

Before deeper work, the AI must follow:

```txt
.acg/artifacts/phase1_reading_order.md
.acg/artifacts/citation_check.md
```

Required output:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files actually read, in order
CITATION_CHECK: one answer per required citation check
RISKS: key risks before deeper processing
QUESTIONS: objective human approvals needed
NEXT: bounded Phase 2 plan or clarification questions
```

The NEXT block must follow:

```txt
.acg/artifacts/phase2_plan_template.md
```

If the AI proposes files outside the current phase queue, asks to read terminal assets directly, skips citation checks, or asks vague questions like "what next?", the process should stop.

---

## Enforcement vs Guidance

ACG has distinct control levels:

| Layer | Control type |
|---|---|
| `ACG_MASTER.md`, adapter docs, prompts | Cooperative guidance |
| `phase1_reading_order.md`, `citation_check.md` | Cooperative proof-of-reading friction |
| `acg-gateway.py` | Advisory gate, not sandbox |
| `acg-enforce.py`, CI, branch/scope checks | Mechanical enforcement |

Natural language instructions are context, not hard enforcement.

Mechanical authority comes from:

```txt
acg.yaml
scripts/acg-enforce.py
GitHub Actions / CI
external verification
JSONL evidence
branch and scope checks
```

`acg-gateway.py` can provide gateway-style read control when the agent is forced to use it. It is not full enforcement if the agent also has unrestricted filesystem access.

---

## Known Gaps v0.4-beta

| ID | Gap | Severity |
|---|---|---|
| GAP-01 | JS/TS path aliases are not fully resolved. | medium |
| GAP-02 | Dynamic imports and runtime module loading are incomplete. | low/medium |
| GAP-03 | Python stem fallback can produce false positives. | low |
| GAP-04 | Gateway is advisory; not a real sandbox. | design boundary |
| GAP-05 | Multi-agent branch conflict detection is absent. | medium |
| GAP-06 | Task-aware outside-scope relevance is not implemented yet. | medium |
| GAP-07 | Citation checks reduce shallow reading but do not prove semantic mastery. | design boundary |

---

## Future Layer

Future versions may include:

- task-aware relevance map;
- potentially relevant outside-scope warnings;
- tsconfig path alias resolution;
- semantic diff;
- behavioral baselines;
- characterization tests;
- adversarial review agents;
- multi-agent branch conflict detection;
- telemetry;
- optional semantic retrieval/RAG.

These are outside the minimal core.

---

## Principle

ACG does not make AI-generated work correct.

ACG makes large-folder AI work guided, structured, ownership-aware, scoped, evidenced, and harder to promote when it goes wrong.
