---
name: native-state-reconciliation
description: Reconcile multi-system mutations against authoritative targets and completion contracts before final handoff.
trigger: When a task mutates an external database and messaging system and requires exact counts or idempotent delivery.
---
1. Resolve the authoritative population and target count from the task-visible source; explicitly distinguish it from legacy or similarly named datasets.
2. Build a stable manifest with one owner per target, including canary, pending, completed, failed, and unverified states.
3. Before mutation, inspect destination schemas and existing records to confirm field types, deduplication keys, and protected state.
4. Perform mutations in disjoint ownership batches, recording every returned external ID immediately.
5. Read back each system independently: count rows, distinct keys, required field values/types, and message folder totals plus recipient/subject uniqueness.
6. Compare readbacks to the manifest, not to assumptions or local files. Treat missing IDs, malformed types, stale flags, and count mismatches as blockers.
7. Update the completion contract and verification report only from direct readback evidence; never mark complete while any target is pending or unverified.
8. Report direct evidence, inferred compatibility, destructive side effects, and unresolved limitations separately in the final handoff.
