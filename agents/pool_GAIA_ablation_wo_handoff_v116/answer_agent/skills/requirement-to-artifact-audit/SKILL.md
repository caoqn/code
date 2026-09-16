---
name: requirement-to-artifact-audit
description: Convert a multi-layer feature request into a complete implementation and verification matrix
trigger: When adding a feature spanning models, services, persistence, APIs, permissions, packaging, or tests
---
1. Extract every explicit requirement and acceptance condition into a checklist, including negative cases and exact route/signature expectations.
2. Inspect the repository for existing domain patterns, duplicate implementations, exports, dependency conventions, and test fixtures before choosing insertion points.
3. Build a matrix mapping each requirement to source file, symbol, caller, public export, and focused test; identify gaps before coding.
4. Implement incrementally on top of established abstractions, preserving compatibility and updating all callers/imports rather than creating isolated parallel workflows.
5. Add or update focused tests for happy paths, invalid inputs, state transitions, authorization, persistence behavior, and boundary conditions.
6. Verify the complete solution tree: enumerate expected files, detect duplicates/placeholders, compile all sources, run focused tests and import smoke tests with dependency stubs when needed.
7. Reconcile failures against actual imported source and environment constraints, then report any unverified requirement explicitly instead of assuming completion.