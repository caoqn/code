---
name: repository-factory-refactor-gate
description: Safely centralize concrete repository construction across a multi-service Python source tree
trigger: When replacing direct data-access repository construction with a factory
---
1. Inventory every concrete repository class definition, import, constructor call, fallback path, singleton, and dependency-injection builder across all service source files; distinguish domain protocols/in-memory test doubles from concrete adapters.
2. Inspect each adapter's real class name and constructor signature before defining factory mappings. Preserve required configuration by forwarding compatible keyword arguments or introducing explicit factory methods for each repository role.
3. Create exactly one canonical factory module with explicit role methods (for example patient, telemetry, device, alert), deterministic backend registration, and lazy imports for optional dependencies.
4. Refactor every production constructor path, including exception fallbacks and module-level singletons, to invoke the factory. Do not leave direct concrete instantiation hidden in error handlers.
5. Keep test files and unrelated configuration untouched; preserve existing behavior and dependency injection seams.
6. Remove malformed source wrappers or generated artifacts if present, then compile every changed source file and import the factory package directly under the intended source path.
7. Grep the complete service tree for direct concrete constructor calls and imports, review remaining matches manually for legitimate class definitions/docstrings, and verify factory aliases plus invalid-backend behavior with a small runtime smoke matrix.
