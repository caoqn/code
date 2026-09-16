---
name: quantity-copy-compatibility-validation
description: Safely migrate code using third-party quantity constructors when copy semantics or keyword support changes across versions
trigger: When a dependency deprecates/removes a constructor keyword affecting array ownership, dtype, or unit conversion
---
1. Reproduce the reported failure against the installed dependency and inspect the dependency constructor implementation/signature to determine whether the keyword is rejected, ignored, or behaviorally changed.
2. Inventory every quantity construction and every caller exposing copy, dtype, units, rescale, slicing, or mutation behavior; include helper functions and inherited/indirect paths.
3. Build a behavior matrix before editing: copy=True with quantity and ndarray inputs, copy=False with both, omitted/default copy, dtype conversion, unit rescaling, and sliced views. Record whether source and result should share storage based on existing tests/contracts.
4. Implement the smallest compatibility adapter that preserves the matrix across old and new dependency versions. Avoid unconditional copying unless the established contract requires it; distinguish constructor ownership from later view/slice semantics.
5. Run the complete nearest test modules, not only tests named for the reported bug, and directly mutate both source and result for each matrix row. Investigate every regression, especially defaults and slice aliasing, before finalizing.
6. Verify dependency metadata permits the target versions, compile all changed modules, inspect the final diff for test modifications or generated artifacts, and report any unverified behavior row as a blocker.