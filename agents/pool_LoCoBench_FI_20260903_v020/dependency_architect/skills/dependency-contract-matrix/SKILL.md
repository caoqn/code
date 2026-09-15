---
name: dependency-contract-matrix
description: Build a cross-module implementation map for features spanning APIs, services, persistence, and gateways.
trigger: When asked to trace dependencies or assess architecture for a requested change.
---
1. Identify the requested feature's public surfaces (REST paths, GraphQL fields, events, CLI or app entrypoints).
2. Locate canonical implementations and all one-hop callers/importers with targeted searches.
3. Record a contract matrix: exact symbol signatures, parameter names/types, return models, serialization names, and error semantics.
4. Compare parallel representations (domain DTOs, API schemas, ORM models, tests) and explicitly flag naming/type mismatches.
5. Verify application wiring: factory/global app, router inclusion, startup dependencies, configuration URLs, and gateway forwarding.
6. Distinguish existing production paths from stale/duplicate test contracts; report which entrypoint hidden tests are likely to import.
7. Send one consolidated report early with required edits, evidence snippets, and compatibility risks; stop once all direct interfaces are covered.