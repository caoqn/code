---
name: cross-layer-completion-gate
description: Verify multi-file features through real imports, dependency injection, and endpoint wiring before finalizing
trigger: When a feature spans models, services, repositories, routes, factories, or package exports
---
1. Enumerate every required artifact and public symbol from the specification.
2. Inspect existing package layout and import conventions before accepting new modules.
3. Trace the runtime path from top-level application/factory through router, service, repository, and response model; verify the concrete objects used at runtime are the same ones tests or dependency overrides target.
4. Check package and module exports in both canonical and compatibility import forms.
5. Exercise success, missing-resource, malformed-input, empty, and boundary cases with controlled dependencies when runtime libraries are unavailable.
6. Compile the complete submission tree and remove generated caches/placeholders.
7. Run the exact evaluator tests; if dependencies are missing, use stubs/static inspection but mark runtime acceptance unverified.
8. Block unconditional completion when import paths or dependency-injection wiring diverge from the expected execution path; require remediation or clearly label the result provisional.