---
name: resource-bounded-review
description: Time-boxed review workflow for multi-agent software tasks under strict budgets
trigger: When validating a generated solution or coordinating reviews with limited time
---
1. Extract exact acceptance contracts (paths, methods, payloads, statuses, auth, artifact names) before opening files.
2. Enumerate output artifacts and inspect only canonical entrypoints plus newly changed files; avoid broad repository scans.
3. Dispatch or request implementation/review within the first few actions using a concise checklist.
4. Use one lightweight static check at most, then compile findings into a single prioritized pass/fail report.
5. Allow one focused correction round; if unresolved or time is low, stop and submit evidence rather than iterating.
6. Avoid repeated status polling and duplicate messages; consolidate all findings for each recipient.
7. End with a clear cutoff decision and preserve remaining budget for final verification or unexpected issues.