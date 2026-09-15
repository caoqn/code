---
name: feature-completeness-gate
description: Ensure multi-layer feature implementations fully satisfy every stated requirement
trigger: When implementing a feature spanning models, schemas, repositories, services, APIs, and security
---
1. Convert the task into a checklist of exact required files, symbols, fields, statuses, method names, endpoint paths, payloads, and authorization rules.
2. Inspect the existing architecture and identify authoritative source paths, dependency signatures, exception types, and router registration patterns before coding.
3. Require implementation to use the requested technology (for example ORM models when ORM is specified), not a simplified substitute, unless explicitly justified by repository constraints.
4. After implementation, grep every checklist symbol and endpoint path across the solution; detect duplicate or conflicting implementations and remove stale alternatives.
5. Exercise each service method directly with stubs for success, missing dependencies/entities, invalid state transitions, and downstream failures; verify state is mutated only after downstream success.
6. Compile every submitted file and inspect imports, response schemas, DI wiring, and RBAC dependencies. Report unavailable runtime dependencies separately from implementation defects.
7. Before finalizing, compare the final file inventory against the checklist and reject minimal implementations that omit integration modules, router registration, or required fields.