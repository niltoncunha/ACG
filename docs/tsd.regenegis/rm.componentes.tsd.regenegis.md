# RM.COMPONENTES — TSD.REGENEGIS

> Descrição estrutural do componente principal `REGENEGIS` e de seus derivados internos.  
> Derivado de `rm.master.tsd.regenegis`.  
> Não é RM.MASTER, não é RM.DocFIELD, não é Obsidian, não é CORPUS e não é execução real.

---

## NATUREZA

`RM.COMPONENTES` descreve o que é o componente, para que serve, qual mecanismo governa seu comportamento, quais contratos exige, quais limites bloqueiam promoção e qual próximo artefato deve ser emitido.

Cadeia ativa:

```text
DOSSIE_CHAT -> TRILHO -> RM.UNIFICATION -> RM.MASTER -> RM.COMPONENTES -> RM.DocFIELD -> OBSIDIAN.COMPONENTES -> OBSIDIAN.BASES -> CORPUS.* -> DocEND | ProtoEXEC | SUSPENSO
```

---

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: vNext
::DOSSIER-KIND:: RM.COMPONENTES
::CHAIN-STAGE:: RM.COMPONENTES
::COMPONENT-ROLE:: principal
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

# 1. CAPA E IDENTIDADE

```yaml
doc_id: rm.componentes.tsd.regenegis
titulo: "REGENEGIS — RM.COMPONENTES"
rev: "v1.0.0"
data: "2026-05-26"
tz: "America/Sao_Paulo"
autor: "TESSERUS.UDA + NILTON.CUNHA"
status: EM_TESTE

doc_kind: RM.COMPONENTES
doc_class: COMPONENT_STRUCTURE
component_role: principal
authority_scope: descrição estrutural soberana do componente

case_id: "tsd.regenegis"
family_id: "regenegis"
component_id: "regenegis"
component_name: "REGENEGIS"
parent_component: "na"

previous_stage_ref: "RM.MASTER"
next_stage_target: "RM.DocFIELD"
```

---

# 2. DESCRIÇÃO NÃO TÉCNICA

```text
O QUE É:
- REGENEGIS é um componente candidato que classifica a sobra de uma análise antes de permitir GENESIS.

PARA QUE SERVE:
- Decide se a sobra é novidade real, recombinação que precisa de reweave ou ruído que deve ser rebaixado.

POR QUE IMPORTA:
- Reduz a chance de o TESSERUS transformar ruído sedutor em proto-regime e preserva novidade fraca em quarantine quando ainda não há lastro suficiente.

COMO PENSAR:
- Funciona como uma alfândega de descoberta: uma sobra só atravessa para GENESIS se carregar sinais mínimos de novidade, estabilidade e segurança.

O QUE NÃO É:
- Não é MASTER.
- Não é RM.DocFIELD.
- Não é Obsidian.
- Não é CORPUS.
- Não é assinatura final.
- Não é execução real por si só.
```

---

# 3. ESTADO DO COMPONENTE

```yaml
component_state:
  source_master: presente
  source_unification: presente

  component_defined: true
  component_role: principal
  parent_defined: na
  mechanism_defined: true
  contracts_defined: partial
  docfield_required: true
  obsidian_required: true
  corpus_required: posterior

  authority_status: resolvida
  coverage_status: partial

  handoff_status: PRONTO_PARA_RM.DocFIELD
```

Nota:

```text
A estrutura do componente está definida para TEST, mas não há teste de campo real nem protocolo mecânico completo para todos os campos. Por isso o status permanece EM_TESTE e a evidência principal é SIMULADO.
```

---

# 4. AI_ROUTER

```yaml
ai_router:
  activation_mode: GOVERNANCE
  activation_source: prefix
  prefix_detected: "@rm-tess componente"
  prefix_valid: true
  precedence_applied: "RM.MASTER -> RM.COMPONENTES"
  default_mode: INFO
  ambiguity_flag: none
  governance_requested: true
  artifact_override: RM.COMPONENTES
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

  kind: RM.COMPONENTES
  runtime_grade: conditional

  dependencies:
    - RM.MASTER.tsd.regenegis
    - RM.UNIFICATION.tsd.regenegis
    - TRILHO.tsd.regenegis
    - DOSSIE_CHAT.tsd.regenegis
    - BOPEX
    - human_review_gate

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
    - simulated_validation_results

  touches_world: false
  requires_proof: true
  requires_gate: true
  requires_rollback: false

  evidence_level: SIMULADO
  gaps:
    - falta teste de campo real
    - case_echo_strength precisa protocolo mecânico
    - TRISEAL está como revisão humana em TEST
    - thresholds precisam calibração real
  conflicts: []
  return_target: RM.DocFIELD
```

