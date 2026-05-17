# Known Limitations

ACG is intentionally limited.

It is a structural guidance, ownership-aware scouting, topology-aware context, and enforcement layer.
It is not a complete software safety system.

---

## Cooperative guidance vs enforcement

ACG has distinct control levels.

| Layer | Control type |
|---|---|
| `AGENTS.md`, adapter docs, prompts | Cooperative guidance only |
| `phase1_reading_order.md`, `citation_check.md` | Cooperative proof-of-reading friction |
| `acg-gateway.py` | Advisory gate, not sandbox |
| `acg-enforce.py`, CI, branch/scope | Mechanical enforcement |

Markdown instructs a compliant model. Markdown cannot physically stop a model with direct filesystem access.

`phase1_reading_order.md` and `citation_check.md` reduce shallow self-reporting, but they are not cryptographic or mechanical proof that the model understood the files.

`acg-gateway.py` is useful when the agent is configured to route through it. It is **not a sandbox** unless the runtime environment independently blocks direct reads through Docker, seccomp, OS permissions, ACLs, mount restrictions, or equivalent controls.

If the agent can directly read any local file, ACG can detect, structure, guide, and audit the workflow, but it cannot guarantee read prevention without OS-level sandboxing.

---

## Mitigated in v0.4-beta

These were important limitations in earlier v0.4 discussions and are now partially mitigated.

### Hotpath was too heuristic

Earlier Scout behavior could over-rank files because of names or folders alone.

v0.4-beta adds:

- `ownership_class`;
- `in_degree` / `out_degree` / `topology_score` for `PROJECT_OWNED` source files;
- import graph restricted to project-owned code;
- score caps for runtime/dependency/reference material.

Remaining limitation: import graph coverage is still language- and pattern-limited.

### Runtime/dependency files could pollute the top queue

Large backups may contain `site-packages`, installed runtimes, plugin repositories, caches or toolchains.

v0.4-beta classifies those as:

```txt
VENDORED_DEPENDENCY
TOOL_RUNTIME
GENERATED_CACHE
REFERENCE_ASSET
UNKNOWN_EXTERNAL
```

Those files are excluded from the main import graph and cannot normally win the primary hotpath queue.

Remaining limitation: unusual project layouts may still need `.acgignore` or explicit task scoping.

### Documentation or agent workspaces could be falsely halted

Earlier readiness logic was too codebase-centric.

v0.4-beta adds `project_kind` and readiness subscores:

```txt
CODEBASE
AGENT_WORKSPACE
DOCUMENTATION_BUNDLE
MIXED_REPO
DATASET_OR_CORPUS
TOOL_RUNTIME
UNKNOWN
```

For agent/documentation workspaces, orientation entrypoints and structural contracts can satisfy readiness.

Remaining limitation: project-kind classification is heuristic and needs more fixtures.

### Phase 1 could be shallow self-reporting

Earlier generated packages asked for `ACG-UNDERSTOOD`, but did not force a more concrete reading check.

v0.4-beta adds:

```txt
phase1_reading_order.md
citation_check.md
```

Remaining limitation: citation checks prove file contact better than pure self-report, but do not prove deep semantic mastery.

---

## Still true limitations

ACG does not protect against:

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
- humans approving changes without understanding the material;
- an AI fabricating citation-check answers unless the environment/tooling allows inspection of the actual reads.

---

## ACG does protect against

When the workflow is followed, ACG protects against:

- reading too much structure too early without prioritization;
- losing the repository/folder map before AI interpretation starts;
- treating a small sample as if it represented the whole folder;
- confusing target project files with runtimes/dependencies/tooling;
- opening terminal assets blindly;
- direct edits outside declared allowed paths;
- direct edits to forbidden paths;
- agentic work directly on the default branch;
- promotion without configured verification;
- treating agent self-report as proof;
- missing minimum audit evidence.

---

## Formal gap register v0.4-beta

### GAP-01 - JS/TS path aliases  
Severity: medium

The JS/TS import extractor resolves relative imports better than aliases. Path aliases configured through `tsconfig.json` `paths`, such as `@/components/...`, are not fully resolved yet.

Impact: `in_degree` may be underestimated for projects that use path aliases. `hotpath_score` topology component may be lower than the real structural centrality.

Workaround: add alias-heavy files to the attention queue manually or configure source roots explicitly in future versions.

Roadmap: v0.4 hardening / v0.5.

### GAP-02 - Dynamic imports and runtime module loading  
Severity: low/medium

Some dynamic imports and runtime module loading patterns are not captured.

Impact: files loaded dynamically may have underestimated `in_degree`.

### GAP-03 - Python stem fallback  
Severity: low

When path resolution fails, the Python extractor can fall back to matching the module leaf name against the file stem index. Two modules with the same stem can produce false positives.

Mitigation: fallback only activates when path reconstruction fails. Impact is limited in well-structured repositories.

### GAP-04 - Gateway is advisory  
Severity: design boundary

`acg-gateway.py` is a cooperative/advisory gate. Agents with direct filesystem access can bypass it entirely.

Formal position: ACG detects, structures, guides and audits. It does not prevent reads without OS-level runtime enforcement.

If you need hard read prevention: run the agent in a Docker container or equivalent restricted runtime with filesystem mounts restricted to allowed paths. Use ACG's `acg.yaml` forbidden list as the source of truth for mount restrictions.

### GAP-05 - Multi-agent branch conflicts  
Severity: medium

ACG enforces isolated branches per agent session. It does not yet detect semantic conflicts between two agents working on separate branches with overlapping scope until merge time.

Roadmap: v0.5.

### GAP-06 - Task-aware outside-scope relevance  
Severity: medium

ACG can classify files and map safe reading phases, but does not yet compute a task-aware `potentially_relevant_outside_scope` set.

Impact: an agent may need a file outside the current declared scope, and ACG currently handles that via human approval rather than proactive dependency relevance analysis.

Roadmap: v0.5.

### GAP-07 - Citation checks are not semantic proof  
Severity: design boundary

`citation_check.md` increases friction against shallow reading. It does not prove deep understanding, and it is still cooperative unless paired with tool-level read logging.

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
