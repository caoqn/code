---
name: f2p-before-finalization
description: Acceptance workflow for repository changes when an evaluator exposes explicit fail-to-pass tests
trigger: When a task includes named evaluator or fail-to-pass cases
---
1. Identify every explicit fail-to-pass test and its exact parameterization from the evaluator contract.
2. Run those tests directly against the captured source after implementation, independently of focused regression suites.
3. If a test fails, inspect the assertion and execution path; do not classify it as legacy or environment-only without reproducing and proving that classification.
4. Exercise adjacent variants, including duplicate, malformed, empty, and cross-path inputs when the requirement concerns validation or aliasing.
5. Only issue a completion summary after all fail-to-pass cases pass; otherwise report the blocker and withhold endorsement.
