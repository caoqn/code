---
name: source-semantic-time-series-validation
description: Determine threshold-crossing years from a named financial data source while respecting adjustment, split, and chart semantics
trigger: When asked for the first year an asset exceeded a price threshold according to a specific website or API
---
1. Read the question literally and identify the exact source, instrument, threshold, date granularity, and qualifiers (e.g., unadjusted, adjusted, close, high).
2. Inspect the named source directly, including chart metadata, downloadable data, API parameters, and explanatory notes. Do not assume that “unadjusted” has its ordinary meaning.
3. Determine whether historical values are back-adjusted for splits, dividends, currency, or denomination changes. Confirm by checking known split dates and prices around those dates.
4. Extract or reproduce the complete candidate-year series from the source. Use the specified metric (daily high vs. close vs. annual value) and timezone/calendar conventions.
5. Find the earliest year satisfying the threshold, checking all earlier years rather than relying on a later news report or a single peak.
6. Cross-check with an independent authoritative source only after obtaining the source-specific result; explain discrepancies as adjustment or metric differences.
7. Report the year and concise evidence, clearly distinguishing directly observed source data from inference and external corroboration.