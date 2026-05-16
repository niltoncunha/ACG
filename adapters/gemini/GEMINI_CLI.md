# Gemini CLI Adapter

Gemini CLI can be used with ACG as an execution agent.

ACG should remain the external guidance, scope, verification, and promotion gate.

```txt
Gemini CLI = executor
ACG = structure + scope + evidence + gate
Git/CI = promotion control
```

## Principle

Do not ask Gemini CLI to "use ACG by itself".

Use Gemini CLI to edit code inside a declared task scope, then let ACG verify externally.

The agent can propose code. It is not the authority that the code is safe, complete, scoped, or promotable.

---

## Minimal smoke test

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

## Recommended user workflow

```txt
1. User describes intent.
2. ACG helps turn vague intent into task scope.
3. Gemini CLI edits only inside the scope.
4. ACG verifies externally.
5. CI blocks promotion if evidence is missing or failed.
```

---

## Safety notes

- Do not give Gemini broad write scope for large refactors.
- Do not let Gemini touch secrets, production configs, migrations, or CI unless explicitly intended.
- Do not trust text such as "tests passed" unless ACG/CI produced evidence.
- Use one task per branch.
- Prefer small, reversible changes.
