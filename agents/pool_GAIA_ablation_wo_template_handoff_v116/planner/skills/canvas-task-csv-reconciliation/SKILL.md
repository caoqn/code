---
name: canvas-task-csv-reconciliation
description: Extract unfinished Canvas assignments/quizzes into fixed CSV artifacts with authoritative filtering, ordering, and verification.
trigger: When a task asks to populate local assignment/quiz CSVs from Canvas data and submission status.
---
1. Inventory the evaluator-visible CSV files and read exact headers, sample rows, and current line counts; treat sample rows as templates until authoritative data is obtained.
2. Establish identity/session and enumerate the complete enrolled-course population. For each course, collect assignments, quizzes, announcements, and per-user submission/attempt status.
3. Resolve exclusions explicitly: remove submitted/completed items and any teacher-announced content that does not require submission; document exemption rules separately from ordinary pending work.
4. Build normalized records with stable course code/title keys, deduplicate, and sort by deadline ascending, then course code lexicographically for equal deadlines.
5. Write only the required existing filenames at the evaluator-visible path, preserving each exact header and CSV encoding. Do not assume a similarly named reference directory is submitted.
6. Re-read files with csv.DictReader, count data rows (excluding header/blank lines), validate every required field, ordering, duplicate keys, and row-level equality against authoritative source records.
7. Record source coverage, selection counts, artifact paths, readback evidence, and zero missing/duplicate/extra/unverified counts in the native contract and manifest. Set ready only after all checks pass.
