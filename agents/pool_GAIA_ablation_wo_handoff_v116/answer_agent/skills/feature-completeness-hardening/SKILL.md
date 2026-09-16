---
name: feature-completeness-hardening
description: Strengthen a minimally implemented feature by systematically covering robustness, comprehensiveness, and API elegance before final review
trigger: When evaluation or review indicates low robustness, incomplete artifact coverage, or a feature implemented only on the happy path
---
1. Enumerate every explicit requirement and infer adjacent contract surfaces: validation, defaults, errors, serialization, docs, exports, compatibility aliases, and tests.
2. Build a requirement-to-symbol matrix listing each source artifact, public callable/route, caller, and expected behavior for success, malformed input, unknown identifiers, empty values, and boundary numbers.
3. Inspect existing abstractions and analogous implementations; extend canonical paths rather than adding isolated shortcuts or duplicate registries.
4. Add deterministic input validation with clear exception types/messages and enforce numeric/date/range boundaries before business logic.
5. Harden optional-dependency and initialization branches with graceful fallbacks, preserving public interfaces and avoiding leaked internal exceptions or sensitive data.
6. Add focused tests or static contract checks for positive, negative, and boundary cases, plus import/export compatibility and exact response schemas.
7. Review naming, aliases, route structure, and documentation for consistency; remove placeholders, dead code, and accidental formatting artifacts.
8. Run complete-tree compilation and the evaluator's explicit suite, then classify any failures as implementation defects versus environment limitations.
9. Before finalizing, re-open every changed file and reconcile evidence against the matrix; report residual risks explicitly and avoid claiming unverified runtime behavior.