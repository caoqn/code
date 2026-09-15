---
name: resource-bounded-coordination
description: Efficient multi-agent workflow for large codebase tasks under strict time and message budgets
trigger: When coordinating implementation across multiple agents with limited execution time
---
1. Dispatch parallel readers immediately with explicit file scopes and concrete deliverables.
2. Set a short exploration deadline; request only interfaces, constraints, and likely change points rather than broad summaries.
3. Assign one implementer early, supplying incremental findings as they arrive instead of waiting for complete analysis.
4. Have reviewers inspect the proposed patch while implementation is still underway, focusing on integration risks and missing requirements.
5. Consolidate communication into milestone updates; avoid repetitive status pings and duplicate requests.
6. Reserve a fixed final window for verification and packaging, and stop exploratory work when that window begins.
7. If blocked after a small number of iterations, submit the best complete solution rather than consuming the entire budget on marginal refinements.