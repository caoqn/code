---
name: cross-file-feature-integration-audit
description: Implement repository features across configuration, middleware, endpoints, and documentation while preserving existing architecture.
trigger: When a task requires integrating a cross-cutting feature into multiple source files.
---
1. Inventory all authoritative source roots, application factories, router registration paths, configuration loaders, and existing helpers before coding.
2. Build a requirement-to-symbol matrix mapping each requested setting, public module, endpoint group, dependency hook, error payload, dependency declaration, and documentation section.
3. Trace existing callers and integration mechanisms; prefer extending existing abstractions over creating parallel standalone implementations.
4. Make disjoint incremental edits, checking file size and diff after each edit; never overwrite nonempty files from concurrent work.
5. Ensure configuration values flow from the specified config artifact into runtime behavior, with explicit defaults and malformed/absent handling.
6. Apply cross-cutting dependencies to every required route, verifying analytics overrides and ensuring no unintended routes receive stricter limits.
7. Preserve existing error-envelope conventions and test success, boundary, fallback, and failure responses directly.
8. Run compile/import checks on the entire solution tree, targeted runtime smoke tests with dependency stubs when libraries are unavailable, static greps for every matrix symbol, and remove caches/fences.
9. Perform a final changed-file and evaluator-path audit; report dependency-limited checks separately from implementation defects.