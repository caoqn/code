---
name: resilience-feature-contract-audit
description: Audit cross-cutting quarantine, retry, or dead-letter features for strict behavioral separation and edge-case completeness
trigger: When adding or reviewing a resilience path that diverts, retries, or commits messages
---
1. Enumerate every destination path (normal ingest, quarantine, dead-letter, retry) and document its trigger conditions.
2. For each path, verify payload shape, callback/producer routing, metrics, logging, and offset commit semantics independently; ensure one path cannot accidentally invoke another path's handler or counters.
3. Exercise mixed, all-invalid, malformed, empty, boundary, and optional-callback configurations with controlled dependency stubs.
4. Inspect commit calls to confirm exact offsets/partitions expected by the consumer API rather than merely confirming that a commit occurred.
5. Verify shutdown/flush behavior is idempotent and does not drop pending diverted messages.
6. Build a requirement-to-symbol matrix covering configuration aliases, public validators, internal routing helpers, and exports; run full compilation and the evaluator's explicit fail-to-pass harness before endorsement.