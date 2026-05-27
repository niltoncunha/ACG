# TESSERUS_TRILHO_STATE_vNext — TSD.REGENEGIS

> TRILHO canônico derivado do `DOSSIE_CHAT — TSD.REGENEGIS`.  
> Organiza estado documental, acervo, taxonomia, registro, família, runtime, vistas e handoff para RM.  
> Não é RM. Não é Obsidian. Não é CORPUS. Não é prova. Não é execução real.

---

## NATUREZA

Documento soberano de **estado documental, cobertura do chat, organização de acervo e handoff para RM**.

O TRILHO não substitui:

```text
RM
RM.DocFIELD
OBSIDIAN.COMPONENTES
OBSIDIAN.BASES
CORPUS
ProtoEXEC
```

Regra local deste trilho:

```text
REGENEGIS está em GO_CONDICIONAL como decisão de teste/promoção controlada,
não como estado final e não como capacidade provada.
```

---

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: vNext
::DOSSIER-KIND:: TRILHO
::CHAIN-STAGE:: TRILHO
::TRILHO-ROLE:: DOCUMENTAL_SOVEREIGN_ORCHESTRATOR
::UNIQUE-REFERENCE:: true
::LOCAL-ONLY:: true

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
doc_id: trilho.tsd.regenegis
titulo: "TRILHO — TSD.REGENEGIS"
trilho_id: "TRILHO.regenegis"
rev: "v1.0.0"
data: "2026-05-26"
tz: "America/Sao_Paulo"
autor: "TESSERUS.UDA + NILTON.CUNHA"
status: EM_TESTE

doc_kind: TRILHO
doc_class: DOCUMENTAL_SOVEREIGN_ORCHESTRATOR
authority_scope: fonte soberana do estado documental deste caso
master_relation: antecede emissao RM e governa o funil documental
unique_reference: true

case_id: "tsd.regenegis"
component_name: "REGENEGIS"
component_slug: "regenegis"
component_role_hint: ponte
```

---

# 2. DESCRIÇÃO NÃO TÉCNICA

```text
O QUE É:
- REGENEGIS é um classificador de resíduo antes de GENESIS.

PARA QUE SERVE:
- Decide se uma sobra de análise é novidade real, recombinação a recosturar ou ruído a rebaixar.

POR QUE IMPORTA:
- Evita que o TESSERUS invente regime novo cedo demais e preserva novidade fraca sem promover sem lastro.

O QUE NÃO É:
- Não é prova final.
- Não é runtime soberano.
- Não é RM.
- Não é CORPUS.
- Não é implantação no Gênio.

EXEMPLO HUMANO:
- Antes de abrir uma porta nova, REGENEGIS pergunta se aquilo é porta, parede mal vista ou sombra.
```

---

# 3. ESTADO DO FUNIL

```yaml
fase_atual: HANDOFF_RM
fase_status: FECHADA_COM_ASSUNCOES
proxima_fase_valida: HANDOFF_RM
modo: governance
runtime_applicability: PENDENTE
handoff_target: RM.UNIFICATION
handoff_status: PRONTO_PARA_RM_UNIFICATION
```

Justificativa:

```text
O caso tem nome canônico fixado pelo usuário, mas carrega aliases históricos, versões concorrentes descartadas, família ainda a sanear e fronteira entre componente, subcomponente e rota BOPEX. Portanto o próximo destino correto é RM.UNIFICATION, não RM.MASTER direto.
```

---

# 4. AI_ROUTER

```yaml
ai_router:
  activation_mode: GOVERNANCE
  activation_source: prefix
  prefix_detected: "@trilho-tess"
  prefix_valid: true
  precedence_applied: "DOSSIE_CHAT -> TRILHO"
  default_mode: INFO
  ambiguity_flag: none
  governance_requested: true
  tests_requested: false
  artifact_override: TRILHO
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

  kind: TRILHO
  runtime_grade: conditional

  dependencies:
    - DOSSIE_CHAT.tsd.regenegis
    - BOPEX
    - GENIO_DISCOVERY
    - TESSERUS principles
    - human_review_gate

  provides:
    - documental_state
    - acervo_inventory
    - taxonomy_seed
    - rm_seed
    - dossier_graph_seed
    - handoff_to_rm_unification

  consumes:
    - dossie-chat.tsd.regenegis
    - chat_messages
    - external_ai_responses
    - simulated_test_results

  touches_world: false
  requires_proof: true
  requires_gate: true
  requires_rollback: false

  evidence_level: SIMULADO
  gaps:
    - falta bateria de campo real
    - case_echo_strength precisa protocolo de medicao
    - TRISEAL esta como revisao humana no TEST
    - thresholds precisam calibragem real
  conflicts:
    - REGENESIS como nome historico nao pode concorrer com REGENEGIS
    - v2.4-CANON descartada nao pode virar base
    - S7-alpha suspenso nao pode virar arquitetura ativa sem novo ganho absurdo
  return_target: RM.UNIFICATION
