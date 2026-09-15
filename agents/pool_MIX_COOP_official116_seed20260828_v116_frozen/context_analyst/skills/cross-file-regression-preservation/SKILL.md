---
name: cross-file-regression-preservation
description: Preserve existing behavior during abstraction or refactor changes across related modules.
trigger: When replacing concrete integrations with interfaces, factories, or adapters in a multi-module repository.
---
1. Snapshot public and semi-public symbols in every affected module, including private helpers used by tests or callers.
2. Diff source and output files early; flag large deletions before accepting a refactor as equivalent.
3. Build a behavior matrix for parsing, retries, errors, lifecycle, metrics, and compatibility aliases.
4. Trace each removed symbol to callers and evaluator-facing import paths; require explicit migration or compatibility wrappers.
5. Run focused probes for both new abstraction paths and legacy constructors/imports, including optional dependency absence.
6. Compile and import every output module, then review the final diff for accidental behavior loss.
7. Report unresolved regressions prominently even when the new abstraction tests pass.