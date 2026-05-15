# Codex Adapter

Use Codex with ACG-Core as an external enforcement system.

Recommended workflow:

1. Ask Codex to produce a task scope first.
2. Put that scope in `acg.yaml`.
3. Ask Codex to implement only inside `task.scope.allowed`.
4. Open a PR.
5. Let ACG CI verify externally.

Prompt:

```txt
You are operating under ACG-Core. Read acg.yaml before editing. Edit only task.scope.allowed. Do not edit task.scope.forbidden. Do not claim verification success; CI verifies externally.
```
