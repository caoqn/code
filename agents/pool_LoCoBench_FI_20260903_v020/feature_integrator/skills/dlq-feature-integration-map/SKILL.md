---
name: dlq-feature-integration-map
description: Evidence-first workflow for integrating dead-letter or per-record failure handling into ETL pipelines
trigger: When a repository requests DLQ, failed-record capture, or resilient per-record processing
---
1. Identify every runtime path that consumes records (batch strategy, streaming consumer, API background task) and distinguish canonical versus legacy implementations.
2. Search models, settings, registries, exports, serializers, and tests for existing failure-record or queue contracts before proposing symbols.
3. Lock the failure record schema: arbitrary payload, human-readable reason, processing step, and UTC timestamp with an explicit serialization format.
4. Lock backend configuration and precedence, including defaults, environment variable names, path creation, and unsupported-backend behavior.
5. Map per-record control flow: invoke processor, catch only record-level failures, emit exactly one model to the writer, continue successful and later records, preserve ordering, and define writer-error semantics.
6. Verify all public exports and factory registration, including compatibility aliases only when justified by repository evidence.
7. Send one consolidated developer report containing confirmed requirements, inferred hypotheses, exact paths/symbols, edge cases, and a final static/import/test checklist; avoid repeated speculative messages.