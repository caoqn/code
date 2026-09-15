---
name: bounded-final-review
description: Complete a fast, single-pass implementation review under strict budgets.
trigger: When reviewing a teammate's broad multi-file implementation near a hard deadline.
---
1. Read only the changed-file list and task acceptance criteria; do not rescan the entire repository.
2. Select the two or three highest-risk interfaces (canonical entrypoint, public schema/API, persistence or contract boundary).
3. Inspect those files plus directly imported definitions for syntax, names, and edge-case semantics.
4. Send one consolidated report to the implementer, ordered as blocking defects, likely defects, and non-blocking caveats.
5. Allow at most one focused recheck after corrections; otherwise stop and preserve budget for final validation.
