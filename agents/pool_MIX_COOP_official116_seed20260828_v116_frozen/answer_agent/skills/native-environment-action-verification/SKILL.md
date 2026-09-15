---
name: native-environment-action-verification
description: Execute and verify large batches of external-environment mutations under strict evaluator contracts
trigger: When a task requires populating external records, sending notifications, or producing evaluator-visible artifacts through tools
---
1. Extract the exact target count, destination identifiers, required fields, and completion gate from the native contract.
2. Build the complete payload deterministically from the authoritative source, preserving ordering and all required fields.
3. Prefer one atomic/bulk mutation when supported; if constrained, partition into bounded batches and record each batch's intended range and result.
4. After every mutation, perform evaluator-shaped readback from the destination rather than trusting update counts. Check contiguous IDs, required fields, and duplicate/missing records.
5. Treat tool truncation, parser offsets, or ambiguous responses as verification failures—not evidence of success. Change the readback strategy (smaller ranges, alternate endpoint, or per-record checks) and continue mutations until the full target count is independently confirmed.
6. For messages, verify recipient, subject/body template, links, and one-to-one coverage against the target IDs; aggregate mailbox counts are insufficient.
7. Validate required manifest/contract artifacts and readiness flags after all actions. If blockers remain, report exact verified and pending counts, but do not stop while feasible actions remain.
8. Before finalizing, run the evaluator or closest contract check and reconcile every failure against the actual persisted destination state.