---
name: cross-file-refactor-completeness
description: Checklist for safely refactoring duplicated adapters across a source tree
trigger: When introducing a shared abstraction and migrating multiple concrete implementations
---
1. Inventory every target implementation, public method, constructor signature, context-manager/close method, and factory/DI call site.
2. Record each method's transport semantics (HTTP verb, path, payload, expected statuses, error translation, retries) before editing.
3. Define the shared abstraction with compatibility aliases and explicit configuration fields needed by all callers.
4. Migrate every implementation in scope, preserving public signatures and domain-level return/error behavior; avoid replacing rich models with placeholders unless explicitly allowed.
5. Update dependency injection to derive registrations dynamically from authoritative configuration, while retaining explicit accessors needed by existing callers.
6. Add focused fakes that exercise URL construction, headers, timeout, retries, status handling, empty responses, and malformed payloads.
7. Run compile/import checks, relevant tests, and grep for forbidden low-level imports or direct transport construction in adapters.
8. Review the final file inventory and remove generated artifacts before submission.