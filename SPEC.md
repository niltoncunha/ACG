# ACG Specification v0.2.2

ACG (Agentic Code Guidance) is a structural guidance and mechanical enforcement layer for AI-assisted software work.

## Core Thesis

Large-codebase AI failures usually happen because the model is forced to:

- open too much context too early;
- infer structure without guidance;
- modify broad areas without stable scope;
- self-report verification;
- promote changes without external evidence.

ACG exists to reduce those failure modes.

## Structure Scout

The Structure Scout runs before deep AI execution.

Its job is to map the repository structurally before the model attempts broad semantic interpretation.

Outputs may include:

- inventory;
- language/runtime map;
- entrypoints;
- control files;
- reference graph;
- hubs and orphans;
- broken references;
- attention queue;
- phased reading plan;
- execution brief.

The Scout is designed to answer:

```txt
what should the AI open first?
what can wait?
what should be ignored?
```

## Enforcement Core

The enforcement layer keeps four hard rules:

1. **Isolated branch** — AI work must not happen directly on the default branch.
2. **Technical scope fence** — changed files must stay inside declared allowed paths and outside forbidden paths.
3. **External verification** — verification is executed by CI/orchestrator, not trusted from agent self-report.
4. **Fail-closed promotion with evidence** — no evidence, no promotion.

## Process Layer

Recommended operational discipline:

- phased reading;
- small scoped tasks;
- human checkpoints;
- impact maps;
- done-when per slice;
- circuit breakers.

## Future Layer

Future versions may include:

- semantic diff;
- behavioral baselines;
- characterization tests;
- adversarial review agents;
- telemetry;
- policy engines;
- multi-agent orchestration.

These are intentionally outside the minimal core.

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
scout_report
execution_brief
acg.yaml
external verification
CI evidence
```
