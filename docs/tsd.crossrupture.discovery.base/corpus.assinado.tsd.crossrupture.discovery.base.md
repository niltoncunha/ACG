# CORPUS.ASSINADO — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: CORPUS.ASSINADO
::CHAIN-STAGE:: CORPUS.ASSINADO
::PREVIOUS-STAGE:: CORPUS.REGISTRO
::NEXT-STAGE:: SUSPENSO
::DOCFIELD-CANON:: RM.DocFIELD
::SIGNATURE-RULE:: final_freeze_only
```

## CAPA

```yaml
doc_id: corpus.assinado.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
status: SUSPENSO
previous_stage_ref: corpus.registro.tsd.crossrupture.discovery.base
final_state_signed: SUSPENSO
```

## ASSINATURA DOCUMENTAL

```yaml
signed_freeze:
  final_state: SUSPENSO
  docend_signed: false
  protoexec_signed: false
  reason: "Cadeia documental emitida e rastreavel, mas lacunas fortes impedem fechamento DocEND ou ProtoEXEC."
  frozen_scope: corpus_documental_crossrupture_discovery_base
```

## CAUSAS DA SUSPENSAO

```yaml
suspension_causes:
  - autoridade_simbolica_incompleta
  - corpus_de_calibracao_ausente
  - corpus_multimodal_ausente
  - sem_medicao_real
  - tabela_de_problema_forte_pendente
```

## O QUE FICA CONGELADO

```yaml
frozen:
  - trilho
  - rm_unification
  - rm_master
  - rm_componentes
  - rm_docfield
  - obsidian_componentes
  - obsidian_bases
  - corpus_overview
  - corpus_prontidao
  - corpus_pseudoruntime
  - corpus_resultados
  - corpus_gauntlet
  - corpus_promocao_sequencial
  - corpus_auditoria
  - corpus_relatorio
  - corpus_registro
```

## REGRA DE RETOMADA

```yaml
resume_when:
  - symbol_map_binder_lsu_available
  - calibration_corpus_available
  - multimodal_corpus_available
  - strong_problem_table_available
resume_target: CORPUS.PRONTIDAO
```

## INTEGRIDADE

```yaml
final_guard:
  no_docend_claim: true
  no_protoexec_claim: true
  no_runtime_claim: true
  no_production_state: true
  suspended_with_trace: true
```

OBSIDIAN: [crossrupture.discovery.base:corpus-assinado]
