---
name: api-feature-acceptance-audit
description: Audit feature requests that add API strategy/options across implementation, routing, schemas, and docs.
trigger: When a task adds a selectable API option or a new endpoint to an existing service.
---
1. Inventory the canonical application entrypoint and any duplicate legacy entrypoints; inspect how routes are mounted.
2. Trace the full request path from HTTP body/query parameters through validation models into service dispatch and registries.
3. For every newly named option, confirm it is represented in the live request schema and actually influences dispatch; documentation-only or registry-only additions are incomplete.
4. Match the exact route path, HTTP method, authentication behavior, status code, and JSON field names/types requested.
5. Preserve existing interfaces additively; avoid rewriting unrelated scaffolding.
6. Independently inspect changed files, grep exact acceptance literals, compile statically, and remove generated caches before submission.
