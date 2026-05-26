# SPEC / REGENEGIS v2.1.2-TEST

## Função

Classificar a sobra de análise antes de permitir gênese.

## Entradas oficiais

```text
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
```

## Derivados oficiais

### residue_absorption_estimate

```text
residue_absorption_estimate =
  0.40 * (1 - coverage_score)
+ 0.30 * irreducibility_index
+ 0.30 * residue_stability_score
```

### novelty_support

```text
novelty_support =
  0.40 * residue_stability_score
+ 0.35 * residue_absorption_estimate
+ 0.25 * case_echo_strength
```

Nota: pesos são andaime de TEST, não tecnologia final.

## case_echo_strength

```text
0.00-0.39 = sem eco
0.40-0.59 = eco fraco
0.60-0.69 = eco moderado
>=0.70   = eco forte
```

Default sem histórico:

```text
case_echo_strength = 0.50
```

## is_hard_noisy

```text
is_hard_noisy =
  object_integrity_score < 0.45
  OR object_fragility > 0.70
  OR signal_density < signal_floor
```

## Ordem oficial do classificador

```text
P0 hard_noisy
P1 self_application
P2 high_risk
P3 simple_reading
P4 obvious_noise
P5 combinatory
P6 novel_strong
P7 novel_borderline
P9 fallback_shadow
```

P8 foi removido em v2.1.2-TEST porque era qualitativo demais.

## Regras

### P0 hard_noisy

```text
if is_hard_noisy == true
or object_integrity_score < 0.45:
  route = blocked
```

### P1 self_application

```text
if is_self_application == true:
  route = meta_shadow
```

### P2 high_risk

```text
if risk_profile == high:
  route = shadow
  allow_GENESIS = false
```

### P3 simple_reading

```text
if coverage_score >= 0.85
and irreducibility_index < 0.50:
  route = reading
```

### P4 obvious_noise

```text
if irreducibility_index < 0.42
and residue_stability_score < 0.46:
  route = shadow
```

### P5 combinatory

```text
if coverage_score >= 0.60
and irreducibility_index < 0.69
and residue_stability_score < 0.68:
  route = reweave
```

### P6 novel_strong

```text
if irreducibility_index >= 0.69
and residue_stability_score >= 0.68
and novelty_support >= 0.60
and (
  coverage_score <= 0.68
  OR conflict_index >= 0.52
  OR residue_absorption_estimate >= 0.68
)
and (
  object_fragility <= 0.52
  OR (
    object_fragility <= 0.60
    AND case_echo_strength >= 0.70
  )
):
  route = genesis_candidate
```

### P7 novel_borderline

```text
if irreducibility_index >= 0.65
and residue_stability_score >= 0.60
and novelty_support >= 0.55:
  route = quarantine
```

### P5 + P7 simultâneos

```text
if P5_COMBINATORY == true
and P7_NOVEL_BORDERLINE == true:
  route = quarantine
```

A exceção vence a prioridade.

### P9 fallback

```text
else:
  route = shadow
```

## TRISEAL no TEST

```text
TRISEAL = human_review_gate
```

No TEST, TRISEAL não é automação. É revisão humana final para `genesis_candidate`.

## Saídas finais

```text
blocked
meta_shadow
shadow
reading
reweave
quarantine
genesis_candidate
```

## Proibições de versão

- Não reabrir S7-alpha.
- Não retornar para v2.4-CANON.
- Não usar v2.1 calibrada/híbrida como spec soberana.
- Não adicionar operador, lattice interno ou SevenD antes da bateria de campo.
