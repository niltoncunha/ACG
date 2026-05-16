# ACG Specification v0.3

ACG (Agentic Code Guidance) is a structural guidance and mechanical enforcement layer for AI-assisted software work.

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

ACG has three layers.

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

Outputs:

```txt
.acg/context_manifest.jsonl
.acg/structure_map.md
.acg/hotpaths.json
.acg/reading_queues.json
.acg/search_targets.md
.acg/execution_brief.md
.acg/phase1_pack/
```

The primary artifact is:

```txt
.acg/structure_map.md
```

The phase pack is derived from the full map. It is not the complete understanding of the codebase.

### 3. Enforcement Core

The enforcement layer keeps four hard rules:

1. **Isolated branch** — AI work must not happen directly on the default branch.
2. **Technical scope fence** — changed files must stay inside declared allowed paths and outside forbidden paths.
3. **External verification** — verification is executed by CI/orchestrator, not trusted from agent self-report.
4. **Fail-closed promotion with evidence** — no evidence, no promotion.

---

## Structure Scout v0.3

The Scout performs:

```txt
full inventory
folder family classification
hotpath scoring
risk scoring
strategy assignment
reading queue generation
search target extraction
execution brief generation
```

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

### Folder families

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

### Strategies

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

## AI Handshake

Before execution, ACG should generate an execution brief.

The AI should confirm understanding before doing deeper work:

```txt
ACG-UNDERSTOOD: <task-id>
SCOPE: <files actually read or planned>
RISKS: <what could break or confuse analysis>
QUESTIONS: <what needs human approval>
```

If the AI proposes files outside the allowed path or asks to read terminal assets directly, the process should stop and ask the human.

---

## Process Layer

Recommended operational discipline:

- phased reading;
- small scoped tasks;
- human checkpoints;
- impact maps;
- done-when per slice;
- circuit breakers.

---

## Future Layer

Future versions may include:

- semantic diff;
- behavioral baselines;
- characterization tests;
- adversarial review agents;
- telemetry;
- policy engines;
- multi-agent orchestration.

These are outside the minimal core.

---

## Principle

Natural language instructions are context, not enforcement.

Files such as:

```txt
AGENTS.md
CLAUDE.md
.cursor/rules
```

are useful adapters, but not the authority of the method.

The authority is:

```txt
structure_map.md
reading_queues.json
execution_brief.md
acg.yaml
external verification
CI evidence
```
