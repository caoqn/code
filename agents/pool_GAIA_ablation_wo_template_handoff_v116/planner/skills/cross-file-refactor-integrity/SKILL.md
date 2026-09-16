---
name: cross-file-refactor-integrity
description: Safely perform cross-file domain model refactors while preserving existing behavior and exact public contracts.
trigger: When decomposing a shared model or changing interfaces across modules.
---
1. Inventory every authoritative source path, duplicate tree, public symbol, implementation, caller, test, and documentation reference before editing.
2. Build a requirement-to-symbol matrix listing exact field names, defaults, types, method signatures, return values, and export locations.
3. Choose one canonical definition for new domain objects; make compatibility modules re-export it rather than redefining parallel classes.
4. Apply incremental edits that preserve complete existing modules; never replace a nontrivial adapter with a small monkeypatch or wrapper.
5. Update ports and every adapter implementation together, then grep for all old signatures/usages and duplicate definitions.
6. Run compile/import smoke tests in both normal and dependency-limited environments where fallbacks exist; directly instantiate each public model and invoke changed methods.
7. Check dataclass inheritance and default ordering, optional dependency imports, and serialization/default behavior explicitly.
8. Perform final artifact-path existence/readback, changed-file inventory, cache cleanup, and documentation contract review before submission.