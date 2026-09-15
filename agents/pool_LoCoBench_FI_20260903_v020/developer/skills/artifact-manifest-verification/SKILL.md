---
name: artifact-manifest-verification
description: Verify generated solution artifacts against source inventory and task scope before finalization
trigger: When producing files for evaluation or patch delivery in repositories with duplicate or legacy entrypoints
---
1. Inventory all source/context files and identify canonical and alternate entrypoints.
2. Build an explicit expected output manifest from the task wording, planner instructions, and repository structure.
3. Copy or edit required artifacts incrementally, preserving complete content and exact paths.
4. Normalize generated files (remove accidental formatting fences) without deleting requested files.
5. Run syntax/static checks on every generated code artifact.
6. Compare the final file listing against the expected manifest; investigate both missing and unexpected files.
7. Remove only generated caches and unrelated artifacts after confirming they are not required outputs.
8. Report the final manifest and any compatibility caveats to the planner.