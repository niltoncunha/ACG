# ACG-Core Specification v0.2

ACG-Core is the minimum mechanical enforcement layer for AI coding agents.

## Hard Core

ACG-Core has four hard rules:

1. **Isolated branch** — agentic work must not happen directly on the default branch.
2. **Technical scope fence** — changed files must stay inside declared allowed paths and outside forbidden paths.
3. **External verification** — verification is run by CI/orchestrator, not trusted from agent self-report.
4. **Fail-closed promotion with evidence** — no evidence, no promotion.

## Process Layer

Recommended, but not hard Core:

- Impact Map.
- Human Gate.
- Small PR.
- Circuit Breaker.
- Done-When per slice.

## Full Layer

Future ACG-Full may include:

- semantic diff;
- behavioral baselines;
- characterization tests;
- adversarial review agents;
- telemetry;
- distributed ledger;
- policy engine;
- multi-agent orchestration.

These are intentionally out of Core.

## Principle

Natural language instructions are context, not enforcement.

`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, and similar files are useful. They are not safety boundaries.
