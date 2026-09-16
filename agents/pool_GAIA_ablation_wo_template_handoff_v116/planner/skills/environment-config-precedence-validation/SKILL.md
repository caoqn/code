---
name: environment-config-precedence-validation
description: Validate configuration precedence and environment-derived defaults without breaking absent-config behavior
trigger: When fixing bugs involving config files, environment variables, or CI autodetection
---
1. Inventory every configuration source (explicit arguments, config file, generic environment, provider-specific environment, CI autodetection) and record the current assignment order.
2. Build a matrix covering config present/absent and each relevant credential combination; include expected CI service labels, not just the reported override case.
3. Reproduce the reported failure on baseline, then run all matrix rows against the candidate fix.
4. Ensure defaults derived from environment are computed after all environment variables are loaded, while explicit user settings retain their documented precedence.
5. Run the complete relevant test module and inspect hidden-like boundary cases where a value is populated indirectly (for example, token loading changing service classification).
6. Confirm the final diff is limited to source files and preserves unrelated configuration semantics.