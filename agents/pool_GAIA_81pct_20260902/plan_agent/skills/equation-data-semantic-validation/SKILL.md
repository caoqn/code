---
name: equation-data-semantic-validation
description: Validate quantitative answers that combine an attached table with an equation from an external paper, avoiding semantic or parameter misinterpretation.
trigger: When a question asks to calculate a value from spreadsheet inputs using a named paper's equation.
---
1. Inspect the attachment completely, including all sheets, hidden columns, notes, formulas, and exact row labels for the requested record.
2. Retrieve the primary source and transcribe the exact requested equation, preserving variable definitions and any corrections, approximations, or reciprocal forms; do not substitute a modern textbook equation without proving equivalence.
3. Map every equation variable to a spreadsheet field by definition, checking whether a field is a rate constant, concentration, maximum velocity, enzyme amount, or fitted parameter.
4. Test multiple plausible mappings if terminology is ambiguous, and compare outputs against expected physical scale and source context.
5. Recalculate with high precision, then round only at the final step as requested.
6. Have an independent verifier inspect both the equation transcription and the data mapping; disagreements require returning to the primary source rather than majority voting.
7. In the final handoff, include exact row values, equation text, variable mapping, arithmetic, and strict output format.