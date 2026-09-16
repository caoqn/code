---
name: time-boxed-mutation-coordination
description: Efficiently coordinate large multi-item environment mutations under strict wall-clock and communication budgets.
trigger: When a task requires many API mutations plus artifacts and verification within a bounded execution window.
---
1. Parse the task into authoritative population, exact payload, mutation targets, artifacts, and verification gates.
2. Dispatch inventory, mutation, and verification assignments immediately; include complete context, disjoint ownership, and explicit evidence requirements.
3. Set a canary and checkpoint, but cap exploratory calls and status messages; use one consolidated progress report per agent.
4. Require the mutation owner to execute the full assigned population without pausing for repeated confirmations, recording counts and stable IDs as it proceeds.
5. Run verification in parallel where safe, prioritizing authoritative aggregate and per-item readbacks over local summaries.
6. Reserve a fixed final time window for artifact readback, reconciliation, contract synchronization, and exact-format submission.
7. If progress is incomplete near the deadline, stop exploratory work, report truthful completed/remaining counts, and submit only after the strongest available reconciliation.