---
name: quantitative-source-reconciliation
description: Verify numerical answers derived from tables, equations, or scanned documents against authoritative source semantics and precision.
trigger: When a task asks for a computed value from a cited row, equation, paper, spreadsheet, or document.
---
1. Identify the exact authoritative artifact and locate the cited row, equation, and surrounding definitions.
2. Transcribe every operand with its units, scaling, and significant figures; check whether labels refer to transformed, normalized, or raw values.
3. Confirm the requested equation matches the source's final equation, including any substitutions, corrections, or alternate notation.
4. Recompute using high precision and test plausible interpretation variants only when the source is ambiguous; preserve units and scaling through each variant.
5. Compare the computed result with any displayed/rounded source value and determine the mandated rounding or formatting rule.
6. Independently recheck arithmetic (e.g., via a second method) and report the exact concise result required by the native contract.