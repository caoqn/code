---
name: time-boxed-delegation
description: Efficient workflow for multi-agent repository fixes under strict time or budget limits
trigger: When coordinating or contributing to a repository task with multiple agents and bounded execution resources
---
1. Inspect only the task statement and repository status initially; avoid broad exploratory scans.
2. Dispatch implementation and verification agents immediately with explicit file targets, hypothesis, and one or two focused checks.
3. Time-box independent investigation; if findings are sufficient to support a minimal fix, stop exploring and report evidence.
4. Keep coordination messages concise and batch updates, requesting complete results rather than incremental speculation.
5. Prefer focused tests covering the changed behavior, followed by a single compilation or smoke check; avoid redundant full-suite runs unless required.
6. Before finalization, reconcile implementation, tests, and output contract once, then submit without further iterative messaging.