---

# 6. SYMBOL_CARD

```yaml
symbol_card:
  glyph: "na"
  symbol_id: "REGENEGIS.CMP"
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
    - RM.DocFIELD
    - OBSIDIAN.COMPONENTES
    - CORPUS.OVERVIEW
  trigger_reactions:
    - sobra_analitica
    - novidade_candidata
    - combinatorio_elegante
    - ruido_sedutor
    - alto_risco
    - autoaplicacao
  boot_index: null
  collapse_priority: "P0..P8"
  fallback_path: "RM.MASTER | RM.UNIFICATION | HUMANO"
  nd_pressure: "nD"
  risk_flag: medium
```

---

# 7. SUMÁRIO EXECUTIVO

```text
COMPONENTE:
- REGENEGIS.

PAPEL:
- Principal.

DESCRIÇÃO NÃO TÉCNICA:
- Classificador de resíduo que decide se uma sobra de análise deve virar genesis_candidate, quarantine, reweave, reading, shadow, meta_shadow ou blocked.

FUNÇÃO ESTRUTURAL:
- Governar a passagem entre análise e GENESIS.

MECANISMO CENTRAL:
- Extrai um vetor mínimo, calcula estimativas de absorção/suporte de novidade e aplica uma precedência BOPEX_ROUTE P0..P8.

CAMADA PRIMÁRIA:
- ENGINE, com contratos relevantes em CONTRACTS.

DEPENDÊNCIAS:
- RM.MASTER.
- RM.UNIFICATION.
- BOPEX_ROUTE.
- TRISEAL_HUMAN_REVIEW.
- Métricas RAE, novelty_support e case_echo_strength.

SAÍDAS / O QUE ENTREGA:
- blocked.
- meta_shadow.
- shadow.
- reading.
- reweave.
- quarantine.
- genesis_candidate.

LIMITES:
- Não prova novidade em campo real.
- Não promove GO final.
- Não substitui CORPUS.
- Não executa GENESIS sozinho.

BLOQUEIOS:
- Sem teste de campo real.
- Sem protocolo mecânico de case_echo_strength.
- Sem RM.DocFIELD.

PRÓXIMA ETAPA:
- RM.DocFIELD.
```

---

# 8. ESCOPO E FRONTEIRAS

```text
INCLUI:
- identidade do componente
- papel na família
- função estrutural
- mecanismo central
- entradas e saídas
- invariantes
- limites
- dependências
- relações com derivados
- lacunas
- bloqueios
- handoff para RM.DocFIELD

NÃO INCLUI:
- roteamento completo da família
- tabelas mecânicas de RM.DocFIELD
- sidecars Obsidian
- pseudoruntime CORPUS
- resultados
- gauntlet
- promoção sequencial
- auditoria CORPUS
- assinatura final

REGRAS DURAS:
- Componente não promove a si mesmo.
- Componente não prova runtime por existir.
- Derivado sempre aponta para principal.
- Sem evidência de campo, GO final fica bloqueado.
```

---

# 9. FONTES E AUTORIDADE

| source_id | fonte | tipo | autoridade | papel no componente | status |
|---|---|---|---|---|---|
| SRC001 | RM.MASTER.tsd.regenegis | documento anterior | alta | define família e papel | lido |
| SRC002 | RM.UNIFICATION.tsd.regenegis | documento anterior | alta | saneia categoria e classe | lido |
| SRC003 | TRILHO.tsd.regenegis | documento anterior | média | estado e handoff | lido |
| SRC004 | DOSSIE_CHAT.tsd.regenegis | fonte contextual | média | gênese e decisões | lido |
| SRC005 | validações Claude | apoio externo | média | simulações e crítica | lido |

```text
AUTHORITY_RESOLUTION:
fonte_soberana_escolhida: RM.MASTER para papel familiar; RM.UNIFICATION para nome e categoria.
fontes_secundarias: TRILHO, DOSSIE_CHAT, Claude.
conflitos_de_autoridade: nenhum bloqueante.
decisao_de_autoridade: REGENEGIS é componente principal; derivados internos seguem subordinados.
```

---

# 10. IDENTIDADE E PAPEL NA FAMÍLIA

