---
name: calendar-artifact-evaluator-reconciliation
description: Validate calendar reminder tasks against persisted artifacts and exact evaluator semantics
trigger: When a task creates or edits calendar events and completion depends on an external evaluator
---
1. Obtain the evaluator ground truth, including target count, exact deadline timestamps, timezone offsets, reminder offset, duration, title matching, and duplicate/extra-event rules.
2. Inspect persisted calendar storage directly or through the evaluator's own read API; do not rely solely on teammate summaries or aggregate counts.
3. Build a per-target comparison keyed by canonical conference identifier, checking every required field and ensuring one-to-one mapping.
4. Explicitly inspect corrected or extended deadlines and verify that superseded events were removed rather than merely adding replacements.
5. Check boundary conditions: timezone/DST, inclusive date windows, event duration, duplicate IDs, unintended extras, and malformed titles.
6. Run the exact fail-to-pass/evaluator harness when available, and distinguish implementation failures from unavailable environment services.
7. Only report completion after all per-target checks and evaluator results agree; summarize counts and any zero-failure guarantees concisely.