---
name: final-integration-contract-audit
description: Final static audit for cross-file feature integrations, focusing on exports, route wiring, persistence, and edge semantics.
trigger: When a multi-file feature implementation is reported complete and requires an independent integration review.
---
1. Enumerate every changed file and map each requirement to a concrete symbol, route, serializer, and persistence method.
2. Identify the canonical factory/runtime entrypoint and inspect route registration order and prefixes, including duplicate or legacy entrypoints.
3. Verify all newly introduced public symbols are importable from their documented modules and included in `__all__` where the project uses export control; check definitions appended after `__all__`.
4. Trace dependency injection and optional-import fallbacks independently so one missing module cannot cause NameError or suppress unrelated functionality.
5. Check exact response/model field names, status codes, path parameters, and exception-to-HTTP mappings against requirements.
6. Audit persistence round-trips: deterministic paths, missing-resource behavior, JSON-safe conversion, overwrite/idempotence, and empty/malformed input.
7. Run only permitted static checks (syntax/compile and source artifact scan); report blockers separately from caveats in one consolidated message before implementation cutoff.