```yaml
component_identity:
  component_doc_id: "rm.componentes.tsd.regenegis"
  derived_doc_id: "na"
  component_role: principal

  family_id: "regenegis"
  master_doc_id: "rm.master.tsd.regenegis"

  parent_component:
    doc_id: "na"
    required: false
    status: na

  relation_to_family:
    role: principal
    reason: "REGENEGIS governa o mecanismo central da família: classificar resíduo antes de GENESIS."
    not_part_of_family_if:
      - "for tratado como alias histórico REGENESIS"
      - "for confundido com S7-alpha ou v2.4-CANON"
      - "for promovido para runtime sem RM.DocFIELD, Obsidian e CORPUS"
```

---

# 11. MECANISMO CENTRAL

```text
MECANISMO CENTRAL:
- REGENEGIS recebe uma sobra analítica, reduz a entrada a um vetor mínimo, calcula residue_absorption_estimate e novelty_support, e aplica BOPEX_ROUTE para colapsar a rota permitida.

ENTRADA:
- objeto ou sobra analítica
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

TRANSFORMAÇÃO:
- calcular RAE
- calcular novelty_support
- aplicar precedência P0..P8
- aplicar exceção P5 + P7 -> quarantine

SAÍDA:
- blocked
- meta_shadow
- shadow
- reading
- reweave
- quarantine
- genesis_candidate

INVARIANTES:
- GENESIS não responde a sobra bruta.
- Ruído não pode virar genesis_candidate.
- Alto risco não sobe para GENESIS no TEST.
- Autoaplicação vira meta_shadow.
- NOVEL + COMBINATORY simultâneos vão para quarantine.
- Simulado não vira prova.

O QUE GOVERNARIA UMA FALHA:
- falso GENESIS alto
- promoção em alto risco
- inflação meta
- recall de novidade real insuficiente em campo
- case_echo_strength arbitrário
```

---

# 12. CONTRATOS DO COMPONENTE

```yaml
component_contract:
  inputs:
    - residue_vector
    - risk_profile
    - self_application_flag
    - hard_noisy_flag
  outputs:
    - route
    - reason
    - evidence_level
    - human_review_requirement
  invariants:
    - "GENESIS só após classificação"
    - "alto risco não sobe no TEST"
    - "P5 + P7 roteia para quarantine"
    - "fallback final é shadow"
  preconditions:
    - "scores mínimos disponíveis ou lacuna declarada"
    - "risk_profile declarado"
    - "flag de autoaplicação avaliada"
  postconditions:
    - "uma rota final emitida"
    - "motivo registrável"
    - "se genesis_candidate, TRISEAL_HUMAN_REVIEW requerido"
  forbidden_states:
    - "genesis_candidate sem novelty_support"
    - "genesis_candidate com high risk no TEST"
    - "uso de versão v2.4-CANON como base ativa"
    - "uso de S7-alpha como arquitetura ativa sem nova evidência"
  fallback_path: "shadow | quarantine | HUMANO"
  rollback_requirement: optional
  evidence_required: true
  symbolic_first: true
  traditional_programming_primary: false
```

---

# 13. MAPA 4-STACK

| camada | papel neste componente | entrada | saída | risco |
|---|---|---|---|---|
| SEMANTIC | interpreta a sobra como NOVEL, COMBINATORY ou NOISY | resíduo analítico | classe de resíduo | subjetividade sem scores |
| SKIN | preserva rotas e leitura visual P0..P8 | estado classificado | rota legível | apagar precedência em prosa |
| ENGINE | calcula RAE, novelty_support e rota | scores | route decision | threshold mal calibrado |
| CONTRACTS | bloqueia promoção indevida e exige TRISEAL | risco, flags, rota | gate/fallback | confundir GO_CONDICIONAL com GO final |

---

# 14. DEPENDÊNCIAS E RELAÇÕES

| origem | relação | destino | motivo | autoridade |
|---|---|---|---|---|
| rm.componentes.tsd.regenegis | depends_on | rm.master.tsd.regenegis | papel familiar | RM |
| RESIDUE_CLASSIFIER | derivative_of | REGENEGIS | núcleo interno | RM |
| BOPEX_ROUTE | derivative_of | REGENEGIS | contrato de precedência | RM |
| TRISEAL_HUMAN_REVIEW | supports | REGENEGIS | gate humano de TEST | RM |
| rm.componentes.tsd.regenegis | materialized_by | rm.docfield.tsd.regenegis | forma mecânica documental | RM.DocFIELD |
| OBSIDIAN.COMPONENTES | mirrors | rm.componentes.tsd.regenegis | sidecar relacional posterior | OBSIDIAN |

```text
GRAFO ASCII:
[RM.MASTER: REGENEGIS]
   └── master_of ──> [RM.COMPONENTES: REGENEGIS]
                         ├── derivative_of <── [RESIDUE_CLASSIFIER]
                         ├── derivative_of <── [BOPEX_ROUTE]
                         ├── supports      <── [TRISEAL_HUMAN_REVIEW]
                         ├── materialized_by ──> [RM.DocFIELD]
                         └── mirrored_by ──> [OBSIDIAN.COMPONENTES]
```

