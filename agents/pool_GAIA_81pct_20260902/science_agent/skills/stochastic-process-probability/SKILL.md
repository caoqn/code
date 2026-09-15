---
name: stochastic-process-probability
description: Derive outcome probabilities in sequential random-transition systems with absorbing events.
trigger: When asked which item/state has the highest probability under repeated random actions.
---
1. Restate the state variables and absorbing success/failure events precisely; clarify ambiguous transition rules before calculating.
2. Define one probability per relevant state (for example, success probability conditional on an item occupying each position).
3. Write first-step equations by conditioning on the next random action, including all state transitions and immediate absorption outcomes.
4. Solve the resulting linear system exactly when feasible, then compare the state-conditioned probabilities.
5. Map each item’s initial state to these probabilities. For finite supplies or termination, establish whether truncation can only reduce probabilities relative to an infinite-horizon model.
6. Check edge cases (initial items, final incomplete transitions) and perform a quick simulation or numerical sanity check only after the analytic derivation.
7. Report the maximizing item and the key equations concisely, noting assumptions about termination and supply.