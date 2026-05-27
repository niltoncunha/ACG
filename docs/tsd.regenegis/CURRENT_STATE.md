# REGENEGIS / CURRENT_STATE

## Identidade

- **Nome canônico:** REGENEGIS
- **Versão:** v2.1.2-TEST
- **Estado de ciclo:** TEST
- **Decisão de promoção:** GO_CONDICIONAL
- **GO final:** NÃO
- **Canônico:** NÃO
- **Runtime soberano:** NÃO

## Escopo

REGENEGIS é um componente candidato para classificar sobra de análise antes de permitir gênese.

Ele atua sobre resíduos de análise e decide rota entre:

```text
blocked | meta_shadow | shadow | reading | reweave | quarantine | genesis_candidate
```

## Teto de claim

- **FATO:** a versão v2.1.2-TEST está documentada neste pacote.
- **INFERENCIA_DOCUMENTADA:** o componente é promissor e elegível para bateria de campo real controlada, com base nas simulações e avaliações externas registradas.
- **SIMULADO:** os números existentes vêm de baterias simuladas/focais; não são prova de campo.
- **LACUNA:** ainda falta bateria de campo real e verificação com corpus real.

## Decisão atual

```text
GO_CONDICIONAL para teste de campo real.
```

Critério para subir posteriormente:

```text
false_genesis = 0
high_risk_overpromotion = 0
meta_inflation = 0
catastrophic_errors = 0
true_novel_recall >= 70%
operational_accuracy >= 95%
```

## Destino atual

```text
niltoncunha/tesserus/docs/tsd.regenegis/
```

## Próxima etapa

Rodar bateria de campo real controlada com 30 a 72 casos reais e registrar resultados em `TEST_STATUS.md` ou novo arquivo de resultados de campo.