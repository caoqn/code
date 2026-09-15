---
name: dynamic-feature-contract-audit
description: Audit dynamically configured validators or plugins across duplicate APIs, injected dependencies, and hidden-test contracts.
trigger: When a feature adds a dynamically loaded strategy, validator, plugin, or repository-backed rule.
---
1. Enumerate every implementation of the strategy interface and every registry/factory that can instantiate it.
2. Trace all constructor callers and entrypoints; identify dependency injection parameters and preserve zero-argument compatibility.
3. Grep tests, generated solution artifacts, docs, and alternate package paths for exact class names, import paths, constructor positional order, and return/error contracts.
4. Distinguish incompatible strategy APIs (exception-raising versus result-returning, dict versus model records) and require explicit adapters rather than silent mixing.
5. Inspect optional dependency modules and singleton initialization; prefer injected fakes and lazy imports to avoid import-time failures.
6. Build a contract matrix for no-history, malformed input, missing configuration, backend failure, unknown registry key, and empty-enabled-list semantics.
7. Send one consolidated report naming canonical and duplicate entrypoints, exact symbols, and required wiring; stop reconnaissance once each requirement has evidence.
8. At final review, verify public exports/importability, all call sites, syntax, test artifact placement, and generated-cache cleanliness.