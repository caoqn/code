---
name: independent-artifact-verification
description: Verify generated code artifacts beyond syntax compilation, including runtime imports, cross-file references, and focused behavioral checks.
trigger: When reviewing an implementation before final submission or validating a multi-file code change
---
1. Enumerate all files under the required output directory and inspect the changed modules plus their import boundaries.
2. Run a syntax/bytecode compilation check, but do not treat compilation as sufficient.
3. Execute minimal runtime imports for each public module; record missing external dependencies separately from implementation failures.
4. Exercise representative pure functions and class constructors, especially dataclasses with inheritance, registries/factories, validators, and serialization boundaries.
5. Grep for all changed function/class names and validation helpers to identify stale callers, duplicate implementations, or inconsistent semantics across files.
6. Check edge cases implied by requirements (malformed input, boundary values, duplicate registration, negative/zero values) with focused commands.
7. Report concrete evidence, environmental limitations, latent concerns, and whether the artifact satisfies the task; never silently fix a failure while calling it verified.