---
name: efficient-verification
description: A time-boxed workflow for validating generated software submissions against requirements.
trigger: When reviewing a completed implementation under a strict time or tool budget.
---
1. Enumerate the output directory and identify required files before reading implementation details.
2. Compare each requirement to a specific file, symbol, or behavior; record gaps in a compact checklist.
3. Read only the smallest relevant sections needed to confirm contracts, imports, and integration points.
4. Run at most one lightweight static check when execution is prohibited or unnecessary.
5. Report pass/fail findings promptly to the coordinating agents, including concrete missing requirements.
6. Stop once coverage is sufficient; do not re-open already verified files or send redundant status messages.