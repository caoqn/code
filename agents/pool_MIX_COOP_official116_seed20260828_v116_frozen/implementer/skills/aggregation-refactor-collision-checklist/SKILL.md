---
name: aggregation-refactor-collision-checklist
description: Safely refactor grouped aggregation naming while preserving collision behavior across aggregation paths.
trigger: When replacing MultiIndex or dictionary aggregation with native named aggregation APIs.
---
1. Inventory every aggregation family (simple, unique-count, variance/std, custom) and identify where each produces output columns.
2. Capture baseline behavior and exact exception class/message for duplicate default aliases, duplicate explicit aliases, and collisions spanning different aggregation families.
3. Build native named-aggregation specs only for compatible families; retain separate paths where special kwargs or semantics are required.
4. Ensure collision detection runs after all result frames are assembled, so cross-family collisions are detected with the established exception type and wording.
5. Test zero, one, and multiple expressions; same source with different functions; same alias across positional and named forms; aliases with punctuation; and mixed special/simple aggregations.
6. Run the exact evaluator-targeted tests plus the complete grouped-aggregation suite, then compile the full tree and inspect the final diff for stale pre-refactor logic.