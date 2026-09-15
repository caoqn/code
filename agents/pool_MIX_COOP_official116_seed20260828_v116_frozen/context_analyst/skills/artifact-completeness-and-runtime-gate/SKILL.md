---
name: artifact-completeness-and-runtime-gate
description: Systematically verify repository deliverables against requirements, including compatibility surfaces, generated outputs, and dependency-limited runtime checks.
trigger: When auditing or implementing a multi-file repository change with hidden or evaluator-facing interfaces
---
1. Enumerate every requirement and map it to a concrete output file, public symbol, caller, or integration hook.
2. Inventory both context and editable trees; distinguish source artifacts, tests, generated caches, and wrappers such as Markdown fences.
3. Search globally for every changed symbol and expected compatibility alias, then inspect complete definitions and call sites.
4. Capture exact signatures, annotations, exception classes/messages, lifecycle behavior, and serialization contracts before edits.
5. Run baseline focused tests or smoke checks before changing behavior; record missing dependencies separately from code failures.
6. After implementation, inspect the complete editable tree for omissions, stale artifacts, accidental wrappers, and generated caches.
7. Run compile checks on exact output files, then perform import/runtime smoke tests with available dependencies; use stubs only to isolate unavailable optional dependencies and clearly report uncertainty.
8. Reconcile the requirement matrix with final diffs and explicitly report unresolved runtime or integration coverage rather than inferring success from compilation alone.