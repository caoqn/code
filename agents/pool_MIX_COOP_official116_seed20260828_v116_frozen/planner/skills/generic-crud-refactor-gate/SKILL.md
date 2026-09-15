---
name: generic-crud-refactor-gate
description: Checklist for introducing a generic CRUD service and migrating concrete services safely
trigger: When consolidating duplicated CRUD logic across service classes
---
1. Inventory every concrete service, model, schema, repository, dependency provider, and package initializer; identify the authoritative source tree and any duplicate layouts.
2. Capture the exact required public method signatures, sync/async expectations, constructor semantics, and type parameters before editing.
3. Implement one canonical generic base class with TypeVars and explicit model/session ownership; support Pydantic v1/v2 schema dumping and preserve transaction/error semantics.
4. Refactor each concrete service to inherit the base, call `super().__init__` with its model, and retain all domain-specific methods/side effects; remove only duplicated CRUD code.
5. Trace all imports and callers, including dependency injection registries and factories; ensure package paths and exports remain valid.
6. Run compile checks plus direct fake-session behavior tests for every CRUD method (create, read, list bounds, update partial fields, remove missing/existing), then inspect changed-file scope and generated artifacts.
7. Report optional-dependency import limitations separately from implementation defects and do not claim full runtime validation when imports cannot execute.