# CORPUS.PROMOCAO.SEQUENCIAL — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: CORPUS.PROMOCAO.SEQUENCIAL
::CHAIN-STAGE:: CORPUS.PROMOCAO.SEQUENCIAL
::PREVIOUS-STAGE:: CORPUS.GAUNTLET
::NEXT-STAGE:: CORPUS.AUDITORIA
::DOCFIELD-CANON:: RM.DocFIELD
::SIGNATURE-RULE:: not_allowed_here
```

## CAPA

```yaml
doc_id: corpus.promocao.sequencial.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
status: EM_TESTE
previous_stage_ref: corpus.gauntlet.tsd.crossrupture.discovery.base
next_stage_target: CORPUS.AUDITORIA
```

## DECISAO DE PROMOCAO

```yaml
promotion_decision:
  document_chain_advance: true
  candidate_final_state: SUSPENSO
  docend_candidate: false
  protoexec_candidate: false
  reason: "Cadeia documental pode seguir para auditoria e registro, mas lacunas impedem estado final forte."
```

## BLOQUEIOS DE PROMOCAO FORTE

```yaml
blockers:
  - autoridade_simbolica_incompleta
  - corpus_de_calibracao_ausente
  - corpus_multimodal_ausente
  - sem_medicao_real
  - tabela_de_problema_forte_pendente
```

## HANDOFF

```yaml
handoff:
  status: PRONTO_PARA_CORPUS.AUDITORIA
  target: CORPUS.AUDITORIA
  final_state_candidate: SUSPENSO
  blockers: []
```

OBSIDIAN: [crossrupture.discovery.base:corpus-promocao]
