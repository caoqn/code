---
name: runtime-compatibility-branch-audit
description: Verify dependency and interpreter compatibility changes across version/platform module-selection branches and evaluator harnesses
trigger: When fixing deprecations, compatibility warnings, or runtime-version-specific imports
---
1. Identify every branch that selects an implementation based on dependency version, interpreter version, platform, or environment flags.
2. Search all imported modules and callers for each branch; confirm the edited source is the one loaded under normal and simulated target runtimes.
3. Reproduce the reported failure with the project’s explicit fail-to-pass test or subprocess harness before changing code.
4. Exercise each branch directly, including the target-version branch that may be unavailable on the host (for example via monkeypatching, subprocess flags, or static import checks).
5. Verify both positive behavior and expected warnings/errors, using warnings-as-errors where compatibility warnings are part of the requirement.
6. Run focused tests plus the full suite, then inspect subprocess stdout/stderr and loaded-module identity to catch wrong-module selection.
7. Report any untested branch explicitly; do not claim completion from host-runtime tests alone.