---
name: final-artifact-reconciliation
description: Reconcile delegated repository changes against native output requirements before issuing a completion summary
trigger: When a task requires final confirmation of generated solution files and tests
---
1. Enumerate the required output files from the task contract and list all files present under the solution tree.
2. Inspect each changed file directly for complete source, public symbols, imports, exports, and compatibility aliases; check callers and wrappers.
3. Run compilation across the entire output tree and targeted behavior checks for success, failure, empty, and boundary inputs.
4. Verify generated artifacts such as caches, placeholders, or Markdown fences are absent.
5. Attempt runtime/import smoke tests; if dependencies are missing, use static checks or controlled stubs and explicitly mark runtime behavior unverified.
6. Reconcile teammate reports with independent evidence, resolve conflicts, and emit only the native contract's required prefix and concise summary.