---
name: pdf-spreadsheet-qualification-count
description: Determine how many applicants meet all but one qualification from a job-listing PDF and applicant spreadsheet.
trigger: When a task asks to count applicants missing exactly one qualification across an attached job listing and tabular applicant data.
---
1. Extract the complete qualification list from the PDF, preserving conjunctions and thresholds (for example, degree field plus degree level may form one compound criterion).
2. Load every applicant row from the spreadsheet and normalize categorical values, missing cells, and yes/no fields.
3. Translate each qualification into an explicit boolean predicate; document any interpretation such as acceptable degree fields, minimum experience, or what counts as a second language.
4. Evaluate all predicates for every applicant and count failures per row.
5. Select rows with exactly one failed predicate, and independently recompute the count using a second method or agent.
6. Before answering, verify the number of spreadsheet rows, the qualification count, and the failure-count distribution; provide only the requested concise answer format.