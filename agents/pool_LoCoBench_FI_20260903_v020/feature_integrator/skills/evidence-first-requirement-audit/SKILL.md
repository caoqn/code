---
name: evidence-first-requirement-audit
description: Build a complete, test-oriented integration map before advising implementation in multi-file repositories.
trigger: When a feature spans multiple modules or the task wording is ambiguous and hidden tests are likely.
---
1. Extract every explicit requirement and acceptance detail from the task statement; do not infer a substitute requirement.
2. Enumerate candidate canonical and duplicate entrypoints, then grep symbols, constructors, serializers, event payloads, exports, and tests for each requirement.
3. For each requirement, record exact source path/symbol, current behavior, intended delta, compatibility constraints, and malformed-input/error semantics.
4. Inspect existing tests and analogous implementations before proposing new APIs. Mark inferred behavior separately from repository evidence.
5. Produce one prioritized contract: must-have changes first, compatibility/edge cases second, optional enhancements last.
6. Include a verification matrix covering syntax, imports, serialization shape, duplicate/invalid input, route or event registration, optional dependencies, and artifact placement.
7. Stop reconnaissance once every requirement has concrete evidence; send the implementer one consolidated report rather than iterative speculation.