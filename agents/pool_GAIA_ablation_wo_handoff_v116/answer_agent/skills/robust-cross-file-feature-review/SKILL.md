---
name: robust-cross-file-feature-review
description: Systematically harden and verify a feature spanning middleware, application wiring, exports, and documentation.
trigger: When a change introduces a cross-cutting service or middleware feature across multiple source files.
---
1. Extract every requirement into a matrix of concrete symbols, configuration keys, callers, exports, persisted or serialized outputs, and documentation locations.
2. Inspect the complete existing call path from application construction through middleware/service invocation; verify the new component is actually mounted exactly once and receives the intended parameters.
3. Validate configuration parsing for absent, malformed, zero, negative, extreme, and alias inputs; confirm deterministic defaults and that runtime values match documented behavior.
4. Exercise identities, routing or partition boundaries, success responses, rejection responses, reset behavior, and concurrent/repeated calls using controlled dependencies.
5. Check all public imports and compatibility aliases, then compile the entire submission tree and scan source artifacts for placeholders or formatting fences.
6. Run the evaluator's exact fail-to-pass tests when available; otherwise record dependency limitations and use static checks or stubs for unavailable integrations.
7. Before finalizing, reconcile evidence against every matrix row and report any unverified path explicitly rather than inferring from aggregate smoke tests.