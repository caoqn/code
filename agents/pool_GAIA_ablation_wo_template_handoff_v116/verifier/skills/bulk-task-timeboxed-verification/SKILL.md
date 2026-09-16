---
name: bulk-task-timeboxed-verification
description: Efficient workflow for large bulk mutations and independent verification under finite time or message budgets
trigger: When a task requires many external records, spreadsheet rows, emails, or other repeated mutations
---
1. Read the task-visible source artifacts once and derive the complete expected target set programmatically, including stable IDs and all required payload fields.
2. Create ownership and manifest metadata before any mutation; assign one writer and avoid overlapping workers.
3. Dispatch execution immediately with the exact target count, payload contract, and one focused verification command or readback plan.
4. Perform mutations in bounded batches, recording returned IDs/statuses; do not retry successful operations merely because messages or responses are delayed.
5. After mutation, issue one authoritative paginated readback and reconcile the full set programmatically for missing, duplicate, extra, and field-mismatched records.
6. Escalate only concrete discrepancies. Use direct per-entity reads for missing IDs when pagination is incomplete, rather than repeated broad polling.
7. Keep coordination concise: send aggregate progress and blockers, not per-item updates. Time-box investigation and stop exploratory calls once contract-level evidence is obtained.
8. Before sign-off, inspect final artifacts and completion metadata, compare counts and identities, and report expected/completed/verified/failed/unverified totals explicitly.