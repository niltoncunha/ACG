# RM.MASTER — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
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

## 1. CAPA E IDENTIDADE

```yaml
doc_id: master.tsd.crossrupture.discovery.base
titulo: "CROSSRUPTURE — Base de Descoberta Viva e Cruzamento TESSERUS — RM.MASTER"
rev: "v0.1.0"
data: "2026-05-26 00:00"
tz: "America/Sao_Paulo"
autor: "TESSERUS.UDA + NILTON.CUNHA"
status: EM_TESTE

doc_kind: RM.MASTER
doc_class: FAMILY_ROUTER
authority_scope: roteamento soberano da familia documental
unique_reference: true

case_id: "tsd.crossrupture.discovery.base"
family_id: "crossrupture.discovery.base"
master_name: "master.tsd.crossrupture.discovery.base"
component_slug: "crossrupture.discovery.base"

previous_stage_ref: "rm.unification.tsd.crossrupture.discovery.base"
next_stage_target: "RM.COMPONENTES"
github_path: "docs/tsd.crossrupture.discovery.base/rm.master.tsd.crossrupture.discovery.base.md"
```

---

## 2. DESCRICAO NAO TECNICA

O QUE E:
- Esta familia documental organiza o metodo CROSSRUPTURE, uma base de descoberta viva e cruzamento com TESSERUS.

PARA QUE SERVE:
- Serve para analisar imagem, video, metafora, ASCII, texto, equacao ou resposta de outra IA sem matar cedo uma hipotese forte por falta inicial de baseline, bound, discriminador ou retroprojecao.

POR QUE IMPORTA:
- O TESSERUS precisa preservar sementes raras durante discovery, mas sem permitir promocao indevida. Esta familia separa abertura criativa de fechamento duro.

COMO PENSAR:
- Este MASTER funciona como roteador da familia. Ele nao executa o metodo, nao prova hipoteses e nao substitui as skills especialistas. Ele define quais pecas pertencem ao metodo, qual papel cada uma ocupa e para onde a cadeia deve seguir.

O QUE NAO E:
- Nao e runtime.
- Nao e benchmark.
- Nao e prova empirica.
- Nao e Obsidian.
- Nao e CORPUS.
- Nao e RM.DocFIELD.
- Nao e assinatura final.

---

## 3. ESTADO DO RM.MASTER

```yaml
rm_master_state:
  source_trilho: presente
  source_unification: presente

  family_defined: true
  principal_component_defined: true
  derived_components_defined: partial
  docfield_required: true
  obsidian_required: true
  corpus_required: true

  authority_status: resolvida
  coverage_status: partial

  handoff_status: PRONTO_PARA_RM.COMPONENTES
```

---

## 4. AI_ROUTER

```yaml
ai_router:
  activation_mode: DISCOVERY
  activation_source: inherited_chain
  prefix_detected: "@rm-tess RM.master"
  prefix_valid: true
  precedence_applied: rm_chain_after_unification
  default_mode: INFO
  ambiguity_flag: none
  governance_requested: false
  tests_requested: false
  artifact_override: RM.MASTER
```

---

## 5. RM_PRESSURE

```yaml
rm_pressure:
  canonical_name: "master.tsd.crossrupture.discovery.base"
  previous_names:
    - "CROSSRUPTURE.DISCOVERY-BASE"
    - "Base de Descoberta Viva"
    - "TSD.CROSSRUPTURE.DISCOVERY-BASE"
  aliases_forbidden_as_authority: true

  layer_primary: SEMANTIC
  vertical_family: DISCOVERY

  kind: RM.MASTER
  runtime_grade: doconly

  dependencies:
    - TRILHO
    - RM.UNIFICATION
    - tsd.discovery.gate.mep.reactivation
    - tsd.bopex
    - tsd.closure.governor

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

  evidence_level: INFERENCIA_DOCUMENTADA
  gaps:
    - corpus_de_calibracao_gptplus
    - symbol_map_binder_lsu
    - componentes_vivos_priorizados
    - tabela_de_problema_forte
    - corpus_multimodal_minimo
  conflicts: []
  return_target: na
```

---

## 6. SYMBOL_CARD

