---
name: cross-file-final-integrity
description: Final verification workflow for multi-file refactors
trigger: When relocating modules, changing shared abstractions, or coordinating edits across handlers and tests
---
1. Inventory all source and test files before editing; record files that must be added, removed, or renamed.
2. Delegate implementation with explicit constraints to preserve complete file contents and avoid duplicate abstractions.
3. After edits, inspect every changed file for nonempty content, expected symbols, and absence of stale imports using file listing and targeted grep.
4. Run syntax compilation and import smoke tests under the intended package path, including optional-dependency environments when practical.
5. Execute focused tests, then integration tests; distinguish genuine implementation failures from test-environment fallback or missing-dependency failures.
6. Check cross-file behavior such as cumulative counters across batching, error paths, and optional service clients—not only happy-path validators.
7. Before final submission, send the answer formatter the exact artifact inventory and concrete verification evidence, including unresolved caveats.