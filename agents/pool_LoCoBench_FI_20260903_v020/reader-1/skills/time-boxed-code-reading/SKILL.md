---
name: time-boxed-code-reading
description: Efficient workflow for analyzing large repositories under strict time or message budgets
trigger: When assigned repository analysis during a multi-agent implementation task
---
1. Identify the exact files and interfaces needed for the assigned feature; avoid broad exploratory scans.
2. Read each target file once, extracting signatures, imports, and key control flow into a concise report.
3. Send one complete handoff to the implementer immediately, including concrete code snippets and assumptions.
4. Only perform follow-up reads when the implementer asks a specific question or a critical dependency is missing.
5. Keep status updates short and avoid duplicating information across planner and developer channels.
