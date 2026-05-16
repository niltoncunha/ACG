# Roadmap

## Current: v0.4-alpha

Goal: make large-codebase AI work topology-aware without making ACG heavy or hard to install.

Delivered:

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

Non-goal for v0.4-alpha:

- full sandboxing;
- embeddings/RAG as a dependency;
- MCP gateway requirement;
- replacing CI/review/testing;
- changing `acg-enforce.py` unless needed.

---

## v0.4-beta

Focus: make topological scoring affect the primary Scout decisions.

Planned:

- integrate `in_degree` / `out_degree` into `hotpath_score`;
- rank high-centrality files above merely well-named files;
- add benchmark fixture where a high `in_degree` utility outranks a low-centrality core-looking file;
- add tests for import graph extraction;
- add tests for surface summaries;
- document performance on 10k+ file repositories.

Success criterion:

```txt
a file with in_degree 45 should rank above a similarly safe file with in_degree 2,
even if the second file has a more attractive name or folder.
```

---

## v0.5

Focus: stronger read-control and enforcement integration.

Planned:

- gateway-first workflow for agents that support tool mediation;
- optional MCP/tool wrapper;
- stricter evidence trail for reads;
- phase approval ledger;
- clearer distinction between cooperative guidance and hard enforcement.

Non-goal:

- pretending Markdown instructions are a sandbox.

---

## v0.6

Focus: semantic retrieval.

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
