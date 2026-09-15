---
name: scientific-equation-data-validation
description: Validate equations, spreadsheet semantics, and source-specific conventions before numerical calculation.
trigger: When asked to calculate a scientific quantity from tabular data and a cited historical or external source.
---
1. Inspect the entire workbook, including hidden sheets, formulas, named ranges, cell comments, and formatting; record exact row/column labels and units.
2. Retrieve the cited source and locate the specific numbered reaction, equation, and surrounding definitions—not merely a modern equation mentioned in the abstract.
3. Map each spreadsheet field to source variables explicitly. Do not equate similarly named terms (e.g., catalytic constant, maximum velocity, rate constant) without textual evidence.
4. Enumerate plausible interpretations if labels are ambiguous, and calculate each candidate. Check which candidate matches source notation, units, and requested reaction number.
5. Verify arithmetic independently (symbolic derivation plus calculator/script), retain full precision, and round only at the end.
6. Perform sensitivity and order-of-magnitude checks; if a result is near a competing interpretation, prioritize source-specific equation and report the ambiguity to the coordinator.
