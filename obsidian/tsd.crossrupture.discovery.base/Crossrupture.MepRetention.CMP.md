---
aliases:
  - Crossrupture.MepRetention.CMP
tags:
  - type/component
  - obsidian/componentes
  - layer/skin
  - cluster/skin
note_kind: component
sidecar_role: obsidian
source_of_truth: rm
ref_id: crossrupture.discovery.base.mep-retention:cmp
component_id: Crossrupture.MepRetention.CMP
component_slug: crossrupture.discovery.base.mep-retention
component_name: Crossrupture MEP Retention
cluster: SKIN
layer: skin
role: derivado
documented_as: derivado
map_axis: SKIN
map_parent: "[[TESSERUS.SKIN]]"
center_policy: component_first
center_guard: documentation_is_support_not_center
status: EM TESTE
decision: NA
status_reason: Derivado definido para retencao e reativacao.
missing_for_release:
  - corpus_de_calibracao_gptplus
research_state: lacuna
relation_state: ok
rm_ref: "[[master.tsd.crossrupture.discovery.base]]"
component_ref: "[[componente.tsd.crossrupture.discovery.base.mep-retention]]"
docfield_ref: "[[docfield.tsd.crossrupture.discovery.base]]"
depends_on:
  - "[[Crossrupture.Core.CMP]]"
derived_from: "[[Crossrupture.Core.CMP]]"
linked_to:
  - "[[Crossrupture.HypothesisCard.CMP]]"
connects_to: []
blocked_by_components: []
blocking_components: []
glyph: na
symbol_id: UNMAPPED
nd_pressure: nD
docfile_alias_forbidden: true
traditional_programming_primary: false
production_as_state_forbidden: true
---

# STATUS

STATUS: EM TESTE
DECISAO: NA
MOTIVO: Retencao de hipotese viva.

# O QUE E

Componente derivado que registra hipotese viva, suspensa ou reativada.

# FUNCAO ESTRUTURAL

Evitar perda de seeds promissoras durante discovery.

# RELACOES

- depende de [[Crossrupture.Core.CMP]]
- liga com [[Crossrupture.HypothesisCard.CMP]]

# MARCACAO DE CRUZAMENTO

OBSIDIAN: [crossrupture.discovery.base.mep-retention:cmp]
