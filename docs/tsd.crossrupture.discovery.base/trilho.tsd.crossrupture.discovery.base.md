# TESSERUS_TRILHO_STATE_v1.1-LOCAL-ONLY

## S1 — CAPA E IDENTIDADE

DOC_ID: trilho.tsd.crossrupture.discovery.base  
TITULO: CROSSRUPTURE — Base de Descoberta Viva e Cruzamento TESSERUS  
TRILHO_ID: trilho.tsd.crossrupture.discovery.base  
REV: v0.1.0  
DATA: 2026-05-24  
TZ: America/Sao_Paulo  
AUTOR: TESSERUS.UDA + Nilton Cunha  
STATUS: PROTO_FORTE

DOC_KIND: trilho  
DOC_CLASS: documental.discovery.orchestrator  
AUTHORITY_SCOPE: metodo operacional de descoberta viva e cruzamento interno  
MASTER_RELATION: antecede eventual RM.UNIFICATION ou RM.MASTER  
UNIQUE_REFERENCE: true

FASE_ATUAL: REGISTRO  
PROXIMA_FASE_VALIDA: RM.UNIFICATION  
MODO: continue  
RUNTIME_APPLICABILITY: no  
HANDOFF_TARGET: rm-unification

CASE_ROOT: tsd.crossrupture.discovery.base  
NOME_CANONICO_DO_CASO: tsd.crossrupture.discovery.base  
GITHUB_PATH: docs/tsd.crossrupture.discovery.base/trilho.tsd.crossrupture.discovery.base.md

---

## AI_MARKERS

```text
AI_MARKERS:
::TESSERUS-DOSSIER-VERSION:: v1.1-LOCAL-ONLY
::DOSSIER-KIND:: TRILHO
::TRILHO-ROLE:: DISCOVERY_LIVE_ORCHESTRATOR
::UNIQUE-REFERENCE:: true
::LOCAL-ONLY:: true
::MODE-HINT:: continue
::INTENT-HINT:: registrar|orquestrar|preparar-handoff|crossrupture
::ANALYZE-TRIGGER:: "analise e cruze com TESSERUS" => ativar CROSSRUPTURE.DISCOVERY-BASE
::NAMING-CANON::
  ::KEY-STYLE:: dot
  ::ID-SCHEME::
    ::DECISION:: D001..D999
    ::ITEM:: ITEM001..ITEM999
    ::ENTITY:: ENT001..ENT999
    ::SOURCE:: SRC001..SRC999
  ::NO-UNDERSCORE:: true

::PHASE-ORDER::
  ::ORDER:: [prepass, analise, bopex-lint, mep-retention, interna, asm-mx14, externa, alien, fechamento, documentacao]
  ::SKIP:: forbidden
  ::EARLIEST-OPEN-PHASE-WINS:: true

::TRILHO-INVARIANTS::
  ::KEEP-HIGH-HYPOTHESES-ALIVE:: true
  ::NO-EARLY-KILL-FOR-MISSING-BASELINE:: true
  ::NO-EARLY-KILL-FOR-MISSING-BOUND:: true
  ::NO-EARLY-KILL-FOR-MISSING-DISCRIMINATOR:: true
  ::NO-EARLY-KILL-FOR-MISSING-RETROPROJECTION:: true
  ::FINAL-KILL-ONLY-IN-FECHAMENTO:: true
  ::DISCOVERY-PERMISSIVE-GOVERNANCE-HARD:: true
  ::ZERO-LOSS:: true

::OUTPUT-POLICY::
  ::LACUNAS-WHEN-MISSING:: true
  ::ASSUMPTIONS-WHEN-NEEDED:: true
  ::BLOCK-WHEN-AUTHORITY-UNCLEAR:: true
  ::DO-NOT-PROMOTE-HYPOTHESIS-AS-PROOF:: true

::LIFECYCLE-SEMANTICS::
  ::STATES:: [build, test, proto, runtime, estavel, canonico, bloqueado]
  ::PRODUCAO-AS-STATE:: forbidden
  ::GO-NOGO-SCOPE:: [runtime, estavel, canonico]
```

---

## S2 — SUMARIO EXECUTIVO

