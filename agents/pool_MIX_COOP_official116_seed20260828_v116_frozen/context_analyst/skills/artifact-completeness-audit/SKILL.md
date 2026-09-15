---
name: artifact-completeness-audit
description: Build and verify a requirement-to-artifact matrix for repository tasks, including public imports, compatibility aliases, and runtime dependencies.
trigger: When auditing or integrating a multi-file repository change with hidden evaluator contracts.
---
1. Enumerate all context and solution files and identify the actual editable/runtime import root.
2. Extract every requirement keyword, public symbol, endpoint, class, and function from specifications and tests; record expected module paths and signatures.
3. Map each expected symbol to a concrete implementation, export, or explicit compatibility alias. Mark unresolved imports and missing dependency modules as blockers rather than assumptions.
4. Search all call sites after implementation for stale names, duplicate providers, and unhandled exception paths; inspect both sync and async contracts.
5. Run a clean-process import smoke test with the solution root first on `sys.path`, then compile every output file. Remove generated artifacts and wrappers before handoff.
6. Report low-confidence rows explicitly, distinguishing static compile success from runtime dependency availability and behavioral verification.