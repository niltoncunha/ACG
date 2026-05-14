# ACG-Core

**Agentic Code Governance Core** is a minimal mechanical enforcement layer for AI coding agents.

It is designed for teams using Codex, Claude Code, Cursor, Aider, Devin, Windsurf, Qwen, DeepSeek, Gemini, Grok, Kimi, Z.ai or any other agent that edits code.

ACG-Core is not a prompt framework. It is not a promise that agents will write correct code. It enforces the minimum conditions that make agentic code changes safer:

1. work happens outside the main branch;
2. changes stay inside declared scope;
3. verification is executed outside the agent;
4. promotion fails closed unless evidence exists.

## Why this exists

AI coding failures usually happen when agents are asked to do large, open-ended work without containment:

```txt
refactor this whole codebase
```

Common outcomes: the app stops compiling, tests fail, files outside the intended scope are modified, the agent claims tests passed without reliable proof, the diff becomes too large to review, and rollback is unclear.

ACG-Core prevents the most common catastrophic workflow failures. It does not solve every semantic, product, security or architectural problem.

## What ACG-Core protects against

- direct edits outside allowed paths;
- code promotion without external verification;
- trusting agent self-reports as proof;
- missing minimum audit evidence;
- accidental mutation of the main branch;
- scope creep in agentic tasks.

## What ACG-Core does not protect against

- semantic drift in untested code paths;
- weak or flaky test suites;
- unsafe database migrations;
- bad architecture decisions;
- external side effects caused by code execution;
- code written inside scope that later performs effects outside scope;
- security or performance issues not covered by verification;
- semantic conflicts from parallel agent branches;
- human rubber-stamping under pressure.

See [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md).

## Quick install

Copy these files into your repository:

```txt
acg.yaml
scripts/acg-enforce.py
.github/workflows/acg.yml
KNOWN_LIMITATIONS.md
```

Then edit `acg.yaml` for your task.

## Minimal `acg.yaml`

```yaml
project:
  name: example-project
  default_branch: main

task:
  id: example-task-001
  description: "Short task description"
  scope:
    allowed:
      - src/**
      - tests/**
    forbidden:
      - .env
      - .env.*
      - secrets/**
      - infra/**
      - migrations/**
  done_when:
    - command: "npm test"

verify:
  commands:
    - npm test
    - npm run typecheck
    - npm run build

promotion:
  fail_closed: true
  require_evidence: true
```

## Local usage

```bash
python3 scripts/acg-enforce.py --config acg.yaml --mode all
```

Available modes:

```bash
python3 scripts/acg-enforce.py --mode branch
python3 scripts/acg-enforce.py --mode scope
python3 scripts/acg-enforce.py --mode verify
python3 scripts/acg-enforce.py --mode done
python3 scripts/acg-enforce.py --mode gate
python3 scripts/acg-enforce.py --mode all
```

The script writes evidence to:

```txt
acg-evidence.jsonl
```

## GitHub Actions usage

```yaml
name: ACG Enforcement
on:
  pull_request:
  workflow_dispatch:

jobs:
  acg:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: ACG Core
        run: python3 scripts/acg-enforce.py --config acg.yaml --mode all
```

The PR should not be merged unless the ACG workflow passes.

## How to use with any AI coding agent

1. Create a branch.
2. Define task scope in `acg.yaml`.
3. Ask the agent to edit only allowed paths.
4. Open a PR.
5. Let ACG run in CI.
6. Merge only when ACG passes and evidence exists.

The agent can help write code. The agent is not the authority that the code is safe.

## License

Free and open source under the MIT License.

Copyright (c) 2026 Nilton Cunha.
