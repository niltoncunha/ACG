# RM.COMPONENTES — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: RM.COMPONENTES
::CHAIN-STAGE:: RM.COMPONENTES
::COMPONENT-ROLE:: principal | derivado
::DERIVED-IS-COMPONENT:: true

::PREVIOUS-STAGE:: RM.MASTER
::NEXT-STAGE:: RM.DocFIELD

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
doc_id: rm.componentes.tsd.crossrupture.discovery.base
titulo: "CROSSRUPTURE — Componentes da Base de Descoberta Viva — RM.COMPONENTES"
rev: "v0.1.0"
data: "2026-05-26 00:00"
tz: "America/Sao_Paulo"
autor: "TESSERUS.UDA + NILTON.CUNHA"
status: EM_TESTE

doc_kind: RM.COMPONENTES
doc_class: COMPONENT_STRUCTURE_SET
authority_scope: descricao estrutural soberana dos componentes da familia

case_id: "tsd.crossrupture.discovery.base"
family_id: "crossrupture.discovery.base"
component_set: "crossrupture.discovery.base.components"
primary_component: "componente.tsd.crossrupture.discovery.base.core"

previous_stage_ref: "master.tsd.crossrupture.discovery.base"
next_stage_target: "RM.DocFIELD"
github_path: "docs/tsd.crossrupture.discovery.base/rm.componentes.tsd.crossrupture.discovery.base.md"
```

---

## 2. DESCRICAO NAO TECNICA

O QUE E:
- Este documento descreve o conjunto de componentes estruturais da familia CROSSRUPTURE.

PARA QUE SERVE:
- Serve para explicar o que cada componente faz dentro da base de descoberta viva: preservar a entrada bruta, manter hipoteses promissoras, aplicar lint estrutural, registrar fichas e matar somente no fechamento.

POR QUE IMPORTA:
- Sem componentes, o metodo ficaria como regra geral. Com componentes, ele ganha fronteiras, contratos, dependencias e handoff para RM.DocFIELD.

COMO PENSAR:
- A familia funciona como uma esteira documental de descoberta: recebe uma semente, preserva sua forma bruta, extrai mecanismo, cruza com TESSERUS, segura lacunas sem descarte e so endurece no fechamento.

O QUE NAO E:
- Nao e MASTER.
- Nao e RM.DocFIELD.
- Nao e Obsidian.
- Nao e CORPUS.
- Nao e assinatura final.
- Nao e execucao real por si so.

---

## 3. ESTADO DOS COMPONENTES

```yaml
component_state:
  source_master: presente
  source_unification: presente

  component_defined: true
  component_role: principal_plus_derivatives
  parent_defined: true
  mechanism_defined: true
  contracts_defined: partial
  docfield_required: true
  obsidian_required: true
  corpus_required: posterior

  authority_status: resolvida
  coverage_status: partial

  handoff_status: PRONTO_PARA_RM.DocFIELD
```

---

## 4. AI_ROUTER

```yaml
ai_router:
  activation_mode: DISCOVERY
  activation_source: inherited_chain
  prefix_detected: "faça"
  prefix_valid: true
  precedence_applied: rm_chain_after_master
  default_mode: INFO
  ambiguity_flag: none
  governance_requested: false
  artifact_override: RM.COMPONENTES
```

---

## 5. RM_PRESSURE

```yaml
rm_pressure:
  canonical_name: "rm.componentes.tsd.crossrupture.discovery.base"
  previous_names:
    - "CROSSRUPTURE.DISCOVERY-BASE"
    - "Base de Descoberta Viva"
  aliases_forbidden_as_authority: true

  layer_primary: MULTI
  vertical_family: DISCOVERY

  kind: RM.COMPONENTES
  runtime_grade: doconly

  dependencies:
    - RM.MASTER
    - RM.UNIFICATION
    - TRILHO
    - tsd.discovery.gate.mep.reactivation
    - tsd.bopex
    - tsd.closure.governor

  provides:
    - component_structure
    - mechanism_summary
    - contracts
    - invariants
    - boundaries
    - handoff_to_docfield
    - handoff_to_obsidian

  consumes:
    - family_map
    - relation_map
    - authority_resolution
    - component_registry

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
  current_name: "rm.componentes.tsd.crossrupture.discovery.base"
  previous_name: "CROSSRUPTURE.DISCOVERY-BASE"
  function: "descrever componentes da familia de descoberta viva e cruzamento TESSERUS"
  executor_guardian: "na"
  responsible_stack: MULTI
  direct_dependencies:
    - RM.MASTER
    - RM.UNIFICATION
    - TRILHO
  reverse_dependencies:
    - RM.DocFIELD
    - OBSIDIAN.COMPONENTES
    - CORPUS.OVERVIEW
  trigger_reactions:
    - "analise e cruze com TESSERUS"
  boot_index: null
  collapse_priority: null
  fallback_path: "RM.MASTER"
  nd_pressure: "nD"
  risk_flag: medium
  symbolic_authority: partial
  symbol_map_required_for_future: true
  binder_required_for_future: true
  lsu_required_for_future: true