```yaml
symbol_card:
  glyph: "na"
  symbol_id: "UNMAPPED"
  current_name: "master.tsd.crossrupture.discovery.base"
  previous_name: "CROSSRUPTURE.DISCOVERY-BASE"
  function: "rotear familia documental de descoberta viva e cruzamento TESSERUS"
  executor_guardian: "na"
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
    - "analise e cruze com TESSERUS"
  boot_index: null
  collapse_priority: null
  fallback_path: "RM.UNIFICATION"
  nd_pressure: "nD"
  risk_flag: medium
  symbolic_authority: partial
  symbol_map_required_for_future: true
  binder_required_for_future: true
  lsu_required_for_future: true
```

---

## 7. SUMARIO EXECUTIVO

FAMILIA:
- `tsd.crossrupture.discovery.base`

DESCRICAO NAO TECNICA:
- Familia metodologica que preserva hipoteses fortes durante discovery, cruza entradas com TESSERUS e aplica morte dura apenas no fechamento.

FUNCAO DO MASTER:
- Roteia a familia documental, sem duplicar teoria dos componentes.

COMPONENTE PRINCIPAL:
- `componente.tsd.crossrupture.discovery.base.core`

COMPONENTES DERIVADOS:
- `componente.tsd.crossrupture.discovery.base.prepass`
- `componente.tsd.crossrupture.discovery.base.bopex-lint`
- `componente.tsd.crossrupture.discovery.base.mep-retention`
- `componente.tsd.crossrupture.discovery.base.final-kill`
- `componente.tsd.crossrupture.discovery.base.hypothesis-card`

RM.DocFIELD:
- necessario e pendente.

OBSIDIAN:
- posterior obrigatorio em modo component-first quando RM.COMPONENTES e RM.DocFIELD estiverem coerentes.

CORPUS:
- posterior obrigatorio para overview, prontidao, pseudoruntime, resultados, gauntlet, promocao sequencial, auditoria, relatorio, registro e assinatura.

BLOQUEIOS:
- nenhum bloqueio para RM.COMPONENTES.
- promocao canonica bloqueada por falta de corpus real, symbol map/binder/LSU e validacao por casos.

DECISAO ATUAL:
- familia propria, `METHOD_LOOP`, pronta para RM.COMPONENTES.

PROXIMA ETAPA:
- RM.COMPONENTES.

---

## 8. ESCOPO E FRONTEIRAS

INCLUI:
- identidade da familia;
- componente principal;
- componentes derivados candidatos;
- papeis documentais;
- relacoes entre pecas;
- autoridade de cada peca;
- dependencias;
- lacunas;
- destino de emissao;
- handoff para RM.COMPONENTES.

NAO INCLUI:
- teoria interna detalhada dos componentes;
- contratos mecanicos de tabela;
- execucao;
- sidecars Obsidian;
- pseudoruntime;
- resultados;
- gauntlet;
- promocao sequencial;
- auditoria CORPUS;
- assinatura final.

REGRAS DURAS:
- MASTER e roteador.
- MASTER nao duplica componente.
- MASTER nao cria ProtoEXEC.
- MASTER nao assina DocEND.
- MASTER nao usa identidade documental legada.
- RM.DocFIELD fica como etapa mecanico-documental posterior.
- Hipotese nao vira prova por organizacao documental.

---

## 9. FONTES E AUTORIDADE

| source_id | fonte | tipo | autoridade | papel no MASTER | status |
|---|---|---|---|---|---|
| SRC001 | trilho.tsd.crossrupture.discovery.base | TRILHO | alta | fonte de estado, escopo e regra central | lido |
| SRC002 | rm.unification.tsd.crossrupture.discovery.base | RM.UNIFICATION | alta | saneamento de categoria e familia | lido |
| SRC003 | chat atual | fonte local | media | comando de emissao RM.MASTER | lido |
| SRC004 | docs BOPEX | apoio | media | lint estrutural auxiliar | referenciado |
| SRC005 | discovery.gate.mep.reactivation | apoio | media | retencao e reativacao | referenciado |
| SRC006 | closure.governor | apoio | media | fechamento e morte final | referenciado |

```text
AUTHORITY_RESOLUTION:
fonte_soberana_escolhida: RM.UNIFICATION
fontes_secundarias: TRILHO, chat atual
conflitos_de_autoridade: nenhum ativo
decisao_de_autoridade: RM.UNIFICATION resolveu CROSSRUPTURE como familia metodologica propria.
```

---

## 10. MAPA DA FAMILIA

