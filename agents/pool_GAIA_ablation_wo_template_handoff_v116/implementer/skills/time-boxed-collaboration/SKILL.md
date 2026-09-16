---
name: time-boxed-collaboration
description: Efficient workflow for completing repository tasks under strict time or message budgets
trigger: When a task involves multiple agents, broad repository exploration, or limited execution budget
---
1. Inspect only the task-relevant files and current diff; avoid broad searches before establishing scope.
2. Dispatch implementation or investigation to the smallest useful set of agents within the first few actions.
3. Include acceptance criteria and exact verification commands in each dispatch to prevent clarification round-trips.
4. Run one focused test set and one broad sanity check; avoid repeated overlapping test runs unless failures require it.
5. Consolidate status updates into concise milestone messages rather than frequent incremental chatter.
6. If progress stalls after a small number of iterations, preserve the best valid artifact and report concrete evidence instead of consuming the entire budget.