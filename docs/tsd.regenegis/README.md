# TSD.REGENEGIS / README

## Status

- **Nome canônico:** REGENEGIS
- **Versão congelada:** v2.1.2-TEST
- **Estado:** TEST
- **Decisão:** GO_CONDICIONAL
- **GO final:** NÃO
- **Destino:** `niltoncunha/tesserus/docs/tsd.regenegis/`
- **Data de fechamento:** 2026-05-26

## Teto de claim

REGENEGIS está pronto para **bateria de campo real controlada**.

Não está canonizado como capacidade validada, não é GO final, não é runtime soberano e não deve ser tratado como prova de capacidade fora dos testes.

## Função

REGENEGIS classifica a sobra de análise antes de permitir gênese.

Ele governa a passagem entre:

```text
sobra bruta -> classificação -> rota permitida
```

Rotas principais:

```text
blocked | meta_shadow | shadow | reading | reweave | quarantine | genesis_candidate
```

## Núcleo fechado

```text
P0 hard_noisy       -> blocked
P1 self_application -> meta_shadow
P2 high_risk        -> shadow
P3 simple_reading   -> reading
P4 obvious_noise    -> shadow
P5 combinatory      -> reweave
P6 novel_strong     -> genesis_candidate
P7 novel_borderline -> quarantine
P9 fallback         -> shadow
```

## Evidência atual

- Simulação focal com 20 casos: 19/20 corretos, 0 falso GENESIS, 0 inflação meta, 0 promoção em risco alto, 0 erro catastrófico.
- Simulação agressiva anterior indicou núcleo defensivo forte, mas recall de novidade real baixo antes dos patches.
- Patches mínimos aplicados em v2.1.2-TEST: `conflict_index` declarado, conflito P5+P7 resolvido para `quarantine`, P8 removido, `is_hard_noisy` definido, TRISEAL declarado como revisão humana no TEST.

## Limite

SIMULADO não é PROVADO.

A próxima etapa obrigatória é bateria de campo real com corpus real e registro de métricas.

## Arquivos

- `CURRENT_STATE.md`
- `SPEC_REGENEGIS_v2.1.2-TEST.md`
- `DECISION_LOG.md`
- `TEST_STATUS.md`
- `OPEN_QUESTIONS.md`
- `AGENT_SYNC_PACKET.md`
- `HANDOFF_TO_FIELD_TEST.md`
