# ACG Structure Scout

**Agentic Code Guidance** for large codebases.

ACG is a structural guidance and enforcement package for AI-assisted software work.

It does **not** try to replace the developer, the reviewer, or the CI system. Its job is narrower and more useful:

```txt
turn a large pile of files into a readable execution path for the AI,
then enforce scope, verification, evidence, and fail-closed promotion.
```

The original failure case is simple:

```txt
"I asked an AI to refactor a large codebase. It spent a long time, burned huge context, and broke the app."
```

The likely failure is not only that the model wrote bad code. The model lost the structure of the system. It opened too much, too early, with no stable chain of reading, no scoped execution path, and no external promotion gate.

ACG exists to prevent that failure mode.

---

## What ACG does

ACG has two layers.

### 1. Structure Scout

The Scout runs before deep AI work.

It maps the repository or file bundle structurally, before asking the model to interpret everything semantically.

It produces:

- automatic file inventory;
- language/runtime detection;
- control-file detection;
- entrypoint detection;
- reference graph;
- hubs;
- orphans;
- broken references;
- terminal assets to skip;
- real attention queue;
- phased reading plan;
- execution brief for the AI.

The goal is not to read every file. The goal is to decide what should be opened first, what should wait, and what should not be read at all.

### 2. ACG enforcement core

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
|        Structure Scout + Mechanical Enforcement for AI Code Work      |
+======================================================================+

  LARGE CODEBASE / FILE BUNDLE
              |
              v
      [01] STRUCTURAL INVENTORY
              |
              v
      [02] LANGUAGE + RUNTIME DETECTION
              |
              v
      [03] CONTROL FILES + ENTRYPOINTS
              |
              v
      [04] REFERENCE GRAPH
              |
              v
      [05] ATTENTION QUEUE
              |
              v
      [06] PHASED READING PLAN
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
|  The AI does the work. ACG gives it structure, order, scope, evidence |
|  and a gate so it does not wander through the codebase blindly.        |
+======================================================================+
```

---

## Core thesis

ACG is not the process itself.

ACG is the guide rail that gives the AI a stable path through the process.

```txt
without ACG:
  huge codebase -> huge context -> scattered reasoning -> broken refactor

with ACG:
  structure -> phased reading -> focused context -> scoped work -> external gate
```

Natural language instructions are useful context. They are not enforcement.

```txt
agent output       = proposal
scout report       = structural map
execution brief    = reading/acting path
external verify    = evidence
fail-closed gate   = promotion control
```

---

## Structure Scout output

The Scout emits a `scout_report` with fields such as:

```json
{
  "system_profile": {},
  "language_map": [],
  "control_files": [],
  "reference_graph": {},
  "attention_queue": [],
  "phased_reading_plan": [],
  "execution_brief": {},
  "readiness_score": 0.82,
  "guardrail_mode": "silent"
}
```

The most important outputs are:

| Output | Purpose |
|---|---|
| `attention_queue` | What to open first, and why. |
| `phased_reading_plan` | How to process the repo in safe phases. |
| `execution_brief` | A compact handoff the AI can follow without losing the chain. |
| `readiness_score` | Whether the structure is clear enough to proceed. |
| `guardrail_mode` | Whether the AI can proceed silently or needs clarification. |

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

## Repository map

```txt
.
├── README.md
├── SPEC.md
├── QUICKSTART.md
├── USER_GUIDE.md
├── KNOWN_LIMITATIONS.md
├── THREAT_MODEL.md
├── CHANGELOG.md
├── PUBLISHING_GUIDE.md
├── VERSION
├── acg.yaml
├── acg.yaml.example
├── scripts/
│   ├── acg-enforce.py
│   ├── acg-bootstrap.py
│   └── acg-enforce.sh
├── schemas/
│   ├── acg.schema.json
│   ├── acg-evidence.schema.json
│   └── scout-report.schema.json
├── tests/
│   ├── test_acg_enforce.py
│   ├── test_structure_scout_smoke.py
│   └── structure_scout_harness.js
├── examples/
│   └── acg-structure-scout/
└── .github/
    └── workflows/
        └── validate.yml
```

---

## Quick start

Run the Scout example locally by opening:

```txt
examples/acg-structure-scout/index.html
```

Run enforcement locally:

```bash
python3 scripts/acg-enforce.py --config acg.yaml --mode all
```

Run the test suite:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
node --check examples/acg-structure-scout/script.js
```

---

## What ACG protects against

- reading too many files too early;
- losing the structural chain of a codebase;
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

## Platform adapters

Files such as `CLAUDE.md`, `CODEX.md`, `.cursor/rules`, and other tool-specific instructions are useful as optional adapters.

They are not the authority of the method.

The authority is:

```txt
scout_report
execution_brief
acg.yaml
scripts/acg-enforce.py
CI evidence
```

Tool adapters may be added later as optional adoption guides. They do not govern the core.

---

## Status

Current package: **ACG Structure Scout v0.2.2**.

Implemented:

- automatic inventory;
- language/runtime detection;
- reference graph;
- orphan detection;
- broken reference detection;
- real attention queue;
- phased reading plan;
- execution brief;
- branch check;
- scope check;
- external verification runner;
- `done_when` checks;
- JSONL evidence;
- fail-closed promotion gate;
- GitHub Actions validation;
- schemas;
- bootstrap helper;
- threat model;
- MIT license.

---

## Claim

ACG does not make AI-generated code correct.

ACG makes large-codebase AI work structurally guided, scoped, evidenced, and harder to promote when it goes wrong.

---

## License

Free and open source under the MIT License.

Copyright 2026 Nilton Cunha.
