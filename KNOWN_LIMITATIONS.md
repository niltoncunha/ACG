# Known Limitations

ACG is intentionally limited.

It is a structural guidance, topology-aware context, and enforcement layer. It is not a complete software safety system.

## Cooperative guidance vs enforcement

ACG has two different control levels.

| Layer | Control type |
|---|---|
| `ACG_MASTER.md`, queues, prompts, adapter docs | Cooperative guidance |
| `acg-gateway.py` | Gateway control only if the agent uses it or is forced to use it |
| `acg-enforce.py`, CI, branch/scope checks | Mechanical enforcement |

Markdown can guide a model. Markdown cannot physically stop a model with direct filesystem access.

If the agent can directly read any local file, ACG can detect, structure, and audit the workflow, but it cannot guarantee read prevention unless the runtime enforces access through a gateway or sandbox.

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
- direct reads by agents with unrestricted filesystem access;
- humans bypassing CI or branch protection;
- humans approving changes without understanding the material.

## ACG does protect against

- reading too much structure too early without prioritization;
- losing the repository map before AI interpretation starts;
- treating a small sample as if it represented the whole codebase;
- opening terminal assets blindly when the process is followed;
- direct edits outside declared allowed paths;
- direct edits to forbidden paths;
- agentic work directly on the default branch;
- promotion without configured verification;
- treating agent self-report as proof;
- missing minimum audit evidence.

## v0.4-alpha limitations

- Static import extraction is best-effort and currently lightweight.
- Topology is valuable for code-heavy repositories; it may be small for documentation-heavy folders.
- `context_payload.json` is a compact payload format, not a full RAG system.
- The lexical index is dependency-free and lexical only; it is not semantic embeddings.
- `acg-gateway.py` is useful, but not a sandbox unless the environment blocks direct reads.
- `hotpath_score` is not yet fully driven by import graph centrality. That is planned for v0.4-beta.

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
