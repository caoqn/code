---
name: resource-bounded-refund-feature
description: Efficient workflow for implementing cross-layer features under strict time and communication budgets.
trigger: When a feature spans schemas, service logic, routes, auditing, and documentation in a multi-module repository.
---
1. Perform a single scope scan to identify canonical model/service/router files and acceptance criteria.
2. Dispatch the implementer plus at most two evidence specialists immediately, assigning non-overlapping files and requiring direct reports to the implementer.
3. Give the implementer a minimum viable target and compatibility checklist: preserve constructors, public schemas, and existing route wiring; add changes rather than replacing scaffolding.
4. Set a hard cutoff: one evidence round, one implementation pass, and one verification pass. Do not request repeated status updates.
5. Have the verifier inspect changed artifacts, route reachability, exact payload fields, and documentation placement using static checks only unless execution is explicitly allowed.
6. If late issues remain, prioritize required endpoint/service/schema behavior over optional polish and submit existing artifacts before the budget expires.
7. Provide the final summary only after confirming solution files exist and list verification results concisely.