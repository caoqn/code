---
name: federated-feature-artifact-checklist
description: Checklist for implementing federated aggregation features across service, schema, and tests
trigger: When adding a cross-service GraphQL or API aggregation feature
---
1. Inventory authoritative source files, framework conventions, downstream endpoint routes, DTO field names, and existing test import paths before editing.
2. Translate requirements into a file/symbol checklist: service method, module-level resolver compatibility, concrete schema types, union name, exact GraphQL field/argument/field casing, endpoint mapping, and unit/integration tests.
3. Implement incrementally on existing architecture rather than replacing modules; preserve existing public methods and constructors unless the task explicitly changes them.
4. Normalize each downstream payload into a stable internal model while retaining required fields (id, action type, timestamp, source, and useful payload), handling malformed timestamps deterministically.
5. Use concurrent requests with per-source exception isolation and explicit endpoint mapping; test success, timeout/HTTP failure, empty responses, malformed records, and limits.
6. Ensure GraphQL union resolution returns concrete object types, exposes required fields with correct camelCase mapping, and uses the exact requested union and query names.
7. Add both unit tests for aggregation/error handling and integration tests for GraphQL response shape/sorting with mocked outbound calls.
8. Compile every submitted file, remove generated artifacts, grep all checklist symbols, and verify package import paths match both requested source paths and existing tests.