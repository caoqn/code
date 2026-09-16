---
name: feature-artifact-contract-audit
description: Implement multi-layer repository features while preserving architecture and evaluator-visible artifacts.
trigger: When a task requests new domain models, application services, adapters, endpoints, tests, and documentation.
---
1. Inventory the authoritative source tree and determine whether duplicate source roots exist; identify which path the evaluator imports.
2. Build a requirement-to-symbol matrix listing every requested class, exact field name/type/default, port method signature, service entry point, adapter path, endpoint method/path, test, and documentation section.
3. Read existing neighboring modules and tests to preserve established constructors, aliases, storage formats, error behavior, and dependency injection patterns.
4. Delegate bounded implementation and independent verification, explicitly requiring all matrix rows and exact evaluator-visible paths.
5. Implement domain contracts first, then application orchestration through abstract ports, then adapters and delivery routes; avoid domain imports of infrastructure libraries unless explicitly required.
6. Add focused tests covering positive, empty, null, numeric, categorical, missing-resource, persistence round-trip, and endpoint behavior. If dependencies are unavailable, provide deterministic stubs and static checks.
7. Run exact targeted tests plus compilation/import smoke tests. Inspect signatures and serialized payloads with runtime introspection rather than relying on compile success.
8. Perform a final diff/file inventory: remove caches/generated artifacts, verify every required file exists in the authoritative root, and ensure duplicate trees are synchronized or intentionally excluded.
9. Report environment limitations separately from implementation results and do not claim endpoint coverage when the web dependency was unavailable.
