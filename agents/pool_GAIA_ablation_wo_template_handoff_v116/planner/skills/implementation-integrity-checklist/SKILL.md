---
name: implementation-integrity-checklist
description: Validate feature changes in inconsistent or multi-tree repositories before submission
trigger: When implementing a feature across layered modules or mirrored source trees
---
1. Identify the authoritative package path and avoid copying unrelated scaffold files unless required.
2. Implement the smallest set of modules required by the requested interface; keep schemas, service signatures, and route calls consistent.
3. Search for duplicate definitions and stale imports of renamed classes or schemas.
4. Run syntax compilation over every submitted Python file, not only edited files; remove generated artifacts and detect markdown-fenced source.
5. Verify route uniqueness, HTTP status, payload keys, and service argument ordering with static inspection.
6. Exercise service logic with dependency stubs covering empty input, all success, missing entities, and per-item downstream exceptions.
7. Confirm documentation and mirrored trees (if present) are synchronized, then report any environment dependency limitations explicitly.