---
name: evaluator-contract-audit
description: Derive and verify hidden/public evaluator contracts across inconsistent repository context before implementation.
trigger: When task requirements are implied by tests, compatibility wrappers, or multiple conflicting source layouts.
---
1. Enumerate every context and solution file, then grep for requirement keywords, public symbols, endpoint names, and import paths.
2. Build a requirement-to-artifact matrix: for each symbol, record expected module path, signature, return shape, side effects, error behavior, and compatibility aliases.
3. Inspect all tests (including apparently stale or skipped tests) for exact signatures, cache keys, event topics, ordering, limits, and exception classes; treat referenced absent imports as mandatory compatibility requirements.
4. Identify the actual runtime import root by inserting the solution root into a clean Python process and checking `module.__file__`; ensure wrappers work from the evaluator's likely cwd.
5. Implement or request separate artifacts for each public surface (service, REST, GraphQL, package exports), rather than assuming one file satisfies all dimensions.
6. Run focused behavioral matrices for valid, invalid, empty, partial-failure, concurrency, and boundary inputs; separately introspect signatures and annotations.
7. Compile every output file, remove generated artifacts, and re-open the final tree to verify all matrix rows have a concrete implementation.