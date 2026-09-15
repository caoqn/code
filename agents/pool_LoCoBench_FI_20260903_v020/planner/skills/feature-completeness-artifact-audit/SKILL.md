---
name: feature-completeness-artifact-audit
description: Ensure implementation tasks satisfy every requested artifact, including tests and documentation, while preserving existing code.
trigger: When a feature request names multiple files or explicitly requires tests/config/docs.
---
1. Parse requirements into a checklist of behavior and explicit artifact paths.
2. Inspect the source tree to identify canonical implementation and existing test conventions.
3. Dispatch implementation and evidence work with the full checklist, explicitly requiring every named artifact (including new tests).
4. After implementation, list solution files and compare against the checklist; missing named files are blockers even if hidden tests may pass.
5. Independently inspect exact public fields, configuration defaults, exception boundaries, continuation behavior, and persistence format.
6. Run static compilation and remove generated caches or accidental markdown fences.
7. Only finalize after a verifier confirms both behavior and artifact completeness.