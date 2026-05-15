# ACG Structure Scout

**Agentic Code Guidance** for large codebases.

ACG is a guidance and enforcement package for AI-assisted software work.

It exists because the first failure often happens before code is written: the user gives the AI a vague mission, too many files, no reading order, no scope, and no external gate.

ACG turns vague human intent into scoped, verifiable AI work.

It does not replace the developer, reviewer, or CI system. It guides the user and the AI into a safer operating path.

```txt
vague request -> guided task contract -> structure scout -> scoped work -> external verify -> evidence gate
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
- there was no stable reading chain;
- there was no scoped execution path;
- verification depended too much on the AI's own report;
- promotion had no hard evidence gate.

ACG exists to reduce that failure mode.

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

## ACG has two layers

### 1. Structure Scout

The Scout runs before deep AI work.

It maps the repository or file bundle structurally before asking the model to interpret everything semantically.

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

### 2. Enforcement Core

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
|  The AI does the work. ACG guides the request, gives structure,       |
|  limits scope, requires evidence, and blocks unsafe promotion.         |
+======================================================================+
```

---

## Core thesis

ACG is not the process itself.

ACG is the guide rail that gives the user and the AI a stable path through the process.

```txt
without ACG:
  vague request -> huge context -> scattered reasoning -> broken refactor

with ACG:
  guided task -> structure -> phased reading -> scoped work -> external gate
```

Natural language instructions are useful context. They are not enforcement.

```txt
human intent       = raw input
scout report       = structural map
execution brief    = reading/acting path
agent output       = proposal
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

- vague requests turning into uncontrolled AI work;
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

## Claim

ACG does not make AI-generated code correct.

ACG makes large-codebase AI work guided, structured, scoped, evidenced, and harder to promote when it goes wrong.

---

## License

Free and open source under the MIT License.

Copyright 2026 Nilton Cunha.
