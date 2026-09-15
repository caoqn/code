---
name: dlq-feature-completion
description: Implement dead-letter handling comprehensively across models, configuration, processing, persistence, and tests
trigger: When adding DLQ or per-record failure quarantine behavior to an ETL/data pipeline
---
1. Inventory canonical models, settings, strategy/processor abstractions, registries, and all existing tests before editing.
2. Define an explicit failure-record schema with stable field names, serialization rules, and timezone-aware ISO timestamps; support conservative coercion of datetime inputs.
3. Add configuration as a nested section with backend type and path, environment override semantics, validation of supported backends, and compatibility accessors only when needed.
4. Implement an injectable writer interface plus a local JSONL writer that creates parent directories and appends exactly one serialized record per failure.
5. Add per-record processing APIs that catch only processor failures, capture step/reason/timestamp, invoke the writer once, preserve successful output order, and continue iteration.
6. Preserve existing DataFrame/strategy interfaces and register new strategies through canonical factories; expose public symbols from expected modules.
7. Add focused tests covering schema serialization, config overrides, writer output, failed-record capture, continuation, ordering, and writer invocation count.
8. Run syntax checks and the focused test suite, then verify the artifact manifest, remove caches/fences, and inspect diffs for accidental deletions.