---
name: scientific-source-equation-input-verification
description: Verify a quantitative answer that combines a named historical or scientific source equation with values in a supplied table.
trigger: When a prompt asks to calculate a number using a specific equation from a cited scientific source and spreadsheet or document inputs.
---
1. Extract the source document's exact requested equation, including all final terms, definitions, signs, and any stated unit or transformation conventions. Do not substitute a familiar textbook equation merely because variable labels look similar.
2. Obtain the cited primary text or its official supplement. If access is blocked, use an independent archival copy or structured repository endpoint; report inability to see the equation rather than treating a secondary discussion as proof.
3. Inspect the input document structurally, enumerate headers and the selected row, and map each equation symbol to a column only where the source definitions support that mapping.
4. Check whether the equation needs initial values, a transformed observable, product/inhibition terms, logarithms, or a time interval; distinguish rate constants from maximum velocities and catalytic constants.
5. Compute the result at full precision, then test only source-supported alternative parameter mappings or equation forms. Use dimensional analysis and limiting behavior to reject implausible mappings.
6. Independently reproduce the selected calculation and apply the requested rounding only at the end.
7. Report the exact equation, row values, intermediate precision, alternative interpretations considered, source URL/location, and the required final output granularity to the lead.
