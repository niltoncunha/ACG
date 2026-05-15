# ACG-Core

**Agentic Code Governance Core** is a minimal mechanical governance layer for AI-assisted software work.

ACG-Core is built for teams using tools such as Codex, Claude Code, Cursor, Aider, Devin, Windsurf, Gemini, Grok, DeepSeek, Qwen, Kimi, Z.ai and similar systems.

It is not a prompt framework. It is an enforcement core.

## System control map

```txt
+======================================================================+
|                              ACG-CORE                                |
|              Agentic Code Governance / Enforcement Core              |
+======================================================================+

  MISSION
  --------------------------------------------------------------------
  Convert open-ended AI code changes into scoped, verified, auditable
  pull requests.

  CONTROL LOOP
  --------------------------------------------------------------------

      [01] ISOLATED BRANCH
              |
              v
      [02] DECLARED TASK SCOPE
              |
              v
      [03] AI CODE EXECUTION
              |
              v
      [04] SCOPE CHECK
              |
              v
      [05] EXTERNAL VERIFY
              |
              v
      [06] EVIDENCE RECORD
              |
              v
      [07] PROMOTION GATE

+======================================================================+
|  The model proposes code. ACG-Core controls scope, evidence and gate. |
+======================================================================+
```

## Four hard rules

1. Work outside the default branch.
2. Declare task scope before execution.
3. Verify outside the model.
4. Block promotion when evidence is missing or failed.

## Repository map

- `SPEC.md` — core specification.
- `QUICKSTART.md` — setup and first use.
- `USER_GUIDE.md` — user workflow.
- `PLATFORM_ADAPTERS.md` — Claude, Codex, Cursor and Aider guidance.
- `KNOWN_LIMITATIONS.md` — explicit limits.
- `acg.yaml` — governance configuration.
- `scripts/acg-enforce.py` — enforcement runner.
- `.github/workflows/acg.yml` — GitHub Actions gate.

## Status

Current package: **ACG-Core v0.2**.

Implemented: branch check, scope check, external verification runner, done_when checks, JSONL evidence, promotion gate, GitHub Actions workflow, adapters and MIT license.

## License

Free and open source under the MIT License.

Copyright 2026 Nilton Cunha.
