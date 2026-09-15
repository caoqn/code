---
name: contract-reconciliation
description: Reconcile competing interfaces, schemas, routes, and tests before advising implementation
trigger: When a repository contains duplicate entrypoints or multiple versions of an API contract
---
1. Enumerate all candidate entrypoints, route prefixes, schema definitions, and service-layer DTOs relevant to the feature.
2. For each candidate, capture exact field names, types, aliases, status codes, and dependency/context keys.
3. Read integration tests and fixtures to identify the externally enforced contract; treat tests as evidence, not assumptions.
4. Build a compact comparison table highlighting agreements, conflicts, and likely canonical implementations.
5. Report concrete code excerpts and explicitly recommend which contract to target, including risks of alternate modules.
6. Include one focused verification checklist covering route mounting, payload shape, serialization, and caller compatibility.