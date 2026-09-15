---
name: resource-efficient-review
description: Conduct implementation review quickly under strict time or message budgets.
trigger: When reviewing a multi-agent code task with limited execution time.
---
1. Inspect the changed-file summary and only the interfaces most likely to break; avoid broad repository scans.
2. Produce a prioritized checklist of correctness risks (API contracts, imports, edge cases, integration) in one concise message.
3. Ask the implementer for a single consolidated status/update rather than multiple incremental exchanges.
4. Perform at most one focused follow-up inspection after fixes, then report residual risks and stop.
5. If the task is nearing its budget, favor a clear partial review over additional exploratory calls.
