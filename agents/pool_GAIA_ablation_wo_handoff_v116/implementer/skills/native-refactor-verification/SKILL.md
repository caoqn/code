---
name: native-refactor-verification
description: Workflow for multi-module refactors with shared abstractions and optional dependencies
trigger: When consolidating duplicated logic across handlers or introducing a shared module
---
1. Inventory the complete source tree and identify every definition and import of the abstraction being consolidated.
2. Copy or create output files, then immediately remove transport wrappers such as Markdown fences before any testing.
3. Implement the shared abstraction while preserving adapters for each existing public API; normalize differing record shapes at the shared boundary.
4. Grep all callers and concrete class definitions to ensure imports are redirected and duplicates are removed.
5. Make nonessential third-party dependencies optional at import time, while preserving explicit runtime failure only when functionality requiring them is invoked.
6. Track cumulative counters separately from flush buffers in streaming handlers.
7. Run compileall, import smoke tests for every public module, focused behavioral checks, and targeted tests; inspect failures for environment dependency gaps versus regressions.
8. Enumerate final files and remove generated cache artifacts before handoff, reporting exact verification commands and known test limitations.