---
name: bulk-mutation-readback-reconciliation
description: Execute bulk updates and notifications with deterministic ownership, correction handling, and authoritative reconciliation.
trigger: When a task requires many external record updates plus per-recipient notifications and artifacts.
---
1. Resolve the complete target set from authoritative sources and build a stable ID manifest.
2. Perform a canary mutation and read it back before bulk execution; never repeat successful canaries.
3. Execute disjoint batches, recording every success/failure and preserving protected fields.
4. After all batches, independently query destination state with pagination and reconcile expected IDs, extras, and missing IDs; if pagination conflicts, vary page size and explicitly document unresolved records.
5. For notifications, prefer direct per-recipient sends when evaluator expects recipient records; if using BCC, verify delivery union and acknowledge that Sent-folder count differs from recipient count.
6. Correct accidental mutations immediately via explicit inverse update and read back the correction.
7. Update manifests, verification reports, and completion gates only from fresh authoritative evidence; never claim readiness while any discrepancy remains.