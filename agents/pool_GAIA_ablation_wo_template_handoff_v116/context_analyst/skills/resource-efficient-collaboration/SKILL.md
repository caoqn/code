---
name: resource-efficient-collaboration
description: Time-boxed workflow for completing repository tasks under strict wall-clock and communication budgets.
trigger: At the start of any multi-agent code task where latency, quota, or cost may be constrained.
---
1. Confirm workspace and task scope with one lightweight status/listing command.
2. Dispatch implementation and verification as soon as the likely target file is identified; do not wait for exhaustive repository exploration.
3. Give each agent a concise objective, exact paths or search terms, and requested evidence/commands so they can work independently.
4. Consolidate findings in batches; prefer one summary message over repeated progress pings.
5. Time-box exploratory loops and test runs; prioritize focused tests plus compile/import smoke checks, then stop when acceptance evidence is sufficient.
6. If blocked, report the blocker immediately and reassign rather than spending multiple rounds on speculation.
7. Before final handoff, verify diff scope and required artifacts once, then conclude without redundant status checks.