---
name: resource-efficient-architecture-scan
description: Rapidly produce a dependable dependency map without exhausting task budgets
trigger: When assigned a cross-file architecture or dependency analysis task
---
1. Identify the requested feature's named modules, interfaces, and integration points from the prompt.
2. Read only those files plus one-hop callers/importers; prefer targeted symbol searches over broad directory scans.
3. Extract exact signatures and data flow, recording risks as soon as discovered.
4. Send a concise dependency map to the implementer immediately, including required edits and verification hints.
5. Reserve follow-up reads for explicit gaps or questions; do not repeatedly restate unchanged findings.
6. If the team is iterating near its time budget, provide the best-supported map and stop rather than pursuing exhaustive coverage.