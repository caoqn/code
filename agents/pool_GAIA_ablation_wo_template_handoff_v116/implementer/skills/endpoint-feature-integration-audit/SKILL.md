---
name: endpoint-feature-integration-audit
description: Safely integrate cross-cutting middleware or dependencies across existing endpoint modules.
trigger: When a feature must be applied consistently to multiple routes or mirrored endpoint files.
---
1. Inventory every authoritative endpoint module and enumerate route functions, required parameters, and existing dependencies.
2. Normalize transport wrappers and copy files only after inspecting complete source blocks.
3. Prefer router-level dependencies or decorators that do not alter required function argument ordering.
4. Build a route-to-policy matrix (default, stricter subgroup, unauthenticated behavior, headers, errors) and verify each route explicitly.
5. Preserve existing service imports and API signatures; add compatibility shims rather than replacing implementations wholesale.
6. Run AST/compile checks and static greps for each required decorator/import/policy symbol.
7. Execute dependency-light policy tests, then optional framework import tests when dependencies are available; report limitations precisely.
8. Remove generated caches and inspect final artifact paths before handoff.