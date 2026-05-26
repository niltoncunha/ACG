# CORPUS.OVERVIEW — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: CORPUS.OVERVIEW
::CHAIN-STAGE:: CORPUS.OVERVIEW
::CORPUS-ROLE:: POST_OBSIDIAN_DOCUMENTAL_OVERVIEW
::PREVIOUS-STAGE:: OBSIDIAN.BASES
::NEXT-STAGE:: CORPUS.PRONTIDAO
::OBSIDIAN-RULE:: components_not_documents
::OBSIDIAN-CANON:: OBSIDIAN.COMPONENTES + OBSIDIAN.BASES
::DOCFIELD-CANON:: RM.DocFIELD
::DOCFILE-ALIAS:: forbidden
::PSEUDORUNTIME-RULE:: not_in_overview
```

---

## 1. CAPA E IDENTIDADE

```yaml
doc_id: corpus.overview.tsd.crossrupture.discovery.base
titulo: "CROSSRUPTURE — Visao Consolidada Pos-Obsidian — CORPUS.OVERVIEW"
rev: "v0.1.0"
data: "2026-05-26 00:00"
tz: "America/Sao_Paulo"
autor: "TESSERUS.UDA + NILTON.CUNHA"
status: EM_TESTE

doc_kind: CORPUS.OVERVIEW
doc_class: POST_OBSIDIAN_DOCUMENTAL_OVERVIEW
authority_scope: visao consolidada do corpo documental pos-Obsidian

case_id: "tsd.crossrupture.discovery.base"
family_id: "crossrupture.discovery.base"
component_scope: familia

previous_stage_ref: "OBSIDIAN.COMPONENTES + OBSIDIAN.BASES"
next_stage_target: "CORPUS.PRONTIDAO"
github_path: "docs/tsd.crossrupture.discovery.base/corpus.overview.tsd.crossrupture.discovery.base.md"
```

---

## 2. DESCRICAO NAO TECNICA

O QUE E:
- Visao consolidada do corpo documental CROSSRUPTURE depois da projecao Obsidian.

PARA QUE SERVE:
- Verifica se os componentes, bases, relacoes, lacunas e estados estao legiveis como sistema antes de seguir para CORPUS.PRONTIDAO.

POR QUE IMPORTA:
- Sem OVERVIEW, o mapa pode existir, mas ainda nao estar inteligivel como corpo documental.

O QUE NAO E:
- Nao e Obsidian.
- Nao e RM.
- Nao e DocFIELD.
- Nao e PSEUDORUNTIME.
- Nao e RESULTADOS.
- Nao e GAUNTLET.
- Nao e PROMOCAO.
- Nao e AUDITORIA.
- Nao e ASSINADO.

---

## 3. ESTADO DO OVERVIEW

```yaml
overview_state:
  rm_master_available: true
  rm_componentes_available: true
  rm_docfield_available: true
  obsidian_componentes_available: true
  obsidian_bases_available: true

  component_map_readable: true
  bases_readable: true
  documentation_as_support_confirmed: true
  false_center_detected: false
  relation_states_visible: true

  authority_status: resolvida
  coverage_status: partial

  handoff_status: PRONTO_PARA_CORPUS.PRONTIDAO
```

---

## 4. RM_PRESSURE

```yaml
rm_pressure:
  canonical_name: "corpus.overview.tsd.crossrupture.discovery.base"
  layer_primary: CONTRACTS
  vertical_family: DOCUMENTAL
  kind: CORPUS.OVERVIEW
  runtime_grade: doconly
  dependencies:
    - RM.MASTER
    - RM.COMPONENTES
    - RM.DocFIELD
    - OBSIDIAN.COMPONENTES
    - OBSIDIAN.BASES
  provides:
    - consolidated_component_overview
    - obsidian_map_reading
    - relation_state_summary
    - gap_summary
    - readiness_handoff
  consumes:
    - family_map
    - component_registry
    - docfield_mechanical_contract
    - obsidian_projection
    - base_views
  touches_world: false
  requires_proof: false
  requires_gate: false
  requires_rollback: false
  evidence_level: INFERENCIA_DOCUMENTADA
  gaps:
    - symbol_map_binder_lsu
    - corpus_de_calibracao_gptplus
    - tabela_de_problema_forte
    - corpus_multimodal_minimo
  conflicts: []
  return_target: na
