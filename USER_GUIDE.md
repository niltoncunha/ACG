# User Guide

ACG is used around your coding agent, not inside it.

The normal user should not need to know how to design prompts, build manifests, or decide the first reading queue manually.

## Standard workflow

1. Generate the ACG package:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

2. Give the AI one instruction:

```txt
Open .acg/ACG_MASTER.md first and follow it exactly.
```

3. Wait for the AI to return:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files actually read
RISKS: key risks before deeper processing
QUESTIONS: objective approvals needed
NEXT: bounded Phase 2 plan
```

4. Approve or reject only a bounded file list.

5. Do not approve edits until the reading plan is clear.

## What to approve

Good approval:

```txt
ACG Phase 2 approved for reading only.
Open only these files:
1. <file>
2. <file>
Do not edit files.
Do not open search_only, terminal_asset, legacy, logs, exports, binary/database files.
```

Bad approval:

```txt
Continue exploring.
```

## When the AI asks a vague question

If the AI asks:

```txt
What should I do next?
```

reject the answer. ACG is supposed to propose the next bounded safe step from generated artifacts.

## Coding workflow with enforcement

For actual code changes:

1. Create a branch.
2. Define the task in `acg.yaml`.
3. Run your agent with clear scope.
4. Open a pull request.
5. Let ACG run in CI.
6. Merge only when ACG passes.

Tell the agent:

```txt
You are operating under ACG.
Read acg.yaml before editing.
Edit only task.scope.allowed.
Do not edit task.scope.forbidden.
Do not claim verification success.
CI will verify externally.
```

## What to check as a human

- Did the AI read only the approved phase files?
- Did it avoid search-only and terminal assets?
- Did the change stay inside the declared scope?
- Did CI run verification externally?
- Is there evidence?
- Is the diff small enough to understand?
- Are the limitations relevant to this PR?

## Optional gateway mode

Use `acg-gateway.py` if you want phase-aware reads through a CLI:

```bash
python scripts/acg-gateway.py list --acg .acg --phase 1
python scripts/acg-gateway.py read --acg .acg --phase 1 --path 00_core/README.md
```

This only becomes hard control if the agent cannot bypass it with direct filesystem access.

## Intake before execution

If the real problem is that the human is feeding the model badly, use:

```txt
examples/acg-guardrail/
```

That example forces:

- clear objective;
- material scope;
- limit of what the AI can do;
- human checkpoints;
- stopping rule;
- copyable operating contract.

## When not to rely on ACG alone

Use additional review for:

- database migrations;
- authentication and authorization;
- payments;
- production infrastructure;
- large refactors;
- low test coverage;
- security-critical code.
