---
name: dependency-regression-triage
description: Systematically distinguish baseline failures from dependency-induced regressions and ensure evaluator-targeted tests are fixed.
trigger: When a compatibility patch leaves targeted tests failing, especially after a dependency upgrade.
---
1. Run the exact failing tests before editing and record each failure.
2. Inspect dependency versions and identify whether current behavior differs from the project's historical assumptions.
3. Reproduce each failure with a minimal isolated snippet against the repository import path.
4. Search neighboring code and tests for the intended contract, including validation strictness, aliases, and error wrapping.
5. Implement the smallest compatibility-preserving fix; avoid dismissing failures as pre-existing unless a clean baseline proves they existed before the task.
6. Re-run every originally failing test, then the focused module suite and full suite.
7. Report remaining failures only with evidence that they are outside the requested contract and unaffected by the change.