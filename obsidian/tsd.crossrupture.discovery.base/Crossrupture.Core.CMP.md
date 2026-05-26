---
aliases:
  - "Crossrupture.Core.CMP"
  - "crossrupture.core"
  - "CROSSRUPTURE"
tags:
  - type/component
  - obsidian/componentes
  - layer/semantic
  - cluster/semantica
cssclasses:
  - tess-component
  - cluster-semantica
note_kind: component
sidecar_role: obsidian
source_of_truth: rm
ref_id: "crossrupture.discovery.base.core:cmp"
component_id: "Crossrupture.Core.CMP"
component_slug: "crossrupture.discovery.base.core"
component_name: "Crossrupture Core"
cluster: SEMANTICA
layer: semantic
role: principal
documented_as: principal
map_axis: SEMANTICA
map_parent: "[[TESSERUS.SEMANTICA]]"
center_policy: component_first
center_guard: documentation_is_support_not_center
status: EM TESTE
decision: NA
status_reason: "Metodo documentado; falta corpus de calibracao e autoridade simbolica completa."
missing_for_release:
  - symbol_map_binder_lsu
  - corpus_de_calibracao_gptplus
  - tabela_de_problema_forte
research_state: lacuna
relation_state: ok
orbita: none
transversal_refs: []
rm_ref: "[[master.tsd.crossrupture.discovery.base]]"
component_ref: "[[componente.tsd.crossrupture.discovery.base.core]]"
docfield_ref: "[[docfield.tsd.crossrupture.discovery.base]]"
master_ref: ""
inventario_ref:
  - "crossrupture.discovery.base:inv"
docs:
  - "tsd.crossrupture.discovery.base:rm"
  - "tsd.crossrupture.discovery.base:docfield"
chat_refs:
  - "tsd.crossrupture.discovery.base:chat"
depends_on: []
derived_from: ""
linked_to:
  - "[[Crossrupture.Prepass.CMP]]"
  - "[[Crossrupture.BopexLint.CMP]]"
  - "[[Crossrupture.MepRetention.CMP]]"
  - "[[Crossrupture.FinalKill.CMP]]"
  - "[[Crossrupture.HypothesisCard.CMP]]"
connects_to: []
blocked_by_components: []
blocking_components: []
glyph: "na"
symbol_id: "UNMAPPED"
nd_pressure: "nD"
docfile_alias_forbidden: true
traditional_programming_primary: false
production_as_state_forbidden: true
---

# STATUS

```text
STATUS: EM TESTE
DECISAO: NA
MOTIVO: Metodo documentado; falta corpus de calibracao e autoridade simbolica completa.
FALTA PARA LIBERAR:
- symbol_map_binder_lsu
- corpus_de_calibracao_gptplus
- tabela_de_problema_forte
```

# O QUE E

Componente principal da familia CROSSRUPTURE. Governa a descoberta viva e o cruzamento com TESSERUS sem substituir as skills especialistas.

## Para que serve

Mantem hipoteses altas vivas durante discovery, organiza lacunas sem descarte e direciona a rota ate fechamento.

## O que resolve

Reduz morte precoce de sementes fortes por falta inicial de baseline, bound, discriminador ou retroprojecao.

## O que nao e

- Nao e documento soberano.
- Nao e RM.
- Nao e DocFIELD.
- Nao e CORPUS.
- Nao e execucao real.

# FUNCAO ESTRUTURAL

Orquestrar a rota de descoberta viva sem promover hipotese como prova.

# RELACOES

Depende de RM como autoridade documental e liga os derivados prepass, bopex-lint, mep-retention, final-kill e hypothesis-card.

# MECANISMO RESUMIDO

ENTRADA:
- imagem, video, metafora, ASCII, texto, equacao, resposta de IA ou seed bruta.

TRANSFORMACAO:
- preservar bruto, extrair mecanismo, registrar hipotese viva, aplicar lint/retencao quando necessario e declarar proxima rota.

SAIDA:
- hipotese viva, lacunas nomeadas, handoff e estado de descoberta.

INVARIANTE:
- hipotese alta nao morre por lacuna inicial.

# LACUNAS

- symbol_map_binder_lsu
- corpus_de_calibracao_gptplus
- tabela_de_problema_forte
- corpus_multimodal_minimo

# BLOQUEIOS

- promocao canonica sem corpus
- camada simbolica forte sem symbol map/binder/LSU

# MARCACAO DE CRUZAMENTO

```text
OBSIDIAN: [crossrupture.discovery.base.core:cmp]
```