```

---

## 5. SYMBOL_CARD

```yaml
symbol_card:
  glyph: "na"
  symbol_id: "UNMAPPED"
  current_name: "CORPUS.OVERVIEW.crossrupture.discovery.base"
  function: "consolidar leitura pos-Obsidian do corpo documental"
  responsible_stack: CONTRACTS
  direct_dependencies:
    - RM.MASTER
    - RM.COMPONENTES
    - RM.DocFIELD
    - OBSIDIAN.COMPONENTES
    - OBSIDIAN.BASES
  reverse_dependencies:
    - CORPUS.PRONTIDAO
    - CORPUS.PSEUDORUNTIME
  fallback_path: "OBSIDIAN.COMPONENTES | RM.COMPONENTES | HUMANO"
  nd_pressure: "nD"
  risk_flag: medium
```

---

## 6. SUMARIO EXECUTIVO

CORPO DOCUMENTAL:
- `crossrupture.discovery.base`

ENTRADA OBSIDIAN:
- OBSIDIAN.COMPONENTES: presente
- OBSIDIAN.BASES: presente

COMPONENTES MAPEADOS:
- 6 componentes.

COMPONENTES COM RELACAO OK:
- Crossrupture.Core.CMP
- Crossrupture.Prepass.CMP
- Crossrupture.BopexLint.CMP
- Crossrupture.MepRetention.CMP
- Crossrupture.FinalKill.CMP
- Crossrupture.HypothesisCard.CMP

COMPONENTES COM RELACAO INCOMPLETA:
- nenhum critico para OVERVIEW.

COMPONENTES COM RELACAO QUEBRADA:
- nenhum.

CENTRO FALSO DETECTADO:
- nao.

LACUNAS PRINCIPAIS:
- symbol_map_binder_lsu
- corpus_de_calibracao_gptplus
- tabela_de_problema_forte
- corpus_multimodal_minimo

DECISAO DO OVERVIEW:
- PRONTO_PARA_PRONTIDAO.

---

## 7. FONTES E AUTORIDADE

| source_id | fonte | tipo | autoridade | papel no OVERVIEW | status |
|---|---|---|---|---|---|
| SRC001 | rm.master.tsd.crossrupture.discovery.base | RM | alta | define familia e autoridade | lido |
| SRC002 | rm.componentes.tsd.crossrupture.discovery.base | RM | alta | define componentes | lido |
| SRC003 | rm.docfield.tsd.crossrupture.discovery.base | RM | alta | define forma mecanica documental | lido |
| SRC004 | OBSIDIAN.COMPONENTES | Obsidian | media | mapa visual de componentes | lido |
| SRC005 | OBSIDIAN.BASES | Obsidian | media | views operacionais | lido |

```text
AUTHORITY_RESOLUTION:
fonte_soberana_escolhida: RM
fontes_secundarias: OBSIDIAN.COMPONENTES, OBSIDIAN.BASES
conflitos_de_autoridade: nenhum ativo
decisao_de_autoridade: Obsidian e camada visual relacional; autoridade permanece no RM.
```

---

## 8. MAPA DE COMPONENTES

| component_id | component_name | cluster | role | documented_as | map_parent | relation_state | research_state | status |
|---|---|---|---|---|---|---|---|---|
| Crossrupture.Core.CMP | Crossrupture Core | SEMANTICA | principal | principal | TESSERUS.SEMANTICA | ok | lacuna | EM TESTE |
| Crossrupture.Prepass.CMP | Crossrupture Prepass | SEMANTICA | derivado | derivado | TESSERUS.SEMANTICA | ok | lacuna | EM TESTE |
| Crossrupture.BopexLint.CMP | Crossrupture Bopex Lint | CONTRATO | derivado | derivado | TESSERUS.CONTRATO | ok | lacuna | EM TESTE |
| Crossrupture.MepRetention.CMP | Crossrupture MEP Retention | SKIN | derivado | derivado | TESSERUS.SKIN | ok | lacuna | EM TESTE |
| Crossrupture.FinalKill.CMP | Crossrupture Final Kill | CONTRATO | derivado | derivado | TESSERUS.CONTRATO | ok | lacuna | EM TESTE |
| Crossrupture.HypothesisCard.CMP | Crossrupture Hypothesis Card | SKIN | derivado | derivado | TESSERUS.SKIN | ok | lacuna | EM TESTE |

---

## 9. CHECAGEM DE CENTRO VISUAL

```yaml
visual_center_check:
  component_first_confirmed: true
  documentation_support_confirmed: true
  false_centers_detected: []
  action_required: none
