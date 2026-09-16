---
name: artifact-integrity-validation
description: Validate that submitted repository artifacts are complete, executable source files rather than wrappers or placeholders
trigger: Before finalizing any repository task with generated or mirrored solution files
---
1. Enumerate all files under the required output directory and compare against the task's expected artifact list.
2. Detect Markdown fences, prose headers, placeholder stubs, and truncated files in source-language files; inspect representative and changed files directly.
3. Run syntax compilation across the entire output tree, not only changed modules, and record every failure.
4. Check duplicate or mirrored source trees for consistency and verify the runtime import path resolves to the submitted tree.
5. Run focused tests for valid inputs, invalid/empty inputs, partial failures, and boundary conditions; distinguish missing dependencies from code defects.
6. Only report completion when artifact completeness and compilation status are reconciled with the evaluator's expected file set.