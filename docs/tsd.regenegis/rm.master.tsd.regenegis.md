# RM.MASTER — TSD.REGENEGIS

> Roteador soberano da família documental `regenegis`.  
> Derivado de `rm.unification.tsd.regenegis`.  
> Não é RM.COMPONENTES, não é RM.DocFIELD, não é Obsidian, não é CORPUS e não é execução real.

---

## NATUREZA

`RM.MASTER` define a família, o componente principal, os componentes subordinados, a autoridade macro e o próximo destino documental.

```text
DOSSIE_CHAT -> TRILHO -> RM.UNIFICATION -> RM.MASTER -> RM.COMPONENTES -> RM.DocFIELD -> OBSIDIAN.COMPONENTES -> OBSIDIAN.BASES -> CORPUS.* -> DocEND | ProtoEXEC | SUSPENSO
```

---

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: vNext
::DOSSIER-KIND:: RM.MASTER
::CHAIN-STAGE:: RM.MASTER
::MASTER-ROLE:: FAMILY_ROUTER
::MASTER-NEVER-DERIVES:: true
::DERIVED-IS-COMPONENT:: true
::UNIQUE-REFERENCE:: true

::PREVIOUS-STAGE:: RM.UNIFICATION
::NEXT-STAGE:: RM.COMPONENTES

::DOCFIELD-CANON:: RM.DocFIELD
::DOCFILE-ALIAS:: forbidden
::PRODUCTION-AS-STATE:: forbidden
::TRADITIONAL-PROGRAMMING:: not_primary_model
::SYMBOLIC-FIRST:: true
::VECTORIAL-ND:: true
::RM-PRESSURE-REQUIRED:: true
::OBSIDIAN-CROSSREF-REQUIRED:: true

::CANONICAL-STACK:: SEMANTIC | SKIN | ENGINE | CONTRACTS
::AUTHORITY-RULE:: authority_does_not_come_from_engine
::DATA-RULE:: data_flow_is_not_authority_flow
::EVIDENCE-RULE:: no_promotion_without_evidence
```

---

# 1. CAPA E IDENTIDADE

```yaml
doc_id: rm.master.tsd.regenegis
titulo: "REGENEGIS — RM.MASTER"
rev: "v1.0.0"
data: "2026-05-26"
tz: "America/Sao_Paulo"
autor: "TESSERUS.UDA + NILTON.CUNHA"
status: EM_TESTE

doc_kind: RM.MASTER
doc_class: FAMILY_ROUTER
authority_scope: roteamento soberano da família documental
unique_reference: true

case_id: "tsd.regenegis"
family_id: "regenegis"
master_name: "REGENEGIS"
component_slug: "regenegis"

previous_stage_ref: "RM.UNIFICATION"
next_stage_target: "RM.COMPONENTES"
```

---

# 2. DESCRIÇÃO NÃO TÉCNICA

```text
O QUE É:
- REGENEGIS é uma família documental centrada em um componente candidato que classifica resíduo antes de autorizar GENESIS.

PARA QUE SERVE:
- Organiza a passagem entre análise e criação de proto-regime, distinguindo novidade real, recombinação e ruído.

POR QUE IMPORTA:
- Reduz promoção prematura de ideias sedutoras e preserva novidade fraca por quarantine sem tratar simulado como prova.

COMO PENSAR:
- Este MASTER é o mapa da família: mostra o componente principal, as peças subordinadas e para onde cada uma deve seguir.

O QUE NÃO É:
- Não é teoria detalhada do componente.
- Não é execução.
- Não é Obsidian.
- Não é CORPUS.
- Não é RM.DocFIELD.
- Não é assinatura final.
```

---

# 3. ESTADO DO RM.MASTER

```yaml
rm_master_state:
  source_trilho: presente
  source_unification: presente

  family_defined: true
  principal_component_defined: true
  derived_components_defined: true
  docfield_required: true
  obsidian_required: true
  corpus_required: true

  authority_status: resolvida
  coverage_status: partial

  handoff_status: PRONTO_PARA_RM.COMPONENTES