```

---

# 6. SYMBOL_CARD

```yaml
symbol_card:
  glyph: "na"
  symbol_id: "na"
  current_name: "REGENEGIS"
  previous_name: "REGENESIS"
  function: "Classificar resíduo antes de autorizar GENESIS."
  executor_guardian: "BOPEX_ROUTE / human_review_gate"
  responsible_stack: ENGINE
  direct_dependencies:
    - residue_absorption_estimate
    - novelty_support
    - case_echo_strength
    - BOPEX_ROUTE
  reverse_dependencies:
    - GENIO_DISCOVERY
    - RM.DocFIELD futuro
    - CORPUS futuro
  trigger_reactions:
    - sobra analitica
    - novidade candidata
    - combinatorio elegante
    - ruido sedutor
    - alto risco
    - autoaplicacao
  boot_index: null
  collapse_priority: "P0..P8"
  fallback_path: "RM.UNIFICATION | HUMANO"
  nd_pressure: "nD"
  risk_flag: medium
```

---

# 7. SUMÁRIO EXECUTIVO

```text
TEMA / ACERVO:
- REGENEGIS, componente candidato para classificar resíduo antes de permitir GENESIS.

DESCRIÇÃO NÃO TÉCNICA:
- REGENEGIS decide se uma sobra de análise é descoberta real, recombinação a recosturar ou ruído a rebaixar.

FASE ATUAL:
- HANDOFF_RM / FECHADA_COM_ASSUNCOES.

O QUE JÁ FOI FECHADO:
- Nome canônico: REGENEGIS.
- Versão de teste: v2.1.2-TEST.
- Estado documental: GO_CONDICIONAL por simulação e validação externa, não GO final.
- v2.4-CANON descartada como regressão operacional.
- S7-alpha suspenso por complexidade alta e ganho baixo.
- TRISEAL no TEST é revisão humana.

BLOQUEIOS ATIVOS:
- Sem bateria de campo real.
- Sem protocolo final para case_echo_strength.
- Sem RM.UNIFICATION.
- Sem RM.DocFIELD.
- Sem CORPUS.

O QUE FOI CLASSIFICADO:
- REGENEGIS é componente candidato de ENGINE/DISCOVERY.
- RESIDUE_CLASSIFIER é subnúcleo candidato.
- BOPEX_ROUTE é rota/gate candidato.

O QUE AINDA ESTÁ SEM DESTINO:
- Calibração real dos thresholds.
- Medição empírica de case_echo_strength.
- Critérios automáticos futuros de TRISEAL.

DECISÃO ATUAL:
- Enviar para RM.UNIFICATION.

PRÓXIMA AÇÃO VÁLIDA:
- Emitir RM.UNIFICATION antes de qualquer RM.MASTER, DocFIELD ou implantação no Gênio.

HANDOFF ESPERADO:
- RM.UNIFICATION.
```

---

# 8. ESCOPO E REGRAS DURAS

```text
INCLUI:
- organização do acervo REGENEGIS
- taxonomia documental inicial
- rm_seed
- dossier_graph_seed
- resolução de autoridade pendente
- plano de família documental
- decisão de aplicabilidade de runtime como PENDENTE
- vistas e destinos
- handoff para RM.UNIFICATION

NÃO INCLUI:
- RM.UNIFICATION completo
- RM.MASTER
- RM.COMPONENTES
- RM.DocFIELD
- Obsidian
- CORPUS
- teste de campo real
- implantação no Gênio
- ProtoEXEC

