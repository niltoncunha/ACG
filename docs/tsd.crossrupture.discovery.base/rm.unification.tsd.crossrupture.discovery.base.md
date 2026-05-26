# RM.UNIFICATION — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: RM.UNIFICATION
::CHAIN-STAGE:: RM.UNIFICATION
::PREVIOUS-STAGE:: TRILHO
::NEXT-STAGE:: RM.MASTER
::DOCFIELD-CANON:: RM.DocFIELD
::DOCFILE-ALIAS:: forbidden
::OBSIDIAN-CROSSREF-REQUIRED:: true
::LOCAL-ONLY:: true
::MODE-HINT:: continue
::INTENT-HINT:: unify|classify|route|prepare-rm-master
```

---

## 1. CAPA

```yaml
doc_id: rm.unification.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
titulo: CROSSRUPTURE — RM.UNIFICATION
status: EM_TESTE
authority_scope: saneamento RM de categorias, familia, dependencias e autoridade documental
author: TESSERUS.UDA + Nilton Cunha
date: 2026-05-26
timezone: America/Sao_Paulo
github_path: docs/tsd.crossrupture.discovery.base/rm.unification.tsd.crossrupture.discovery.base.md
source_trilho: docs/tsd.crossrupture.discovery.base/trilho.tsd.crossrupture.discovery.base.md
```

---

## 2. RM_PRESSURE

```yaml
rm_pressure:
  pressure_type: unification
  central_question: "CROSSRUPTURE.DISCOVERY-BASE e familia propria ou derivado de discovery.gate?"
  decision_needed: true
  reason: >
    O TRILHO registrou a base como metodo operacional de descoberta viva e cruzamento TESSERUS,
    mas deixou ambiguidade entre familia independente e derivacao de discovery.gate/MEP.REACTIVATION.
  pressure_sources:
    - hipotese_alta_viva
    - separacao_discovery_fechamento
    - BOPEX_lint_auxiliar
    - MEP_retention
    - ASM_X_MX14_formalizacao
    - closure_governor_fechamento
  risk_if_unresolved:
    - duplicar autoridade com discovery.gate
    - transformar MEP em pai indevido
    - promover metodo como runtime
    - perder regra de morte somente no fechamento
```

---

## 3. CATEGORY_REGISTRY

```yaml
category_registry:
  chain_stage: RM.UNIFICATION
  doc_class: METHOD_LOOP
  final_state: na
  case_shape: METHOD_LOOP
  primary_role: discovery_live_crossing_orchestrator
  lifecycle_state: EM_TESTE
  source_status: PROTO_FORTE
  runtime_applicability: no
  canonical_family_decision: independent_method_family
```

### 3.1 Categorias saneadas

| Entidade | Categoria RM | Decisao | Motivo |
|---|---|---|---|
| CROSSRUPTURE.DISCOVERY-BASE | METHOD_LOOP / MASTER_CANDIDATE | manter como familia propria | governa metodo transversal de descoberta e cruzamento |
| discovery.gate / MEP.REACTIVATION | DEPENDENCY / METHOD_SUPPORT | manter separado | fornece retencao e reativacao, mas nao cobre todo o metodo |
| BOPEX | DEPENDENCY / LINT_STRUCTURAL | manter separado | saneia classe, nome e representacao; nao decide ruptura |
| ASM-X / MX14 | METHOD_REFERENCE | manter como referencia metodologica | pressiona campo neutro, prova condicional, bound e kill-switch |
| closure.governor | DOWNSTREAM_CONSUMER | manter separado | aplica fechamento e morte final, nao discovery |
| inventario TESSERUS | REFERENCE_ATLAS | manter como fonte auxiliar | orienta interna-tess e evita redundancia |
| symbol map / binder / LSU | BLOCKING_REFERENCE_MISSING | lacuna | necessario para simbolico forte futuro |

---

## 4. UNIFICATION_CARD

```yaml
unification_card:
  family_id: crossrupture.discovery.base
  doc_id: rm.unification.tsd.crossrupture.discovery.base
  doc_class: METHOD_LOOP
  primary_doc_id: trilho.tsd.crossrupture.discovery.base
  family_shape: METHOD_LOOP
  sanitation_action: reclassify
  coverage_status: partial
  confidence_level: high
  missing_critical: no
  review_required: yes
  return_target: RM
```

### 4.1 Decisao de unificacao

```yaml
unification_decision:
  keep_as_independent_family: true
  parent_family: null
  support_dependencies:
    - tsd.discovery.gate.mep.reactivation
    - tsd.bopex
    - tsd.closure.governor
  method_references:
    - ASM-X
    - MX14-FORJA
    - SCS-nD
  next_rm_stage: RM.MASTER
