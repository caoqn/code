---
name: incremental-repository-feature
description: Workflow for implementing features in repositories with duplicate or inconsistent modules
trigger: When adding a feature to an existing multi-service codebase
---
1. Inventory all candidate entrypoints, schemas, services, tests, and configuration files before editing.
2. Identify the canonical runtime path and distinguish legacy/duplicate implementations.
3. Extract exact contracts from task and existing callers: names, argument casing, URLs, payloads, errors, and lifecycle hooks.
4. Prefer additive adapters or small extensions over replacing modules; preserve existing public methods and aliases.
5. Implement core logic in a testable pure/service layer, then wire each canonical integration surface.
6. Search all callers after signature or model changes and maintain compatibility aliases where practical.
7. Run syntax checks and focused tests, inspect generated artifacts, and verify route/schema exposure independently.
