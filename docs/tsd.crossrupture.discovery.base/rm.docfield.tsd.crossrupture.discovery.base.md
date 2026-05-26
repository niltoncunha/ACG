# RM.DocFIELD — TSD.CROSSRUPTURE.DISCOVERY.BASE

## AI_MARKERS

```text
::TESSERUS-DOC-VERSION:: v1.2
::DOSSIER-KIND:: RM.DocFIELD
::CHAIN-STAGE:: RM.DocFIELD
::PREVIOUS-STAGE:: RM.COMPONENTES
::NEXT-STAGE:: OBSIDIAN.COMPONENTES
::DOCFIELD-CANON:: RM.DocFIELD
```

## CAPA

```yaml
doc_id: rm.docfield.tsd.crossrupture.discovery.base
case_id: tsd.crossrupture.discovery.base
family_id: crossrupture.discovery.base
status: EM_TESTE
previous_stage_ref: rm.componentes.tsd.crossrupture.discovery.base
next_stage_target: OBSIDIAN.COMPONENTES
```

## ESTADO

```yaml
docfield_state:
  source_component: presente
  source_master: presente
  source_unification: presente
  mechanical_shape_defined: true
  obsidian_ready: true
  corpus_ready: false
  handoff_status: PRONTO_PARA_OBSIDIAN
```

## FORMA MECANICA MINIMA

```yaml
logical_file_name: docfield.tsd.crossrupture.discovery.base
internal_table_name: tbl_crossrupture_discovery_base_core
fields:
  - doc_id
  - case_id
  - family_id
  - primary_component
  - derived_components
  - invariants
  - lacunas
  - obsidian_target
binds:
  - file_to_table
  - table_to_value
  - field_to_registry
```

## HANDOFF

```yaml
handoff:
  status: PRONTO_PARA_OBSIDIAN
  target: OBSIDIAN.COMPONENTES
  blockers: []
  lacunas:
    - symbol_map_binder_lsu
    - corpus_de_calibracao_gptplus
    - tabela_de_problema_forte
    - corpus_multimodal_minimo
```

## VALIDACAO LOCAL

```yaml
local_validation:
  one_rm_stage_per_file: OK
  ai_markers_present: OK
  handoff_present: OK
  logical_file_name_present: OK
  internal_table_name_present: OK
  field_registry_present: OK
  no_runtime_promotion: OK
  github_path_ready: OK
```
