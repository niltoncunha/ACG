# RM.UNIFICATION — TSD.REGENEGIS

> Saneamento RM de categorias, família, aliases e fronteiras do componente candidato `REGENEGIS`.
> Derivado do TRILHO `trilho.tsd.regenegis`.
> Não substitui RM.MASTER, RM.COMPONENTES ou RM.DocFIELD.

---

## NATUREZA

`RM.UNIFICATION` decide o que cada entidade é antes da emissão forte.

Cadeia ativa:

```text
DOSSIE_CHAT -> TRILHO -> RM.UNIFICATION -> RM.MASTER -> RM.COMPONENTES -> RM.DocFIELD -> OBSIDIAN.COMPONENTES -> OBSIDIAN.BASES -> CORPUS.* -> DocEND | ProtoEXEC | SUSPENSO
```

---

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
::PRODUCTION-AS-STATE:: forbidden
::EVIDENCE-RULE:: no_promotion_without_evidence
```

---

# 1. CAPA

```yaml
doc_id: rm.unification.tsd.regenegis
case_id: tsd.regenegis
family_id: regenegis
titulo: "RM.UNIFICATION — TSD.REGENEGIS"
status: EM_TESTE
authority_scope: saneamento RM de categorias e família
component_slug: regenegis
canonical_name: REGENEGIS
previous_stage: TRILHO
next_stage: RM.MASTER
```

---

# 2. CATEGORY_REGISTRY

```yaml
category_registry:
  chain_stage: RM.UNIFICATION
  doc_class: PRINCIPAL
  final_state: na

category_decision:
  primary_entity: REGENEGIS
  class: COMPONENT_CANDIDATE
  role: principal
  layer_primary: ENGINE
  vertical_family: DISCOVERY
  runtime_grade: conditional
  evidence_level: SIMULADO
```

Decisão:

```text
REGENEGIS é componente candidato principal da família `regenegis`.
Não é apenas rota solta de BOPEX.
Não é nome histórico anterior.
```

---

# 3. UNIFICATION_CARD

```yaml
unification_card:
  family_id: regenegis
  doc_id: rm.unification.tsd.regenegis
  doc_class: PRINCIPAL
  primary_doc_id: rm.master.tsd.regenegis
  family_shape: METHOD_LOOP
  sanitation_action: freeze
  coverage_status: partial
  confidence_level: medium
  missing_critical: no
  review_required: yes
  return_target: RM
```

Justificativa:

```text
O nome canônico foi fixado pelo usuário.
A versão de teste ativa é v2.1.2-TEST.
As versões e arquiteturas anteriores ficam históricas, suspensas ou descartadas.
As lacunas restantes pertencem a RM.MASTER, RM.COMPONENTES, RM.DocFIELD e CORPUS futuro.
```

---

# 4. DECISÃO

```yaml
decision:
  status: PRONTO_PARA_RM.MASTER
  reason: "Nome canônico, família principal e fronteiras de aliases saneadas."
  unresolved_categories:
    - "detalhar RESIDUE_CLASSIFIER e BOPEX_ROUTE em RM.COMPONENTES"
    - "detalhar campos, binds e tabelas em RM.DocFIELD"
    - "definir protocolo de case_echo_strength em fase posterior"
```

---

# 5. SANEAMENTO DE NOMES

| termo | decisão | classe | regra |
|---|---|---|---|
| REGENEGIS | manter como canônico | COMPONENT_CANDIDATE / PRINCIPAL | usar em RM.MASTER |
| REGENESIS | histórico | HISTORICAL_ALIAS | não usar como autoridade |
| REGENESIS.PRIME | histórico de simplificação | HISTORICAL_VERSION | não usar como base ativa |
| REGIME-GENESIS | ancestral conceitual | HISTORICAL | não emitir como componente ativo |
| AXIOMA-13 | ancestral conceitual | HISTORICAL | não emitir como componente ativo |
| v2.4-CANON | descartada | BLOCKED_VERSION | não usar como base |
| S7-alpha | suspensa | RESEARCH_ONLY | reabrir só com ganho empírico alto |
| v2.1.2-TEST | versão de teste ativa | TEST_VERSION | base para RM.MASTER |

---

# 6. ENTIDADES DA FAMÍLIA

| entity_id | canonical_name | papel | decisão | próximo destino |
|---|---|---|---|---|
| ENT-001 | REGENEGIS | componente principal candidato | principal da família | RM.MASTER |
| ENT-002 | RESIDUE_CLASSIFIER | núcleo interno | subcomponente candidato | RM.COMPONENTES |
| ENT-003 | BOPEX_ROUTE | rota/gate de precedência | contrato interno | RM.COMPONENTES / RM.DocFIELD |
| ENT-004 | RAE | métrica derivada | campo mecânico candidato | RM.DocFIELD |
| ENT-005 | novelty_support | métrica derivada | campo mecânico candidato | RM.DocFIELD |
| ENT-006 | case_echo_strength | campo candidato | requer protocolo | RM.DocFIELD |
| ENT-007 | TRISEAL_HUMAN_REVIEW | gate humano de TEST | suporte/contrato | RM.COMPONENTES |

---

# 7. RM_PRESSURE

```yaml
rm_pressure:
  canonical_name: "REGENEGIS"
  previous_names:
    - REGENESIS
    - REGENESIS.PRIME
    - REGIME-GENESIS
    - AXIOMA-13
  aliases_forbidden_as_authority: true

  layer_primary: ENGINE
  vertical_family: DISCOVERY

  kind: RM.UNIFICATION
  runtime_grade: conditional

  dependencies:
    - DOSSIE_CHAT.tsd.regenegis
    - TRILHO.tsd.regenegis
    - BOPEX
    - GENIO_DISCOVERY
    - human_review_gate

  provides:
    - category_sanitation
    - alias_resolution
    - family_shape
    - rm_master_handoff

  consumes:
    - dossie-chat.tsd.regenegis
    - trilho.tsd.regenegis
    - Claude validation outputs
    - simulated test results

  touches_world: false
  requires_proof: true
  requires_gate: true
  requires_rollback: false

  evidence_level: SIMULADO
  gaps:
    - falta bateria de campo real
    - case_echo_strength precisa protocolo mecânico
    - TRISEAL está como revisão humana em TEST
    - thresholds precisam calibração real
  conflicts:
    - aliases históricos saneados
    - versões descartadas bloqueadas
  return_target: RM.MASTER
