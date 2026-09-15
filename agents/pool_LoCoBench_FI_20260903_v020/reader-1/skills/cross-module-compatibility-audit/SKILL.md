---
name: cross-module-compatibility-audit
description: Audit interfaces across schemas, services, repositories, and tests before handing implementation guidance
trigger: When a feature spans multiple modules or parallel/legacy implementations exist
---
1. Enumerate all requested files plus adjacent contract files (schemas, routers, models, repositories, tests).
2. Extract exact public signatures, field names, enums, error types, and async/sync conventions from each.
3. Build a compact compatibility matrix identifying mismatches and likely canonical contracts; distinguish production imports from test-only/legacy packages.
4. Search for all references to key classes/functions to find duplicate entrypoints and integration wiring.
5. Send the implementer one prioritized report with code excerpts, must-match interfaces, and explicit mismatch warnings.
6. After implementation, perform one focused read-only check of changed integration points and report any unresolved contract risks.