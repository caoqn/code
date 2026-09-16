---
name: artifact-completion-checklist
description: End-to-end checklist for validating repository changes before handoff
trigger: When implementing or reviewing multi-file code changes
---
1. Enumerate every file under the required output directory and identify duplicate or mirrored source trees.
2. Parse and compile all production and test Python files, then run the project's actual test command; compilation alone is insufficient.
3. Grep changed symbols and signatures across the entire tree to find stale callers, duplicate routes, and mismatched schemas.
4. Import public modules using the same PYTHONPATH/package layout that evaluation will use. Record dependency failures separately, and use focused dependency-free tests where possible.
5. Exercise representative success, failure, malformed-input, boundary, and partial-failure cases for changed behavior.
6. Inspect diffs or file synchronization across mirrored trees and confirm required artifacts are non-empty and complete.
7. Report concrete evidence, unresolved failures, and environmental limitations without labeling an unexecuted runtime path as verified.