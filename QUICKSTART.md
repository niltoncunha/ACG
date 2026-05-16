# Quickstart

This is the recommended v0.4-alpha flow.

## 1. Generate the ACG context package

From the repository you want to inspect, run:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Windows:

```powershell
python scripts\acg-v04.py --source "E:\path\to\project" --out ".acg"
```

Fast first run:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg --skip-lexical-index
```

This creates:

```txt
.acg/
  ACG_MASTER.md
  phase1_pack/
  artifacts/
    structure_map.md
    cluster_map.md
    surface_summaries.md
    phase1_queue.md
    phase2_queue.md
    approval_required.md
    search_targets.md
    execution_brief.md
    next_prompt.md
    phase2_plan_template.md
    context_payload.json
    performance_report.md
```

## 2. Give the AI one instruction

```txt
Open .acg/ACG_MASTER.md first and follow it exactly.
```

Do not manually design the next prompt. The generated ACG files tell the AI what to read, what not to read, and how to return the next bounded plan.

## 3. Approve or reject the NEXT block

The AI should return:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files actually read
RISKS: key risks before deeper processing
QUESTIONS: objective approvals needed
NEXT: bounded Phase 2 plan
```

Approve only an exact file list.

Do not approve open-ended requests like:

```txt
Let me inspect the repository.
```

Prefer:

```txt
ACG Phase 2 approved for reading only.
Open only these files:
1. <file>
2. <file>
Do not edit files.
Do not open search_only, terminal_asset, legacy, logs, exports, binary/database files.
```

## 4. Add enforcement to a coding repo

For actual code changes, copy these into the target repository:

```txt
acg.yaml
scripts/acg-enforce.py
.github/workflows/acg.yml
KNOWN_LIMITATIONS.md
```

Configure `acg.yaml`:

```yaml
task:
  id: auth-refactor-001
  description: "Refactor auth module"
  scope:
    allowed:
      - src/auth/**
      - tests/auth/**
    forbidden:
      - migrations/**
      - .env
```

Run locally:

```bash
python scripts/acg-enforce.py --config acg.yaml --mode all
```

Then open a PR and let CI verify externally.

## 5. Optional gateway read control

`acg-gateway.py` can read only files allowed in a selected phase:

```bash
python scripts/acg-gateway.py list --acg .acg --phase 1
python scripts/acg-gateway.py read --acg .acg --phase 1 --path 00_core/README.md
```

For Phase 2 reads:

```bash
python scripts/acg-gateway.py read --acg .acg --phase 2 --source /path/to/project --path src/index.ts
```

This is not a full sandbox unless the agent is forced to read through the gateway.

## 6. Optional guardrail example

If the problem is bad AI intake rather than code scope, open:

```txt
examples/acg-guardrail/index.html
```

That example guides the human before the model starts summarizing, comparing, or concluding.
