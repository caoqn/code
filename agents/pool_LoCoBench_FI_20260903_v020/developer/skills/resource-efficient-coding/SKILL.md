---
name: resource-efficient-coding
description: Time-boxed workflow for implementing features in large repositories under strict budgets
trigger: When assigned a multi-file implementation task with limited execution time
---
1. Identify the minimum files and interfaces needed; avoid broad repository exploration.
2. Delegate parallel targeted reads immediately, specifying exact questions and expected snippets.
3. Start drafting implementation once core contracts are available; do not wait for every report.
4. Consolidate teammate feedback into one change list and apply changes in a single focused pass.
5. Run only lightweight syntax/static checks, then report completion; avoid repeated test loops unless a concrete failure is found.
6. Keep coordination messages concise and batch status updates to reduce communication overhead.