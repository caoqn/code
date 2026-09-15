---
name: cross-cutting-contract-verification
description: Verify cross-cutting middleware, decorators, configuration, and error contracts across a generated software submission.
trigger: When reviewing a feature that modifies routing, middleware, decorators, configuration, or global error handling.
---
1. Enumerate every required output artifact and compare exact paths and names against the task contract.
2. Identify the canonical application entrypoint and inspect all router-registration and middleware wiring paths, including fallback or exception-suppression branches.
3. Grep all endpoint handlers for the new decorator/dependency and verify each has the framework-required request parameter and correct decorator ordering.
4. Trace configuration values from environment/file definitions through import-time initialization and runtime settings; check naming, precedence, and whether files are actually loaded.
5. Inspect success and failure paths in instrumentation/decorators: initialize status variables before `try`, ensure exception responses are counted, and avoid unbound locals or masking the original error.
6. Compare each error response status, JSON shape, and headers (especially retry/correlation headers) against documentation and requirements.
7. Check imports for every mounted router; do not approve broad ImportError suppression that silently removes required routes unless this is explicitly intended.
8. Run one static compile/import-oriented check where permitted, then verify the check did not create forbidden artifacts. Report blocking issues in one prioritized checklist.