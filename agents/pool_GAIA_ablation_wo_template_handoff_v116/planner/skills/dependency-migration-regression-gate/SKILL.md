---
name: dependency-migration-regression-gate
description: Safely migrate APIs and schema generation while preserving downstream behavior
trigger: When updating dependency-facing payloads, parsers, or typed schemas
---
1. Reproduce the reported failure before edits and record exact output.
2. Inventory every caller and downstream consumer of changed fields, including response parsing and helper-generated static objects.
3. Implement the smallest compatibility layer that supports the new API while preserving legacy semantics where callers still depend on them.
4. Build a behavior matrix for parser styles, annotations, defaults, enums, custom overrides, and malformed documentation.
5. Run focused tests plus the complete nearest downstream test modules, not just unit tests for changed files.
6. Investigate every regression even if unrelated-looking; parser output changes can alter search, routing, or model behavior indirectly.
7. Verify final diff scope, imports, generated artifacts, and runtime smoke tests under representative dependency versions.