---
name: comprehensive-repository-refactor
description: Safely refactor a family of repositories onto a shared client while preserving contracts
trigger: When replacing transport implementations across multiple repository modules
---
1. Inventory all target modules and extract public classes, constructors, methods, DTOs, and exceptions into a checklist.
2. Inspect tests and callers for exact signatures, return shapes, status handling, and lifecycle methods.
3. Implement the shared client abstraction first, including transport injection, retries, timeout behavior, and explicit error classes.
4. Refactor each repository incrementally, preserving compatibility aliases and constructor forms while removing direct transport imports.
5. Build the DI/factory layer from configuration, validating every configured service and exposing deterministic lookup APIs.
6. Run import smoke tests and introspection for every public symbol, then compile the complete output tree.
7. Verify no direct transport imports remain, no placeholders or fenced code exist, and remove generated caches before handoff.
