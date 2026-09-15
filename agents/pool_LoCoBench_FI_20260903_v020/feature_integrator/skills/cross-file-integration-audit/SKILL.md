---
name: cross-file-integration-audit
description: Audit multi-entry-point repositories and produce a robust implementation contract
trigger: When a feature may affect routing, schemas, configuration, validation, or multiple application factories
---
1. Enumerate all source files, application factories, routers, schemas, and test imports.
2. Trace the canonical runtime path from test/client import through factory, router mounting, and handler/schema execution.
3. Mark duplicate or legacy entry points explicitly; determine whether hidden tests or compatibility require wiring them too.
4. For each requirement, identify concrete symbols, configuration sources, registration hooks, serialization behavior, and failure modes.
5. Inspect analogous tests and enumerate edge cases: literals versus variables, nesting, aliases/fragments, invalid input, and error transport status.
6. Send one consolidated implementation map to the implementer with prioritized must-have changes and a verification checklist.
7. Before closing, confirm every requirement maps to at least one file/symbol and every changed integration has a corresponding test or static verification step.