```yaml
family_map:
  family_id: "crossrupture.discovery.base"
  master_doc_id: "master.tsd.crossrupture.discovery.base"

  principal_component:
    doc_id: "componente.tsd.crossrupture.discovery.base.core"
    name: "crossrupture.core"
    role: principal
    status: pendente

  derived_components:
    - doc_id: "componente.tsd.crossrupture.discovery.base.prepass"
      name: "crossrupture.prepass"
      role: derivado
      parent: "componente.tsd.crossrupture.discovery.base.core"
      status: pendente
    - doc_id: "componente.tsd.crossrupture.discovery.base.bopex-lint"
      name: "crossrupture.bopex-lint"
      role: derivado
      parent: "componente.tsd.crossrupture.discovery.base.core"
      status: pendente
    - doc_id: "componente.tsd.crossrupture.discovery.base.mep-retention"
      name: "crossrupture.mep-retention"
      role: derivado
      parent: "componente.tsd.crossrupture.discovery.base.core"
      status: pendente
    - doc_id: "componente.tsd.crossrupture.discovery.base.final-kill"
      name: "crossrupture.final-kill"
      role: derivado
      parent: "componente.tsd.crossrupture.discovery.base.core"
      status: pendente
    - doc_id: "componente.tsd.crossrupture.discovery.base.hypothesis-card"
      name: "crossrupture.hypothesis-card"
      role: derivado
      parent: "componente.tsd.crossrupture.discovery.base.core"
      status: pendente

  docfield:
    doc_id: "rm.docfield.tsd.crossrupture.discovery.base"
    required: true
    status: pendente

  obsidian:
    component_map: "OBSIDIAN.COMPONENTES"
    bases: "OBSIDIAN.BASES"
    optional_visual_exception: "none"
    status: posterior

  corpus:
    status: posterior
```

---

## 11. REGISTRO DE COMPONENTES

| component_id | doc_id | nome | papel | camada 4-stack | funcao | status | proxima acao |
|---|---|---|---|---|---|---|---|
| CMP001 | componente.tsd.crossrupture.discovery.base.core | crossrupture.core | principal | SEMANTIC | governa o metodo de descoberta viva e cruzamento | pendente | emitir RM.COMPONENTES |
| CMP002 | componente.tsd.crossrupture.discovery.base.prepass | crossrupture.prepass | derivado | SEMANTIC | preserva bruto e separa forma, sensacao, mecanismo e claim | pendente | emitir RM.COMPONENTES |
| CMP003 | componente.tsd.crossrupture.discovery.base.bopex-lint | crossrupture.bopex-lint | derivado | CONTRACTS | aplica BOPEX como saneamento estrutural sem decidir ruptura | pendente | emitir RM.COMPONENTES |
| CMP004 | componente.tsd.crossrupture.discovery.base.mep-retention | crossrupture.mep-retention | derivado | SKIN | registra hipotese viva, suspensa ou reativada | pendente | emitir RM.COMPONENTES |
| CMP005 | componente.tsd.crossrupture.discovery.base.final-kill | crossrupture.final-kill | derivado | CONTRACTS | concentra criterio de morte somente no fechamento | pendente | emitir RM.COMPONENTES |
| CMP006 | componente.tsd.crossrupture.discovery.base.hypothesis-card | crossrupture.hypothesis-card | derivado | SKIN | estrutura ficha minima de hipotese viva | pendente | emitir RM.COMPONENTES |

---

## 12. RELACOES E GRAFO DOCUMENTAL

| origem | relacao | destino | motivo | autoridade |
|---|---|---|---|---|
| master.tsd.crossrupture.discovery.base | master_of | componente.tsd.crossrupture.discovery.base.core | componente principal da familia | RM.MASTER |
| componente.tsd.crossrupture.discovery.base.prepass | derivative_of | componente.tsd.crossrupture.discovery.base.core | etapa inicial do metodo | RM.MASTER |
| componente.tsd.crossrupture.discovery.base.bopex-lint | derivative_of | componente.tsd.crossrupture.discovery.base.core | saneamento estrutural auxiliar | RM.MASTER |
| componente.tsd.crossrupture.discovery.base.mep-retention | derivative_of | componente.tsd.crossrupture.discovery.base.core | retencao de hipotese viva | RM.MASTER |
| componente.tsd.crossrupture.discovery.base.final-kill | derivative_of | componente.tsd.crossrupture.discovery.base.core | morte final no fechamento | RM.MASTER |
| componente.tsd.crossrupture.discovery.base.hypothesis-card | derivative_of | componente.tsd.crossrupture.discovery.base.core | envelope de registro da hipotese | RM.MASTER |
| rm.docfield.tsd.crossrupture.discovery.base | materializes | componente.tsd.crossrupture.discovery.base.core | forma mecanico-documental futura | RM.DocFIELD |