Este TRILHO registra a base operacional `CROSSRUPTURE.DISCOVERY-BASE`, criada para descoberta viva e cruzamento com TESSERUS.

O problema central resolvido e o descarte precoce de hipoteses fortes quando elas ainda nao possuem baseline, bound, discriminador inevitavel ou retroprojecao em dois ou mais dominios. Esses elementos continuam obrigatorios para fechamento forte, mas nao devem matar a hipotese durante a fase de descoberta.

A decisao principal e separar rigorosamente duas fases:

```text
DISCOVERY:
  manter hipoteses vivas
  registrar lacunas
  cruzar com TESSERUS
  acumular pressao estrutural

FECHAMENTO:
  aplicar kill final
  exigir principios TESSERUS
  decidir promover, suspender, arquivar ou matar
```

A base usa como rota principal:

```text
entrada bruta
  -> analise-tess
  -> BOPEX lint
  -> MEP retention
  -> interna-tess
  -> ASM-X / MX14
  -> externa-tess
  -> alien-tess
  -> fechamento-tess
```

Estado autorizado: `PROTO_FORTE`.  
Uso autorizado: analise, descoberta, cruzamento interno, imagem, video, metafora, ASCII, seed bruta e resposta de outra IA.  
Uso nao autorizado: declarar runtime real, benchmark, canone final ou prova empirica.

---

## S2.1 — DESCRICAO NAO TECNICA

O QUE E:
- Uma base de descoberta que mantem ideias promissoras vivas ate o fechamento.

PARA QUE SERVE:
- Serve para transformar imagens, metaforas, videos, textos, ASCII ou ideias brutas em hipoteses cruzaveis com o TESSERUS, sem matar cedo o que ainda pode amadurecer.

IMPORTANCIA DENTRO DO TESSERUS:
- Protege a fase de descoberta contra excesso de governanca prematura.
- Mantem rastreabilidade das lacunas sem transformar lacuna em descarte.
- Permite que `analise-tess` e `interna-tess` operem com mais contexto e menos perda.

DIFERENCA PRINCIPAL:
- Baseline, bound, discriminador e retroprojecao continuam necessarios, mas deixam de ser gatilhos de morte imediata.
- Eles viram lacunas vivas ate a fase de fechamento.

---

## S3 — ESCOPO E FONTES

### Escopo

Inclui:
- metodo de descoberta viva;
- cruzamento com TESSERUS;
- preservacao de hipoteses fortes;
- separacao entre descoberta e fechamento;
- BOPEX como lint estrutural auxiliar;
- MEP como retencao e reativacao;
- inventario vivo como orientador de `interna-tess`;
- principios TESSERUS como campo de orientacao;
- criterios de morte final apenas no fechamento.

Nao inclui:
- runtime executavel;
- benchmark real;
- prova empirica;
- promocao canonica;
- emissao RM;
- emissao Obsidian;
- publicacao de corpus;
- substituicao das skills especialistas.

### Fontes locais

```text
SRC001: chat atual sobre base de descoberta viva e crossrupture
SRC002: REGRA PARA DESCOBERTAS.md
SRC003: TESSERUS-LOCKED (LLM-ONLY).md
SRC004: ASM-X v1.3 Discovery-Omega
SRC005: ASM-X v1.4 Discovery-Omega-Infinito
SRC006: ASM-X v1.5b Discovery-REAL-Omega
SRC007: PROMPT_BASE_TESSERUS_ASM_SCS_AUTOCHAT_v1.0.md
SRC008: PROMPT SCS-nD
SRC009: componente.tsd.discovery.gate.mep.reactivation.md
SRC010: BOPEX family docs
SRC011: _Inventario_Documentos_tesserus.md
SRC012: closure.governor core/ecc/validation-pack docs
```

---

## S4 — MATRIZ DE COBERTURA DO CHAT / ACERVO LOCAL

