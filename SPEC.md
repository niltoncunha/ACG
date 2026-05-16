# ACG Specification v0.4-beta

ACG (Agentic Code Guidance) is a structural guidance, topology-aware context, and mechanical enforcement layer for AI-assisted software work over large codebases.

---

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

Current stable package outputs include:

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

### 3. Topology Layer v0.4-beta

The topology layer adds import-graph and formal scoring artifacts:

```txt
.acg/artifacts/import_graph.json
.acg/artifacts/cluster_map.md
.acg/artifacts/surface_summaries.md
.acg/artifacts/context_payload.json
.acg/artifacts/performance_report.md
.acg/scout_report.json                 # beta schema target
schemas/scout_report.schema.json
schemas/readiness_invariants.json
```

These artifacts do not replace phase queues.

They help the AI understand structural centrality and public code surfaces without opening every source file.

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

`acg-scout.py` remains the stable package generator used by `acg-v04.py`.

The v0.4-beta target is to merge import-graph-driven `hotpath_score` into the stable Scout without breaking the `--source/--out` CLI or the `.acg/artifacts/` layout.

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
  "in_degree": 14,
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

## Formal Definitions

This section is normative. The schemas in `schemas/` are the authority.

### hotpath_score

```txt
hotpath_score in [0, 100]

hotpath_score = min(100, topology + size_score + family_score)

topology     in [0, 60] = int(60 * in_degree / max(max_in_degree, 1))
size_score   in [0, 20] = 20 if <=50KB | 12 if <=200KB | 5 if <=500KB | 0 otherwise
family_score in [0, 20] = see schemas/readiness_invariants.json
```

Topology is the primary driver, with 60% of the ceiling.

It is derived from import-graph centrality, not file-name heuristics:

- Python: `ast.parse` -> `ast.Import` + `ast.ImportFrom`.
- JS/TS: relative `import ... from './path'` and `require('./path')`.
- Rust: `use module::path`.
- Go: import blocks and single-line imports.

Resolution order:

1. Reconstruct the path from the importer's directory.
2. Try supported source extensions.
3. Use stem fallback only when path reconstruction fails.

External dependencies do not resolve to local files and do not contribute to `in_degree`. That is correct: `hotpath_score` reflects internal architectural centrality.

#### Invariants: hotpath

| ID | Invariant |
|---|---|
| INV-H1 | `0 <= hotpath_score <= 100` |
| INV-H2 | `topology <= 60`, `family_score <= 20`, `size_score <= 20` |
| INV-H3 | `in_degree == 0 -> topology == 0` |
| INV-H4 | `in_degree == max_in_degree -> topology == 60` |

### readiness_score

```txt
readiness_score in [0.0, 1.0]

readiness_score = round(W1 + W2 + W3 + W4, 3)

W1 = 0.30 * has_entrypoint
W2 = 0.25 * has_control_files
W3 = 0.25 * min(open_now_count / total_files * 4, 1)
W4 = 0.20 * max(0, 1 - broken_refs_count / total_files)

Halt condition:
  if (not has_entrypoint) and (not has_control_files):
      readiness_score = min(readiness_score, 0.44)
```

The halt condition guarantees that a repository with neither a detected entrypoint nor control files can never silently proceed.

#### guardrail_mode thresholds

| Mode | Condition | CI exit code | Behavior |
|---|---|---:|---|
| `silent` | score >= 0.65 | 0 | Proceed. |
| `warn` | 0.45 <= score < 0.65 | 1 | Proceed with human checkpoint. |
| `halt` | score < 0.45 | 2 | Block promotion. |

#### Invariants: readiness

| ID | Invariant |
|---|---|
| INV-R1 | `0.0 <= readiness_score <= 1.0` |
| INV-R2 | `guardrail_mode` is a deterministic function of `readiness_score`. |
| INV-R3 | Halt condition is irrevocable by configuration. |
| INV-R4 | `W3 in [0, 0.25]` |
| INV-R5 | `W4 >= 0` |
| INV-R6 | `guardrail_mode=halt -> exit_code=2 -> CI fails -> promotion blocked` |

The full machine-readable contract is in:

```txt
schemas/readiness_invariants.json
schemas/scout_report.schema.json
```

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

## Enforcement vs Guidance

ACG has two distinct control levels:

| Layer | Control type |
|---|---|
| `AGENTS.md`, adapter docs, prompts | Cooperative guidance only |
| `acg-gateway.py` | Advisory gate, not sandbox |
| `acg-enforce.py`, CI, branch/scope checks | Mechanical enforcement |

Natural language instructions are context, not enforcement.

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
| GAP-01 | JS/TS path aliases are not resolved yet. | medium |
| GAP-02 | Dynamic imports are not captured yet. | low |
| GAP-03 | Python stem fallback can produce false positives. | low |
| GAP-04 | Gateway is advisory; not a real sandbox. | design boundary |
| GAP-05 | Multi-agent branch conflict detection is absent. | medium |

Full gap descriptions with mitigations are in `schemas/readiness_invariants.json` and `KNOWN_LIMITATIONS.md`.

---

## Future Layer

Future versions may include:

- merge of import-graph `hotpath_score` into the stable Scout package generator;
- tsconfig path alias resolution;
- semantic diff;
- behavioral baselines;
- characterization tests;
- adversarial review agents;
- multi-agent branch conflict detection;
- telemetry;
- policy engines.

These are outside the minimal core.

---

## Principle

ACG does not make AI-generated code correct.

ACG makes large-codebase AI work guided, structured, scoped, evidenced, and harder to promote when it goes wrong.
