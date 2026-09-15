---
name: canonical-integration-verification
description: Verify cross-cutting changes across application factories, optional imports, configuration, routes, and transport behavior
trigger: When a feature modifies middleware, routing, configuration, or multiple endpoint modules
---
1. Identify every application factory and determine which one tests and runtime imports actually use.
2. Trace route registration from factory through router prefixes; enumerate expected paths and inspect the final route table statically.
3. Search all endpoint modules for the feature hook and confirm every required handler has the hook, required parameters, and compatible decorator ordering.
4. Trace configuration names from environment files/settings objects into the runtime component; verify defaults, prefixes, and compatibility aliases.
5. Inspect optional imports independently. Ensure one unavailable module cannot silently suppress unrelated routes; distinguish intentional fallback from hidden failure.
6. Compare error-handler registration and payload shape across canonical and legacy factories; align documentation with the active response contract.
7. Check dependency manifests and generated artifacts, then run a final requirement matrix mapping each acceptance criterion to a concrete file and static verification.