```

---

## 7. SUMARIO EXECUTIVO

COMPONENTE PRINCIPAL:
- `componente.tsd.crossrupture.discovery.base.core`

PAPEL:
- principal.

DESCRICAO NAO TECNICA:
- O core governa o metodo inteiro: manter hipotese alta viva durante discovery, cruzar com TESSERUS e impedir morte antes do fechamento.

FUNCAO ESTRUTURAL:
- Orquestrar a rota de descoberta viva sem substituir `analise-tess`, `interna-tess`, BOPEX, MEP, ASM/MX14, externa, alien ou fechamento.

MECANISMO CENTRAL:
- Recebe uma entrada bruta, preserva o bruto, gera hipotese viva, aciona lint/retencao/cruzamento e entrega a linha para formalizacao ou fechamento.

CAMADA PRIMARIA:
- SEMANTIC.

DEPENDENCIAS:
- TRILHO, RM.UNIFICATION, RM.MASTER, BOPEX, MEP.REACTIVATION, closure.governor.

SAIDAS:
- hipotese viva, lacunas sem descarte, rota de proxima skill, handoff para fechamento ou persistencia.

LIMITES:
- nao prova, nao executa, nao promove, nao substitui skills especialistas.

BLOQUEIOS:
- sem validacao por casos reais para promocao canonica.
- sem symbol map/binder/LSU para camada simbolica forte.

PROXIMA ETAPA:
- RM.DocFIELD.

---

## 8. COMPONENTES DA FAMILIA

| component_id | doc_id | nome | papel | camada primaria | funcao | status |
|---|---|---|---|---|---|---|
| CMP001 | componente.tsd.crossrupture.discovery.base.core | crossrupture.core | principal | SEMANTIC | governa a rota de descoberta viva e cruzamento | EM_TESTE |
| CMP002 | componente.tsd.crossrupture.discovery.base.prepass | crossrupture.prepass | derivado | SEMANTIC | preserva entrada bruta e separa forma, sensacao, mecanismo e claim | EM_TESTE |
| CMP003 | componente.tsd.crossrupture.discovery.base.bopex-lint | crossrupture.bopex-lint | derivado | CONTRACTS | aplica BOPEX como saneamento estrutural sem decidir valor de ruptura | EM_TESTE |
| CMP004 | componente.tsd.crossrupture.discovery.base.mep-retention | crossrupture.mep-retention | derivado | SKIN | registra hipotese viva, suspensa ou reativada | EM_TESTE |
| CMP005 | componente.tsd.crossrupture.discovery.base.final-kill | crossrupture.final-kill | derivado | CONTRACTS | concentra criterios de morte final apenas no fechamento | EM_TESTE |
| CMP006 | componente.tsd.crossrupture.discovery.base.hypothesis-card | crossrupture.hypothesis-card | derivado | SKIN | estrutura a ficha minima de hipotese viva | EM_TESTE |

---

## 9. FONTES E AUTORIDADE

| source_id | fonte | tipo | autoridade | papel no componente | status |
|---|---|---|---|---|---|
| SRC001 | master.tsd.crossrupture.discovery.base | RM.MASTER | alta | define familia, principal e derivados | lido |
| SRC002 | rm.unification.tsd.crossrupture.discovery.base | RM.UNIFICATION | alta | saneia categoria, familia e autoridade | lido |
| SRC003 | trilho.tsd.crossrupture.discovery.base | TRILHO | media | preserva regra central e rota | lido |
| SRC004 | chat atual | fonte local | media | ativa proxima etapa | lido |

```text
AUTHORITY_RESOLUTION:
fonte_soberana_escolhida: RM.MASTER
fontes_secundarias: RM.UNIFICATION, TRILHO, chat atual
conflitos_de_autoridade: nenhum ativo
decisao_de_autoridade: RM.MASTER definiu o conjunto de componentes e liberou RM.COMPONENTES.
```

---

## 10. IDENTIDADE E PAPEL NA FAMILIA

```yaml
component_identity:
  family_id: "crossrupture.discovery.base"
  master_doc_id: "master.tsd.crossrupture.discovery.base"

  principal_component:
    component_doc_id: "componente.tsd.crossrupture.discovery.base.core"
    component_role: principal
    parent_component:
      doc_id: "na"
      required: false
      status: na
    relation_to_family:
      role: principal
      reason: "governa o metodo completo de descoberta viva e cruzamento"
      not_part_of_family_if:
        - "for tratado como runtime real"
        - "for tratado como substituto de analise-tess ou interna-tess"

  derived_components:
    - derived_doc_id: "componente.tsd.crossrupture.discovery.base.prepass"
      component_role: derivado
      parent_component: "componente.tsd.crossrupture.discovery.base.core"
      reason: "prepara entrada bruta sem matar hipotese"
    - derived_doc_id: "componente.tsd.crossrupture.discovery.base.bopex-lint"
      component_role: derivado
      parent_component: "componente.tsd.crossrupture.discovery.base.core"
      reason: "saneia classe, nome e representacao"
    - derived_doc_id: "componente.tsd.crossrupture.discovery.base.mep-retention"
      component_role: derivado
      parent_component: "componente.tsd.crossrupture.discovery.base.core"
      reason: "mantem hipotese viva, suspensa ou reativada"
    - derived_doc_id: "componente.tsd.crossrupture.discovery.base.final-kill"
      component_role: derivado
      parent_component: "componente.tsd.crossrupture.discovery.base.core"
      reason: "aplica morte dura somente no fechamento"
    - derived_doc_id: "componente.tsd.crossrupture.discovery.base.hypothesis-card"
      component_role: derivado
      parent_component: "componente.tsd.crossrupture.discovery.base.core"
      reason: "registra o estado minimo de hipotese viva"