```

Critério aplicado:
- componentes sao nos;
- documentos entram como apoio;
- bases sao vistas operacionais;
- nenhum documento foi tratado como centro do grafo.

---

## 10. CHECAGEM DAS BASES OBSIDIAN

| base | funcao | presente | coerente | observacao |
|---|---|---|---|---|
| Componentes | listar componentes | sim | sim | lista 6 componentes |
| Ligacoes | mostrar relacoes | sim | sim | core liga derivados; derivados apontam para core |
| Bloqueios | mostrar bloqueios | sim | sim | lacunas principais estao visiveis |
| Pendencias | mostrar pendencias | sim | parcial | arquivo existe em forma minima por bloqueio de conector anterior |

---

## 11. MATRIZ DE RELACOES

| origem | relacao | destino | relation_state | evidencia | acao |
|---|---|---|---|---|---|
| Crossrupture.Core.CMP | linked_to | derivados | ok | OBSIDIAN.BASES | manter |
| Crossrupture.Prepass.CMP | derived_from | Crossrupture.Core.CMP | ok | OBSIDIAN.BASES | manter |
| Crossrupture.BopexLint.CMP | derived_from | Crossrupture.Core.CMP | ok | OBSIDIAN.BASES | manter |
| Crossrupture.MepRetention.CMP | derived_from | Crossrupture.Core.CMP | ok | OBSIDIAN.BASES | manter |
| Crossrupture.FinalKill.CMP | derived_from | Crossrupture.Core.CMP | ok | OBSIDIAN.BASES | manter |
| Crossrupture.HypothesisCard.CMP | derived_from | Crossrupture.Core.CMP | ok | OBSIDIAN.BASES | manter |

---

## 12. COBERTURA DOCUMENTAL DE APOIO

| component_id | rm_ref | docfield_ref | docs | chat_refs | status |
|---|---|---|---|---|---|
| Crossrupture.Core.CMP | presente | presente | presente | presente | ok |
| Crossrupture.Prepass.CMP | presente | presente | presente | parcial | ok |
| Crossrupture.BopexLint.CMP | presente | presente | presente | parcial | ok |
| Crossrupture.MepRetention.CMP | presente | presente | presente | parcial | ok |
| Crossrupture.FinalKill.CMP | presente | presente | presente | parcial | ok |
| Crossrupture.HypothesisCard.CMP | presente | presente | presente | parcial | ok |

---

## 13. LACUNAS, CONFLITOS E RETORNOS

| gap_id | tipo | descricao | impacto | retorno |
|---|---|---|---|---|
| G001 | simbolico | symbol_map_binder_lsu ausente | bloqueia camada simbolica forte | RM.DocFIELD |
| G002 | corpus | corpus_de_calibracao_gptplus ausente | reduz calibragem de discovery | CORPUS.PRONTIDAO |
| G003 | criterio | tabela_de_problema_forte ausente | reduz precisao do filtro acima de extremo | CORPUS.PRONTIDAO |
| G004 | corpus | corpus_multimodal_minimo ausente | bloqueia corpus forte posterior | CORPUS.PRONTIDAO |
| G005 | base | 04.Pendencias.base esta minima | reduz detalhe operacional, mas nao bloqueia OVERVIEW | OBSIDIAN.BASES |

Conflitos ativos:
- nenhum.

---

## 14. CRITERIO DO OVERVIEW

```yaml
overview_criteria:
  components_are_center: true
  bases_are_present: true
  relation_states_visible: true
  false_center_absent: true
  support_docs_mapped: true
  critical_gaps_explicit: true
  return_targets_defined: true
  decision: PRONTO_PARA_CORPUS.PRONTIDAO
