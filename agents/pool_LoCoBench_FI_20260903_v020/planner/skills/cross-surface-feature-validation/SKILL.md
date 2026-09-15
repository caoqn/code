---
name: cross-surface-feature-validation
description: Checklist for implementing a feature that spans models, services, REST routes, and tests in a repository with parallel abstractions.
trigger: When a requested feature modifies persisted data and exposes a new API operation.
---
1. Inventory every named target file plus application entrypoints and tests that import them.
2. Identify duplicate implementations (for example domain service versus in-memory REST service) and document each public interface, DTO, repository method, and route prefix.
3. Apply additive changes to each surface that is externally observable: persistence model, serialization schema, repository contract, service method, and route.
4. Define missing-resource behavior consistently at both service and HTTP layers, including explicit exception types/status codes.
5. Add an end-to-end test that creates a resource, invokes the exact HTTP method/path, checks the response schema, then fetches again to verify persistence.
6. Independently inspect all changed files against each acceptance criterion and run static compilation; check artifact paths and remove generated files before submission.