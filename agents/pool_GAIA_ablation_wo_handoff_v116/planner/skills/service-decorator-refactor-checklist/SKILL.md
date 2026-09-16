---
name: service-decorator-refactor-checklist
description: Reliable workflow for centralizing service exception handling across multiple modules
trigger: When replacing repeated service try/except blocks with a shared decorator
---
1. Read every explicitly named service and the custom exception definitions before editing; inventory exact exception classes and method targets.
2. Verify the requested custom exceptions already exist; if absent, add minimal compatible definitions rather than assuming names or constructors.
3. Implement one canonical decorator with functools.wraps and both sync and async support when services mix styles.
4. Catch only the requested exception classes. If optional dependencies are unavailable, use private sentinel classes, never broad Exception aliases.
5. Log each translated failure, rollback the instance session safely for database errors, and preserve exception chaining with `raise ... from exc`.
6. Refactor methods by removing only matching boilerplate; preserve unrelated domain exception handling and business logic.
7. Grep all target files for decorator imports/usages and stale inline catches; inspect imports for missing symbols and unused exception imports.
8. Compile every submitted Python file, remove generated caches/fences, and run isolated runtime tests for sync/async SQL errors, rollback, validation translation, and propagation of unrelated exceptions.
9. Confirm final changed-file scope against the task before submission and report any environment-only import limitations separately.