REGRAS DURAS:
- O TRILHO governa estado documental, cobertura e handoff.
- O TRILHO não substitui RM.
- O TRILHO não substitui Obsidian.
- O TRILHO não substitui CORPUS.
- O TRILHO não promove para DocEND ou ProtoEXEC.
- Simulado não vira PROVADO.
- GO_CONDICIONAL é decisão de promoção/teste, não estado final.
- Nada pula RM.UNIFICATION neste caso.
```

---

# 9. MATRIZ DE COBERTURA LOCAL

| item_id | tópico do chat atual | fase destino | status | ação necessária |
|---|---|---|---|---|
| ITEM001 | Origem visual/metafórica: espelho, sombra, unidade paralela | ACERVO | OK | preservar como genesis fértil |
| ITEM002 | KEYCELL.TRICORE.SHADOWTILE | ACERVO | OK | manter como ancestral |
| ITEM003 | TRIAXIS-9 / REGIME.HORIZON / REGIME-GENESIS | TAXONOMIA | OK | classificar como ancestral/descartado útil |
| ITEM004 | REGENESIS -> REGENEGIS | REGISTRO | OK | fixar nome canônico |
| ITEM005 | S7-alpha | TAXONOMIA | OK | suspenso |
| ITEM006 | v2.4-CANON | TAXONOMIA | OK | descartado como regressão |
| ITEM007 | REGENEGIS v2.1.2-TEST | REGISTRO | OK | base de teste |
| ITEM008 | Equações RAE e novelty_support | RM.DocFIELD futuro | OK | preservar para RM |
| ITEM009 | P0..P8 e exceção P5+P7 | RM.DocFIELD futuro | OK | preservar para tabela mecânica |
| ITEM010 | Claude GO_CONDICIONAL | HANDOFF_RM | OK | registrar como lente externa |

| source_id | referência externa / anexo | tipo | origem | relação com o caso | ação |
|---|---|---|---|---|---|
| SRC001 | dossie-chat.tsd.regenegis | DOSSIE_CHAT | GitHub | fonte principal | consumido |
| SRC002 | regenegis_v21_test.html | anexo/Claude | chat | validação GO_CONDICIONAL | registrar |
| SRC003 | regenesis_v21cal_validation.html | anexo/Claude | chat | derrubou spec híbrida | registrar |
| SRC004 | sim_v24 outputs | anexo/Claude | chat | descartou v2.4-CANON | registrar |

---

# 10. ACERVO

## Objetivo

Congelar inventário bruto sem perda.

| item_id | origem | tipo_bruto | tema_aparente | observação_inicial |
|---|---|---|---|---|
| ITEM001 | chat | metáfora/imagem/vídeo | sombra/espelho/projeção | genesis visual |
| ITEM002 | chat | operador | TRI-CORE | ancestral fértil |
| ITEM003 | chat | arquitetura | TRIAXIS-9 | ancestral descartado |
| ITEM004 | chat | arquitetura | REGIME-GENESIS | ancestral pesado |
| ITEM005 | chat | arquitetura | S7-alpha | suspenso |
| ITEM006 | chat | componente | REGENEGIS | candidato ativo |
| ITEM007 | anexos | validação externa | Claude | lente externa, não autoridade final |
| ITEM008 | dossiê publicado | DOSSIE_CHAT | transferência contextual | fonte principal |

| source_id | origem | escopo | status_de_leitura |
|---|---|---|---|
| SRC001 | docs/tsd.regenegis/dossie-chat.tsd.regenegis.md | dossiê contextual completo | lido |
| SRC002 | chat atual | invocação @trilho-tess | lido |
| SRC003 | anexos Claude | validações e dashboards | lido via dossiê e contexto |

| item_id | origem | citado_no_chat | anexado | precisa_classificacao |
|---|---|---|---|---|
| ITEM006 | chat/dossiê | sim | sim | sim |
| ITEM008 | GitHub | sim | não | não |

```text
LACUNAS_INGESTAO:
- Campo real ainda ausente — impede GO final.
- Métrica operacional de case_echo_strength ainda sem protocolo — impede runtime soberano.
```

---

# 11. TAXONOMIA

## Objetivo

Classificar sem confundir documento, entidade, representação, histórico, hipótese ou runtime.

| item_id | tipo_documental | papel_soberano | justificativa |
|---|---|---|---|
| ITEM001 | HISTORICAL | origem fértil | preserva gênese visual |
| ITEM002 | HISTORICAL | ancestral operacional | ajudou a formar o núcleo de classificação |
| ITEM003 | HISTORICAL | arquitetura descartada útil | explica por que não usar regimes fixos |
| ITEM004 | HISTORICAL | arquitetura descartada útil | explica genesis sob pressão do objeto |
| ITEM005 | HISTORICAL | suspensão | complexidade alta para ganho baixo |
| ITEM006 | COMPONENT_CANDIDATE | componente candidato | nome canônico REGENEGIS |
| ITEM007 | SUPPORT | evidência simulada externa | Claude como lente externa |
| ITEM008 | DOSSIE_CHAT | fonte contextual | base principal do TRILHO |
| ITEM009 | TRILHO | estado documental | documento atual |

```text
ITENS_SEM_CLASSE:
- nenhum item crítico sem classe.

