---
name: profile-work-aggregation
description: Compute date-filtered publication counts and averages from researcher profile APIs or pages
trigger: When a task asks for counts/averages of works across identified researchers or contributors
---
1. Parse the source document and enumerate every named person, distinguishing authors, editors, and contributors.
2. Identify the authoritative profile URL/ID for each person; record profiles missing IDs or unavailable records rather than silently excluding them.
3. Read machine-readable profile data when available. Determine whether records are grouped by DOI/title or represented as individual summaries, and use the unit implied by the question.
4. Extract publication year robustly, handling missing, partial, and nonstandard dates; apply the exact cutoff (for example, <2020 means years through 2019).
5. Compute per-person counts, total, and arithmetic mean. Also calculate alternate interpretations (e.g., grouped versus raw records, subset versus full universe) when ambiguity exists.
6. Reconcile results with any visible profile totals or independent search snippets, explain discrepancies, and report the selected interpretation with concise evidence and arithmetic.