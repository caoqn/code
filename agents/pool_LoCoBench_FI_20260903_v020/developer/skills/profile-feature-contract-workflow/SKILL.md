---
name: profile-feature-contract-workflow
description: Implement cross-layer dataset profiling features with exact schemas, persistence, and API contracts
trigger: When adding profiling/statistics metadata across domain, application, storage, and HTTP layers
---
1. Extract exact required model field names and response shape before coding; record numeric, categorical, empty-data, and missing-resource semantics.
2. Identify the canonical service module and all legacy aliases; implement one canonical model/service and make compatibility modules re-export it.
3. Define domain DTOs first, then application ports for loading datasets and persisting profiles; preserve existing storage interfaces through additive protocols or aliases.
4. Implement deterministic profiling with JSON-safe native scalar conversion, explicit null handling, stable categorical frequency ordering, and defined behavior for empty frames.
5. Add storage save/load methods at the exact deterministic path and ensure serialization supports both major validation-library versions.
6. Wire POST (compute/persist) and GET (retrieve or explicitly specified fallback) routes into the canonical router, mapping missing datasets/profiles to the exact HTTP status and detail.
7. Update documentation by replacing stale schema text rather than appending contradictory sections; include an exact example payload.
8. Run syntax checks, grep for duplicate outdated implementations and required symbols, verify route registration, and remove generated caches before handoff.