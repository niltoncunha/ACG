# CORPUS.AUDITORIA — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: CORPUS.AUDITORIA
::CHAIN-STAGE:: CORPUS.AUDITORIA
::PREVIOUS-STAGE:: CORPUS.PROMOCAO.SEQUENCIAL
::NEXT-STAGE:: CORPUS.RELATORIO
::DOCFIELD-CANON:: RM.DocFIELD
::AUDIT-RULE:: return_target_required_on_failure
```

## CAPA

```yaml
doc_id: corpus.auditoria.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
status: EM_TESTE
previous_stage_ref: corpus.promocao.sequencial.tsd.crossrupture.discovery.base
next_stage_target: CORPUS.RELATORIO
```

## AUDITORIA ESTRUTURAL

```yaml
audit:
  chain_order_ok: true
  one_stage_one_file: true
  rm_docfield_canonical: true
  obsidian_component_first: true
  pseudoruntime_marked_simulated: true
  resultados_not_proof: true
  gauntlet_has_pass_fail: true
  promocao_did_not_sign: true
  final_state_candidate: SUSPENSO
```

## ACHADOS

```yaml
findings:
  - id: A001
    level: PROVADO
    text: cadeia_corpus_emitida_ate_promocao
  - id: A002
    level: INFERENCIA_DOCUMENTADA
    text: suspensao_e_estado_final_adequado
  - id: A003
    level: SIMULADO
    text: pseudoruntime_nao_e_execucao_real
```

## DECISAO

```yaml
audit_decision: APROVA_COM_RESSALVA
return_required: false
next: CORPUS.RELATORIO
```

OBSIDIAN: [crossrupture.discovery.base:corpus-auditoria]
