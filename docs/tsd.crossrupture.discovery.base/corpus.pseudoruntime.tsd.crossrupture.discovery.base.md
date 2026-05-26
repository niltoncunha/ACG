# CORPUS.PSEUDORUNTIME — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: CORPUS.PSEUDORUNTIME
::CHAIN-STAGE:: CORPUS.PSEUDORUNTIME
::PREVIOUS-STAGE:: CORPUS.PRONTIDAO
::NEXT-STAGE:: CORPUS.RESULTADOS
::PSEUDORUNTIME-RULE:: simulated_not_proved
::DOCFIELD-CANON:: RM.DocFIELD
```

## CAPA

```yaml
doc_id: corpus.pseudoruntime.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
status: EM_TESTE
simulation_state: SIMULADO_CONDICIONADO
previous_stage_ref: corpus.prontidao.tsd.crossrupture.discovery.base
next_stage_target: CORPUS.RESULTADOS
```

## FLUXO DOCUMENTAL SIMULADO

```yaml
flow:
  input: seed_multimodal_ou_textual
  steps:
    - prepass
    - hypothesis_card
    - bopex_lint_when_needed
    - mep_retention_when_needed
    - route_to_analysis
    - final_kill_only_at_closure
  output: hipotese_viva_lacunas_rota
```

## LEITURA

```yaml
result:
  documentary_flow_coherent: true
  false_center_detected: false
  proof_claim: false
  status: SIMULADO_CONDICIONADO
limits:
  - sem_autoridade_simbolica_completa
  - sem_corpus_multimodal_minimo
  - sem_medicao_real
```

## HANDOFF

```yaml
handoff:
  status: PRONTO_PARA_CORPUS.RESULTADOS
  target: CORPUS.RESULTADOS
  blockers: []
```

OBSIDIAN: [crossrupture.discovery.base:corpus-pseudoruntime]
