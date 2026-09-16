---
name: api-change-regression-audit
description: Validate API payload refactors while detecting unrelated regressions and compatibility breaks
trigger: When changing public API payloads, configuration objects, serializers, or parser output
---
1. Run the task-specific/fail-to-pass tests first, then run the complete relevant test suite rather than only directly edited modules.
2. Inventory every changed public field and method, grep all callers and consumers, and inspect downstream assumptions about legacy and modern representations.
3. Construct a compatibility matrix for legacy payload, modern payload, explicit overrides, empty values, and malformed values; execute each case.
4. Treat unrelated test failures as real regressions until reproduced against the baseline or explained by an intentional contract change.
5. Compare baseline and modified results by test name, not only aggregate counts; investigate every pass-to-fail transition.
6. Report intentional incompatibilities separately from accidental regressions, with exact assertion/error evidence.
