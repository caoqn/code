---
name: rest-endpoint-cross-file-contract
description: Implement and verify a REST endpoint across handler, service, models, documentation, and tests while preserving exact contracts.
trigger: When adding a REST API endpoint requiring multiple source artifacts and concurrent data access.
---
1. Inventory authoritative source roots and existing handlers, service classes, repository protocols, error hierarchy, response builder, model exports, and route registration. Confirm evaluator import paths.
2. Build a literal requirement matrix: HTTP method/path, parameter spelling and requiredness, response keys/nesting/types, exception-to-status mapping, concurrency requirement, exact file paths, and test filename.
3. Trace existing callers and repository method signatures. Design adapters for sync/async repositories only when needed; do not silently substitute alternate method names without tests.
4. Implement business logic in the designated service layer. Validate required timestamps and ordering before I/O; fetch independent datasets with asyncio.gather; normalize records into the exact documented nested schema.
5. Keep handler thin: parse path/query values, invoke service, map domain exceptions through the project ResponseBuilder/error framework, and expose expected handler aliases.
6. Add/extend Pydantic models with safe mutable defaults (default_factory), exact field names/types, datetime/date validation, and package exports where required.
7. Update OpenAPI at the exact requested path with required parameters, response schema, and error responses. Ensure YAML remains structurally valid and avoid duplicate components.
8. Write comprehensive tests for success, missing patient, empty window, malformed timestamps, reversed window, and concurrency/mocked repository behavior.
9. Run exact compile/import checks from the evaluator path, targeted tests, and static greps for every required symbol/path. Read back final files, remove caches, and reconcile verifier findings before submission; unresolved schema or requiredness caveats are blockers, not merely notes.