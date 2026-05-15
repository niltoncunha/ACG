# Known Limitations

ACG is intentionally limited.

It is a structural guidance and enforcement layer, not a complete software safety system.

## ACG does not protect against

- semantic drift in code paths not covered by tests;
- weak or flaky test suites;
- unsafe database migrations;
- bad product decisions;
- bad architecture decisions;
- performance regressions not covered by verification;
- security bugs not covered by verification;
- external side effects caused by executed code;
- code written within scope that later performs effects outside scope;
- network calls or mutations performed by executed code;
- semantic conflicts from parallel agent branches;
- humans bypassing CI or branch protection;
- humans approving changes without understanding the material.

## ACG does protect against

- reading too much structure too early without prioritization;
- direct edits outside declared allowed paths;
- direct edits to forbidden paths;
- agentic work directly on the default branch;
- promotion without configured verification;
- treating agent self-report as proof;
- missing minimum audit evidence.

## Practical interpretation

ACG improves structure, containment, guidance, scope and auditability.

It does not make AI systems automatically correct or safe.

The right question is not:

```txt
Did the AI do it right?
```

The better question is:

```txt
Was the work structurally guided,
properly scoped,
externally verified,
evidenced,
and blocked on failure?
```
