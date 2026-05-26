# CORPUS.GAUNTLET — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: CORPUS.GAUNTLET
::CHAIN-STAGE:: CORPUS.GAUNTLET
::PREVIOUS-STAGE:: CORPUS.RESULTADOS
::NEXT-STAGE:: CORPUS.PROMOCAO.SEQUENCIAL
::DOCFIELD-CANON:: RM.DocFIELD
::GAUNTLET-RULE:: explicit_pass_fail_required
```

## CAPA

```yaml
doc_id: corpus.gauntlet.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
status: EM_TESTE
previous_stage_ref: corpus.resultados.tsd.crossrupture.discovery.base
next_stage_target: CORPUS.PROMOCAO.SEQUENCIAL
```

## CASOS ADVERSARIAIS

| id | caso | criterio | resultado | decisao |
|---|---|---|---|---|
| G001 | documento vira centro visual | falha se documento for no central | nao ocorreu | PASS |
| G002 | simulado vira prova | falha se SIMULADO for promovido | nao ocorreu | PASS |
| G003 | falta autoridade simbolica | falha para promocao executiva | lacuna persiste | FAIL_EXEC |
| G004 | falta corpus multimodal | falha para canonico forte | lacuna persiste | FAIL_CANON |
| G005 | pendencias base minima | falha se impedir overview | nao impediu | PASS_COND |

## DECISAO

```yaml
gauntlet_result:
  documentary_chain: PASS_CONDICIONADO
  executive_promotion: FAIL
  canonical_promotion: FAIL
  reason: "Cadeia documental coerente, mas lacunas impedem promocao forte."
```

## HANDOFF

```yaml
handoff:
  status: PRONTO_PARA_CORPUS.PROMOCAO.SEQUENCIAL
  target: CORPUS.PROMOCAO.SEQUENCIAL
  blockers_for_promotion:
    - autoridade_simbolica_incompleta
    - corpus_multimodal_ausente
    - sem_medicao_real
```

OBSIDIAN: [crossrupture.discovery.base:corpus-gauntlet]
