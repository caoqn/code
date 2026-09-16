---
name: evaluator-contract-completeness
description: Systematically reconcile repository context, evaluator-facing imports, and required artifacts before implementation.
trigger: When implementing a feature in a repository with mirrored trees, incomplete dependencies, or hidden evaluator contracts.
---
1. Inventory every authoritative context file and enumerate all required output paths, including package initializers, application factories, compatibility modules, and tests.
2. Read complete neighboring implementations and tests; preserve existing test suites unless the task explicitly requests replacement.
3. Build a matrix mapping each public import path, symbol, constructor signature, route literal, payload field, response field, and error status to a canonical implementation.
4. Identify mirrored/source trees and determine the evaluator's likely import root by reproducing imports with explicit PYTHONPATH values.
5. Implement the canonical module first, then add thin compatibility re-exports rather than duplicate divergent implementations.
6. For optional dependencies, provide deterministic import-safe boundaries only when required, and statically inspect route decorators and registrations when runtime imports are unavailable.
7. Before handoff, grep every matrix item, compile every Python file in every output tree, run available targeted tests (including negative cases), remove caches, and report any dependency-blocked checks precisely.