# REGENEGIS / HANDOFF_TO_FIELD_TEST

## Objetivo

Rodar bateria de campo real controlada para decidir se REGENEGIS v2.1.2-TEST permanece em GO_CONDICIONAL, sobe para GO controlado no TESSERUS ou retorna para ajuste.

## Versão sob teste

```text
REGENEGIS v2.1.2-TEST
```

## Corpus mínimo

```text
simples: 5
ruído sedutor: 5
combinatório: 5
novidade limpa: 5
novidade suja: 5
meta / alto risco: 5
total mínimo: 30
```

## Corpus ideal

```text
50 a 72 casos reais
```

## Métricas obrigatórias

```text
headline_accuracy
operational_accuracy
true_novel_recall
false_genesis
high_risk_overpromotion
meta_inflation
catastrophic_errors
quarantine_precision
reweave_precision
```

## Critério de GO controlado

```text
false_genesis = 0
high_risk_overpromotion = 0
meta_inflation = 0
catastrophic_errors = 0
true_novel_recall >= 70%
operational_accuracy >= 95%
```

## Registro por caso

Cada caso real deve registrar:

```text
case_id
source_type
input_summary
expected_route
actual_route
coverage_score
conflict_index
irreducibility_index
residue_stability_score
case_echo_strength
object_fragility
object_integrity_score
risk_profile
is_self_application
is_hard_noisy
signal_density
residue_absorption_estimate
novelty_support
human_review_note
result
```

## Regras

- Não ajustar thresholds durante a bateria.
- Não adicionar operador novo.
- Não reabrir arquitetura.
- Registrar erro como erro, não reinterpretar depois.
- `genesis_candidate` exige TRISEAL humano no TEST.
- Alto risco nunca pode virar `genesis_candidate`.
- Autoaplicação vai para `meta_shadow`.

## Resultado esperado

Após a bateria, emitir:

```text
FIELD_TEST_REPORT
DECISION: GO | GO_CONDICIONAL | NO-GO | RETORNAR_DISCOVERY
PATCH_MIN: se necessário
```
