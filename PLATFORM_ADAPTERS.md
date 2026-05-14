# Platform Adapters

ACG-Core is platform-neutral. Use your agent normally, but keep enforcement in CI.

## Universal agent prompt

```txt
You are operating under ACG-Core.
Read acg.yaml before editing.
Edit only files allowed by task.scope.allowed.
Do not edit task.scope.forbidden.
Do not claim verification success.
External verification and merge gating are handled by CI.
```

## Claude Code

Use `CLAUDE.md` as context. Keep enforcement in `acg.yaml` and CI.

## Codex

Use `AGENTS.md` / `CODEX.md` for guidance. Ask for scope first, then implementation.

## Cursor

Use `.cursor/rules/acg.mdc` as project guidance. Cursor edits; ACG gates.

## Aider

Add only allowed files to context where possible. Keep commits small. Let CI enforce.

## Devin / autonomous agents

Use one task per slice. Avoid broad missions such as `refactor the repo`.
