# ACG Structure Scout

ACG Structure Scout is a structural intake layer that runs before semantic reading.

It inventories files, detects probable runtimes and control files, maps lightweight references, and builds an attention queue before deeper AI analysis.

## Goals

- avoid reading entire repositories too early
- reduce context waste
- detect entrypoints and broken references
- identify sovereign/control files
- separate terminal assets from operational files
- feed the Guardrail with a scout_report

## Output

The component emits a `scout_report.json` structure containing:

- system_profile
- language_map
- control_files
- reference_graph
- attention_queue
- readiness_score
- guardrail_mode

## Current Status

Prototype / structural MVP.
