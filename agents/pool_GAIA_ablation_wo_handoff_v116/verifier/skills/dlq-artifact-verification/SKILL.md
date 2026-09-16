---
name: dlq-artifact-verification
description: Verify dead-letter processing changes across queue models, writers, pipelines, configuration, and exports.
trigger: When reviewing or implementing record-failure isolation and dead-letter queue support.
---
1. Inventory all changed modules and context tests; identify required public classes, aliases, fields, and constructor signatures.
2. Inspect import boundaries and optional dependency fallbacks before runtime testing; simulate absent dependencies when possible.
3. Compile every submitted source file, then run the narrowest DLQ-focused tests.
4. Exercise success, single failure, multiple failures, empty input, iterable input, failing intermediate pipeline step, custom writer, and disabled-writer paths.
5. Parse emitted JSONL and verify exact keys, original payload, failure reason, step identity, ordering, and index semantics.
6. Validate configuration precedence with defaults, environment variables, and explicit overrides; ensure nested and flat compatibility APIs do not conflict.
7. Grep all exports and callers, detect duplicate class definitions or stale aliases, then run the relevant broader test subset and report unrelated collection/dependency failures separately.