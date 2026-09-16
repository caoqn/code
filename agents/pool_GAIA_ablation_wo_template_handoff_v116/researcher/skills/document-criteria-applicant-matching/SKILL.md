---
name: document-criteria-applicant-matching
description: Extract qualification criteria from attached job documents and identify records satisfying all or all-but-one requirements
trigger: When a task asks to count or list applicants against requirements stated in a PDF/document and tabular applicant data
---
1. Inspect the attachment archive and identify all relevant documents and tables.
2. Extract the complete job description text, preserving each qualification bullet and its thresholds, allowed categories, and missing-value semantics.
3. Load applicant tables with headers intact; normalize obvious formatting (whitespace, case, missing cells) without altering substantive values.
4. Translate each qualification into an explicit boolean predicate, documenting inclusive thresholds (e.g., >=) and combined conditions (e.g., degree field plus level).
5. Apply every predicate row-wise and sum satisfied criteria; distinguish a missing qualification from an invalid or unknown value according to the source wording.
6. Filter for the requested match class (such as exactly one failed criterion), then independently inspect each selected row and record the failed predicate for auditability.
7. Report the count and, when useful, names/failed criteria, citing the source files and noting any interpretation assumptions. Verify the final count by a second independent aggregation or manual spot-check.