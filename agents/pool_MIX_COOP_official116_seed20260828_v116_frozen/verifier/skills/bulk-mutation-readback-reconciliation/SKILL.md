---
name: bulk-mutation-readback-reconciliation
description: Verify bulk external mutations by reconstructing targets and reconciling every returned record, payload, and status.
trigger: When a task sends messages, updates rows, or performs any multi-item external mutation.
---
1. Derive the authoritative target set from source data, including stable identity, inclusion rules, and exact expected fields.
2. Before mutation, snapshot relevant external state and record existing duplicates or prior partial mutations.
3. Use one writer and disjoint batches; track each target as pending, completed, failed, or unverified.
4. After each batch, read back the external state and reconcile identities, counts, duplicates, extras, and exact payload fields against the target set.
5. Re-query after any delayed or asynchronous update; never accept a claim that conflicts with a fresh authoritative readback.
6. Distinguish mutation success from metadata/status synchronization; verify both independently.
7. Report remaining, duplicate, malformed, mismatched, and unverified items explicitly, and only mark complete when all are reconciled.