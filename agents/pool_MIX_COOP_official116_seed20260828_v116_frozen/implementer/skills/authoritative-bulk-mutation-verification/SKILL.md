---
name: authoritative-bulk-mutation-verification
description: Safely execute large sets of external record updates and personalized notifications with exact payloads and independent verification.
trigger: When a task requires synchronizing many records and sending one personalized mutation per target.
---
1. Build a canonical manifest directly from the authoritative source, including stable identity, destination, all substituted fields, and expected payload hash.
2. Reconcile the manifest against the destination before any mutation; mark pre-existing records, duplicates, and genuinely pending targets separately.
3. Generate each payload from the canonical record and template, preserving every required section and formatting rule; validate locally before sending.
4. Use one mutation per target with bounded batches and persist the returned external ID immediately. Never infer success from a local manifest update.
5. After each batch, independently read back external state and compare destination, subject, body, and identity one-to-one against the manifest. Treat combined recipients, short bodies, or mismatched fields as failures requiring correction.
6. For database synchronization, verify the exact table and schema, then query counts and representative rows for every required flag/value. If readbacks conflict across tools, stop and report the conflict rather than asserting success.
7. Reconcile counts by unique stable identity, not message count. Track duplicates, failed, pending, and unverified items explicitly.
8. Only mark the completion gate ready when all targets have independently verified payloads and database state; otherwise preserve a truthful partial status.