```

---

## 11. MECANISMO CENTRAL

MECANISMO CENTRAL:
- A familia transforma entrada bruta em hipotese viva rastreavel. Falhas iniciais de baseline, bound, discriminador ou retroprojecao viram lacunas, nao descarte. O descarte duro fica reservado ao fechamento.

ENTRADA:
- imagem, video, metafora, ASCII, texto, equacao, resposta de IA ou seed bruta.

TRANSFORMACAO:
- preservar bruto;
- extrair forma, sensacao, mecanismo e claim;
- criar hipotese viva;
- aplicar BOPEX como lint quando houver risco de classe/nome/representacao;
- registrar MEP quando a linha exigir retencao;
- cruzar com TESSERUS via `analise-tess` e `interna-tess`;
- preparar formalizacao por ASM/MX14 quando houver potencial de ruptura;
- enviar para fechamento apenas quando houver maturidade ou pedido explicito.

SAIDA:
- ficha de hipotese viva;
- lacunas nomeadas;
- rota de proxima skill;
- status de descoberta;
- handoff para fechamento, documentacao ou suspensao.

INVARIANTES:
- hipotese alta nao morre por lacuna inicial;
- lacuna vira trilha, nao descarte;
- BOPEX nao decide ruptura;
- MEP nao vira pai soberano;
- fechamento e o ponto de morte dura;
- hipotese nao vira prova;
- runtime nao nasce por organizacao documental.

O QUE GOVERNARIA UMA FALHA:
- usar criterio de fechamento para matar durante discovery;
- promover hipotese como prova;
- transformar metodo documental em runtime;
- duplicar autoridade de BOPEX, MEP ou closure.governor;
- seguir para simbolico forte sem symbol map/binder/LSU.

---

## 12. CONTRATOS DOS COMPONENTES

```yaml
component_contract:
  inputs:
    - entrada_bruta
    - contexto_tesserus
    - trilho
    - rm_unification
    - rm_master
  outputs:
    - hipotese_viva
    - lacunas_nomeadas
    - bopex_lint_result
    - mep_status
    - rota_de_proxima_skill
    - handoff
  invariants:
    - discovery_permissivo
    - governance_duro
    - hipotese_alta_viva
    - lacuna_nao_e_descarte
    - morte_so_no_fechamento
    - hipotese_nao_vira_prova
    - bopex_lint_nao_decide_ruptura
    - mep_retention_nao_e_pai_soberano
  preconditions:
    - entrada_preservada
    - familia_crossrupture_definida
    - autoridade_rm_master_presente
  postconditions:
    - estado_da_hipotese_explicitado
    - lacunas_nao_promovidas
    - proxima_rota_declarada
  forbidden_states:
    - runtime_claim_sem_evidencia
    - canonico_sem_corpus
    - morte_precoce_por_lacuna_inicial
    - simbolo_inventado
    - fechamento_sem_evidencia
  fallback_path: "RM.MASTER"
  rollback_requirement: na
  evidence_required: true
  symbolic_first: true
  traditional_programming_primary: false
