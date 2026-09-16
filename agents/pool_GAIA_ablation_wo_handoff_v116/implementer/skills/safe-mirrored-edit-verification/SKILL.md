---
name: safe-mirrored-edit-verification
description: Safely apply and verify refactors when multiple agents or mirrored source trees may overwrite files
trigger: When delegated or concurrent edits touch shared output files
---
1. Inventory the exact target files and record their sizes and key symbols before editing.
2. Make one focused edit at a time; avoid broad replacement scripts that can race with other writers.
3. Immediately re-read each edited file and verify nonzero size, expected imports, classes, and method signatures.
4. Search the entire output tree for stale implementations, duplicate constructors, direct I/O calls, transport imports, and Markdown fences.
5. Run compilation across every Python file, then remove generated caches.
6. Re-run symbol and import smoke checks from the exact output tree, not the context tree.
7. Report only after a final file inventory confirms all required artifacts survived concurrent edits.