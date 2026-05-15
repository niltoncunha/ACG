# Quickstart

## 1. Copy files

Add these to your repository:

```txt
acg.yaml
scripts/acg-enforce.py
.github/workflows/acg.yml
KNOWN_LIMITATIONS.md
```

## 2. Configure task scope

Edit `acg.yaml`:

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

## 3. Use your agent

Tell the agent:

```txt
You are working under ACG-Core. Edit only paths allowed by acg.yaml. Do not claim verification success. CI will verify externally.
```

## 4. Run locally

```bash
python3 scripts/acg-enforce.py --config acg.yaml --mode all
```

## 5. Open PR

GitHub Actions should run ACG and block merge if scope or verification fails.

## 6. Optional: use the Guardrail example

If the problem is not coding scope but bad AI intake, open `examples/acg-guardrail/index.html`.

That example guides the human before the model starts summarizing, comparing or concluding.
