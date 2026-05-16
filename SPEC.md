# ACG Specification v0.4-alpha

ACG (Agentic Code Guidance) is a structural guidance, topology-aware context, and mechanical enforcement layer for AI-assisted software work.

## Core Thesis

Large-codebase AI failures usually happen because the workflow asks the model to:

- process too much context too early;
- infer repository structure without a map;
- treat a tiny sample as if it represented the whole codebase;
- modify broad areas without stable scope;
- self-report verification;
- promote changes without external evidence.

ACG exists to reduce those failure modes.

ACG does not read the whole codebase into the model.

ACG maps the shape of the whole codebase first, then gives the AI a controlled reading and execution path.

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

The Scout indexes the whole folder, but does not ask the AI to read the whole folder.

Core outputs:

```txt
.acg/ACG_MASTER.md
.acg/artifacts/context_manifest.jsonl
.acg/artifacts/structure_map.md
.acg/artifacts/hotpaths.json
.acg/artifacts/reading_queues.json
.acg/artifacts/phase1_queue.md
.acg/artifacts/phase2_queue.md
.acg/artifacts/approval_required.md
.acg/artifacts/search_targets.md
.acg/artifacts/execution_brief.md
.acg/artifacts/next_prompt.md
.acg/artifacts/phase2_plan_template.md
.acg/phase1_pack/
```

The primary AI entrypoint is:

```txt
.acg/ACG_MASTER.md
```

The phase pack is derived from the full map. It is not the complete understanding of the codebase.

### 3. Topology Layer v0.4-alpha

The v0.4-alpha orchestrator adds topology-aware artifacts:

```txt
.acg/artifacts/import_graph.json
.acg/artifacts/cluster_map.md
.acg/artifacts/surface_summaries.md
.acg/artifacts/context_payload.json
.acg/artifacts/performance_report.md
```

These artifacts do not replace the phase queues.

They help the AI understand structural centrality and public code surfaces without opening every source file.

### 4. Enforcement Core

The enforcement layer keeps four hard rules:

1. **Isolated branch** — AI work must not happen directly on the default branch.
2. **Technical scope fence** — changed files must stay inside declared allowed paths and outside forbidden paths.
3. **External verification** — verification is executed by CI/orchestrator, not trusted from agent self-report.
4. **Fail-closed promotion with evidence** — no evidence, no promotion.

---

## Recommended command

Run v0.4-alpha:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Fast mode:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg --skip-lexical-index
```

The older `acg-scout.py` remains as a stable Structure Scout component, but `acg-v04.py` is the recommended user entrypoint.

---

## File strategies

Each indexed file receives fields like:

```json
{
  "relative_path": "src/auth/index.ts",
  "absolute_path": "E:/project/src/auth/index.ts",
  "folder_family": "core",
  "role": "source_code",
  "hotpath_score": 87,
  "risk_score": 12,
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
| `terminal_asset` | Large/historical/reference asset; never read blindly. |
| `ignore` | Generated/cache/noise. |

---

## v0.4 topology artifacts

### `import_graph.json`

Machine-readable static import graph.

It includes:

- resolved internal imports where possible;
- `in_degree`;
- `out_degree`;
- `git_velocity_90d` when a Git repository is available;
- `architectural_weight`;
- public surface count.

Do not ask the AI to read this file fully by default. It is for tools and diagnostics.

### `cluster_map.md`

Human-readable topology summary.

The AI should read this before proposing Phase 2.

### `surface_summaries.md`

Allowed summaries of high-weight code surfaces.

Important distinction:

```txt
surface_summaries.md may be read.
The original files summarized there keep their original queue status.
```

If an original file is `search_only`, the summary does not automatically authorize opening the original.

### `context_payload.json`

Optional structured payload mode.

Use it for compact handoff or single-file context passing. Do not duplicate it with normal Phase 1 file reading unless useful.

### `performance_report.md`

Runtime cost report.

Used to check that Scout stays fast enough for adoption.

---

## AI Handshake

Before deeper work, the AI should confirm:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files actually read
RISKS: key risks before deeper processing
QUESTIONS: objective human approvals needed
NEXT: bounded Phase 2 plan or clarification questions
```

The NEXT block must follow:

```txt
.acg/artifacts/phase2_plan_template.md
```

If the AI proposes files outside the current phase queue, asks to read terminal assets directly, or asks vague questions like "what next?", the process should stop.

---

## Enforcement authority

Natural language instructions are context, not enforcement.

Files such as:

```txt
AGENTS.md
CLAUDE.md
.cursor/rules
ACG_MASTER.md
```

are useful guidance, but not a sandbox.

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

## Process discipline

Recommended operational discipline:

- phased reading;
- small scoped tasks;
- human checkpoints;
- exact file lists;
- impact maps;
- done-when per slice;
- circuit breakers;
- external verification before promotion.

---

## Future Layer

Future versions may include:

- direct integration of import graph boosts into primary hotpath scoring;
- stronger gateway/MCP read control;
- semantic index with embeddings;
- token budget optimizer;
- behavioral baselines;
- characterization tests;
- adversarial review agents;
- policy engines;
- multi-agent orchestration.

These are outside the minimal v0.4-alpha core.
