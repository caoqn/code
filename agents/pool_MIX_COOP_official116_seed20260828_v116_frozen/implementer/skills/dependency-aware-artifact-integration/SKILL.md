---
name: dependency-aware-artifact-integration
description: Implement and verify features when optional framework dependencies may be unavailable
trigger: When modifying framework integrations, validation hooks, or generated source in an environment with missing runtime packages
---
1. Inventory every authoritative source file, test import path, and public symbol required by the contract before editing.
2. Determine which dependencies are available; inspect installed API signatures when available, but do not execute untrusted context projects.
3. Keep core logic dependency-independent where practical, and provide safe fallback types that preserve importability without using typing sentinels in runtime checks.
4. Integrate framework hooks conditionally only after confirming the actual constructor/signature; document or test the fallback behavior explicitly.
5. Avoid replacing rich existing configuration or application modules with minimal substitutes; extend the authoritative implementation and preserve required defaults and validators.
6. Compile every generated Python file and run import-level smoke tests for both dependency-present and dependency-absent paths when feasible.
7. Re-read all changed files for duplicate declarations, stale imports, markdown fences, and public export mismatches before handoff.