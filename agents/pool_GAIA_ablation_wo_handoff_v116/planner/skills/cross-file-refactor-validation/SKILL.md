---
name: cross-file-refactor-validation
description: Reliable workflow for centralizing duplicated logic across a source tree
trigger: When introducing a shared helper and replacing repeated inline logic across multiple modules
---
1. Read every explicitly named source file and grep for all relevant patterns, including alternate spellings and semantic fields.
2. Establish whether validation logic actually exists; do not invent behavior changes unless the requirement clearly mandates validation at specific boundaries.
3. Create exactly one canonical package/module for the helper and ensure package initializers exist at every required level.
4. Update imports using the package path that matches the runtime source layout; remove accidental duplicate helper modules.
5. Preserve each caller's prior error type, status code, and message semantics where possible; route decisions through the helper result.
6. Search all modified files afterward to confirm no inline checks remain and every intended caller imports the canonical helper.
7. Run syntax compilation plus runtime import smoke tests for modules with decorators/dataclasses; compilation alone does not catch class-definition errors.
8. Verify edge cases directly (wrong prefix, wrong length, non-hex, non-string, valid mixed-case input) and inspect the final solution tree for stray generated files or markdown fences.