---
aliases:
  - Crossrupture.BopexLint.CMP
tags:
  - type/component
  - obsidian/componentes
  - layer/contracts
  - cluster/contrato
note_kind: component
sidecar_role: obsidian
source_of_truth: rm
ref_id: crossrupture.discovery.base.bopex-lint:cmp
component_id: Crossrupture.BopexLint.CMP
component_slug: crossrupture.discovery.base.bopex-lint
component_name: Crossrupture Bopex Lint
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
status_reason: Derivado definido para saneamento estrutural.
missing_for_release:
  - symbol_map_binder_lsu
research_state: lacuna
relation_state: ok
rm_ref: "[[master.tsd.crossrupture.discovery.base]]"
component_ref: "[[componente.tsd.crossrupture.discovery.base.bopex-lint]]"
docfield_ref: "[[docfield.tsd.crossrupture.discovery.base]]"
depends_on:
  - "[[Crossrupture.Core.CMP]]"
derived_from: "[[Crossrupture.Core.CMP]]"
linked_to: []
connects_to:
  - "[[Crossrupture.FinalKill.CMP]]"
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
MOTIVO: Lint estrutural auxiliar.

# O QUE E

Componente derivado que aplica BOPEX como saneamento de classe, nome e representacao.

# FUNCAO ESTRUTURAL

Evitar erro ontologico sem decidir valor de ruptura.

# RELACOES

- depende de [[Crossrupture.Core.CMP]]
- conecta com [[Crossrupture.FinalKill.CMP]]

# MARCACAO DE CRUZAMENTO

OBSIDIAN: [crossrupture.discovery.base.bopex-lint:cmp]
