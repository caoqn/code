---
name: requirements-first-artifact-audit
description: Build a complete requirements-to-artifacts and tests matrix before independently verifying generated repository changes.
trigger: When reviewing a generated or replacement implementation whose contract is supplied through documentation, context files, or hidden/evaluator tests.
---
1. Inventory every supplied context artifact and extract explicit requirements, public names, signatures, data fields, paths, and integration points.
2. Enumerate the evaluator-visible output tree and map each requirement to an exact file and symbol; flag duplicate source trees or files outside the likely import path.
3. Locate all available tests, fixtures, and caller references before accepting an implementation; derive positive, negative, boundary, and persistence cases from them.
4. Run the narrowest relevant tests plus full per-file compilation, then perform imports using the same path/layout the evaluator will use.
5. Exercise each public API and integration boundary end-to-end, including absent optional dependencies and malformed or empty inputs.
6. Report requirement coverage, concrete command outcomes, environmental limitations, and unresolved concerns; never treat compilation or one smoke test as completeness evidence.