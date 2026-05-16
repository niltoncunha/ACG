# Known Limitations

ACG is intentionally limited.

It is a structural guidance, topology-aware context, and enforcement layer.
It is not a complete software safety system.

---

## Cooperative guidance vs enforcement

ACG has two distinct control levels.

| Layer | Control type |
|---|---|
| `AGENTS.md`, adapter docs, prompts | Cooperative guidance only |
| `acg-gateway.py` | Advisory gate (not sandbox) |
| `acg-enforce.py`, CI, branch/scope | Mechanical enforcement |

Markdown instructs a compliant model. Markdown cannot physically stop a model with direct filesystem access.

`acg-gateway.py` is useful when the agent is configured to route through it. It is **not a sandbox** unless the runtime environment independently blocks direct reads through Docker, seccomp, OS permissions, or equivalent controls. This is GAP-04 in the formal gap register.

If the agent can directly read any local file, ACG can detect, structure, and audit the workflow, but it cannot guarantee read prevention without OS-level sandboxing.

---

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
- semantic conflicts from parallel agent branches (GAP-05);
- direct reads by agents with unrestricted filesystem access (GAP-04);
- humans bypassing CI or branch protection;
- humans approving changes without understanding the material.

---

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

---

## Formal gap register v0.4-beta

These gaps are machine-readable in `schemas/readiness_invariants.json`.

### GAP-01 - JS/TS path aliases  
Severity: medium

The JS/TS import extractor resolves only relative imports such as `./path` and `../path`. Path aliases configured through `tsconfig.json` `paths`, such as `@/components/...`, are not resolved yet.

Impact: `in_degree` is underestimated for projects that use path aliases. `hotpath_score` topology component may be lower than the real structural centrality.

Workaround: Add alias-heavy files to the attention queue manually if the codebase uses path aliases heavily.

Roadmap: v0.4-final.

### GAP-02 - Dynamic imports  
Severity: low

Dynamic `import('./module')` calls in JS/TS are not captured by the current regex extractor.

Impact: files loaded dynamically will have underestimated `in_degree`.

### GAP-03 - Python stem fallback  
Severity: low

When path resolution fails, the Python extractor falls back to matching the module leaf name against the file stem index. Two modules with the same stem can produce false positives.

Mitigation: fallback only activates when path reconstruction fails. Impact is limited in well-structured repositories.

### GAP-04 - Gateway is advisory  
Severity: design boundary

`acg-gateway.py` is a cooperative gate. Agents with direct filesystem access can bypass it entirely.

Formal position: ACG detects, structures, and audits. It does not prevent reads without OS-level runtime enforcement.

If you need hard read prevention: run the agent in a Docker container or equivalent restricted runtime with filesystem mounts restricted to allowed paths. Use ACG's `acg.yaml` forbidden list as the source of truth for mount restrictions.

### GAP-05 - Multi-agent branch conflicts  
Severity: medium

ACG enforces isolated branches per agent session. It does not detect semantic conflicts between two agents working on separate branches with overlapping scope until merge time.

Roadmap: v0.5.

---

## Practical interpretation

ACG improves structure, containment, guidance, scope, and auditability.

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
