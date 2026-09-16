---
name: cross-file-contract-reconciliation
description: Systematically reconcile a multi-file implementation against requirements, existing patterns, and edge cases before final endorsement.
trigger: When reviewing or finalizing a repository change spanning multiple modules or public APIs.
---
1. Extract each requirement into a checklist of concrete symbols, files, exports, callers, and behavior, including negative and boundary cases.
2. Inventory existing implementations and public import paths before accepting new modules; compare old and new symbol/behavior surfaces to detect feature loss.
3. Trace every changed API through all callers and factories, checking defaults, dependency injection, aliases, error types, and optional-dependency branches.
4. Exercise representative success, empty, malformed, unknown-identifier, and missing-dependency paths with focused tests or controlled stubs.
5. Inspect every changed source artifact for syntactic completeness, placeholders, accidental fences, and evaluator-visible location; compile the entire tree.
6. Classify any unverified behavior explicitly and determine whether it is in-scope, reachable, and blocking. Require remediation or a targeted test for reachable in-scope gaps.
7. Report a concise evidence matrix mapping each requirement to verification evidence before issuing completion output.