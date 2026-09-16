---
name: compatibility-fixture-audit
description: Audit compatibility changes against evaluator fixtures using alternate configuration aliases and mode-specific constructor inputs
trigger: When a dependency/API compatibility patch modifies initialization or validation across legacy and modern branches
---
1. Locate the exact fail-to-pass evaluator tests and enumerate every fixture constructor shape.
2. Build a matrix of accepted aliases (for example deployment, engine, model), explicit mode/type flags, and expected validation behavior.
3. Reproduce each fixture before and after the change under simulated dependency versions, using stubs when the real dependency is unavailable.
4. Trace validation order: ensure aliases are normalized before assertions, and only reject configurations that truly lack a required value.
5. Exercise modern and legacy branches separately, including explicit request-type overrides and alternative endpoint/config names.
6. Run the exact evaluator suite, then the full regression suite; treat any fail-to-pass failure as blocking regardless of pass-to-pass results.
7. Report untested network or cache semantics separately from initialization correctness.