---
name: concise-coordination-under-timeout
description: A strict workflow for coordinating implementation tasks under finite wall-clock and message budgets.
trigger: When a task has many agents, broad requirements, or a hard execution timeout.
---
1. Perform one repository listing and identify only the files needed to map the requested feature.
2. Recruit one implementer and at most two non-overlapping evidence specialists; add review capacity only if the scope genuinely requires it.
3. Send each agent a single complete assignment containing file targets, acceptance criteria, and a hard cutoff; instruct evidence agents to report directly to the implementer.
4. Do not relay intermediate findings or request repeated confirmations. Allow implementation to proceed as soon as the first sufficient evidence arrives.
5. Use one checkpoint to confirm artifact creation, then one final verification pass covering file placement, syntax, interfaces, and exact acceptance literals.
6. If the cutoff approaches, prioritize a complete minimal implementation and submit existing artifacts rather than spending time on iterative polish or broad test execution.
