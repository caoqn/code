---
name: security-robustness-artifact-review
description: Review delegated code changes for security, robustness, maintainability, and artifact correctness before endorsing completion
trigger: When teammates report a cross-cutting implementation complete and tests are partial or dependencies unavailable
---
1. Enumerate changed files and map each requirement to symbols, routes, exports, and callers.
2. Read critical source directly, especially authentication, rate limiting, persistence, and input-validation paths.
3. Trace untrusted inputs through key construction, database/API calls, exceptions, and response headers; check for injection, leakage, and unbounded values.
4. Verify fallback behavior when optional dependencies fail, including initialization and error paths.
5. Compile every source file in the submitted tree and scan for placeholders or formatting fences.
6. Run focused contract tests or static import/signature checks; distinguish environment failures from implementation defects.
7. Report concrete evidence and residual unverified risks rather than relying on aggregate teammate claims.