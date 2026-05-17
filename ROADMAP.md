# Roadmap

## Current: v0.4-beta experimental

Goal: make large-folder AI work structurally mapped, ownership-aware, topology-aware when code exists, and harder to fake during Phase 1 orientation.

Delivered in the v0.4 line:

### v0.4-alpha delivered

- single-command v0.4 orchestrator: `scripts/acg-v04.py`;
- stable Structure Scout component: `scripts/acg-scout.py`;
- compact phase queues;
- `ACG_MASTER.md` generated as the AI entrypoint;
- automatic continuation protocol via `next_prompt.md`;
- strict Phase 2 NEXT template;
- static import graph extractor;
- cluster map;
- surface summaries;
- optional context payload;
- performance report;
- topology cache;
- minimal gateway CLI;
- lightweight lexical index hook.

### v0.4-beta experimental delivered

- ownership-aware file classification:
  - `PROJECT_OWNED`
  - `VENDORED_DEPENDENCY`
  - `TOOL_RUNTIME`
  - `GENERATED_CACHE`
  - `REFERENCE_ASSET`
  - `UNKNOWN_EXTERNAL`
- main import graph restricted to `PROJECT_OWNED` source files;
- external/runtime/dependency files capped out of primary hotpath competition;
- adaptive `project_kind` classification:
  - `CODEBASE`
  - `AGENT_WORKSPACE`
  - `DOCUMENTATION_BUNDLE`
  - `MIXED_REPO`
  - `DATASET_OR_CORPUS`
  - `TOOL_RUNTIME`
  - `UNKNOWN`
- readiness subscores:
  - `code_readiness`
  - `orientation_readiness`
  - `dataset_readiness`
  - `runtime_penalty`
- readiness gate with configurable minimum score;
- scout regime detection:
  - `minimal`
  - `standard`
  - `extended`
  - `large`
- no-git environment detection:
  - `enforcement_level=full`
  - `enforcement_level=scout_only`
- explicit Phase 1 reading order;
- citation checks for Phase 1 proof-of-reading friction;
- `scout_report.json` as compact machine-readable summary without duplicating the full manifest.

Non-goals for v0.4-beta:

- full sandboxing;
- embeddings/RAG as a dependency;
- MCP gateway requirement;
- replacing CI/review/testing;
- full semantic understanding proof;
- task-aware outside-scope dependency relevance.

---

## v0.4-beta hardening

Focus: stabilize the new Scout behavior before expanding surface area.

Planned:

- tests for `project_kind` classification:
  - classic codebase;
  - agent workspace;
  - documentation bundle;
  - mixed repo;
  - dataset/corpus;
  - tool runtime;
  - unknown folder.
- tests for `ownership_class` classification;
- tests proving runtime/dependency files do not win primary hotpath ranking;
- tests proving `phase1_reading_order.md` and `citation_check.md` are generated;
- schema updates for the current `scout_report.json` contract;
- performance fixture for 10k+ file folders;
- documentation stabilization.

Success criteria:

```txt
1. A vendored dependency with high in_degree cannot outrank PROJECT_OWNED files in the primary queue.
2. A codebase with entrypoint/build controls is classified as CODEBASE.
3. An agent/documentation workspace with AGENTS.md + contracts is not falsely halted as a broken codebase.
4. A runtime-only folder is classified as TOOL_RUNTIME and does not silently pass readiness.
5. Phase 1 output requires citation checks, not only self-reported understanding.
```

---

## v0.5

Focus: stronger read-control and enforcement integration.

Planned:

- task-aware relevance map;
- potentially relevant outside-scope warnings;
- gateway-first workflow for agents that support tool mediation;
- optional MCP/tool wrapper;
- stricter evidence trail for reads;
- phase approval ledger;
- clearer distinction between cooperative guidance and hard enforcement;
- multi-agent branch conflict warning.

Non-goal:

- pretending Markdown instructions are a sandbox.

---

## v0.6

Focus: optional semantic retrieval.

Planned:

- optional embedding-backed semantic index;
- local or pluggable vector store;
- chunk-level search;
- token budget optimizer;
- payload compaction profiles.

Non-goal:

- making embeddings mandatory for basic ACG use.

---

## ACG-Core stable line

The enforcement core remains intentionally small:

- branch isolation;
- scope fence;
- forbidden path check;
- external verification;
- fail-closed evidence gate.

This layer should stay stable and boring.

---

## Principle

Do not make ACG impressive at the cost of adoption.

Every version must remain useful as a standalone layer.