```

Nota:

```text
A cobertura é parcial porque o componente ainda não tem teste de campo real, RM.DocFIELD, Obsidian ou CORPUS. Isso não bloqueia o MASTER; bloqueia GO final e runtime soberano.
```

---

# 4. AI_ROUTER

```yaml
ai_router:
  activation_mode: GOVERNANCE
  activation_source: prefix
  prefix_detected: "@rm-tess Master"
  prefix_valid: true
  precedence_applied: "RM.UNIFICATION -> RM.MASTER"
  default_mode: INFO
  ambiguity_flag: none
  governance_requested: true
  tests_requested: false
  artifact_override: RM.MASTER
```

---

# 5. RM_PRESSURE

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

  kind: RM.MASTER
  runtime_grade: conditional

  dependencies:
    - TRILHO.tsd.regenegis
    - RM.UNIFICATION.tsd.regenegis
    - BOPEX
    - GENIO_DISCOVERY
    - human_review_gate

  provides:
    - family_router
    - component_registry
    - relation_map
    - authority_map
    - handoff_to_components
    - handoff_to_docfield

  consumes:
    - rm_seed
    - dossier_graph_seed
    - authority_resolution
    - family_emit_plan

  touches_world: false
  requires_proof: false
  requires_gate: false
  requires_rollback: false

  evidence_level: SIMULADO
  gaps:
    - falta teste de campo real
    - case_echo_strength precisa protocolo mecânico
    - TRISEAL está como revisão humana em TEST
    - thresholds precisam calibração real
  conflicts: []
  return_target: RM.COMPONENTES
```

---

# 6. SYMBOL_CARD

```yaml
symbol_card:
  glyph: "na"
  symbol_id: "REGENEGIS.MASTER"
  current_name: "REGENEGIS"
  previous_name: "REGENESIS"
  function: "Roteia a família documental do componente classificador de resíduo antes de GENESIS."
  executor_guardian: "RM.MASTER"
  responsible_stack: CONTRACTS
  direct_dependencies:
    - TRILHO
    - RM.UNIFICATION
  reverse_dependencies:
    - RM.COMPONENTES
    - RM.DocFIELD
    - OBSIDIAN.COMPONENTES
    - OBSIDIAN.BASES
    - CORPUS.OVERVIEW
  trigger_reactions:
    - emissão de componente principal
    - emissão de subcomponentes
    - emissão de DocFIELD
  boot_index: null
  collapse_priority: null
  fallback_path: "RM.UNIFICATION | TRILHO | HUMANO"
  nd_pressure: "nD"
  risk_flag: medium
```

---

# 7. SUMÁRIO EXECUTIVO

```text
FAMÍLIA:
- regenegis

DESCRIÇÃO NÃO TÉCNICA:
- Família documental do componente REGENEGIS, que classifica resíduos antes de permitir GENESIS.

FUNÇÃO DO MASTER:
- Roteia a família documental, sem duplicar teoria dos componentes.

COMPONENTE PRINCIPAL:
- REGENEGIS.

COMPONENTES DERIVADOS:
- RESIDUE_CLASSIFIER.
- BOPEX_ROUTE.
- TRISEAL_HUMAN_REVIEW.

DocFIELD:
- Necessário.

OBSIDIAN:
- Sidecar posterior obrigatório quando RM estiver coerente.

CORPUS:
- Etapa posterior obrigatória para prontidão, pseudoruntime, resultados, gauntlet, promoção, auditoria, registro e assinatura.

BLOQUEIOS:
- Sem teste de campo real.
- Sem protocolo mecânico de case_echo_strength.
- Sem RM.DocFIELD.
- Sem Obsidian.
- Sem CORPUS.

DECISÃO ATUAL:
- Emitir RM.COMPONENTES.

PRÓXIMA ETAPA:
- RM.COMPONENTES.
```

---

# 8. ESCOPO E FRONTEIRAS

```text
INCLUI:
- identidade da família
- componente principal
- componentes derivados
- papéis documentais
- relações entre peças
- autoridade de cada peça
- dependências
- conflitos
- lacunas
- destino de emissão
- handoff para RM.COMPONENTES

NÃO INCLUI:
- teoria interna de componentes
- contratos mecânicos de tabela
- execução
- sidecars Obsidian
- pseudoruntime
- resultados
- gauntlet
- promoção sequencial
- auditoria CORPUS
- assinatura final

REGRAS DURAS:
- MASTER é roteador.
- MASTER não duplica componente.
- MASTER não cria derivado sem componente principal.
- MASTER não promove por organização textual.
- MASTER não cria ProtoEXEC.
- MASTER não assina DocEND.
- MASTER usa apenas RM.DocFIELD como etapa mecânica posterior.
```

