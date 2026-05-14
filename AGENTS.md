# Agent Context

This file is context for coding agents. It is not enforcement.

The real enforcement layer is:

```txt
acg.yaml
scripts/acg-enforce.py
GitHub Actions / CI
```

## Rules for agents

- Read `acg.yaml` before editing.
- Edit only paths in `task.scope.allowed`.
- Do not edit paths in `task.scope.forbidden`.
- Do not claim tests passed unless external evidence exists.
- Keep changes minimal.
- Do not touch secrets, production config, migrations, or infrastructure unless explicitly allowed.

## Final report format

```md
## Agent Report
- Task:
- Files changed:
- Scope concerns:
- Verification requested:
- Risks:
```
