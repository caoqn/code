---
name: middleware-contract-validation
description: Checklist for implementing and validating HTTP middleware with exact response contracts
trigger: When adding cross-cutting request middleware such as rate limiting, authentication, tracing, or headers
---
1. Extract exact configuration names, defaults, window semantics, identity key, status code, JSON body, and required headers.
2. Inspect every application factory and router mounting surface; identify canonical and legacy entrypoints.
3. Implement non-HTTP passthrough and preserve request/response streaming semantics.
4. Ensure normal responses receive required headers without overwriting existing headers; ensure rejection responses include the complete contract.
5. Validate malformed configuration deterministically with a safe fallback or explicit startup error.
6. Consider concurrency protection, window reset behavior, identity normalization, and state growth/cleanup.
7. Integrate middleware with intentional ordering relative to compression, CORS, authentication, and observability.
8. Run static compilation, focused behavioral checks for under-limit/at-limit/over-limit and reset cases, and scan output for generated artifacts or formatting fences.