```

---

## 15. HANDOFF PARA CORPUS.PRONTIDAO

```yaml
handoff:
  status: PRONTO_PARA_CORPUS.PRONTIDAO
  target: CORPUS.PRONTIDAO
  payload:
    corpus_overview_doc_id: "corpus.overview.tsd.crossrupture.discovery.base"
    component_scope: familia
    components_mapped:
      - Crossrupture.Core.CMP
      - Crossrupture.Prepass.CMP
      - Crossrupture.BopexLint.CMP
      - Crossrupture.MepRetention.CMP
      - Crossrupture.FinalKill.CMP
      - Crossrupture.HypothesisCard.CMP
    relation_summary:
      ok:
        - core_to_derivatives
        - derivatives_to_core
      incompleto:
        - pendencias_base_detail
      quebrado: []
    false_center_detected: false
    bases_status: parcial
    critical_gaps:
      - symbol_map_binder_lsu
      - corpus_de_calibracao_gptplus
      - tabela_de_problema_forte
      - corpus_multimodal_minimo
    return_targets:
      - RM.DocFIELD
      - OBSIDIAN.BASES
      - CORPUS.PRONTIDAO

handoff_compacto:
  tema: "CROSSRUPTURE"
  foco: "overview pos-Obsidian"
  objetivo: "verificar inteligibilidade do corpo documental"
  estado_atual: "CORPUS.OVERVIEW EM_TESTE"
  evidencia: alta
  bloqueios: []
  saida_esperada: "CORPUS.PRONTIDAO"
```

---

## 16. FIDELIDADE CANONICA

```text
- CORPUS.OVERVIEW emitido como visao pos-Obsidian.
- Componentes tratados como nos centrais.
- Documentos tratados como apoio.
- OBSIDIAN.COMPONENTES consumido como fonte visual.
- OBSIDIAN.BASES consumido como views operacionais.
- RM permaneceu autoridade.
- RM.DocFIELD permaneceu forma mecanica documental.
- Nenhum PSEUDORUNTIME foi executado.
- Nenhum RESULTADO foi emitido.
- Nenhum GAUNTLET foi aplicado.
- Nenhuma PROMOCAO foi feita.
- Nenhuma AUDITORIA final foi feita.
- Nenhum estado final foi assinado.
- Handoff para CORPUS.PRONTIDAO definido.
```

---

## 17. RODAPE DE INTEGRIDADE

```yaml
evidence_summary:
  provado:
    - RM.DocFIELD publicado existe
    - OBSIDIAN.COMPONENTES publicado existe
    - OBSIDIAN.BASES publicado existe
  inferencia_documentada:
    - corpo documental esta inteligivel o suficiente para CORPUS.PRONTIDAO
    - pendencias minimas nao bloqueiam OVERVIEW
  hipotese:
    - etapas futuras poderao medir repetibilidade e ganho de descoberta
  simulado:
    - nenhum pseudoruntime foi executado
    - nenhum benchmark foi medido

activation_trace:
  route_taken: "OBSIDIAN.BASES -> CORPUS.OVERVIEW"
  route_reason: "upstreams obrigatorios presentes"
  suppressed_modes:
    - CORPUS.PRONTIDAO
    - CORPUS.PSEUDORUNTIME
    - CORPUS.RESULTADOS
    - CORPUS.GAUNTLET
    - CORPUS.PROMOCAO.SEQUENCIAL
    - CORPUS.AUDITORIA
    - CORPUS.RELATORIO
    - CORPUS.REGISTRO
    - CORPUS.ASSINADO
  next_allowed_activation: "CORPUS.PRONTIDAO"

audit_trace:
  rm_docfield_ref: "rm.docfield.tsd.crossrupture.discovery.base"
  obsidian_componentes_ref: "obsidian/tsd.crossrupture.discovery.base/*.CMP.md"
  obsidian_bases_ref: "obsidian/tsd.crossrupture.discovery.base/00-04"
  symbol_map_ref: "UNMAPPED"

obsidian_trace:
  componentes_ref: "OBSIDIAN.COMPONENTES"
  bases_ref: "OBSIDIAN.BASES"
  false_center_check: false
  relation_state_check: ok

next_stage:
  expected: CORPUS.PRONTIDAO
  allowed: true
  reason: "componentes e bases estao legiveis como corpo documental pos-Obsidian"

final_guard:
  overview_is_not_prontidao: true
  overview_is_not_pseudoruntime: true
  overview_is_not_auditoria: true
  overview_does_not_promote: true
  obsidian_maps_components_not_docs: true
  no_docfile_alias: true
  no_traditional_programming_as_primary_model: true
  no_protoexec_without_later_corpus: true
```

---

## 18. MARCACAO OBSIDIAN

```text
OBSIDIAN: [crossrupture.discovery.base:corpus-overview]
```
