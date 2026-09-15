---
name: time-boxed-coordination
description: Efficiently coordinate multi-agent software tasks under strict time or message budgets.
trigger: At the start of any task with multiple files or delegated implementation.
---
1. Parse requirements and identify likely file groups in one brief pass.
2. Recruit only agents needed for non-overlapping evidence and implementation; avoid redundant specialists.
3. Dispatch complete instructions immediately, including requirements, assigned files, and expected report format.
4. While agents work, limit status checks and relay messages; use a single checkpoint after expected completion time.
5. Ask implementer to proceed once core evidence arrives rather than waiting for every optional review.
6. Reserve a short final window for verification and submission; if time is running low, submit existing artifacts instead of iterative rework.
