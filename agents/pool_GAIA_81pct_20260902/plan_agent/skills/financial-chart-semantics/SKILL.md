---
name: financial-chart-semantics
description: Resolve stock-price questions whose wording combines a named finance site, historical thresholds, and stock-split adjustments.
trigger: When answering a historical security-price threshold question that mentions a charting provider or split adjustment.
---
1. Treat the named provider's displayed series as the primary object, rather than substituting a reconstructed or alternative vendor's historical series.
2. Determine and document whether that provider displays prices adjusted for splits, dividends, neither, or an interface-specific default; inspect its stated methodology, chart labels, downloadable rows, and relevant date range.
3. Parse any split-adjustment qualifier syntactically before calculating: distinguish an instruction not to transform the provider's displayed values from an instruction to use nominal contemporaneous prices.
4. Test both plausible interpretations only to expose ambiguity. Do not select a transformed series merely because it is economically historical; select the interpretation that matches the provider wording and the question's explicit operation.
5. For the selected series, establish the first threshold crossing by checking the entire preceding history and identify whether the site's plotted observation is close, high, or another field.
6. Have an independent reviewer specifically challenge the series-definition interpretation, not just the arithmetic or date. State the candidate answer and strict requested format to the final-answer service.
