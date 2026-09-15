---
name: contract-first-feature-implementation
description: Implement multi-file features against an explicit contract and verify completeness
trigger: When adding a new domain workflow spanning models, schemas, persistence, services, APIs, and authorization
---
1. Read task instructions and inspect context to identify authoritative entities, fields, enum values, required paths, and method signatures.
2. Build a checklist before coding; distinguish required files from optional compatibility shims.
3. Search the workspace for existing implementations of the same concept and decide whether to extend, replace, or remove duplicates.
4. Implement the domain model and transitions first, preserving exact field names/types and validation invariants.
5. Implement repository interfaces and service orchestration with dependency injection; ensure mutation occurs only after dependent operations succeed.
6. Add schemas, routes, and authorization dependencies matching established project patterns.
7. Verify every checklist path exists, inspect exports/imports, and grep callers for signature compatibility.
8. Compile every generated Python file, run dependency-independent lifecycle tests, and report unavailable optional dependencies explicitly.