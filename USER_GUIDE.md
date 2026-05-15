# User Guide

ACG-Core is used around your coding agent, not inside it.

## Daily workflow

1. Create a branch.
2. Define the task in `acg.yaml`.
3. Run your agent with clear scope.
4. Open a pull request.
5. Let ACG run in CI.
6. Merge only when ACG passes.

## What to tell the agent

```txt
You are operating under ACG-Core.
Read acg.yaml before editing.
Edit only task.scope.allowed.
Do not edit task.scope.forbidden.
Do not claim verification success.
CI will verify externally.
```

## What to check as a human

- Did the change stay inside the declared scope?
- Did CI run verification externally?
- Is there evidence?
- Is the diff small enough to understand?
- Are the limitations relevant to this PR?

## Intake before execution

If the real problem is that the human is feeding the model badly, use `examples/acg-guardrail/` before running the agent.

That example forces:

- objetivo claro
- escopo material
- limite do que a AI pode fazer
- checkpoints humanos
- regra de parada
- contrato operacional copiavel

## When not to rely on ACG-Core alone

Use additional review for:

- database migrations;
- authentication and authorization;
- payments;
- production infrastructure;
- large refactors;
- low test coverage;
- security-critical code.
