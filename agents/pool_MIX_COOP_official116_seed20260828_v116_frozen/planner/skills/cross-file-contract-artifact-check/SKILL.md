---
name: cross-file-contract-artifact-check
description: Safely implement small cross-file refactors with exact symbols, imports, and evaluator-visible artifacts.
trigger: When a task adds a shared utility and migrates multiple service methods.
---
1. Inventory every requested method and its current behavior, including method names that may differ from prose; grep all callers and related exception definitions.
2. Build a requirement matrix listing exact file paths, function signatures, query semantics, exception source, message text, imports, and expected exports.
3. Implement the shared utility first, importing the canonical exception module; avoid introducing alternate exception classes or unrelated helper APIs.
4. Refactor each target method explicitly, preserving async/sync behavior and return contracts while replacing only duplicated lookup logic.
5. Reconcile package `__init__` exports and dependency fallbacks so importing the utility through both module and package paths works.
6. Perform static checks: grep each required symbol/import, parse or compile every changed file, inspect for markdown fences/caches, and verify exact file inventory under the required output directory.
7. Run a fake-session behavior matrix for found and missing records, asserting object identity and exact exception message; record dependency-limited runtime tests separately rather than treating them as passes.