```

---

## 13. MAPA 4-STACK

| camada | papel neste componente | entrada | saida | risco |
|---|---|---|---|---|
| SEMANTIC | interpretar seed e preservar hipotese | imagem/metafora/video/texto | mecanismo suspeito e familia candidata | confundir metafora com prova |
| SKIN | registrar ficha, status e lacunas | hipotese viva | card, MEP, handoff | perder rastreabilidade |
| ENGINE | orquestrar rota entre skills | analise/interna/ASM/externa/alien | rota e pressao estrutural | pular etapa |
| CONTRACTS | impedir promocao indevida e morte precoce | principios, RM, closure | limites, kill final, bloqueios | governanca prematura ou frouxa |

---

## 14. DEPENDENCIAS E RELACOES

| origem | relacao | destino | motivo | autoridade |
|---|---|---|---|---|
| componente.tsd.crossrupture.discovery.base.core | depends_on | master.tsd.crossrupture.discovery.base | familia e autoridade | RM |
| componente.tsd.crossrupture.discovery.base.core | depends_on | tsd.discovery.gate.mep.reactivation | retencao e reativacao | RM |
| componente.tsd.crossrupture.discovery.base.core | depends_on | tsd.bopex | lint estrutural | RM |
| componente.tsd.crossrupture.discovery.base.core | depends_on | tsd.closure.governor | fechamento e morte final | RM |
| componente.tsd.crossrupture.discovery.base.prepass | derivative_of | componente.tsd.crossrupture.discovery.base.core | derivado subordinado | RM |
| componente.tsd.crossrupture.discovery.base.bopex-lint | derivative_of | componente.tsd.crossrupture.discovery.base.core | derivado subordinado | RM |
| componente.tsd.crossrupture.discovery.base.mep-retention | derivative_of | componente.tsd.crossrupture.discovery.base.core | derivado subordinado | RM |
| componente.tsd.crossrupture.discovery.base.final-kill | derivative_of | componente.tsd.crossrupture.discovery.base.core | derivado subordinado | RM |
| componente.tsd.crossrupture.discovery.base.hypothesis-card | derivative_of | componente.tsd.crossrupture.discovery.base.core | derivado subordinado | RM |
| rm.docfield.tsd.crossrupture.discovery.base | materializes | componente.tsd.crossrupture.discovery.base.core | forma mecanico-documental futura | RM.DocFIELD |
| obsidian.crossrupture.discovery.base.cmp | mirrors | componente.tsd.crossrupture.discovery.base.core | sidecar relacional futuro | OBSIDIAN |

```text
GRAFO ASCII:
[RM.MASTER]
   -> [RM.COMPONENTES: crossrupture.core]
        -> [prepass]
        -> [bopex-lint]
        -> [mep-retention]
        -> [final-kill]
        -> [hypothesis-card]
        -> [RM.DocFIELD futuro]
        -> [OBSIDIAN.COMPONENTES futuro]
```

---

## 15. ACHADOS E EVIDENCIAS

| achado_id | achado | evidencia | nivel | impacto |
|---|---|---|---|---|
| A001 | familia CROSSRUPTURE foi definida como metodologica propria | RM.UNIFICATION | PROVADO | libera componente principal |
| A002 | RM.MASTER definiu principal e derivados candidatos | RM.MASTER | PROVADO | libera RM.COMPONENTES |
| A003 | BOPEX deve sanear estrutura sem decidir ruptura | TRILHO + RM.UNIFICATION | INFERENCIA_DOCUMENTADA | evita censura indevida |
| A004 | MEP deve reter e reativar, nao governar a familia | RM.UNIFICATION | INFERENCIA_DOCUMENTADA | evita pai soberano incorreto |
| A005 | derivados listados ainda podem ser ajustados | RM.MASTER | HIPOTESE | preserva flexibilidade para RM.DocFIELD |
| A006 | nenhum benchmark real do metodo foi executado | RM.MASTER | SIMULADO | bloqueia promocao canonica |

---

## 16. DISCOVERY DOS COMPONENTES

```yaml
component_discovery:
  status: ativo
  rupture_candidates:
    - hipotese_viva_sem_descarte_precoce
    - cruzamento_multimodal_com_tesserus
    - final_kill_no_fechamento
  hypotheses:
    - "A preservacao de hipoteses altas reduz falso negativo criativo em discovery."
    - "BOPEX como lint estrutural reduz erro ontologico sem censurar ruptura."
    - "MEP como retencao reduz perda de seeds raras."
  neutral_fields:
    - entrada_bruta_para_mecanismo
    - lacuna_para_trilha
    - hipotese_para_fechamento
  unresolved_questions:
    - "Qual tabela formal define problema forte?"
    - "Qual corpus calibra cruzamentos bons antigos?"
    - "Qual symbol map/binder/LSU governa camada simbolica forte?"
  kill_switches:
    - morte_lexical
    - morte_baseline
    - morte_bound
    - morte_discriminador
    - morte_retroprojecao
    - morte_tesserus
    - morte_externa
    - morte_overformal
  promotion_blockers:
    - sem_corpus_real
    - sem_symbol_map_binder_lsu
    - sem_benchmark_do_metodo
