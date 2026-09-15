---
name: quality-feature-audit
description: Audit and integrate data-quality features across batch and streaming paths with robust contracts.
trigger: When a task adds validation, quality checks, quarantine, or auditing to a pipeline.
---
1. Enumerate every execution path (batch stages, streaming consumers, scheduled/CLI auditors) and identify the canonical path plus duplicates.
2. Search for existing validators, metrics, artifacts, exception classes, serializers, configuration fields, and callback contracts before proposing APIs.
3. Lock the helper contract explicitly: accepted input types, tuple/object shape, success and failure reason semantics, threshold/range validation, and preservation of original data.
4. Trace invalid input handling end-to-end: malformed payloads, missing fields, wrong types, NaN/infinite values, out-of-range values, empty data, and duplicate processing. Define whether to reject, quarantine, retry, or commit offsets.
5. Map configuration and registration wiring, including environment aliases, topic names, producer/consumer lifecycle, and optional dependency fallbacks.
6. Inspect or add focused tests for helper behavior, stage integration, stream quarantine, metrics/artifacts, and shutdown cleanup; run static compilation and remove generated artifacts.
7. Deliver one prioritized implementation contract and final checklist, distinguishing confirmed requirements from inferred compatibility choices.