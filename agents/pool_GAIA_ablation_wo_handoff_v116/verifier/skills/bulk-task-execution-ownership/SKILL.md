---
name: bulk-task-execution-ownership
description: Safely execute assigned bulk mutations while preventing duplicate writers and coordination stalls
trigger: When multiple agents share a bulk external-state mutation and ownership or authorization may change
---
1. Derive and freeze the exact target subset from authoritative source data, including stable IDs and payload fields.
2. Record one authoritative writer per mutable resource and confirm the writer's ownership before the first mutation.
3. If messages conflict, obtain one explicit latest authorization from the task lead; do not infer permission from an older message.
4. Once authorized, execute the assigned batch promptly using the available bulk or sequential interface; do not wait for unrelated verification work.
5. Record every returned mutation ID and immediately perform a fresh authoritative readback for the assigned subset.
6. Reconcile missing, duplicate, extra, and malformed records, including status/type fields—not only counts.
7. Report blockers with exact remaining counts and evidence, distinguishing inability to execute from a failed mutation.