---
name: integration-preserving-feature-work
description: Safely add features to an existing multi-module service without discarding established interfaces.
trigger: When implementing a feature in a repository with existing schemas, services, routes, and tests.
---
1. Read the complete target files and identify existing public classes, query fields, constructors, imports, and exports.
2. Inspect all direct callers and tests before changing signatures or replacing implementations.
3. Prefer additive changes: preserve existing queries, mutations, service methods, dependency injection, and framework setup while adding the new feature.
4. Trace actual downstream endpoints and payload schemas from route files/configuration; encode per-service paths and configurable base URLs.
5. Ensure domain models and GraphQL DTOs expose the exact acceptance names (including camelCase aliases) while retaining compatibility aliases where useful.
6. Add tests that exercise both the new behavior and coexistence with existing functionality.
7. Independently compare every changed artifact against the original interfaces and run syntax/static checks before submission.