```

### 4.2 Justificativa

`CROSSRUPTURE.DISCOVERY-BASE` nao deve ser absorvido por `discovery.gate`, porque seu escopo excede retencao e reativacao. Ele organiza a cadeia completa de descoberta viva: prepass, analise, BOPEX lint, MEP retention, interna, ASM/MX14, externa, alien e fechamento.

`MEP.REACTIVATION` permanece como dependencia funcional, nao pai soberano. Sua funcao e preservar e reativar candidatos. O metodo CROSSRUPTURE governa a rota maior de cruzamento.

`BOPEX` permanece dependencia consultiva de saneamento estrutural, nao componente interno a ser duplicado.

`closure.governor` permanece consumidor posterior de fechamento, nao etapa de discovery.

---

## 5. SYMBOL_CARD

```yaml
symbol_card:
  symbolic_authority: partial
  uses_symbolic_map: false
  symbol_map_required_for_future: true
  binder_required_for_future: true
  lsu_required_for_future: true
  current_symbolic_scope: method_labels_and_status_enums
  unmapped_items:
    - symbol_map_canon
    - binder_universal
    - lsu_domain_pack
  promotion_blocked_for_symbolic_runtime: true
```

Observacao:
- O metodo pode seguir para `RM.MASTER` sem `symbol_map` soberano, porque a etapa atual e metodologica/documental.
- Promocao para camada simbolica forte, DocFIELD mecanico ou ProtoEXEC fica bloqueada ate haver autoridade simbolica.

---

## 6. DECISAO

```yaml
decision:
  status: PRONTO_PARA_RM.MASTER
  reason: >
    A unificacao resolveu que CROSSRUPTURE.DISCOVERY-BASE e uma familia metodologica propria,
    com MEP como dependencia de retencao, BOPEX como lint estrutural, ASM/MX14 como referencias de formalizacao
    e closure.governor como consumidor de fechamento.
  unresolved_categories:
    - symbol_map_binder_lsu
    - corpus_de_calibracao_gptplus
    - componentes_vivos_priorizados
    - tabela_de_problema_forte
  blockers_for_rm_master: []
  blockers_for_canonical_promotion:
    - sem_validacao_por_casos_reais
    - sem_corpus_minimo_multimodal
    - sem_comparison_log_metodo_antigo_vs_novo
    - sem_hash_manifesto_documental
```

---

## 7. EVIDENCIAS ROTULADAS

### FATO

- Existe TRILHO publicado para `tsd.crossrupture.discovery.base`.
- O TRILHO declara `PROXIMA_FASE_VALIDA: RM.UNIFICATION`.
- O TRILHO define a rota principal de descoberta viva ate fechamento.

### INFERENCIA_DOCUMENTADA

- A familia deve ser propria porque governa um metodo transversal maior que MEP.REACTIVATION.
- `MEP.REACTIVATION` e dependencia de retencao, nao pai soberano.
- `BOPEX` e lint estrutural auxiliar, nao juiz de ruptura.
- `closure.governor` fecha e mata, mas nao deve governar a descoberta.

### HIPOTESE

- A familia podera gerar componentes derivados no RM.COMPONENTES, por exemplo:
  - crossrupture.prepass
  - crossrupture.bopex-lint
  - crossrupture.mep-retention
  - crossrupture.final-kill
  - crossrupture.hypothesis-card

### SIMULADO

- Nenhum benchmark de ganho do metodo foi executado.
- Nenhum corpus real de entradas multimodais foi rodado.
- Nenhuma comparacao quantitativa contra fluxo antigo foi registrada.

---

## 8. MATRIZ DE ALIASES E NAO-ALIENACAO

| Nome / termo | Tratamento | Acao |
|---|---|---|
| CROSSRUPTURE | alias curto permitido | preservar como label operacional |
| TSD.CROSSRUPTURE.DISCOVERY-BASE | nome funcional | mapear para `tsd.crossrupture.discovery.base` |
| Base de Descoberta Viva | label humano | preservar em descricao, nao como doc_id |
| Discovery.Gate | dependencia relacionada | manter separado |
| MEP.REACTIVATION | dependencia funcional | manter separado |
| BOPEX | dependencia consultiva | manter separado |
| Closure.Governor | consumidor de fechamento | manter separado |

Regra:

```text
Nenhum alias substitui o case_root canonico:
ts d.crossrupture.discovery.base -> INVALIDO por espaco
case_root canonico: tsd.crossrupture.discovery.base
```

---

## 9. FULL_CHAIN_COVERAGE_CARD

```yaml
full_chain_coverage_card:
  required_chain:
    - DOSSIE_CHAT
    - TRILHO
    - RM.UNIFICATION
    - RM.MASTER
    - RM.COMPONENTES
    - RM.DocFIELD
    - OBSIDIAN.COMPONENTES
    - OBSIDIAN.BASES
    - CORPUS.OVERVIEW
    - CORPUS.PRONTIDAO
    - CORPUS.PSEUDORUNTIME
    - CORPUS.RESULTADOS
    - CORPUS.GAUNTLET
    - CORPUS.PROMOCAO.SEQUENCIAL
    - CORPUS.AUDITORIA
    - CORPUS.RELATORIO
    - CORPUS.REGISTRO
    - CORPUS.ASSINADO
    - DocEND | ProtoEXEC | SUSPENSO

  current_stage: RM.UNIFICATION
  previous_stage_ok: true
  next_stage: RM.MASTER

  universal_requirements:
    component_first_obsidian: true
    rm_docfield_without_docfile_alias: true
    evidence_labels_required: true
    ai_router_required_when_mode_sensitive: true
    rm_pressure_required: true
    symbol_card_required_when_symbolic: true
    obsidian_crossref_required: true
    handoff_required: true
    footer_integrity_required: true
    no_production_as_cycle_state: true
    no_traditional_programming_as_primary_model: true

  missing_allowed_only_if_declared:
    - lacuna
    - bloqueio
    - hipotese
    - simulado
    - suspenso
