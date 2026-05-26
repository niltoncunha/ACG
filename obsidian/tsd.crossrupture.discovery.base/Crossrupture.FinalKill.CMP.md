---
aliases:
  - Crossrupture.FinalKill.CMP
tags:
  - type/component
  - obsidian/componentes
  - layer/contracts
  - cluster/contrato
note_kind: component
sidecar_role: obsidian
source_of_truth: rm
ref_id: crossrupture.discovery.base.final-kill:cmp
component_id: Crossrupture.FinalKill.CMP
component_slug: crossrupture.discovery.base.final-kill
component_name: Crossrupture Final Kill
cluster: CONTRATO
layer: contracts
role: derivado
documented_as: derivado
map_axis: CONTRATO
map_parent: "[[TESSERUS.CONTRATO]]"
center_policy: component_first
center_guard: documentation_is_support_not_center
status: EM TESTE
decision: NA
status_reason: Derivado definido para criterio final de descarte.
missing_for_release:
  - tabela_de_problema_forte
research_state: lacuna
relation_state: ok
rm_ref: "[[master.tsd.crossrupture.discovery.base]]"
component_ref: "[[componente.tsd.crossrupture.discovery.base.final-kill]]"
docfield_ref: "[[docfield.tsd.crossrupture.discovery.base]]"
depends_on:
  - "[[Crossrupture.Core.CMP]]"
derived_from: "[[Crossrupture.Core.CMP]]"
linked_to:
  - "[[Crossrupture.BopexLint.CMP]]"
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
MOTIVO: Criterio final de descarte.

# O QUE E

Componente derivado que concentra a morte final da hipotese apenas no fechamento.

# FUNCAO ESTRUTURAL

Impedir que lacuna inicial mate descoberta antes do ponto correto.

# RELACOES

- depende de [[Crossrupture.Core.CMP]]
- liga com [[Crossrupture.BopexLint.CMP]]

# MARCACAO DE CRUZAMENTO

OBSIDIAN: [crossrupture.discovery.base.final-kill:cmp]