```

---

# 8. SYMBOL_CARD

```yaml
symbol_card:
  glyph: "na"
  symbol_id: "REGENEGIS"
  current_name: "REGENEGIS"
  previous_name: "REGENESIS"
  function: "Classificar resíduo antes de autorizar GENESIS."
  executor_guardian: "BOPEX_ROUTE / TRISEAL_HUMAN_REVIEW"
  responsible_stack: ENGINE
  direct_dependencies:
    - residue_absorption_estimate
    - novelty_support
    - case_echo_strength
    - BOPEX_ROUTE
  reverse_dependencies:
    - GENIO_DISCOVERY
    - RM.COMPONENTES futuro
    - RM.DocFIELD futuro
    - CORPUS futuro
  collapse_priority: "P0..P8"
  fallback_path: "RM.MASTER -> RM.COMPONENTES -> RM.DocFIELD"
  nd_pressure: "nD"
  risk_flag: medium
```

---

# 9. EVIDÊNCIA E STATUS

| item | classe | base | decisão |
|---|---|---|---|
| Nome canônico REGENEGIS | PROVADO | decisão explícita do usuário | usar como canônico |
| DOSSIE_CHAT publicado | PROVADO | arquivo GitHub existente | fonte contextual |
| TRILHO publicado | PROVADO | arquivo GitHub existente | fonte de estado documental |
| GO_CONDICIONAL | INFERENCIA_DOCUMENTADA | validação Claude + simulações | manter como decisão de teste |
| eficácia em campo real | HIPOTESE | não testado | não promover |
| resultados de baterias | SIMULADO | Claude e simulações no chat | suporte, não prova |

---

# 10. HANDOFF PARA RM.MASTER

```yaml
handoff:
  status: PRONTO_PARA_RM.MASTER
  target: RM.MASTER
  reason: "Identidade e família principal saneadas."
  blockers: []
  payload:
    canonical_name: REGENEGIS
    component_slug: regenegis
    family_shape: METHOD_LOOP
    role: principal
    layer_primary: ENGINE
    vertical_family: DISCOVERY
    runtime_grade: conditional
    evidence_level: SIMULADO
    active_version: v2.1.2-TEST
    subcomponents:
      - RESIDUE_CLASSIFIER
      - BOPEX_ROUTE
      - TRISEAL_HUMAN_REVIEW
    docfield_candidates:
      - coverage_score
      - conflict_index
      - irreducibility_index
      - residue_stability_score
      - case_echo_strength
      - object_fragility
      - object_integrity_score
      - risk_profile
      - is_self_application
      - is_hard_noisy
      - signal_density
      - residue_absorption_estimate
      - novelty_support
      - route
    unresolved_for_later:
      - field test protocol
      - case_echo_strength metric protocol
      - TRISEAL automation criteria
      - threshold calibration
```

---

# 11. MARCAÇÃO OBSIDIAN

```text
OBSIDIAN: [regenegis:rm-unification]
@ref: regenegis:rm-unification
@ref: regenegis:trilho
@ref: regenegis:chat
```

---

# 12. RODAPÉ DE INTEGRIDADE

```yaml
local_validation:
  one_rm_stage_per_file: true
  ai_markers_present: true
  rm_pressure_present: true
  symbol_card_present: true
  obsidian_mark_present: true
  no_critical_placeholders: true
  no_legacy_alias_active: true
  evidence_labeled: true
  docfield_canon_preserved: true
  no_corpus_jump: true

next_stage:
  expected: RM.MASTER
  allowed: true
  reason: "RM.UNIFICATION saneou nome, família, aliases e versões concorrentes."

final_guard:
  no_runtime_by_document_only: true
  no_promotion_without_evidence: true
  no_docfile_alias: true
  no_traditional_programming_as_primary_model: true
  no_corpus_before_obsidian: true
  no_protoexec_by_text: true
```

---

# STAMP

```text
data: 2026-05-26 America/Sao_Paulo
tema: regenegis
status: EM_TESTE
decisao: PRONTO_PARA_RM.MASTER
obsidian: [regenegis:rm-unification]
```
