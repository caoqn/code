---
name: cross-layer-integration-smoke
description: Verify that newly added modules integrate through real application call paths, imports, and dependency-injection wiring rather than only isolated unit smoke tests.
trigger: When a change adds repositories, services, factories, adapters, or compatibility modules across multiple layers
---
1. Enumerate every changed public symbol and its expected import path; inspect package __init__ exports and all internal callers.
2. Build a requirement-to-symbol matrix covering happy path, invalid input, empty state, missing optional dependency, and connector failure behavior.
3. Instantiate the top-level factory with a minimal fake connector and invoke one representative operation per service, tracing repository calls and return shapes.
4. Import modules through the same package path used by the application, checking for circular imports and absent re-exports; do not rely solely on direct file imports.
5. Run static compilation across the complete source tree, then targeted integration tests that exercise service→repository→connector and compatibility aliases.
6. Record untested branches explicitly; treat any reachable import mismatch, uncaught connector error, or inconsistent return shape as a blocker or documented limitation.