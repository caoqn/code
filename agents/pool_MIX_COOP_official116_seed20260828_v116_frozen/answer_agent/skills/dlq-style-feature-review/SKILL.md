---
name: dlq-style-feature-review
description: Review cross-cutting resilience features for contract coverage, robustness, and maintainable integration
trigger: When adding failure capture, retries, dead-letter handling, or similar cross-layer infrastructure
---
1. Extract the exact public contract: model fields and serialization keys, writer methods, strategy signatures, exports, configuration defaults, and environment overrides.
2. Build a matrix mapping each contract item to its defining file, all import/re-export paths, callers, and focused tests.
3. Validate success, per-item failure continuation, empty input, malformed configuration/path, writer I/O failure, and optional-dependency absence. Ensure failures do not leak sensitive payloads through logs or exceptions.
4. Inspect serialization determinism (timestamps, null/optional fields, JSON encoding), ordering guarantees, thread/process safety, directory creation, and append semantics.
5. Check compatibility aliases and abstract interfaces; preserve existing strategy behavior while integrating the new path rather than bypassing it.
6. Run the exact evaluator plus complete-tree compilation, then inspect artifacts for placeholders/fences and verify the runtime import resolves to the submitted source tree.
7. Report any environment-only failures separately and summarize residual untested branches instead of claiming blanket correctness.