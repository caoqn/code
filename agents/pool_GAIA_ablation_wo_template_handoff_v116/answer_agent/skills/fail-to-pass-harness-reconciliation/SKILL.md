---
name: fail-to-pass-harness-reconciliation
description: Validate fixes against explicit evaluator fail-to-pass tests, especially under monkeypatched or simulated dependency/runtime conditions
trigger: When a task provides named fail-to-pass tests or an evaluator harness in addition to regression tests
---
1. Locate the exact evaluator test file and read its fixtures, monkeypatches, imports, warning capture, and assertions.
2. Run the exact fail-to-pass command against the captured working tree before endorsing any implementation; record each test result.
3. If failures occur despite broad tests passing, classify whether the discrepancy comes from simulated dependencies, fallback stubs, warning filters, alternate constructors, or source/import resolution.
4. Inspect the implementation branch exercised by the failing fixture and compare its behavior to the exact assertion, including warning categories/messages and public symbols.
5. Request remediation or a targeted regression test when any evaluator case remains failing; do not issue a completion summary based solely on pass-to-pass suites.
6. Re-run both the exact fail-to-pass harness and relevant regression suites after remediation, then report reconciled results and any environment-only limitations.