---
name: feature-scope-preservation-gate
description: Safely implement small repository features without replacing existing architecture or tests.
trigger: When adding a field, service method, endpoint, and tests to an existing codebase.
---
1. Read every target source file and its nearest analogous model/service/route/test before delegating implementation.
2. Build a requirement-to-symbol matrix containing exact paths, route strings including router prefixes, method signatures, response models, error status, and test expectations.
3. Record the existing public API and file sizes; require additive edits unless the task explicitly requests replacement.
4. Trace imports and application composition to establish the canonical evaluator import path. Do not create parallel package trees unless existing imports prove they are required.
5. Delegate implementation with explicit prohibition on overwriting existing tests or unrelated modules, and require preserving all existing endpoints and fixtures.
6. After edits, compare git diff/stat and file sizes against the baseline. Reject newly invented architecture, duplicate routes, or truncated tests.
7. Run exact relevant tests and a direct endpoint smoke test when dependencies permit; if blocked, use stubs or static route introspection and report the limitation.
8. Verify every matrix item literally, including route prefixes, parameter types, defaults, 404 behavior, response serialization, and test fixture wiring.
9. Clean generated caches and perform a final import-path and changed-file audit before submission.