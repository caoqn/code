---
name: cross-file-refactor-evaluator-gate
description: Contract-first workflow for cross-file refactors in inconsistent repositories, including source normalization, dependency wiring, and independent behavior verification.
trigger: When a task requires moving logic across layers or introducing a reusable abstraction across multiple files.
---
1. Build a requirement-to-symbol matrix listing exact paths, public classes/functions, signatures, imports, integration points, and prohibited remnants.
2. Inventory all provided files and caller paths before editing; identify duplicate source roots, malformed wrappers, absent modules, and incompatible parallel protocols.
3. Establish the evaluator-visible output root and copy only required complete source files there, preserving package initialization and removing generated caches.
4. Implement the abstraction against the named interface while adding a deliberate compatibility adapter only when existing concrete implementations have a different call signature.
5. Preserve the core use case's business behavior and apply cross-cutting policies at the composition root when separation of concerns is required.
6. Remove old implementation paths completely and grep for stale imports, concrete dependencies, duplicate registrations, and forbidden logic in consumers.
7. Run compile/import checks plus direct behavior matrices for cache miss/hit, backend failure, omitted/default arguments, and legacy concrete implementations.
8. Independently verify final file existence, exact symbols/signatures, package import paths, changed-file scope, and absence of pycache/fenced artifacts before submitting.