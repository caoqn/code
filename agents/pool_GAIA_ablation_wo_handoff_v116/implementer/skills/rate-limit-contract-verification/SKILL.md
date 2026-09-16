---
name: rate-limit-contract-verification
description: Implement and verify configurable request limiting across middleware, settings, and documentation.
trigger: When adding or modifying request-rate limiting behavior in a web service.
---
1. Extract the exact public environment variable names, defaults, identity precedence, window algorithm, status code, response body, and headers from requirements/tests.
2. Implement one canonical parser for environment values that handles malformed, zero, negative, and whitespace inputs deterministically; ensure settings-layer parsing cannot reject values before middleware fallback.
3. Wire settings to middleware using the same parser and verify direct middleware construction honors environment overrides when explicit arguments are omitted.
4. Define identity precedence explicitly and avoid trusting spoofable forwarding headers unless the deployment contract says otherwise.
5. Apply limit, remaining, and reset headers to every response path, including throttled responses; add retry metadata only where required.
6. Export the middleware and compatibility aliases from package initializers, then grep all callers and imports.
7. Add or update documentation with a titled section covering algorithm, defaults, identity, headers, 429 body, and configuration.
8. Run full-tree compilation, dependency-light parser edge checks, and a focused middleware response test; remove generated caches before handoff.
