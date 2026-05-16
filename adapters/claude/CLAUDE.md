# Claude Code Adapter

Claude Code can be used with ACG in two modes:

1. **orientation mode** — read the generated `.acg/` package and propose a bounded plan;
2. **execution mode** — edit code inside a declared scope while ACG verifies externally.

This file is context only. Enforcement is performed by `acg.yaml`, `scripts/acg-enforce.py`, and CI.

## Orientation mode

Generate ACG:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Then tell Claude:

```txt
Open .acg/ACG_MASTER.md first and follow it exactly.
```

Claude must not ask the human to invent the next prompt. It should return `SCOPE`, `RISKS`, `QUESTIONS`, and a bounded `NEXT` block.

## Execution mode

Before editing:

1. Read `acg.yaml`.
2. Respect `task.scope.allowed`.
3. Do not touch `task.scope.forbidden`.
4. Do not claim tests passed unless external evidence exists.
5. Prefer small, scoped changes.

Open a PR and let ACG CI decide promotion.

## Boundary

`ACG_MASTER.md` and this adapter are guidance, not a sandbox. Mechanical enforcement comes from branch/scope checks, external verification, and CI evidence.
