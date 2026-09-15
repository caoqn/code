---
name: final-artifact-audit
description: Bounded final verification of generated code artifacts against explicit contracts, syntax, tests, and cleanliness.
trigger: When acting as verifier on a multi-file generated software submission
---
1. Enumerate every file under the required output directory and compare names/paths against the task's explicit artifact list.
2. Read only canonical changed modules plus configuration and tests; grep for each required symbol, field, status, persistence path, and compatibility alias.
3. Inspect happy path and at least one malformed input, unknown key, missing resource, empty data, and per-item failure continuation path.
4. Run one bounded syntax/import check over all generated Python files; remove any caches or generated artifacts immediately afterward.
5. Record runtime-test status explicitly (executed, passed/failed, or unavailable) rather than implying static checks prove behavior.
6. Send one concise report distinguishing blockers (contract mismatches/missing artifacts) from non-blocking robustness or untested-runtime concerns to the implementer and lead.