```

Regra:

```text
Discovery preserva descoberta sem promover.
Nenhuma descoberta altera o estado dos componentes sem passar por evidencia, RM e CORPUS.
```

---

## 17. LIMITES E QUANDO NAO USAR

| limite_id | condicao | por que importa | acao |
|---|---|---|---|
| L001 | usuario pede fechamento/governanca | discovery nao deve substituir fechamento | rotear para fechamento-tess |
| L002 | seed exige prova externa | discovery interna nao basta | rotear para externa-tess |
| L003 | conflito de duas leituras vivas | colapso cedo pode matar mecanismo maior | rotear para ponte-tess |
| L004 | falta simbolo canonico | evita inventar simbolo | marcar UNMAPPED |
| L005 | pedido de runtime/ProtoEXEC | metodo ainda documental | bloquear promocao e rotear cadeia posterior |

QUANDO NAO USAR:
- quando o usuario pedir decisao final sem discovery;
- quando houver necessidade de auditoria operacional;
- quando o material ja estiver fechado para RM.DocFIELD;
- quando a entrada exigir busca publica antes de qualquer hipotese interna.

FALLBACK:
- fechamento-tess, externa-tess, ponte-tess, rm-tess ou humano, conforme o caso.

RETORNO:
- RM.MASTER se papel de componente ficar ambiguo.
- RM.UNIFICATION se categoria/familia colidir.
- HUMANO se autoridade nao puder ser resolvida.

---

## 18. LACUNAS, CONFLITOS E RETORNOS

| gap_id | tipo | descricao | impacto | retorno |
|---|---|---|---|---|
| G001 | lacuna | corpus de calibracao GPTplus ainda ausente | reduz repetibilidade e calibragem fina | RM.DocFIELD |
| G002 | lacuna | symbol map, binder e LSU ausentes | bloqueia promocao simbolica forte | RM.DocFIELD |
| G003 | lacuna | lista priorizada de componentes vivos nao derivada | aumenta custo de cruzamento interno | RM.DocFIELD |
| G004 | lacuna | tabela de problema forte nao formalizada | reduz precisao do filtro acima de extremo | RM.DocFIELD |
| G005 | lacuna | corpus multimodal minimo ausente | bloqueia CORPUS posterior | CORPUS |

Conflitos ativos:
- nenhum.

---

## 19. MATRIZ DE COBERTURA DOS COMPONENTES

| item | esperado | presente | status | acao |
|---|---|---|---|---|
| fonte RM.MASTER | sim | sim | ok | preservar |
| papel do componente principal | sim | sim | ok | materializar em RM.DocFIELD |
| derivados | sim | sim | ok | materializar em RM.DocFIELD |
| mecanismo central | sim | sim | ok | materializar em RM.DocFIELD |
| contratos | sim | parcial | ok | detalhar em RM.DocFIELD |
| mapa 4-stack | sim | sim | ok | preservar |
| limites/quando nao usar | sim | sim | ok | preservar |
| discovery preservado | sim | sim | ok | preservar |
| handoff | sim | sim | ok | seguir RM.DocFIELD |

---

## 20. HANDOFF PARA PROXIMA ETAPA

```yaml
handoff:
  status: PRONTO_PARA_RM.DocFIELD

  target: RM.DocFIELD

  payload:
    component_doc_id: "componente.tsd.crossrupture.discovery.base.core"
    derived_components:
      - "componente.tsd.crossrupture.discovery.base.prepass"
      - "componente.tsd.crossrupture.discovery.base.bopex-lint"
      - "componente.tsd.crossrupture.discovery.base.mep-retention"
      - "componente.tsd.crossrupture.discovery.base.final-kill"
      - "componente.tsd.crossrupture.discovery.base.hypothesis-card"
    component_role: principal_plus_derivatives
    parent_component: "na"

    mechanism_summary: presente
    component_contract: parcial
    stack_map: presente
    relation_map: presente
    docfield_required: true
    obsidian_required: true
    blockers: []
    lacunas:
      - corpus_de_calibracao_gptplus
      - symbol_map_binder_lsu
      - componentes_vivos_priorizados
      - tabela_de_problema_forte
      - corpus_multimodal_minimo