| Topico-chave | Origem | Secao destino | Status | Acao necessaria |
|---|---|---|---|---|
| manter hipoteses vivas na descoberta | chat atual | S5/S6/S7 | OK | preservar regra |
| matar apenas no fechamento | chat atual | S6/S10/S12 | OK | preservar fronteira |
| nao descartar cedo por falta de baseline | chat atual | S5/S10 | OK | converter em lacuna |
| nao descartar cedo por falta de bound | chat atual | S5/S10 | OK | converter em lacuna |
| nao descartar cedo por falta de discriminador | chat atual | S5/S10 | OK | converter em lacuna |
| nao descartar cedo por falta de retroprojecao | chat atual | S5/S10 | OK | converter em lacuna |
| principios TESSERUS regem descoberta | chat atual | S6/S9 | OK | preservar lista |
| conservadorismo maximo no fechamento | chat atual | S6/S10 | OK | aplicar no selo final |
| BOPEX como lint estrutural | docs BOPEX | S7/S8 | OK | usar como auxiliar |
| MEP.REACTIVATION como retencao | docs discovery.gate | S7/S8 | OK | usar como memoria viva |
| inventario vivo como base interna | inventario | S7/S8 | OK | usar em interna-tess |

Estado:
- [x] Cobertura local suficiente para TRILHO v0.1.0.
- [x] Lacunas residuais registradas em S12.

---

## S5 — ACHADOS E EVIDENCIAS

### A001 — hipotese alta nao deve morrer na descoberta

MECANISMO:
- Durante discovery, ausencia de baseline, bound, discriminador ou retroprojecao nao e falha terminal.
- Esses itens viram lacunas nomeadas.

EFEITO:
- Reduz descarte prematuro.
- Mantem sementes fortes em circulacao controlada.

STATUS: INFERENCIA_DOCUMENTADA.

### A002 — fechamento e o unico ponto de morte dura

MECANISMO:
- A morte final so ocorre em `fechamento-tess` ou fase equivalente de closure.
- Antes disso, a hipotese pode ser `VIVA`, `SUSPENSA` ou `REATIVADA`.

EFEITO:
- Evita usar governanca como censura antecipada.

STATUS: INFERENCIA_DOCUMENTADA.

### A003 — principios TESSERUS sao campo de orientacao

MECANISMO:
- Os principios regem a direcao de busca, nao um checklist de descarte precoce.
- No fechamento, eles viram criterio duro.

EFEITO:
- Mantem liberdade criativa com destino verificavel.

STATUS: INFERENCIA_DOCUMENTADA.

### A004 — BOPEX saneia forma, mas nao decide ruptura

MECANISMO:
- BOPEX separa representacao, nome historico, tipo estrutural, alias e classe.
- Ele impede erro ontologico, mas nao substitui `analise-tess` nem `interna-tess`.

EFEITO:
- Evita confundir imagem, ASCII, metafora ou nome historico com tipo estrutural real.

STATUS: INFERENCIA_DOCUMENTADA.

### A005 — MEP e a memoria de hipotese viva

MECANISMO:
- MEP registra sinal minimo, condicao de ativacao, status e reativacao futura.
- Hipotese incompleta pode ser suspensa sem ser morta.

EFEITO:
- Evita perda de sementes raras.

STATUS: INFERENCIA_DOCUMENTADA.

### A006 — ASM-X e MX14 pressionam para prova condicional

MECANISMO:
- Campo neutro, invariantes, operador emergente, claim, bound e kill-switch formam a trilha de maturacao.
- Esses elementos nao precisam estar completos na entrada, mas precisam ser buscados.

EFEITO:
- Permite ruptura agressiva sem vender fantasia como prova.

STATUS: INFERENCIA_DOCUMENTADA.

---

## S6 — DECISOES

| ID | Decisao | Motivo | Impacto |
|---|---|---|---|
| D001 | classificar a base como `PROTO_FORTE` | ja e operavel em discovery, mas nao canonica | permite uso imediato |
| D002 | usar TRILHO como forma documental inicial | metodo governa rota e fases | prepara RM futura |
| D003 | preservar hipoteses altas ate fechamento | evita perda de ruptura potencial | discovery mais fértil |
| D004 | converter falhas iniciais em lacunas vivas | lacuna nao e descarte | melhor rastreabilidade |
| D005 | aplicar kill duro apenas no fechamento | separa discovery e governance | reduz falso negativo criativo |
| D006 | manter BOPEX como lint, nao juiz de valor | BOPEX classifica estrutura | evita censura indevida |
| D007 | usar MEP como suspensao e reativacao | discovery precisa memoria | evita duplicacao e perda |
| D008 | nao declarar runtime ou canone | estado ainda documental | evita promocao indevida |