```text
GRAFO ASCII:
[RM.MASTER]
   └── master_of ──> [crossrupture.core]
                       ├── derivative_of <── [crossrupture.prepass]
                       ├── derivative_of <── [crossrupture.bopex-lint]
                       ├── derivative_of <── [crossrupture.mep-retention]
                       ├── derivative_of <── [crossrupture.final-kill]
                       ├── derivative_of <── [crossrupture.hypothesis-card]
                       └── materialized_by -> [RM.DocFIELD futuro]
```

---

## 13. DECISOES DO MASTER

| decision_id | decisao | motivo | impacto | estado |
|---|---|---|---|---|
| D001 | manter CROSSRUPTURE como familia metodologica propria | RM.UNIFICATION resolveu que o escopo excede MEP.REACTIVATION | evita absorcao indevida por discovery.gate | ativa |
| D002 | definir `crossrupture.core` como componente principal | a familia precisa de centro documental antes dos derivados | prepara RM.COMPONENTES | ativa |
| D003 | tratar BOPEX como dependencia/lint, nao componente interno duplicado | BOPEX ja e familia propria | evita duplicacao de autoridade | ativa |
| D004 | tratar MEP como dependencia de retencao, nao pai soberano | MEP retém, mas nao cobre a rota completa | preserva fronteira de familia | ativa |
| D005 | tratar closure.governor como consumidor de fechamento | fechamento mata/promove, mas nao governa discovery | preserva discovery permissivo | ativa |
| D006 | bloquear promocao simbolica forte sem symbol map/binder/LSU | autoridade simbolica ausente | impede simbolo inventado | ativa |
| D007 | seguir para RM.COMPONENTES | principal e derivados estao roteados | proxima etapa liberada | ativa |

```text
DECISAO D007:
- o que decide: emitir RM.COMPONENTES como proxima etapa.
- por que decide: a familia foi saneada e o master ja mapeou principal e derivados candidatos.
- o que permite: detalhar mecanismo, contratos, relacoes e limites de cada componente.
- o que bloqueia: pular para RM.DocFIELD antes de componentes.
- evidencia: INFERENCIA_DOCUMENTADA.
```

---

## 14. LACUNAS, CONFLITOS E RETORNOS

| gap_id | tipo | descricao | impacto | retorno |
|---|---|---|---|---|
| G001 | lacuna | corpus de calibracao GPTplus ainda ausente | bloqueia maturidade canonica | RM.COMPONENTES |
| G002 | lacuna | symbol map, binder e LSU ausentes | bloqueia promocao simbolica forte e DocFIELD mecanico robusto | RM.DocFIELD |
| G003 | lacuna | lista priorizada de componentes vivos nao derivada do inventario | aumenta custo de interna-tess | RM.COMPONENTES |
| G004 | lacuna | tabela de problema forte ainda nao formalizada | reduz precisao de ruptura acima de extremo | RM.COMPONENTES |
| G005 | lacuna | corpus multimodal minimo ausente | bloqueia CORPUS posterior | CORPUS |

RETORNOS POSSIVEIS:
- RM.UNIFICATION: apenas se nova colisao de familia surgir.
- HUMANO: apenas se Nilton decidir absorver CROSSRUPTURE por outra familia.
- RM.COMPONENTES: caminho normal.

---

## 15. MATRIZ DE COBERTURA DO MASTER

| item | esperado | presente | status | acao |
|---|---|---|---|---|
| fonte TRILHO | sim | sim | ok | preservar |
| RM.UNIFICATION | sim | sim | ok | preservar |
| componente principal | sim | sim | ok | emitir RM.COMPONENTES |
| derivados | opcional | parcial | ok | detalhar em RM.COMPONENTES |
| RM.DocFIELD requerido | decidir | sim | ok | emitir depois de componentes |
| grafo documental | sim | sim | ok | preservar |
| handoff | sim | sim | ok | seguir RM.COMPONENTES |
| evidencias rotuladas | sim | sim | ok | preservar |

---

## 16. HANDOFF PARA PROXIMA ETAPA

