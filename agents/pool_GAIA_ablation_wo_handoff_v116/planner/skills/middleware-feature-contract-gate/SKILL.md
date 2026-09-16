---
name: middleware-feature-contract-gate
description: Implement and verify configurable HTTP middleware features while preserving application integration and exact response contracts.
trigger: When adding middleware that tracks request state, derives client identity, or modifies responses.
---
1. Inventory the authoritative application factory, middleware registration order, configuration mechanism, and documentation path before editing.
2. Convert requirements into an exact matrix covering environment variables, defaults, precedence, identity derivation, state transitions, response status/body, and headers.
3. Implement state updates atomically for concurrent requests; define window rollover and behavior at the limit explicitly.
4. Preserve exact public response contracts, including error JSON text and whether headers apply to success, errors, or both.
5. Test configuration-present, absent, malformed, zero, and negative values; test each identity source and ensure independent buckets.
6. Exercise first, boundary, over-limit, and post-reset requests with a deterministic clock or stub; verify remaining and reset calculations.
7. Audit middleware exports, registration uniqueness/order, imports under available dependencies, and documentation headings/content.
8. Compile all submitted files, remove generated artifacts, and directly verify evaluator-visible paths and exact symbols before finalizing.