CONFLITOS_DE_CLASSE:
- REGENEGIS pode ser componente, subcomponente ou rota BOPEX. Decisão requerida em RM.UNIFICATION.
- RESIDUE_CLASSIFIER pode ser subcomponente de REGENEGIS ou núcleo interno. Decisão requerida em RM.UNIFICATION.
```

---

# 12. REGISTRO

## Objetivo

Preparar `RM_SEED` e `DOSSIER_GRAPH_SEED`.

| entity_id | canonical_name | layer_primary | kind | status | runtime_grade | alias_of | superseded_by | conflicts | notes |
|---|---|---|---|---|---|---|---|---|---|
| ENT001 | REGENEGIS | ENGINE | COMPONENT_CANDIDATE | EM_TESTE | conditional | na | na | aliases históricos | classificador de resíduo antes de GENESIS |
| ENT002 | RESIDUE_CLASSIFIER | ENGINE | SUBCOMPONENT_CANDIDATE | EM_TESTE | conditional | na | ENT001? | fronteira de identidade | núcleo NOVEL/COMBINATORY/NOISY |
| ENT003 | BOPEX_ROUTE | CONTRACTS | ROUTE_CANDIDATE | EM_TESTE | conditional | na | ENT001? | fronteira de identidade | ordem P0..P8 |
| ENT004 | TRISEAL_HUMAN_REVIEW | CONTRACTS | GATE_SUPPORT | EM_TESTE | doconly | na | na | critérios automáticos ausentes | revisão humana no TEST |
| ENT005 | REGENESIS | ENGINE | HISTORICAL_ALIAS | encerrado | na | ENT001 | ENT001 | não usar como canônico | nome anterior |
| ENT006 | S7-alpha | ENGINE | HISTORICAL_OPTION | suspenso | research_only | na | na | ganho insuficiente | não ativar sem nova evidência |
| ENT007 | v2.4-CANON | ENGINE | HISTORICAL_VERSION | descartado | blocked | na | na | regressão operacional | não usar como base |

| master_of | principal_of | derivative_of | representation_of | runtime_of | overview_of | map_of |
|---|---|---|---|---|---|---|
| REGENEGIS | pendente | na | na | na | na | na |
| RESIDUE_CLASSIFIER | na | REGENEGIS? | na | na | na | na |
| BOPEX_ROUTE | na | REGENEGIS? | na | na | na | na |

```text
AUTHORITY_RESOLUTION:
fonte_soberana_escolhida: TRILHO para estado documental; RM.UNIFICATION pendente para autoridade de identidade.
fontes_secundarias: DOSSIE_CHAT, Claude, anexos, chat atual.
conflitos_de_autoridade:
- REGENEGIS como componente versus subrota de BOPEX.
- RESIDUE_CLASSIFIER como subcomponente versus núcleo interno.
- GO_CONDICIONAL como decisão de teste, não estado final.
decisao_de_autoridade:
- Enviar para RM.UNIFICATION.
```

---

# 13. FAMÍLIA

## Objetivo

Definir se há família documental e qual emissão RM é permitida.

```yaml
familia_emit_plan:
  rm_unification: sim
  master: pendente
  principal: "REGENEGIS"
  derivados:
    - RESIDUE_CLASSIFIER
    - BOPEX_ROUTE
    - TRISEAL_HUMAN_REVIEW
  docfield: pendente
  obsidian: posterior
  corpus: posterior
  justificativa: "Há aliases históricos, versões descartadas e fronteira ambígua entre componente, subcomponente e rota. RM.UNIFICATION deve sanear antes de RM.MASTER."
```

```text
ENTRA_NA_FAMILIA:
- REGENEGIS
- RESIDUE_CLASSIFIER
- BOPEX_ROUTE
- RAE
- novelty_support
- case_echo_strength
- TRISEAL_HUMAN_REVIEW como suporte/gate de TEST

