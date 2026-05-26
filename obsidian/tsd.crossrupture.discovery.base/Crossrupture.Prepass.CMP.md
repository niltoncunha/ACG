---
aliases:
  - Crossrupture.Prepass.CMP
tags:
  - type/component
  - obsidian/componentes
  - layer/semantic
  - cluster/semantica
note_kind: component
sidecar_role: obsidian
source_of_truth: rm
ref_id: crossrupture.discovery.base.prepass:cmp
component_id: Crossrupture.Prepass.CMP
component_slug: crossrupture.discovery.base.prepass
component_name: Crossrupture Prepass
cluster: SEMANTICA
layer: semantic
role: derivado
documented_as: derivado
map_axis: SEMANTICA
map_parent: "[[TESSERUS.SEMANTICA]]"
center_policy: component_first
center_guard: documentation_is_support_not_center
status: EM TESTE
decision: NA
status_reason: Derivado definido pelo RM.MASTER e RM.COMPONENTES.
missing_for_release:
  - corpus_de_calibracao_gptplus
research_state: lacuna
relation_state: ok
rm_ref: "[[master.tsd.crossrupture.discovery.base]]"
component_ref: "[[componente.tsd.crossrupture.discovery.base.prepass]]"
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
MOTIVO: Derivado do core para preparar entrada bruta.

# O QUE E

Componente derivado que preserva a entrada bruta antes do cruzamento.

# FUNCAO ESTRUTURAL

Separar forma, sensacao, mecanismo e claim.

# RELACOES

- depende de [[Crossrupture.Core.CMP]]
- liga com [[Crossrupture.HypothesisCard.CMP]]

# MARCACAO DE CRUZAMENTO

OBSIDIAN: [crossrupture.discovery.base.prepass:cmp]
