---
name: evaluator-contract-matrix
description: Build and verify a complete requirement-to-symbol matrix for multi-file repository tasks
trigger: When implementing or reviewing a feature spanning services, APIs, exports, and compatibility layers
---
1. Extract every explicit requirement and evaluator expectation, including exact names, fields, routes, return types, limits, and error semantics.
2. Map each requirement to concrete source files, symbols, public import paths, callers, and tests; mark unknowns rather than assuming.
3. Inspect existing patterns and compatibility entry points before approving new implementations; ensure the new path extends canonical behavior rather than bypassing it.
4. Verify positive, negative, boundary, partial-failure, and dependency-absence cases with targeted tests or controlled stubs.
5. Run the exact evaluator/fail-to-pass harness when available, then compile every source file in the submission tree.
6. Reconcile test results against the actual imported source tree and report unverified contracts (such as optional framework execution) explicitly.
7. Before finalizing, check artifact completeness, exports, exact public field names, and absence of placeholders or generated artifacts.