NAO_ENTRA_NA_FAMILIA:
- v2.4-CANON como base ativa
- S7-alpha como arquitetura ativa
- REGIME-GENESIS como componente ativo
- TRIAXIS-9 como componente ativo

MOTIVO:
- Entram apenas elementos necessários ao teste v2.1.2-TEST e à identidade atual.
```

---

# 14. RUNTIME

## Objetivo

Decidir se runtime se aplica sem transformar documento em execução.

```yaml
runtime_applicability: PENDENTE
runtime_decisao:
  motivo: "REGENEGIS é elegível para teste real controlado, mas ainda não possui bateria de campo, RM.DocFIELD, Obsidian ou CORPUS."
  pre_requisitos:
    - RM.UNIFICATION
    - RM.DocFIELD para campos e regras
    - bateria de campo real
    - logs de rota
    - critério formal para case_echo_strength
    - revisão humana TRISEAL no TEST
  handoff_para_docfield: pendente
  blockers:
    - sem campo real
    - sem RM.UNIFICATION
    - sem RM.DocFIELD
    - sem Obsidian
    - sem CORPUS
```

Regra:

```text
Runtime aplicável não autoriza ProtoEXEC.
ProtoEXEC só pode nascer depois de RM.DocFIELD + OBSIDIAN + CORPUS.
```

---

# 15. VISTAS

## Objetivo

Classificar vistas derivadas sem dar autoridade indevida.

| item_id | destino | justificativa |
|---|---|---|
| ITEM006 | overview.guide | leitura humana de REGENEGIS |
| ITEM008 | doc.support | DOSSIE_CHAT como fonte contextual |
| EQ001 | docfield.candidate | campo calculável RAE |
| EQ002 | docfield.candidate | campo calculável novelty_support |
| VIS004 | map.structural | pipeline/gate P0..P8 |
| MAT002 | map.structural | tabela de regras e rotas |

```text
SOBRAS_RESOLVIDAS:
- Nome canônico REGENEGIS.
- v2.1.2-TEST como versão de teste.
- v2.4-CANON descartada.
- S7-alpha suspenso.

SOBRAS_AINDA_PENDENTES:
- Identidade formal do componente no RM.
- Protocolo de medição de case_echo_strength.
- Critérios automáticos futuros de TRISEAL.
- Bateria de campo real.
```

---

# 16. BLOQUEIOS, LACUNAS E ASSUNÇÕES

| blocker_id | fase | motivo | impacto | owner | ação necessária | evidence_ref |
|---|---|---|---|---|---|---|
| B001 | REGISTRO | identidade RM ainda não saneada | bloqueia RM.MASTER direto | RM.UNIFICATION | decidir componente/subcomponente/rota | SRC001 |
| B002 | RUNTIME | sem teste de campo real | bloqueia GO final | HUMANO/CORPUS futuro | rodar bateria controlada | SRC002 |
| B003 | RUNTIME | case_echo_strength sem protocolo real | bloqueia runtime soberano | RM.DocFIELD futuro | definir medição | SRC001 |
| B004 | RUNTIME | TRISEAL humano em TEST | bloqueia automação plena | HUMANO | manter gate humano ou especificar automático | SRC001 |

| campo_ausente | por_que_importa | o_que_impede |
|---|---|---|
| protocolo case_echo_strength | evita arbitrariedade em eco de caso | GO final e runtime |
| corpus real de teste | diferencia simulado de evidência real | GO final |
| RM.UNIFICATION | saneia identidade | RM.MASTER e DocFIELD |
| tabela DocFIELD | transforma regras em estrutura mecânica | CORPUS futuro |

| assuncao | grau_de_confianca | risco_de_invalidacao |
|---|---|---|
| Pesos simples são suficientes para TEST | médio | campo real mostrar baixa discriminação |
| Quarantine preserva novidade sem inflar | médio | muitos casos úteis morrerem em quarantine |
| P5+P7 -> quarantine é rota mais segura | alto | campo real exigir reweave mais eficiente |
| S7-alpha não compensa massa | médio | nova bateria mostrar ganho absurdo |

---

# 17. HANDOFF CANÔNICO

```yaml
handoff:
  status: PRONTO_PARA_RM_UNIFICATION
  target: RM.UNIFICATION

  payload:
    acervo_ingestao_index: presente
    taxonomia_documental: presente
    rm_seed: presente
    dossier_graph_seed: presente
    authority_resolution: parcial
    familia_emit_plan: presente
    runtime_applicability: PENDENTE
    vistas_derivadas: presente
    blockers: presente
    lacunas: presente

