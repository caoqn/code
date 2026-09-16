---
name: maintainable-cross-service-refactor
description: Checklist for implementing shared service behavior across multiple applications while preserving clarity and compatibility
trigger: When introducing a shared utility, exception model, middleware, or cross-service API behavior
---
1. Translate the request into a matrix of affected services, modules, public symbols, registrations, and tests.
2. Define one canonical implementation and explicit compatibility aliases only where existing callers require them.
3. Search all repository references to affected symbols; classify each consumer as in-scope, out-of-scope, or requiring migration.
4. Update application/bootstrap registration points consistently across all in-scope services.
5. Preserve exact public contracts: names, signatures, return shapes, status codes, and user-visible messages.
6. Exercise success, not-found, invalid-operation, and boundary paths with focused tests or controlled stubs when dependencies are unavailable.
7. Compile the complete submitted source tree and inspect files for wrappers, placeholders, accidental duplication, or formatting artifacts.
8. Review maintainability: avoid unnecessary branching, keep handlers small, document compatibility behavior, and ensure error details do not leak sensitive internals.
9. Report any out-of-scope consumer failures separately from acceptance evidence, distinguishing environment limitations from implementation defects.