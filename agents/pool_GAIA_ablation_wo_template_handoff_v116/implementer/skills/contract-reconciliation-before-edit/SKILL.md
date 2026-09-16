---
name: contract-reconciliation-before-edit
description: Reconcile task requirements, context architecture, and evaluator-facing symbols before implementing multi-file features.
trigger: When requirements may have multiple interpretations or existing source is transport-wrapped/incomplete.
---
1. Extract an explicit matrix of required paths, public symbols, constructor defaults, route literals, payload fields, and response fields from task messages and available tests.
2. Inspect all authoritative neighboring modules and identify whether source files are complete, fenced, duplicated, or intentionally incompatible.
3. Confirm ambiguous domain terminology with the coordinator before writing code; do not implement a plausible but unconfirmed interpretation.
4. Preserve existing APIs by extending rather than replacing implementations; if source is unusable, create a compatibility layer that retains expected symbols and behavior.
5. Implement schema, service, strategy, and endpoint changes as one dependency chain, wiring configuration defaults consistently across every layer.
6. Verify exact runtime signatures with imports/introspection, test both sync and async dependency variants, and run full-tree compilation.
7. Re-read every changed file after delegated/concurrent edits, grep required symbols and literals, remove caches, and report dependency limitations explicitly.