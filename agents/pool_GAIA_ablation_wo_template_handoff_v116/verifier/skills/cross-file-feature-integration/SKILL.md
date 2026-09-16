---
name: cross-file-feature-integration
description: Checklist for implementing and reviewing a feature spanning models, schemas, services, repositories, routes, and security
trigger: When a requested feature adds multiple modules or a new API workflow
---
1. Extract explicit requirements into a matrix of entities, fields, state transitions, endpoint contracts, authorization, and dependencies.
2. Search the repository for existing modules, enums, services, route prefixes, and authentication helpers before creating new files.
3. Choose one canonical implementation tree and ensure package initializers and imports expose it; identify and remove or reconcile duplicate implementations.
4. Trace each request field from schema through service and persistence into response serialization; verify no values are dropped or changed incompatibly.
5. Trace every state transition through domain model, service, and route, including authorization checks and failure/rollback behavior.
6. Reuse existing repository/service patterns and dependency injection conventions rather than standalone substitutes.
7. Compile all files, then run focused tests for success, malformed input, unauthorized access, invalid transitions, and downstream failure.
8. Inspect all changed symbols and callers with grep, and report unresolved dependency or integration limitations explicitly.