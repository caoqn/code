---
name: bulk-cross-system-execution-gate
description: Execute and verify large multi-item synchronization and notification tasks without stopping at canary or conflicting ownership.
trigger: When a task requires syncing many records and sending one message per record across APIs.
---
1. Resolve the authoritative population and cardinality from task-visible sources before any mutation; explicitly distinguish singleton criteria from merely recent records.
2. Build a stable ordered manifest with one owner per disjoint range and record canary ownership. Do not change ownership mid-batch.
3. Perform one canary end-to-end, including destination write and message readback, then immediately launch the remaining ranges using a loop or script; never treat tool-call overhead as a reason to stop.
4. Use idempotency keys (email/record ID), and check existing destination/message state before retrying. Remove accidental canaries immediately and record the correction.
5. Validate destination schema types after bulk load; confirm booleans/timestamps are native types, not strings, and preserve unrelated protected rows unless replacement is explicitly required.
6. After every range, read back aggregate counts and per-item identities/payloads. Reconcile expected, completed, missing, duplicate, and unintended-extra counts.
7. Populate the native completion contract and verification report only after all mutations and readbacks pass; otherwise report blockers truthfully and never claim completion.