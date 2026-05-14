# Known Limitations

ACG-Core is intentionally limited. It is a minimum enforcement layer, not a complete safety system.

## ACG-Core does not protect against

- Semantic drift in code paths not covered by tests.
- Weak test suites.
- Flaky tests and false confidence from unstable verification.
- Unsafe database migrations.
- Bad product decisions.
- Bad architecture decisions.
- Performance regressions not covered by verification.
- Security bugs not covered by verification.
- External side effects caused by code execution.
- Code written within scope that later executes effects outside scope.
- Network calls or system mutations performed by executed code.
- Semantic conflicts from parallel agent branches with non-overlapping scopes.
- Human reviewers approving without real context.
- Teams disabling or bypassing CI gates under deadline pressure.

## ACG-Core does protect against

- Direct edits outside declared allowed paths.
- Direct edits to declared forbidden paths.
- Running agentic work directly on the default branch.
- Promoting changes without running configured external verification.
- Treating an agent's self-report as proof.
- Missing minimum evidence for verification.

## Practical interpretation

ACG-Core improves containment. It does not make agents safe by itself.

The right question is not:

```txt
Did the AI do it right?
```

The right question is:

```txt
Was the change scoped, externally verified, evidenced, and blocked on failure?
```
