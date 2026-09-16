---
name: modular-refactor-contract-matrix
description: Systematic workflow for refactoring monolithic web applications into modular routers/services while preserving public behavior
trigger: When splitting a monolithic application across authentication, endpoint routers, and application assembly modules
---
1. Inventory every source module named by the task and enumerate all public symbols, routes, dependencies, configuration fields, and factories.
2. Build a requirement-to-symbol matrix mapping each requested new file to migrated functions, route paths/methods, imports, and compatibility exports.
3. Assign implementation against the matrix, requiring package initializers at every new directory level and forbidding duplicate inline definitions.
4. Preserve route prefixes, response payloads, status codes, exception messages, dependency signatures, and factory aliases exactly unless explicitly changed.
5. After implementation, grep the entire solution for each old symbol and route; confirm each moved symbol has one canonical definition and each route appears exactly once.
6. Run compile checks and import smoke tests for every module, including decorator-bearing modules; test with optional dependencies absent when feasible.
7. Verify application assembly statically (all required routers imported and included) and dynamically when framework dependencies are available.
8. Inspect the final file inventory for missing modules, generated artifacts, markdown fences, and unrelated files before submission.