---

## S7 — ARQUITETURA / DEVLINE

### 7.1 4-stack

```text
SEMANTIC:
  metafora, imagem, video, seed, principios, hipotese

SKIN:
  ficha de hipotese, MEP, registro de lacunas, handoff

ENGINE:
  analise-tess, interna-tess, BOPEX lint, ASM-X, MX14

CONTRACTS:
  principios TESSERUS, kill final, closure.governor, UNISKELL R3
```

### 7.2 Pipeline operacional

```text
INPUT
  imagem | video | metafora | ASCII | texto | equacao | resposta de IA

PREPASS
  preservar bruto
  separar forma, sensacao, mecanismo e claim

ANALISE-TESS
  extrair hipotese minima
  mapear mecanismo central
  detectar familia candidata

BOPEX-LINT
  separar representacao de ontologia
  separar nome historico de tipo estrutural
  identificar conflito nominal ou estrutural

MEP-RETENTION
  registrar hipotese viva
  marcar lacunas
  suspender ou reativar por condicao

INTERNA-TESS
  cruzar com inventario vivo
  detectar redundancia, conflito, fusao ou familia

ASM-MX14
  campo neutro
  invariantes
  operador emergente
  claim verificavel
  bound esperado
  kill-switch futuro

EXTERNA-TESS
  buscar baseline publico e equivalentes

ALIEN-TESS
  recombinar se sobreviver e ainda houver espaco de ruptura

FECHAMENTO-TESS
  aplicar morte final, suspensao ou promocao documental
```

### 7.3 Devline

```text
boot -> prepass -> analise -> lint -> retain -> interna -> formalize -> externalize -> alienate -> close -> document
```

---

## S7.5 — COMPONENT MATRIX DO METODO

| Layer | Inputs | Outputs | Estado | Invariantes |
|---|---|---|---|---|
| SEMANTIC | imagem, metafora, video, seed, principios | hipotese minima, mecanismo suspeito | vivo | nao matar cedo |
| SKIN | ficha, MEP, lacunas, handoff | trilha consultavel | proto | zero perda |
| ENGINE | analise, bopex, interna, ASM-X | cruzamento e pressao formal | proto | ordem de fases |
| CONTRACTS | principios, closure, UNISKELL | morte final ou promocao | fechado no fim | hipotese nao vira prova |

---

## S8 — CONTRATO DE HIPOTESE VIVA

```text
HYPOTHESIS_CARD:
  id:
  entrada_bruta:
  tipo_entrada: imagem | video | metafora | ascii | texto | equacao | outro
  mecanismo_suspeito:
  familia_candidata:
  principios_tesserus_ativados:
  ganho_suspeito:
  lacunas:
    - baseline
    - bound
    - discriminador
    - retroprojecao
    - simbolos
    - evidencia
  status:
    - VIVA
    - SUSPENSA
    - REATIVADA
    - EM_FECHAMENTO
    - MORTA_FINAL
  motivo_de_nao_morte:
  proxima_pressao:
```

### Estados permitidos

| Estado | Significado |
|---|---|
| VIVA | hipotese promissora, mesmo incompleta |
| SUSPENSA | faltam pecas, mas nao merece descarte |
| REATIVADA | novo material cruzou condicao de ativacao |
| EM_FECHAMENTO | pronta para pressao dura |
| MORTA_FINAL | falhou no fechamento |

---

## S9 — PRINCIPIOS TESSERUS NORTEADORES

```text
Universalidade
Eficiencia
Compactacao
Seguranca
Simplicidade
Tempo
Reversibilidade Temporal Segura
Ruptura/Transcendencia
Dimensional
Inteligencia
Consciencia Inerte
100% Vetorial nD
Opcodes/binary baixo nivel
Blindagem absoluta
Economia Energetica
Execucao vetorial
Intencao Ressonante
Pressao simbolica
Coerencia Maxima
Forma: simbolo, nD, vetorial
Aprendizado pelo Paradoxo
Evolucao
Prova Auditavel / Transparencia Total
Conservadorismo maximo: vies forte para NADA ENCONTRADO
```

Uso em discovery:
- orientar busca;
- expandir possibilidades;
- marcar lacunas;
- preservar hipotese alta.

