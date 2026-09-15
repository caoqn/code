---
name: source-patch-integrity-audit
description: Verify a completed source patch is minimal, clean, and regression-safe before handoff.
trigger: When asked to perform a final integrity or evidence audit of a repository change
---
1. Inspect `git status --short`, `git diff --stat`, and the complete diff to confirm only intended source files changed.
2. Check for accidental test, generated, or unrelated artifacts; ensure the patch remains minimal and repository-native.
3. Run `git diff --check` to detect whitespace and patch formatting issues.
4. Execute the full available test suite (or the narrowest justified suite if time-limited), recording exact pass/fail counts and environment versions.
5. Distinguish direct evidence (commands and outputs) from inferences (likely compatibility or hidden-test behavior) and explicitly note residual risks.
6. Send a concise handoff listing changed paths, key symbols, validation evidence, and unresolved limitations.