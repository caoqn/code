---
name: cross-file-contract-gate
description: Enforce exact public exception/API contracts during cross-file refactors
trigger: When centralizing shared behavior or changing exceptions across services
---
1. Extract every literal contract from the task (class names, inheritance, status codes, response JSON keys) into a checklist before editing.
2. Inventory all target implementations, imports, raises, registrations, and tests; distinguish required scope from unrelated services.
3. Implement one canonical shared module with exact symbols and handlers first, preserving compatibility aliases only when needed.
4. Update each target service and direct caller to import and raise the exact canonical classes; replace generic or local exceptions at all specified boundaries.
5. Verify handlers by direct introspection or a minimal fake app: assert registration for each required class and exact response body/status.
6. Run grep to ensure stale target imports/raises/handlers are gone, compile all changed files, and remove generated artifacts.
7. Report dependency-limited tests separately from implementation failures, and do not claim broader services were refactored unless explicitly required.