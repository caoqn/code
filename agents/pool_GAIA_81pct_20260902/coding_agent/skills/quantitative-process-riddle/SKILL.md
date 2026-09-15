---
name: quantitative-process-riddle
description: Solve stochastic sequential-process riddles using exact state modeling, dynamic programming, and recurrence validation.
trigger: When asked to identify a maximizing item or probability in a random sequential mechanism.
---
1. Parse each operation into an explicit state transition, carefully distinguishing removed, ejected, and advancing items.
2. Implement a small exact-probability dynamic program over reachable states; use rational arithmetic when feasible.
3. Independently run a Monte Carlo simulation as a sanity check, but do not rely on simulation for the final maximizer when exact DP is tractable.
4. Tabulate initial probabilities and inspect them for a simple recurrence or limiting behavior.
5. Prove the candidate is globally maximal using the recurrence (including boundary cases), rather than only checking a finite sample.
6. Report the exact maximizing index and probability, plus enough transition detail for an independent reviewer to reproduce the result.