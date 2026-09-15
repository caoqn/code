---
name: quantitative-source-answer-check
description: Verify concise numerical answers derived from a named source or spreadsheet before submission.
trigger: When asked for a calculated number using tabular source data and a specified equation or convention.
---
1. Restate the requested quantity and identify the exact source row or record.
2. Extract each required input with its column label, units, and any possible alternate interpretations.
3. Write the source-prescribed equation explicitly; do not substitute a familiar proxy formula without confirmation.
4. Substitute values using full precision and independently recompute the arithmetic.
5. Check whether the requested rounding is decimal places, significant figures, or another convention.
6. Compare the result against any candidate answer, resolving discrepancies by revisiting row selection, parameter meanings, and formula orientation.
7. Return only the required concise format after all checks pass.