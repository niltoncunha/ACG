# CORPUS.PRONTIDAO — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: CORPUS.PRONTIDAO
::CHAIN-STAGE:: CORPUS.PRONTIDAO
::CORPUS-ROLE:: MINIMUM_READINESS_GATE
::PREVIOUS-STAGE:: CORPUS.OVERVIEW
::NEXT-STAGE:: CORPUS.PSEUDORUNTIME
::DOCFIELD-CANON:: RM.DocFIELD
::OBSIDIAN-MODEL:: component_first
::READINESS-STATE:: condicionado
::PSEUDORUNTIME-RULE:: not_before_readiness
```

## CAPA

```yaml
doc_id: corpus.prontidao.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
status: EM_TESTE
readiness_state: condicionado
previous_stage_ref: corpus.overview.tsd.crossrupture.discovery.base
next_stage_target: CORPUS.PSEUDORUNTIME
```

## CRITERIO

```yaml
checks:
  rm_docfield: OK
  obsidian_componentes: OK
  obsidian_bases: OK
  corpus_overview: OK
  component_first: OK
  false_center_detected: false
  relation_state_visible: OK
  lacunas_explicit: OK
```

## DECISAO

```yaml
decision: CONDICIONADO
can_continue_to_pseudoruntime: true
cannot_promote_to_runtime: true
reason: "A cadeia documental esta legivel, mas ha lacunas que impedem promocao executiva."
```

## LACUNAS

```yaml
lacunas:
  - symbol_map_binder_lsu
  - corpus_de_calibracao_gptplus
  - tabela_de_problema_forte
  - corpus_multimodal_minimo
  - pendencias_base_minima
```

## HANDOFF

```yaml
handoff:
  status: PRONTO_PARA_CORPUS.PSEUDORUNTIME
  target: CORPUS.PSEUDORUNTIME
  blockers_for_pseudoruntime: []
  blockers_for_exec_promotion:
    - symbol_map_binder_lsu
    - corpus_de_calibracao_gptplus
    - corpus_multimodal_minimo
```

OBSIDIAN: [crossrupture.discovery.base:corpus-prontidao]
