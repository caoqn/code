---
name: feature-artifact-integrity
description: Checklist for implementing cross-cutting features in incomplete or duplicated repositories
trigger: When adding infrastructure that touches routers, configuration, dependencies, and documentation
---
1. Inventory canonical application factories and every alternate router registration path before editing.
2. Record exact runtime contracts (environment variable names, response envelope, headers, route prefixes) and use shared constants rather than literals.
3. Inspect imports transitively: identify optional or missing modules and isolate failures per component so one unavailable feature cannot suppress unrelated routes.
4. Preserve existing documentation by patching targeted sections instead of replacing whole files.
5. Ensure framework decorators are ordered according to the framework's registration semantics and preserve handler signatures.
6. Add or update dependency manifests and configuration examples consistently with the names actually read at runtime.
7. Run static compilation and inspect output for accidental markdown fences, malformed expressions, duplicate middleware, and generated cache artifacts.
8. Perform one final contract review covering route reachability, error payloads, limits, fallback behavior, and source cleanliness.