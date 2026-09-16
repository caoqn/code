---
name: artifact-integration-smoke
description: Verify newly generated modules integrate with existing discovery, dependency injection, and async/sync boundaries.
trigger: After implementing a cross-module feature or adding endpoint/service artifacts
---
1. Identify the host module's discovery convention (module-level symbol, registration function, package export, or route prefix).
2. Compare the new artifact's public symbols and signatures against that convention and all expected import paths.
3. Search every caller and consumer for assumptions about coroutine status, exception classes, response models, and return types.
4. Run import and compile smoke tests with the intended package root, then instantiate the smallest dependency-injected object available.
5. Exercise both synchronous and asynchronous collaborator variants when the feature accepts external services.
6. Verify generated artifacts contain no wrappers, stale caches, or missing package initializers, and report unresolved integration gaps explicitly.