# Gemini CLI Adapter

Gemini CLI can be used with ACG in two modes:

1. **orientation mode** — Gemini reads the generated `.acg/` package and proposes a bounded reading/action plan;
2. **execution mode** — Gemini edits code inside a declared task scope while ACG verifies externally.

ACG remains the guidance, scope, verification, and promotion gate.

```txt
Gemini CLI = agent
ACG = structure + topology + scope + evidence + gate
Git/CI = promotion control
```

---

## Orientation mode: recommended first step

Generate the ACG package:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg
```

Fast mode:

```bash
python scripts/acg-v04.py --source /path/to/project --out .acg --skip-lexical-index
```

Then prompt Gemini:

```txt
Open .acg/ACG_MASTER.md first and follow it exactly.
```

Gemini should read only what `ACG_MASTER.md` allows, then return:

```txt
ACG-UNDERSTOOD: structure-scout
SCOPE: files actually read
RISKS: key risks before deeper processing
QUESTIONS: objective approvals needed
NEXT: bounded Phase 2 plan
```

Do not approve open-ended exploration. Approve only exact file lists.

---

## Execution mode: scoped code work

### 1. Create a branch

```bash
git checkout -b acg/gemini-smoke
```

### 2. Configure a small task in `acg.yaml`

```yaml
project:
  name: acg-gemini-smoke
  default_branch: main

task:
  id: gemini-smoke-001
  description: "Improve README wording only"
  scope:
    allowed:
      - README.md
    forbidden:
      - scripts/**
      - .github/**
      - .env
      - .env.*
      - secrets/**
  done_when:
    - command: "python3 scripts/acg-enforce.py --config acg.yaml --mode scope"

verify:
  commands:
    - python3 scripts/acg-enforce.py --config acg.yaml --mode scope

promotion:
  fail_closed: true
  require_evidence: true
```

### 3. Prompt Gemini CLI

```txt
You are operating under ACG.

Read acg.yaml first.

Task:
Improve only the wording of README.md.

Rules:
- Edit only README.md.
- Do not edit scripts, workflows, configs, secrets, or any other file.
- Do not claim verification success.
- After editing, summarize what changed.
- External verification will be run outside you.
```

### 4. Run ACG outside Gemini

```bash
python3 scripts/acg-enforce.py --config acg.yaml --mode all
```

Expected successful output includes:

```txt
ACG branch passed
ACG scope passed
ACG verify passed
ACG done_when passed
ACG gate passed
```

---

## Negative test

After the smoke test, intentionally ask Gemini to go out of scope:

```txt
Also update scripts/acg-enforce.py if needed.
```

If Gemini edits `scripts/acg-enforce.py`, ACG should block the change because the file is outside the allowed scope.

Expected behavior:

```txt
ACG SCOPE FAILED
```

This is a good result. It means the gate works.

---

## Safety notes

- Do not give Gemini broad write scope for large refactors.
- Do not let Gemini touch secrets, production configs, migrations, or CI unless explicitly intended.
- Do not trust text such as "tests passed" unless ACG/CI produced evidence.
- Use one task per branch.
- Prefer small, reversible changes.
- Remember: `ACG_MASTER.md` is guidance, not a filesystem sandbox.
