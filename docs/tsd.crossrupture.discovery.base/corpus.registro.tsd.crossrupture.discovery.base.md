# CORPUS.REGISTRO — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: CORPUS.REGISTRO
::CHAIN-STAGE:: CORPUS.REGISTRO
::PREVIOUS-STAGE:: CORPUS.RELATORIO
::NEXT-STAGE:: CORPUS.ASSINADO
::DOCFIELD-CANON:: RM.DocFIELD
```

## CAPA

```yaml
doc_id: corpus.registro.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
status: EM_TESTE
previous_stage_ref: corpus.relatorio.tsd.crossrupture.discovery.base
next_stage_target: CORPUS.ASSINADO
```

## REGISTRO INDEXAVEL

```yaml
registry_entry:
  corpus_family: crossrupture.discovery.base
  corpus_stage: REGISTRO
  corpus_state: coerente_com_ressalvas
  final_state_candidate: SUSPENSO
  docend_allowed: false
  protoexec_allowed: false
  reason: "cadeia documental registrada, mas lacunas fortes permanecem abertas"
```

## INDICE DE ARTEFATOS CORPUS

```yaml
corpus_files:
  - corpus.overview.tsd.crossrupture.discovery.base.md
  - corpus.prontidao.tsd.crossrupture.discovery.base.md
  - corpus.pseudoruntime.tsd.crossrupture.discovery.base.md
  - corpus.resultados.tsd.crossrupture.discovery.base.md
  - corpus.gauntlet.tsd.crossrupture.discovery.base.md
  - corpus.promocao.sequencial.tsd.crossrupture.discovery.base.md
  - corpus.auditoria.tsd.crossrupture.discovery.base.md
  - corpus.relatorio.tsd.crossrupture.discovery.base.md
  - corpus.registro.tsd.crossrupture.discovery.base.md
```

## BLOQUEIOS REGISTRADOS

```yaml
registered_blockers:
  - autoridade_simbolica_incompleta
  - corpus_de_calibracao_ausente
  - corpus_multimodal_ausente
  - sem_medicao_real
```

## HANDOFF

```yaml
handoff:
  status: PRONTO_PARA_CORPUS.ASSINADO
  target: CORPUS.ASSINADO
  final_state_candidate: SUSPENSO
```

OBSIDIAN: [crossrupture.discovery.base:corpus-registro]
