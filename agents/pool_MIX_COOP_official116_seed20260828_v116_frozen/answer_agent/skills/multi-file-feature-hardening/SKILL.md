---
name: multi-file-feature-hardening
description: Harden and verify a multi-file feature beyond minimal compilation and happy-path tests
trigger: When a change spans shared abstractions, implementations, exports, and optional dependencies
---
1. Enumerate every requirement as a file/symbol/API matrix, including compatibility aliases and package exports.
2. Inspect each changed file directly for complete source, clear control flow, and absence of placeholders or accidental wrappers.
3. Trace all callers and import paths, including both package-level and dotted-module imports, to detect shadowing or stale interfaces.
4. Exercise constructors and public methods with valid, empty, malformed, missing-dependency, insufficient-resource, and boundary inputs.
5. Test abstract/interface contracts explicitly (instantiation failures, required methods, return shapes, and aliases).
6. Run full-tree compilation plus the evaluator's exact tests; if dependencies are unavailable, use controlled stubs and record limitations.
7. Review maintainability and robustness: input validation, deterministic errors, exception boundaries, optional dependency behavior, and duplicated exports.
8. Reconcile artifacts under the evaluator-visible solution path and report any uncovered behavior as a qualification rather than claiming unconditional completeness.