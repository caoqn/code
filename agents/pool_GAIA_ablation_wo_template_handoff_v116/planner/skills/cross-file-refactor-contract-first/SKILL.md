---
name: cross-file-refactor-contract-first
description: Contract-first workflow for repository/service dependency refactors in inconsistent source trees.
trigger: When a task requests moving instantiation or dependency wiring across multiple files.
---
1. Extract every literal requirement into a matrix: exact file path, class/function name, constructor signature, configuration key, integration point, and expected test seam.
2. Inventory the repository and determine the canonical evaluator-visible source root; identify duplicate trees, malformed wrappers, and actual concrete class names before editing.
3. Trace all callers and factories of each changed service. Decide explicitly whether to preserve legacy positional/keyword forms or intentionally break them, and test that decision.
4. Implement the provider at the exact requested path. Keep construction lazy and memoized, validate unknown keys, and normalize configuration into explicit registrations rather than returning raw config dictionaries.
5. Refactor consumers to depend on the provider abstraction and remove direct concrete imports. Wire the provider at the true composition root, not merely in an unrelated orchestrator constructor.
6. Add or update configuration schema and sample config with exact requested keys and valid parseable syntax; test config-present and default/absent cases.
7. Run targeted runtime checks that instantiate services with a mock provider and assert each provider getter is called and repository identity is reused. Also test legacy paths if preserved.
8. Perform final static grep for stale direct imports/instantiations, exact symbol/path checks, whole-tree compilation, config parse/readback, and changed-file/diff cleanup. Treat unresolved imports or malformed artifacts as blockers, not caveats.