handoff_compacto:
  tema: "REGENEGIS"
  foco: "classificador de resíduo antes de GENESIS"
  objetivo: "sanear identidade, família, aliases, subcomponentes e fronteira com BOPEX_ROUTE antes de RM.MASTER"
  estagio_atual: "HANDOFF_RM / FECHADA_COM_ASSUNCOES"
  evidencia: media
  baseline: presente em simulações; ausente em campo real
  bloqueios:
    - sem teste de campo real
    - sem protocolo de case_echo_strength
    - sem RM.UNIFICATION
    - sem RM.DocFIELD
  saida_esperada: "RM.UNIFICATION"
  fontes:
    - dossie-chat.tsd.regenegis
    - validações Claude
    - chat atual
```

---

# 18. FIDELIDADE CANÔNICA

```text
- ordem obrigatória mantida
- nenhuma fase pulada
- acervo não comprimido em prosa solta
- taxonomia não promovida sem autoridade
- conteúdo ausente virou LACUNAS / ASSUNÇÕES / BLOQUEIOS
- RM.DocFIELD preservado sem DOCFILE
- OBSIDIAN mantido como etapa posterior
- CORPUS mantido como etapa posterior
- DocEND, ProtoEXEC e SUSPENSO não emitidos pelo TRILHO
- promoção indevida bloqueada
```

---

# 19. RODAPÉ DE INTEGRIDADE

```yaml
evidence_summary:
  provado:
    - "Usuário fixou o nome canônico REGENEGIS."
    - "DOSSIE_CHAT foi publicado em docs/tsd.regenegis/dossie-chat.tsd.regenegis.md."
  inferencia_documentada:
    - "REGENEGIS é componente candidato de ENGINE/DISCOVERY."
    - "A próxima etapa documental correta é RM.UNIFICATION."
    - "O núcleo útil é classificar resíduo antes de permitir GENESIS."
  hipotese:
    - "REGENEGIS melhora discovery em campo real."
    - "case_echo_strength preserva novidade fraca sem inflar ruído."
  simulado:
    - "Claude validou v2.1.1-TEST com 19/20 e GO_CONDICIONAL."
    - "v2.4-CANON foi descartada após regressão operacional em simulado."
    - "Baterias anteriores indicaram zero falso GENESIS, zero meta inflation e zero high-risk overpromotion nas versões corrigidas."

activation_trace:
  route_taken: "trilho-tess"
  route_reason: "usuário invocou @trilho-tess após DOSSIE_CHAT"
  suppressed_modes:
    - DOSSIE_CHAT
    - RM
    - OBSIDIAN
    - CORPUS
    - ProtoEXEC
  unsafe_or_legacy_terms_seen:
    - legacy_document_file_identity: blocked
    - legacy_required_visual_master_route: blocked
    - legacy_cycle_state_pstate: blocked
  next_allowed_activation: RM.UNIFICATION

audit_trace:
  rm_seed_ref: "ENT001..ENT007"
  dossier_graph_ref: "VIS004 / MAT002 / BOPEX_ROUTE"
  ledger_ref: "D001..D006 in DOSSIE_CHAT"
  chrona_ref: "linha do tempo do DOSSIE_CHAT"
  symbol_map_ref: "SYMBOL_CARD.REGENEGIS"

next_stage:
  expected: RM.UNIFICATION
  allowed: true
  reason: "há aliases, versões descartadas e fronteira entre componente/subcomponente/rota a sanear antes de RM.MASTER"

final_guard:
  no_runtime_by_document_only: true
  no_promotion_without_evidence: true
  no_docfile_alias: true
  no_traditional_programming_as_primary_model: true
  no_corpus_before_obsidian: true
```

---

# 20. MARCAÇÃO OBSIDIAN

```text
OBSIDIAN: [regenegis:trilho]
@ref: regenegis:trilho
@ref: regenegis:chat
@ref: regenegis:eq
@ref: regenegis:bopex
@ref: regenegis:matriz
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
decisao: PRONTO_PARA_RM_UNIFICATION
obsidian: [regenegis:trilho]
```
