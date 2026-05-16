# Codex Adapter

Codex can be used with ACG in two modes:

1. **orientation mode** — read the generated `.acg/` package and propose a bounded reading/action plan;
2. **execution mode** — implement code only inside `task.scope.allowed` while ACG verifies externally.

## Orientation mode

Generate ACG:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Then prompt Codex:

```txt
Open .acg/ACG_MASTER.md first and follow it exactly.
```

Codex should return:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files actually read
RISKS: key risks before deeper processing
QUESTIONS: objective approvals needed
NEXT: bounded Phase 2 plan
```

## Execution mode

Recommended workflow:

1. Ask Codex to produce or refine a task scope first.
2. Put that scope in `acg.yaml`.
3. Ask Codex to implement only inside `task.scope.allowed`.
4. Open a PR.
5. Let ACG CI verify externally.

Prompt:

```txt
You are operating under ACG. Read acg.yaml before editing. Edit only task.scope.allowed. Do not edit task.scope.forbidden. Do not claim verification success; CI verifies externally.
```

## Boundary

Natural language adapter files guide the agent. They do not enforce security. Mechanical enforcement comes from `acg-enforce.py`, external verification, and CI evidence.
