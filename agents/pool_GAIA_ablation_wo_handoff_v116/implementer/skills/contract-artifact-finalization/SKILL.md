---
name: contract-artifact-finalization
description: Finalize multi-file changes against exact endpoint, schema, and artifact contracts
trigger: When implementing a feature from tests or a written contract across source and documentation files
---
1. Extract exact required paths, symbols, route literals, response keys, defaults, and validation rules into a checklist before editing.
2. Inspect all existing implementations and preserve behavior unless the contract explicitly changes it; avoid speculative aliases or extra response fields on strict endpoints.
3. Normalize transport artifacts (fences, wrappers) immediately after copying source, then inspect the first and last lines.
4. Implement schema validation and route wiring together, ensuring request fields are actually consumed or deliberately documented as metadata-only.
5. Compile every Python file under the output tree and run import/module smoke tests where dependencies permit.
6. Verify route registration and exact response shape through introspection or lightweight tests; record dependency limitations explicitly.
7. Remove generated caches and enumerate final output files before handoff.
