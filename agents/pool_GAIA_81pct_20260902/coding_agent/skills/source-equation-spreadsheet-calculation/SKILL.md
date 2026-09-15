---
name: source-equation-spreadsheet-calculation
description: Calculate a requested value from spreadsheet inputs when the governing equation is specified in an external primary source.
trigger: When a task asks for a numerical calculation using selected spreadsheet data and an equation from a named paper, translation, standard, or other external source.
---
1. Extract the specified row and columns programmatically, preserving headers, units, cell formulas, and displayed values.
2. Obtain the named source or an authoritative faithful transcription. Locate the exact equation requested by its local label or position; do not substitute a modern or canonical formula merely because the topic resembles it.
3. Transcribe the equation symbol-for-symbol and determine how every source variable maps to the spreadsheet headers. Check whether a listed rate-related quantity is a rate, a limiting rate, a constant, or a transformed quantity.
4. Reproduce the computation with high-precision decimal arithmetic. Show intermediate numerator, denominator, conversions, and rounding mode.
5. Independently assess numerical plausibility by trying only source-supported interpretations. If the source cannot be accessed or the mapping remains ambiguous, report that limitation rather than presenting a guessed calculation as confirmed.
6. Before communicating a final candidate, state both the exact cited equation and the complete variable mapping so another reviewer can check the interpretation.