```yaml
handoff:
  status: PRONTO_PARA_RM.COMPONENTES

  target: RM.COMPONENTES

  payload:
    master_doc_id: "master.tsd.crossrupture.discovery.base"
    family_id: "crossrupture.discovery.base"
    principal_component: "componente.tsd.crossrupture.discovery.base.core"
    derived_components:
      - "componente.tsd.crossrupture.discovery.base.prepass"
      - "componente.tsd.crossrupture.discovery.base.bopex-lint"
      - "componente.tsd.crossrupture.discovery.base.mep-retention"
      - "componente.tsd.crossrupture.discovery.base.final-kill"
      - "componente.tsd.crossrupture.discovery.base.hypothesis-card"
    docfield_required: true
    relation_map: presente
    authority_resolution: presente
    blockers: []
    lacunas:
      - corpus_de_calibracao_gptplus
      - symbol_map_binder_lsu
      - componentes_vivos_priorizados
      - tabela_de_problema_forte
      - corpus_multimodal_minimo

handoff_compacto:
  tema: "CROSSRUPTURE"
  foco: "base de descoberta viva e cruzamento TESSERUS"
  objetivo: "emitir componentes da familia metodologica"
  estado_atual: "RM.MASTER EM_TESTE"
  evidencia: alta
  bloqueios: []
  saida_esperada: "RM.COMPONENTES"
```

---

## 17. FIDELIDADE CANONICA

```text
- MASTER emitido como roteador de familia.
- Nenhuma teoria interna de componente foi duplicada.
- Nenhum derivado foi tratado como classe raiz.
- Componente principal definido.
- RM.DocFIELD tratado como etapa futura.
- Obsidian tratado como etapa posterior component-first.
- CORPUS tratado como etapa posterior.
- DocEND, ProtoEXEC e SUSPENSO nao emitidos pelo MASTER.
- Handoff definido para RM.COMPONENTES.
```

---

## 18. RODAPE DE INTEGRIDADE

```yaml
evidence_summary:
  provado:
    - TRILHO publicado existe
    - RM.UNIFICATION publicado existe
  inferencia_documentada:
    - CROSSRUPTURE e familia metodologica propria
    - MEP e dependencia de retencao
    - BOPEX e lint estrutural auxiliar
    - closure.governor e consumidor de fechamento
  hipotese:
    - derivados listados poderao ser ajustados em RM.COMPONENTES
  simulado:
    - nenhum benchmark do metodo foi executado
    - nenhum corpus multimodal foi rodado

activation_trace:
  route_taken: "RM.UNIFICATION -> RM.MASTER"
  route_reason: "familia saneada como METHOD_LOOP independente"
  suppressed_modes:
    - RM.DocFIELD
    - OBSIDIAN
    - CORPUS
  unsafe_or_legacy_terms_seen: []
  next_allowed_activation: "RM.COMPONENTES"

audit_trace:
  rm_seed_ref: "trilho.tsd.crossrupture.discovery.base"
  dossier_graph_ref: "rm.unification.tsd.crossrupture.discovery.base"
  ledger_ref: null
  chrona_ref: null
  symbol_map_ref: "UNMAPPED"

next_stage:
  expected: RM.COMPONENTES
  allowed: true
  reason: "familia e principal/derivados candidatos estao roteados"

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

## 19. MARCACAO OBSIDIAN

```text
OBSIDIAN: [crossrupture.discovery.base:master]
```

Obsidian futuro deve seguir:

```text
OBSIDIAN.COMPONENTES -> OBSIDIAN.BASES
```

---

## 20. FULL_CHAIN_COVERAGE_CARD

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

  current_stage: RM.MASTER
  previous_stage_ok: true
  next_stage: RM.COMPONENTES

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

## 21. VALIDACAO LOCAL

```yaml
local_validation:
  one_rm_stage_per_file: OK
  ai_markers_present: OK
  rm_pressure_present: OK
  symbol_card_present: OK
  obsidian_crossref_present: OK
  evidence_labels_present: OK
  handoff_present: OK
  no_critical_placeholders: OK
  no_legacy_alias_authority: OK
  no_docfield_promotion: OK
  no_runtime_promotion: OK
  no_production_as_cycle_state: OK
  github_path_ready: OK
```

---

## 22. REGRA FINAL RM.MASTER

```text
CROSSRUPTURE roteia a descoberta viva.
O core governa a familia.
Os derivados detalham etapas.
MEP retém.
BOPEX saneia.
Closure fecha.
A hipotese vive ate fechamento.
RM.COMPONENTES pode seguir.
```