---

# 15. ACHADOS E EVIDÊNCIAS

| achado_id | achado | evidência | nível | impacto |
|---|---|---|---|---|
| A001 | Nome canônico é REGENEGIS | decisão explícita do usuário | PROVADO | fixa identidade |
| A002 | REGENEGIS é componente principal candidato | RM.UNIFICATION + RM.MASTER | INFERENCIA_DOCUMENTADA | permite componente |
| A003 | Núcleo é classificar resíduo antes de GENESIS | DOSSIE_CHAT + TRILHO + RM | INFERENCIA_DOCUMENTADA | define mecanismo |
| A004 | Resultados de Claude sustentam GO_CONDICIONAL | baterias simuladas | SIMULADO | autoriza teste controlado |
| A005 | Eficácia em campo real ainda não existe | ausência de campo | HIPOTESE | bloqueia GO final |

---

# 16. DISCOVERY DO COMPONENTE

```yaml
component_discovery:
  status: arquivado
  rupture_candidates:
    - "classificação de resíduo antes de GENESIS"
    - "quarantine como preservação de borda sem promoção"
  hypotheses:
    - "REGENEGIS reduz falso GENESIS em campo real"
    - "case_echo_strength melhora recall de novidade real"
  neutral_fields:
    - "coverage_score"
    - "conflict_index"
    - "irreducibility_index"
    - "residue_stability_score"
    - "case_echo_strength"
  unresolved_questions:
    - "qual protocolo mecânico mede case_echo_strength?"
    - "qual recall real de novidade suja em campo?"
  kill_switches:
    - "false_genesis > limite definido em CORPUS futuro"
    - "high_risk_overpromotion > 0"
    - "meta_inflation > 0"
  promotion_blockers:
    - "sem teste de campo real"
    - "sem RM.DocFIELD"
    - "sem Obsidian"
    - "sem CORPUS"
```

---

# 17. LIMITES E QUANDO NÃO USAR

| limite_id | condição | por que importa | ação |
|---|---|---|---|
| L001 | objeto sem scores mínimos | decisão vira intuição | bloquear ou HUMANO |
| L002 | risk_profile alto | não deve promover em TEST | shadow |
| L003 | autoaplicação | risco de inflação meta | meta_shadow |
| L004 | case_echo_strength arbitrário | falso suporte NOVEL | quarantine ou HUMANO |
| L005 | tentativa de GO final com simulado | promoção indevida | bloquear |

```text
QUANDO NÃO USAR:
- Quando não houver objeto/resíduo mínimo.
- Quando a decisão exigir teste físico ou impacto externo.
- Quando o caso for de alto risco e não houver revisão humana.
- Quando a entrada pedir promoção canônica sem CORPUS.

FALLBACK:
- shadow
- quarantine
- HUMANO

RETORNO:
- RM.MASTER se papel familiar voltar a ficar ambíguo.
- RM.UNIFICATION se nome/categoria colidir.
- HUMANO se houver colisão de autoridade.
- CORPUS se a falha aparecer apenas em simulação documental futura.
```

---

# 18. LACUNAS, CONFLITOS E RETORNOS

| gap_id | tipo | descrição | impacto | retorno |
|---|---|---|---|---|
| G001 | lacuna | falta teste de campo real | bloqueia GO final | CORPUS futuro |
| G002 | lacuna | case_echo_strength sem protocolo mecânico | bloqueia runtime soberano | RM.DocFIELD |
| G003 | lacuna | TRISEAL humano não automatizado | limita TEST | HUMANO / RM.DocFIELD |
| G004 | lacuna | thresholds ainda simulados | exige calibração real | CORPUS futuro |
| G005 | conflito resolvido | REGENESIS versus REGENEGIS | resolvido por nome canônico | RM.UNIFICATION |

---

# 19. MATRIZ DE COBERTURA DO COMPONENTE

| item | esperado | presente | status | ação |
|---|---|---|---|---|
| fonte RM.MASTER | sim | sim | ok | — |
| papel do componente | sim | sim | ok | — |
| mecanismo central | sim | sim | ok | materializar em RM.DocFIELD |
| contratos | sim | parcial | ok para TEST | detalhar em RM.DocFIELD |
| mapa 4-stack | sim | sim | ok | — |
| limites/quando não usar | sim | sim | ok | — |
| discovery preservado | se existir | sim | ok | arquivar como contexto |
| handoff | sim | sim | ok | seguir para RM.DocFIELD |

