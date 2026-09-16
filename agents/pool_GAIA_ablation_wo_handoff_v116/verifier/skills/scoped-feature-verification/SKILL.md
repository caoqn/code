---
name: scoped-feature-verification
description: Verify a narrowly requested cross-file feature without being distracted by unrelated repository modules
trigger: When a task adds one behavior to an existing multi-service codebase
---
1. Identify the authoritative task-specific requirement and evaluator tests before inventorying unrelated modules.
2. Trace the feature end-to-end across model/schema, repository, service, route, package exports, and tests; record each required symbol and caller.
3. Compare changed files against the pre-existing architecture and preserve established constructor signatures, dependency injection, and import namespaces.
4. Run the exact focused evaluator tests first, then compile all changed files and inspect runtime imports using the evaluator's PYTHONPATH.
5. If dependencies are unavailable, isolate dependency failures from implementation failures with minimal stubs or static checks, and clearly label unverified behavior.
6. Exercise positive, missing-resource, malformed-ID, repeated-operation, and state-persistence cases for the new operation.
7. Re-read the final tree and diff, remove generated artifacts, and report concrete evidence plus unresolved integration risks rather than inferring success from compilation.