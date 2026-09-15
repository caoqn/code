---
name: bulk-task-authority-and-execution
description: Resolve conflicting task artifacts and complete large external mutations with authoritative evidence.
trigger: When a task requires filtering many records, updating external state, and notifying a population.
---
1. Identify the native evaluator-visible contract and task-provided authoritative sources before any mutation.
2. Build a literal requirement matrix covering population predicates, ordering, artifact schema, mutation targets, recipient set, and expected counts.
3. Reconcile conflicting counts by prioritizing explicit source files for population and direct service readbacks for state; record unresolved conflicts as blockers, not assumptions.
4. Assign a single execution owner and require uninterrupted completion of the full target set. Do not stop at a canary or ask the Chairman to manually construct large payloads.
5. Use a canary only to validate payload shape, then execute the complete batch via a generated loop or batch API.
6. Read back aggregate and per-item state, including every notification recipient and exact attachment/body, before declaring completion.
7. Update completion artifacts only from final readbacks, and refuse to submit a success summary when mutations remain incomplete or counts conflict.