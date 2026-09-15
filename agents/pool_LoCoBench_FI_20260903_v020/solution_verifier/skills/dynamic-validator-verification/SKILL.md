---
name: dynamic-validator-verification
description: Verify database-backed dynamic threshold validators and their pipeline registration across API, persistence, and edge cases.
trigger: When reviewing or implementing validators that query historical values and are loaded dynamically by a registry.
---
1. Extract the validator constructor contract and compare every call site, factory, and registry adapter; ensure required keys, window size, multiplier, and connection are supplied consistently.
2. Inspect the historical-value helper for injectable connection support, query parameterization, malformed-row handling, bounded result size, and behavior when no connection or data exists.
3. Verify statistical semantics explicitly: minimum history threshold, mean/std-dev calculation (population vs sample), inclusive bounds, and outlier error fields/codes.
4. Check malformed records: missing metric identifier, missing value fields, nonnumeric values, nonpositive window/multiplier, NaN/infinite values, and DB exceptions. Confirm behavior is intentional (reject, skip, or warning) and distinguish robustness caveats from blockers.
5. Verify dynamic registry integration: decorator registration, enabled-name lookup, unknown-name errors, adapter conversion from result objects to pipeline exceptions, and dependency injection through the top-level pipeline.
6. Run one static compile/import check, then remove generated caches and enumerate final artifacts. Report exact PASS/BLOCKER/CAVEAT findings with runtime tests explicitly marked as run or unrun.