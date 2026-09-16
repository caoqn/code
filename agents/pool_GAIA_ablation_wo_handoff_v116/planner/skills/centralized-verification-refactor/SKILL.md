---
name: centralized-verification-refactor
description: Refactor duplicated cryptographic or validation logic into one service while preserving caller behavior and public APIs.
trigger: When multiple modules contain overlapping verification logic and a canonical service must be introduced.
---
1. Inventory every target file and grep all verification-related symbols, including private helpers, inline checks, exception handling, and tests.
2. Build a requirement-to-symbol matrix: canonical method name/signature/return semantics, supported input forms, error behavior, and each caller's expected control flow.
3. Reproduce baseline behavior for valid, invalid, malformed, and unsupported inputs before editing; record whether invalid input returns False or raises.
4. Implement one canonical public method in the designated service. Keep backend-specific operations in private service helpers, and avoid duplicating cryptographic primitives at call sites.
5. Refactor each caller with minimal changes: import the canonical service, preserve dependency injection and existing constructor/positional compatibility, and preserve error/logging/rejection semantics.
6. Remove only redundant local verification code; retain private compatibility helpers when they are part of the existing callable surface unless removal is explicitly required and tested.
7. Validate exact signatures and annotations via introspection, grep for residual inline verification, and ensure each intended caller invokes the canonical method.
8. Compile every changed file, run focused behavior tests with dependency stubs where optional packages are unavailable, and test malformed signatures, wrong addresses/keys, falsey values, and unsupported schemes.
9. Audit final scope and artifacts: verify evaluator-visible paths, no markdown fences or caches, no unrelated copied files, and direct readback of all solution files.