handoff_compacto:
  tema: "CROSSRUPTURE"
  foco: "componentes da base de descoberta viva"
  objetivo: "materializar forma mecanico-documental em RM.DocFIELD"
  estado_atual: "RM.COMPONENTES EM_TESTE"
  evidencia: alta
  bloqueios: []
  saida_esperada: "RM.DocFIELD"
```

---

## 21. FIDELIDADE CANONICA

```text
- RM.COMPONENTES emitido como descricao estrutural de componente.
- Nenhuma divisao documental legada foi usada.
- Nenhuma teoria do MASTER foi duplicada.
- Nenhuma tabela mecanica de RM.DocFIELD foi emitida.
- Componente principal definido.
- Derivados tratados como componentes subordinados.
- Mecanismo central descrito sem fingir execucao.
- Contratos e invariantes explicitos.
- Limites e quando-nao-usar registrados.
- Discovery preservado sem promocao.
- RM.DocFIELD preservado como etapa posterior.
- Obsidian tratado como etapa posterior.
- CORPUS tratado como etapa posterior.
- DocEND, ProtoEXEC e SUSPENSO nao emitidos pelo componente.
- Handoff definido para RM.DocFIELD.
```

---

## 22. RODAPE DE INTEGRIDADE

```yaml
evidence_summary:
  provado:
    - TRILHO publicado existe
    - RM.UNIFICATION publicado existe
    - RM.MASTER publicado existe
  inferencia_documentada:
    - crossrupture.core governa metodo de descoberta viva
    - derivados representam etapas estruturais do metodo
    - BOPEX e lint, MEP e retencao, closure e fechamento
  hipotese:
    - derivados poderao ser ajustados em RM.DocFIELD
  simulado:
    - nenhum benchmark do metodo foi executado
    - nenhum corpus multimodal foi rodado

activation_trace:
  route_taken: "RM.MASTER -> RM.COMPONENTES"
  route_reason: "principal e derivados candidatos foram roteados pelo MASTER"
  suppressed_modes:
    - RM.DocFIELD
    - OBSIDIAN
    - CORPUS
  unsafe_or_legacy_terms_seen: []
  next_allowed_activation: "RM.DocFIELD"

audit_trace:
  rm_seed_ref: "trilho.tsd.crossrupture.discovery.base"
  dossier_graph_ref: "rm.unification.tsd.crossrupture.discovery.base"
  ledger_ref: null
  chrona_ref: null
  symbol_map_ref: "UNMAPPED"

next_stage:
  expected: RM.DocFIELD
  allowed: true
  reason: "componentes estruturais foram definidos com contratos e lacunas"

final_guard:
  component_is_not_master: true
  component_is_not_docfield: true
  component_is_not_corpus: true
  no_runtime_by_document_only: true
  no_promotion_without_evidence: true
  no_docfield_alias: true
  no_traditional_programming_as_primary_model: true
  no_corpus_before_obsidian: true
```

---

## 23. MARCACAO OBSIDIAN

```text
OBSIDIAN: [crossrupture.discovery.base:cmp]
```

Para componentes futuros:

```text
OBSIDIAN.COMPONENTES -> OBSIDIAN.BASES
```

---

## 24. FULL_CHAIN_COVERAGE_CARD

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

  current_stage: RM.COMPONENTES
  previous_stage_ok: true
  next_stage: RM.DocFIELD

  universal_requirements:
    component_first_obsidian: true
    rm_docfield_without_docfield_alias: true
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

## 25. VALIDACAO LOCAL

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

## 26. REGRA FINAL RM.COMPONENTES

```text
O core governa.
Prepass preserva.
BOPEX saneia.
MEP retém.
Hypothesis-card registra.
Final-kill mata somente no fechamento.
RM.DocFIELD pode seguir.
```