---

# 20. HANDOFF PARA PRÓXIMA ETAPA

```yaml
handoff:
  status: PRONTO_PARA_RM.DocFIELD
  target: RM.DocFIELD

  payload:
    component_doc_id: "rm.componentes.tsd.regenegis"
    derived_doc_id: "na"
    component_role: principal
    parent_component: "na"

    mechanism_summary: presente
    component_contract: presente
    stack_map: presente
    relation_map: presente
    docfield_required: true
    obsidian_required: true
    blockers:
      - "sem teste de campo real"
      - "case_echo_strength sem protocolo mecânico"
      - "TRISEAL humano ainda não automatizado"
    lacunas:
      - "definir fields, binds, tabelas e slots"
      - "definir cálculo mecânico de is_hard_noisy"
      - "definir registro de rota e logs"
      - "definir readiness para CORPUS futuro"

handoff_compacto:
  tema: "REGENEGIS"
  foco: "componente principal"
  objetivo: "materializar campos, binds, tabelas e rotas em RM.DocFIELD"
  estado_atual: "EM_TESTE / PRONTO_PARA_RM.DocFIELD"
  evidencia: media
  bloqueios:
    - "sem campo real"
    - "sem protocolo case_echo_strength"
  saida_esperada: "RM.DocFIELD"
```

---

# 21. FIDELIDADE CANÔNICA

```text
- RM.COMPONENTES emitido como descrição estrutural de componente.
- Nenhuma teoria do MASTER foi duplicada.
- Nenhuma tabela mecânica de RM.DocFIELD foi emitida.
- Componente principal definido.
- Derivados tratados como subordinados.
- Mecanismo central descrito sem fingir execução.
- Contratos e invariantes explícitos.
- Limites e quando-não-usar registrados.
- Discovery preservado sem promoção.
- RM.DocFIELD preservado como etapa posterior.
- Obsidian tratado como etapa posterior.
- CORPUS tratado como etapa posterior.
- DocEND, ProtoEXEC e SUSPENSO não emitidos pelo componente.
- Handoff definido para RM.DocFIELD.
```

---

# 22. RODAPÉ DE INTEGRIDADE

```yaml
evidence_summary:
  provado:
    - "Nome canônico REGENEGIS fixado pelo usuário."
    - "RM.UNIFICATION e RM.MASTER publicados."
  inferencia_documentada:
    - "REGENEGIS é componente principal candidato."
    - "RESIDUE_CLASSIFIER, BOPEX_ROUTE e TRISEAL_HUMAN_REVIEW são derivados/suporte da família."
  hipotese:
    - "REGENEGIS terá valor em campo real como classificador de resíduo antes de GENESIS."
  simulado:
    - "Validações Claude e baterias simuladas sustentam GO_CONDICIONAL, não GO final."

activation_trace:
  route_taken: "rm-tess / RM.COMPONENTES"
  route_reason: "usuário invocou @rm-tess componente após RM.MASTER"
  suppressed_modes:
    - DOSSIE_CHAT
    - TRILHO
    - RM.UNIFICATION
    - RM.MASTER
    - RM.DocFIELD
    - OBSIDIAN
    - CORPUS
    - ProtoEXEC
  unsafe_or_legacy_terms_seen:
    - legacy_document_file_identity: blocked
    - legacy_rm_doc_abc_split: blocked
    - legacy_three_stage_documentary_chain: blocked
  next_allowed_activation: RM.DocFIELD

audit_trace:
  rm_seed_ref: "rm.master.tsd.regenegis"
  dossier_graph_ref: "trilho.tsd.regenegis"
  ledger_ref: "dossie-chat.tsd.regenegis"
  chrona_ref: "dossie-chat.tsd.regenegis chronology"
  symbol_map_ref: "SYMBOL_CARD.REGENEGIS.CMP"

next_stage:
  expected: RM.DocFIELD
  allowed: true
  reason: "Componente principal está estruturalmente descrito; forma mecânica pertence a RM.DocFIELD."

final_guard:
  component_is_not_master: true
  component_is_not_docfield: true
  component_is_not_corpus: true
  no_runtime_by_document_only: true
  no_promotion_without_evidence: true
  no_docfile_alias: true
  no_traditional_programming_as_primary_model: true
  no_corpus_before_obsidian: true
```

---

# 23. MARCAÇÃO OBSIDIAN

```text
OBSIDIAN: [regenegis:cmp]
@ref: regenegis:cmp
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
decisao: PRONTO_PARA_RM.DocFIELD
obsidian: [regenegis:cmp]
```