---

# 9. FONTES E AUTORIDADE

| source_id | fonte | tipo | autoridade | papel no MASTER | status |
|---|---|---|---|---|---|
| SRC001 | TRILHO.tsd.regenegis | documento anterior | alta | estado documental e handoff | lido |
| SRC002 | RM.UNIFICATION.tsd.regenegis | documento anterior | alta | saneamento de categorias e família | lido |
| SRC003 | DOSSIE_CHAT.tsd.regenegis | fonte contextual | média | preservação de gênese e decisões | lido |
| SRC004 | validações Claude | apoio externo | média | evidência simulada/lente crítica | lido |

```text
AUTHORITY_RESOLUTION:
fonte_soberana_escolhida: RM.UNIFICATION para identidade e família; TRILHO para estado documental.
fontes_secundarias: DOSSIE_CHAT, Claude, chat atual.
conflitos_de_autoridade: nenhum bloqueante para RM.MASTER.
decisao_de_autoridade: REGENEGIS é família principal e componente principal candidato; subpeças seguem para RM.COMPONENTES.
```

---

# 10. MAPA DA FAMÍLIA

```yaml
family_map:
  family_id: "regenegis"
  master_doc_id: "rm.master.tsd.regenegis"

  principal_component:
    doc_id: "rm.componentes.tsd.regenegis"
    name: "REGENEGIS"
    role: principal
    status: definido

  derived_components:
    - doc_id: "rm.componentes.tsd.regenegis.residue-classifier"
      name: "RESIDUE_CLASSIFIER"
      role: derivado
      parent: "rm.componentes.tsd.regenegis"
      status: definido
    - doc_id: "rm.componentes.tsd.regenegis.bopex-route"
      name: "BOPEX_ROUTE"
      role: derivado
      parent: "rm.componentes.tsd.regenegis"
      status: definido
    - doc_id: "rm.componentes.tsd.regenegis.triseal-human-review"
      name: "TRISEAL_HUMAN_REVIEW"
      role: suporte
      parent: "rm.componentes.tsd.regenegis"
      status: definido

  docfield:
    doc_id: "rm.docfield.tsd.regenegis"
    required: true
    status: pendente

  obsidian:
    component_map: "OBSIDIAN.COMPONENTES"
    bases: "OBSIDIAN.BASES"
    status: posterior

  corpus:
    status: posterior
```

---

# 11. REGISTRO DE COMPONENTES

| component_id | doc_id | nome | papel | camada 4-stack | função | status | próxima ação |
|---|---|---|---|---|---|---|---|
| CMP001 | rm.componentes.tsd.regenegis | REGENEGIS | principal | ENGINE | classificar resíduo antes de autorizar GENESIS | definido | emitir RM.COMPONENTES |
| CMP002 | rm.componentes.tsd.regenegis.residue-classifier | RESIDUE_CLASSIFIER | derivado | ENGINE | separar NOVEL, COMBINATORY e NOISY | definido | detalhar em RM.COMPONENTES |
| CMP003 | rm.componentes.tsd.regenegis.bopex-route | BOPEX_ROUTE | derivado/contrato | CONTRACTS | aplicar precedência P0..P8 e rotas | definido | detalhar em RM.COMPONENTES |
| CMP004 | rm.componentes.tsd.regenegis.triseal-human-review | TRISEAL_HUMAN_REVIEW | suporte | CONTRACTS | revisar promoção final no TEST | definido | detalhar limite em RM.COMPONENTES |

---

# 12. RELAÇÕES E GRAFO DOCUMENTAL

