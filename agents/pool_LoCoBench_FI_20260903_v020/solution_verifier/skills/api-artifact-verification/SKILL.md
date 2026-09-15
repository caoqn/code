---
name: api-artifact-verification
description: Reusable checklist for validating small API feature submissions and their packaged artifacts.
trigger: When reviewing a generated API endpoint, strategy/plugin, or documentation change before final approval.
---
1. Enumerate the output directory and compare it to the task's exact required file paths; flag missing, renamed, or extra artifacts.
2. Read the implementation symbols that define the new behavior, then trace imports and registration/wiring into the canonical application entrypoint.
3. Verify every literal contract explicitly: HTTP method, route path, authentication dependency, status code, response field names, and numeric/string values.
4. Check robustness boundaries statically: invalid inputs, unknown registry keys, duplicate registration, missing optional dependencies, and import-time failures.
5. Inspect documentation for an example matching the implemented route and exact payload, while separating cosmetic formatting issues from blockers.
6. Run one lightweight syntax/static check, then remove any generated caches and re-enumerate artifacts.
7. Send one concise prioritized report listing PASS items and concrete blockers; do not approve based on inferred framework defaults.