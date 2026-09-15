---
name: feature-contract-integration-gate
description: Implement cross-layer repository features by mapping exact contracts to existing architecture and verifying integration.
trigger: When adding an API feature that spans schemas, services, configuration, core logic, and tests.
---
1. Inventory the authoritative source tree, application/router registration, existing service constructors, configuration loader, and target business calculation before editing.
2. Build a requirement-to-symbol matrix listing exact endpoint path, request/response field names, public exports, configuration keys, defaults, and error semantics.
3. Trace all callers and integration hooks for the target calculation; extend the existing class or service rather than replacing it with a minimal substitute unless preservation is proven.
4. Implement state management with explicit expiry boundary behavior, deterministic normalization, and configuration values wired into runtime construction rather than merely written to a config file.
5. Support the documented dependency signature first, then compatibility variants only when verified by introspection or tests; avoid catching internal TypeErrors as signature detection without care.
6. Add focused tests for success/failure, sync/async dependencies, expiry before/at/after boundary, multiplier active/inactive, and configuration-present/absent behavior.
7. Run compile, targeted tests, static greps for exact symbols/routes/keys, and inspect changed-file inventory. Verify the evaluator-visible artifact path and remove generated caches.