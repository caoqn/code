---
name: strategy-refactor-contract-audit
description: Safely consolidate heterogeneous strategy implementations onto a shared base while preserving constructors, registries, and behavior.
trigger: When introducing or refactoring a shared strategy abstraction across multiple protocol modules.
---
1. Inventory every strategy class, constructor signature, registry, export, and optional dependency before editing.
2. Extract an explicit contract matrix for required base constructor parameters, abstract methods, helper semantics, aliases, and concrete wrappers.
3. Implement the new base in isolation with robust validation for dependency absence, malformed inputs, and multiple adapter APIs; preserve compatibility aliases.
4. Update each concrete strategy atomically, retaining existing domain methods and adding thin wrappers only where required by the shared contract.
5. Verify registry behavior independently; do not merge registries or auto-register classes unless explicitly required.
6. Normalize generated or fenced source before tests and run full-tree compilation.
7. Run import smoke tests with optional dependencies absent, introspect signatures/abstractness/exports, and exercise edge cases for validation and wrapper delegation.
8. Re-read all changed files, grep required symbols, inspect git diff/status, remove caches, and report exact commands plus limitations.