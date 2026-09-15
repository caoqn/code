---
name: mirrored-refactor-contract-audit
description: Safely extend mirrored repositories while preserving existing implementations and handling optional dependencies.
trigger: When adding cross-layer models, ports, or adapter methods to an existing source tree.
---
1. Inventory all target files, public classes, methods, constructors, and exports before editing.
2. Build a contract matrix mapping each required symbol to its canonical module and every re-export path.
3. Read complete existing implementations before modifying; never replace a file with a patch fragment or monkeypatch that assumes symbols remain defined.
4. Implement canonical models in the authoritative layer, then make compatibility modules re-export them to avoid divergent schemas and field names.
5. Add optional-dependency fallbacks at every import boundary, including constructor signatures and behavior needed by tests (such as replay/history semantics).
6. After each edit, inspect file size and key symbols; grep all callers and adapters for signature compatibility.
7. Normalize transport wrappers, compile every Python file in every output tree, and run clean-process import smoke tests with optional dependencies both available and absent when feasible.
8. Remove caches and temporary artifacts, then review staged/unstaged diff and verify required paths exist before handoff.