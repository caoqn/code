---
name: evaluator-first-regression-diagnosis
description: Diagnose and resolve designated fail-to-pass tests even when baseline also fails
trigger: When evaluator reports fail-to-pass tests that remain failing after an apparently correct patch
---
1. Enumerate every designated fail-to-pass test and run them individually, preserving parametrized IDs.
2. Compare each failure against baseline, but do not dismiss baseline failures: the evaluator contract still requires them to pass.
3. Trace the failing path from public entrypoint through schema construction, validation, coercion, and output; inspect any migration/version-specific branches.
4. Build a minimal input/output matrix covering valid values, invalid types, missing required fields, nested promises, and extra keys.
5. Identify the smallest shared logic change that satisfies the required matrix without weakening unrelated compatibility behavior.
6. Rerun all designated tests, then the focused module and evaluator-relevant broader suite; report remaining failures by exact test ID and classify environmental versus implementation causes.