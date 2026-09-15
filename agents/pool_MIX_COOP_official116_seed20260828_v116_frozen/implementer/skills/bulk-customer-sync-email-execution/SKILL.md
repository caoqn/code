---
name: bulk-customer-sync-email-execution
description: Safely synchronize a canonical customer population and send personalized first-order emails with strict mutation and readback controls.
trigger: When a task requires bulk database synchronization plus one email per selected customer.
---
1. Resolve the authoritative population and selection predicate before any mutation; materialize a deduplicated manifest keyed by stable identity.
2. Reconcile the manifest against both database and mailbox state, recording pre-existing, missing, duplicate, and unintended records.
3. Validate destination schema types using a representative readback. Avoid CSV loaders whose write mode or type coercion is uncertain; prefer typed DML or test a disposable canary first.
4. Generate payloads from the exact template and source fields, including explicit amount/date derivation rules. Validate every payload locally before sending.
5. Freeze disjoint ownership ranges and obtain explicit confirmation before parallel writes. Never send a canary outside the target set, and never proceed on ambiguous ownership.
6. Execute a canary within the true target set, independently read back its email and database row, then continue bounded batches while persisting returned IDs immediately.
7. After each batch, query mailbox state by recipient and exact subject/body, and query database counts, distinct identities, typed flags, and required timestamps. Treat aggregate success as insufficient.
8. Before finalization, re-read all artifacts and update the completion contract only when every target is sent and verified, schema values are correctly typed, protected pre-existing state is reconciled, and no unintended extras remain.