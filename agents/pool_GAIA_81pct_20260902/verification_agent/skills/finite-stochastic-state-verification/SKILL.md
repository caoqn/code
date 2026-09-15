---
name: finite-stochastic-state-verification
description: Solve and verify finite stochastic process puzzles by reducing object positions to state values and checking boundary effects.
trigger: When a puzzle asks which item maximizes success probability under random transitions, removals, or finite resources.
---
1. Parse each action exactly: identify which object is struck, which objects move, and which objects are removed without success.
2. Define continuation values for an object in each possible state/position, including immediate success and failure probabilities.
3. Write Bellman-style equations by conditioning on the next random action; solve symbolically before using decimals.
4. Map each candidate item to its initial state or arrival-state distribution. For later arrivals, account for both the probability of reaching that state and the continuation value.
5. Prove an upper bound using the maximum state value; check whether any candidate attains it and whether the maximizer is unique.
6. Analyze finite-resource/termination boundaries separately. Show the candidate's resolution occurs before exhaustion, or quantify any truncation effect.
7. Test the equations against explicit action paths and a small simulation or hand enumeration when practical.
8. Report the requested item in the exact output format, retaining probability details only as supporting evidence.