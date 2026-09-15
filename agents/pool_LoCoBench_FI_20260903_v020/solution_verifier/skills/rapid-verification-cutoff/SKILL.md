---
name: rapid-verification-cutoff
description: Time-boxed validation workflow that minimizes exploration and communication overhead while preserving contract coverage.
trigger: When reviewing generated artifacts under strict wall-clock or message budgets.
---
1. Extract exact required paths, endpoints, payload fields, statuses, and artifact names from the task before reading files.
2. Dispatch any needed review requests immediately with the concise checklist and a fixed cutoff.
3. Enumerate solution outputs once; inspect only canonical entrypoints, changed modules, and one representative test or documentation artifact.
4. Perform at most one static syntax or import check; avoid runtime execution when prohibited or likely to generate artifacts.
5. Consolidate blocking and non-blocking findings into one prioritized report per recipient.
6. Do not poll repeatedly or reopen already verified files unless new evidence of a defect appears.
7. Stop at the cutoff and submit evidence, even if optional enhancements remain unreviewed.