| origem | relação | destino | motivo | autoridade |
|---|---|---|---|---|
| rm.master.tsd.regenegis | master_of | rm.componentes.tsd.regenegis | componente principal da família | RM |
| rm.componentes.tsd.regenegis.residue-classifier | derivative_of | rm.componentes.tsd.regenegis | núcleo interno | RM |
| rm.componentes.tsd.regenegis.bopex-route | derivative_of | rm.componentes.tsd.regenegis | contrato de roteamento | RM |
| rm.componentes.tsd.regenegis.triseal-human-review | supports | rm.componentes.tsd.regenegis | gate humano de TEST | RM |
| rm.docfield.tsd.regenegis | materializes | rm.componentes.tsd.regenegis | forma mecânica documental | RM.DocFIELD |
| OBSIDIAN.COMPONENTES | mirrors | rm.componentes.tsd.regenegis | mapa relacional posterior | OBSIDIAN |

```text
GRAFO ASCII:
[RM.MASTER: REGENEGIS]
   ├── master_of ──> [RM.COMPONENTES: REGENEGIS]
   │                     ├── derivative_of <── [RESIDUE_CLASSIFIER]
   │                     ├── derivative_of <── [BOPEX_ROUTE]
   │                     ├── supports      <── [TRISEAL_HUMAN_REVIEW]
   │                     └── materialized_by ──> [RM.DocFIELD]
   └── mirrored_by ──> [OBSIDIAN.COMPONENTES]
```

---

# 13. DECISÕES DO MASTER

| decision_id | decisão | motivo | impacto | estado |
|---|---|---|---|---|
| D001 | REGENEGIS é componente principal da família | RM.UNIFICATION saneou nome e aliases | permite RM.COMPONENTES | ativa |
| D002 | RESIDUE_CLASSIFIER é derivado interno | é núcleo de discriminação, não família raiz | detalhar em componentes | ativa |
| D003 | BOPEX_ROUTE é derivado/contrato interno | governa precedência P0..P8 | detalhar em componentes e DocFIELD | ativa |
| D004 | TRISEAL_HUMAN_REVIEW é suporte de TEST | ainda não é gate automático completo | manter limite humano | ativa |
| D005 | RM.DocFIELD é obrigatório | há campos, binds, métricas e rotas | emitir após componentes | ativa |
| D006 | GO final bloqueado | evidência ainda é simulada | exige campo real e CORPUS | ativa |

```text
DECISÃO D001:
- o que decide: REGENEGIS é componente principal.
- por que decide: usuário fixou nome canônico e RM.UNIFICATION saneou aliases.
- o que permite: emitir RM.COMPONENTES.
- o que bloqueia: usar REGENESIS como nome ativo.
- evidência: PROVADO para naming; INFERENCIA_DOCUMENTADA para papel de componente.
```

---

# 14. LACUNAS, CONFLITOS E RETORNOS

| gap_id | tipo | descrição | impacto | retorno |
|---|---|---|---|---|
| G001 | lacuna | falta teste de campo real | bloqueia GO final | CORPUS futuro |
| G002 | lacuna | case_echo_strength sem protocolo mecânico | bloqueia runtime soberano | RM.DocFIELD |
| G003 | lacuna | TRISEAL humano não automatizado | limita TEST | RM.COMPONENTES / HUMANO |
| G004 | lacuna | thresholds ainda simulados | exige calibração | CORPUS futuro |

```text
RETORNOS POSSÍVEIS:
- TRILHO: se faltar estado documental ou cobertura.
- RM.UNIFICATION: se novo alias ou família conflitante aparecer.
- HUMANO: se houver colisão de autoridade não resolvível.
```

---

# 15. MATRIZ DE COBERTURA DO MASTER

| item | esperado | presente | status | ação |
|---|---|---|---|---|
| fonte TRILHO | sim | sim | ok | — |
| RM.UNIFICATION | sim | sim | ok | — |
| componente principal | sim | sim | ok | emitir RM.COMPONENTES |
| derivados | opcional | sim | ok | detalhar |
| DocFIELD requerido | decidir | sim | ok | emitir depois de componentes |
| grafo documental | sim | sim | ok | preservar |
| handoff | sim | sim | ok | seguir para RM.COMPONENTES |

---

# 16. HANDOFF PARA PRÓXIMA ETAPA

