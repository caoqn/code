---
name: feature-artifact-integrity-gate
description: Safely implement and verify multi-file features in a scaffolded repository without losing existing functionality
trigger: When adding a feature across utility, domain, and integration modules
---
1. Inventory authoritative source files and package import paths before editing; identify duplicate or compatibility trees.
2. Preserve existing files by applying targeted edits or patches rather than replacing whole modules from context copies.
3. Implement the new utility and domain class with the exact requested signature, including dependency injection and edge-case behavior.
4. Trace every integration factory/registry caller and update constructor arguments consistently.
5. Add focused tests or smoke scripts that monkeypatch the documented utility at the import path used by the implementation.
6. Run compile checks and direct runtime checks for valid, invalid, insufficient-history, zero-variance, and missing-resource cases.
7. Verify artifact integrity: no markdown fences, generated caches, truncated modules, undefined globals, or stale constructor calls; inspect diff/file inventory before final response.