Uso em fechamento:
- aplicar criterio duro;
- bloquear promocao indevida;
- declarar `NADA ENCONTRADO` quando nao sustentar;
- separar HIPOTESE, INFERENCIA_DOCUMENTADA, SIMULADO e PROVADO.

---

## S10 — CRITERIO DE MORTE FINAL

A hipotese so morre no fechamento quando persistir uma ou mais condicoes:

| Morte final | Definicao |
|---|---|
| MORTE_LEXICAL | so renomeia algo conhecido, sem ganho estrutural |
| MORTE_BASELINE | baseline equivalente explica tudo com custo igual ou menor |
| MORTE_BOUND | bound torna o ganho impossivel ou irrelevante |
| MORTE_DISCRIMINADOR | nao ha predicado que separe a hipotese de alternativas |
| MORTE_RETROPROJECAO | nao retroprojeta em dominios suficientes sem contradicao |
| MORTE_TESSERUS | viola seguranca, reversibilidade, vetorialidade ou auditabilidade |
| MORTE_EXTERNA | equivalente publico forte cobre o mecanismo |
| MORTE_OVERFORMAL | formalismo fica maior que o problema |

Regra:

```text
Durante discovery:
  registrar risco e lacuna.

Durante fechamento:
  matar, suspender, promover ou documentar.
```

---

## S11 — SAIDA PADRAO QUANDO O USUARIO PEDIR ANALISE E CRUZAMENTO

```text
MODO: TSD.CROSSRUPTURE.DISCOVERY-BASE

1. HIPOTESE VIVA
2. MECANISMO CENTRAL
3. PRINCIPIOS TESSERUS ATIVADOS
4. CRUZAMENTO INTERNO
5. BOPEX-LINT
6. POTENCIAL DE RUPTURA
7. LACUNAS SEM DESCARTE
8. PROXIMA ROTA
```

Rota padrao:

```text
analise-tess -> interna-tess
```

Rota com ambiguidade forte:

```text
analise-tess -> BOPEX lint -> ponte-tess -> interna-tess
```

Rota com maturidade suficiente:

```text
analise-tess -> interna-tess -> externa-tess -> alien-tess -> fechamento-tess
```

---

## S12 — LACUNAS E BLOQUEIOS

LACUNAS atuais:
- exemplos antigos de cruzamentos bons do GPTplus ainda nao foram formalizados como corpus de calibracao;
- symbol map, binder universal e LSU ainda nao aparecem aqui como autoridade soberana deste metodo;
- lista priorizada de componentes vivos para cruzamento rapido ainda precisa ser derivada do inventario;
- criterios formais de `problema forte` ainda precisam de tabela propria;
- nao ha benchmark real deste metodo;
- nao ha RM emitido para a familia `tsd.crossrupture.discovery.base`.

BLOQUEIOS para promocao canonica:
- falta RM.UNIFICATION ou RM.MASTER;
- falta validacao por casos reais;
- falta corpus minimo de entradas multimodais;
- falta comparison log entre descoberta antiga e metodo novo;
- falta hash/manifesto documental.

---

## S13 — HANDOFF PARA RM

```text
HANDOFF_TO_RM_UNIFICATION:
  case_root: tsd.crossrupture.discovery.base
  doc_id: trilho.tsd.crossrupture.discovery.base
  estado: PROTO_FORTE
  familia: discovery / crossrupture / metodo operacional
  objetivo: documentar base de descoberta viva e cruzamento TESSERUS
  ambiguidades:
    - se deve virar RM.MASTER proprio ou derivado de discovery.gate
    - se CROSSRUPTURE vira familia independente ou camada operacional
    - se MEP.REACTIVATION e dependencia ou componente pai
  recomendacao:
    - iniciar por RM.UNIFICATION
    - depois decidir entre RM.MASTER e componente derivado de discovery.gate
```

---

## S14 — REGRA FINAL DO TRILHO

```text
Discovery permissivo.
Governance duro.
Hipotese alta fica viva.
Lacuna vira trilha, nao descarte.
Morte so no fechamento.
Prova so com premissas, bound e evidencia.
TESSERUS nao perde semente rara por falta de forma inicial.
```