```yaml
handoff:
  status: PRONTO_PARA_RM.COMPONENTES
  target: RM.COMPONENTES

  payload:
    master_doc_id: "rm.master.tsd.regenegis"
    family_id: "regenegis"
    principal_component: "rm.componentes.tsd.regenegis"
    derived_components:
      - "RESIDUE_CLASSIFIER"
      - "BOPEX_ROUTE"
      - "TRISEAL_HUMAN_REVIEW"
    docfield_required: true
    relation_map: presente
    authority_resolution: presente
    blockers:
      - "sem teste de campo real para GO final"
      - "case_echo_strength sem protocolo mecânico"
    lacunas:
      - "definir contrato interno do componente"
      - "definir limites e dependências"
      - "preparar campos para RM.DocFIELD"

handoff_compacto:
  tema: "REGENEGIS"
  foco: "família/componente principal"
  objetivo: "emitir RM.COMPONENTES para definir mecanismo, contratos, dependências e limites"
  estado_atual: "EM_TESTE / PRONTO_PARA_RM.COMPONENTES"
  evidencia: media
  bloqueios:
    - "sem campo real"
    - "sem protocolo case_echo_strength"
  saida_esperada: "RM.COMPONENTES"
```

---

# 17. FIDELIDADE CANÔNICA

```text
- MASTER emitido como roteador de família.
- Nenhuma teoria interna de componente foi duplicada.
- Nenhum derivado foi tratado como classe raiz.
- Componente principal definido.
- DocFIELD tratado como RM.DocFIELD.
- Obsidian tratado como etapa posterior.
- CORPUS tratado como etapa posterior.
- DocEND, ProtoEXEC e SUSPENSO não emitidos pelo MASTER.
- Handoff definido para RM.COMPONENTES.
```

---

# 18. RODAPÉ DE INTEGRIDADE

```yaml
evidence_summary:
  provado:
    - "Nome canônico REGENEGIS fixado pelo usuário."
    - "DOSSIE_CHAT, TRILHO e RM.UNIFICATION já publicados."
  inferencia_documentada:
    - "REGENEGIS é componente principal candidato da família regenegis."
    - "RESIDUE_CLASSIFIER, BOPEX_ROUTE e TRISEAL_HUMAN_REVIEW pertencem à família como derivados/suporte."
  hipotese:
    - "REGENEGIS terá valor em campo real como classificador de resíduo antes de GENESIS."
  simulado:
    - "Validações Claude e baterias simuladas sustentam GO_CONDICIONAL, não GO final."

activation_trace:
  route_taken: "rm-tess / RM.MASTER"
  route_reason: "usuário invocou @rm-tess Master após RM.UNIFICATION"
  suppressed_modes:
    - DOSSIE_CHAT
    - TRILHO
    - RM.COMPONENTES
    - RM.DocFIELD
    - OBSIDIAN
    - CORPUS
    - ProtoEXEC
  unsafe_or_legacy_terms_seen:
    - legacy_document_file_identity: blocked
    - legacy_rm_doc_abc_split: blocked
    - legacy_three_stage_documentary_chain: blocked
  next_allowed_activation: RM.COMPONENTES

audit_trace:
  rm_seed_ref: "rm.unification.tsd.regenegis"
  dossier_graph_ref: "trilho.tsd.regenegis"
  ledger_ref: "dossie-chat.tsd.regenegis"
  chrona_ref: "dossie-chat.tsd.regenegis chronology"
  symbol_map_ref: "SYMBOL_CARD.REGENEGIS.MASTER"

next_stage:
  expected: RM.COMPONENTES
  allowed: true
  reason: "Família roteada e componente principal definido; mecanismo interno pertence a RM.COMPONENTES."

final_guard:
  master_is_router_only: true
  no_theory_duplication: true
  no_runtime_by_document_only: true
  no_promotion_without_evidence: true
  no_docfile_alias: true
  no_traditional_programming_as_primary_model: true
  no_corpus_before_obsidian: true
```

---

# 19. MARCAÇÃO OBSIDIAN

```text
OBSIDIAN: [regenegis:master]
@ref: regenegis:master
@ref: regenegis:rm-unification
@ref: regenegis:trilho
@ref: regenegis:chat
```

---

## BLOCO TRANSVERSAL — COBERTURA TOTAL DE CADEIA v1.2

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
```

---

# STAMP

```text
data: 2026-05-26 America/Sao_Paulo
tema: regenegis
status: EM_TESTE
decisao: PRONTO_PARA_RM.COMPONENTES
obsidian: [regenegis:master]
```
