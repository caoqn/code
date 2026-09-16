---
name: repository-refactor-completion-gate
description: Safely introduce repository layers while preserving service behavior and validating cross-file contracts
trigger: When decoupling application services from infrastructure connectors or adding repository abstractions
---
1. Inventory every connector call in services, all concrete connector methods, and every service/factory caller.
2. Build a requirement matrix mapping each direct operation to a repository method, including argument order, sync/async behavior, return values, and error semantics.
3. Implement repositories as thin, explicit adapters; avoid speculative in-memory behavior unless required, and provide clear handling when connector capabilities are absent.
4. Refactor services to depend only on repository protocols/classes; grep the entire application layer to ensure no low-level connector references remain.
5. Update factory wiring and preserve existing public factory exports and service aliases; verify constructor signatures by introspection.
6. Run focused mocked tests for every repository operation, including malformed IDs, missing connector methods, transaction errors, and read-after-write behavior.
7. Compile/import the exact evaluator source tree with optional dependencies absent where possible; use TYPE_CHECKING or lazy imports for infrastructure-only dependencies.
8. Audit final diff scope, remove generated caches/fences, verify required artifact paths directly, and run a full nearest test suite before submission.