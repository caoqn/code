---
name: external-mutation-evaluator-reconciliation
description: Reconcile externally persisted mutations against evaluator-visible destination state and identity semantics
trigger: When a task mutates email, calendar, storage, or another external environment and completion depends on an evaluator
---
1. Read the evaluator contract to identify the authoritative actor, destination account, expected sender/owner, and target records.
2. Build a per-record checklist covering identifiers, direction (inbox/sent/outbox), sender, recipients, subject/title, payload, attachments, and status flags.
3. Perform mutations using the account and API context specified by the contract; do not assume a successful API call or local session corresponds to the expected actor.
4. Read back from the evaluator-visible destination (for email, inspect both sender Sent and recipient Inbox when direction matters), then compare every record to the checklist.
5. Treat mismatched actor identity, folder, direction, or recipient-side visibility as a contract failure even when counts and payloads match.
6. Verify artifacts and manifests at the exact evaluator-visible paths, and run the complete evaluator or closest validation harness before finalizing.
7. Report only reconciled counts and explicitly identify any unresolved identity or destination discrepancy.