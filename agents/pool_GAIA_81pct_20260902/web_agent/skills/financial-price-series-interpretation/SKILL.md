---
name: financial-price-series-interpretation
description: Determine a price-threshold date/year using the exact adjustment convention intended by a named financial-data source.
trigger: When a question asks when a security, fund, currency, or index first crossed a price threshold and mentions stock splits, dividends, adjusted prices, or a named finance site.
---
1. Parse the requested convention before collecting numbers. Separate: (a) values as displayed by the named source, (b) split-adjusted historical values, (c) raw contemporaneous/nominal values, and (d) total-return or dividend-adjusted values.
2. Treat wording such as "according to <source>" as a requirement to use that source's displayed series unless the question explicitly says to reconstruct another series. Do not silently reverse or apply split factors.
3. Find primary documentation, labels, or UI text establishing whether that source's history/chart is adjusted. If the source cannot be fetched statically, use an accessible official endpoint, browser-visible tooltip, export, or cached source representation; report the limitation rather than substituting a different provider as decisive evidence.
4. Define the crossing metric: for chart series use the displayed point (normally close); for an explicit price table distinguish Close from High. If wording merely says "went above," calculate both only after identifying which metric the named source actually provides.
5. Identify the first observation strictly greater than the threshold, then inspect the immediately prior observation (and prior calendar year where relevant) to establish it is truly first.
6. Report the calendar year in the requested format, plus a short statement of the adjustment convention and metric. Include direct URLs and exact source labels/quotes. Do not present results from a transformed series as the source's unadjusted result.
