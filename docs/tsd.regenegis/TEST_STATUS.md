# REGENEGIS / TEST_STATUS

## Estado

- **Versão:** v2.1.2-TEST
- **Status:** GO_CONDICIONAL
- **Tipo de evidência atual:** SIMULADO + avaliação externa por Claude
- **Campo real:** ainda não executado

## Resultado focal registrado

Bateria focal de 20 casos:

```text
headline_accuracy = 19/20
operational_accuracy = 100% sem contar o caso ambíguo como falha operacional
true_novel_recall = 4/4 na bateria focal
false_genesis = 0
high_risk_overpromotion = 0
meta_inflation = 0
catastrophic_errors = 0
```

## Diagnóstico da validação focal

O núcleo está sólido para TEST.

Problemas encontrados foram de especificação:

1. `conflict_index` usado mas não declarado.
2. P5 e P7 podiam passar juntos sem precedência explícita.
3. P8 qualitativo demais.
4. `is_hard_noisy` precisava origem declarada.
5. TRISEAL precisava teto de automação declarado.

Todos foram fechados em v2.1.2-TEST.

## Critério para subir após campo real

```text
false_genesis = 0
high_risk_overpromotion = 0
meta_inflation = 0
catastrophic_errors = 0
true_novel_recall >= 70%
operational_accuracy >= 95%
```

## Bateria de campo mínima

```text
simples: 5
ruído sedutor: 5
combinatório: 5
novidade limpa: 5
novidade suja: 5
meta / alto risco: 5
total mínimo: 30
```

## Bateria de campo ideal

```text
50 a 72 casos reais
```

## Teto

Enquanto não houver campo real:

```text
PROVADO = não
GO final = não
CANONICO = não
```
