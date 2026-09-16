---
name: cross-cutting-change-quality-review
description: Review broad service-layer changes for completeness, robustness, security, and maintainability beyond basic tests.
trigger: When a change introduces shared middleware/decorators or modifies multiple service modules.
---
1. Build a requirement matrix listing every affected service operation, expected exception mapping, transaction behavior, and public export/import.
2. Inspect all decorated or wrapped callables for sync/async parity, metadata preservation, and consistent dependency fallback behavior.
3. Exercise happy paths plus invalid input, persistence failures, unexpected exceptions, rollback failures, and boundary/empty inputs.
4. Audit logs and error responses for sensitive data exposure, stable message contracts, and appropriate status codes.
5. Check complexity and duplication introduced by the shared abstraction; ensure callers retain clear control flow and type/signature compatibility.
6. Enumerate every required artifact in the submission tree, compile all source files, and run import smoke tests using dependency stubs when environment packages are unavailable.
7. Report unverified branches and environment limitations explicitly; do not equate compilation with full correctness.