```

---

## 10. OBSIDIAN

```text
OBSIDIAN: [crossrupture.discovery.base:rm-unification]
```

Obsidian futuro deve ser component-first:

```text
OBSIDIAN.COMPONENTES -> OBSIDIAN.BASES
```

Nao mapear documento como centro. Mapear componentes, papeis e relacoes.

---

## 11. HANDOFF PARA RM.MASTER

```yaml
handoff_to_rm_master:
  next_skill: rm-tess
  next_stage: RM.MASTER
  case_root: tsd.crossrupture.discovery.base
  master_candidate: rm.master.tsd.crossrupture.discovery.base
  reason: >
    RM.UNIFICATION resolveu a familia como METHOD_LOOP independente.
    A proxima etapa deve definir identidade macro, escopo soberano, principios, fronteiras,
    dependencias e topologia da familia.
  preserve_invariants:
    - discovery_permissivo
    - governance_duro
    - hipotese_alta_viva
    - lacuna_nao_e_descarte
    - morte_so_no_fechamento
    - hipotese_nao_vira_prova
    - bopex_lint_nao_decide_ruptura
    - mep_retention_nao_e_pai_soberano
  declared_lacunas:
    - corpus_de_calibracao
    - symbol_map_binder_lsu
    - lista_priorizada_componentes_vivos
    - tabela_de_problema_forte
```

---

## 12. LACUNAS OBJETIVAS

```yaml
lacunas:
  - id: LAC001
    item: corpus_de_calibracao_gptplus
    impact: melhora repetibilidade do metodo
    blocks_rm_master: false
    blocks_canonico: true
  - id: LAC002
    item: symbol_map_binder_lsu
    impact: bloqueia promocao simbolica forte
    blocks_rm_master: false
    blocks_docfield_strong: true
  - id: LAC003
    item: componentes_vivos_priorizados
    impact: reduz custo de interna-tess
    blocks_rm_master: false
    blocks_runtime: true
  - id: LAC004
    item: tabela_de_problema_forte
    impact: melhora filtro de ruptura acima de extremo
    blocks_rm_master: false
    blocks_canonico: true
  - id: LAC005
    item: corpus_multimodal_minimo
    impact: necessario para corpus posterior
    blocks_rm_master: false
    blocks_corpus: true
```

---

## 13. VALIDACAO LOCAL

```yaml
local_validation:
  one_rm_stage_per_file: OK
  ai_markers_present: OK
  rm_pressure_present: OK
  symbol_card_present: OK
  obsidian_crossref_present: OK
  evidence_labels_present: OK
  no_critical_placeholders: OK
  no_legacy_alias_authority: OK
  no_docfield_promotion: OK
  no_production_as_cycle_state: OK
  github_path_ready: OK
```

---

## 14. FOOTER INTEGRITY

```yaml
footer_integrity:
  doc_id: rm.unification.tsd.crossrupture.discovery.base
  case_id: tsd.crossrupture.discovery.base
  chain_stage: RM.UNIFICATION
  previous_stage: TRILHO
  next_stage: RM.MASTER
  publish_policy: emit-first -> validate-local -> publish-last
  status: EM_TESTE
```

---

## 15. REGRA FINAL RM.UNIFICATION

```text
CROSSRUPTURE.DISCOVERY-BASE permanece familia metodologica propria.
MEP retém.
BOPEX saneia.
ASM/MX14 formalizam.
Closure mata ou promove no fim.
Discovery preserva hipotese alta.
RM.MASTER pode seguir.
```
