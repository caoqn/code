---
name: financial-series-semantics-verification
description: Verify questions about historical financial price thresholds by determining the data provider's actual series convention before calculating a first occurrence.
trigger: When asked for a historical price, threshold-crossing date/year, return, or comparison from a named finance website or data provider.
---
1. Parse the request into the instrument, named provider, metric (close/high/intraday), threshold, time unit, and qualifiers such as split or dividend adjustment.
2. Treat the named provider as authoritative for its displayed series. Do not silently substitute a reconstructed or another vendor's data series.
3. Locate the provider's documentation, chart labeling, or downloadable data that states whether historical observations are adjusted for splits, dividends, currency changes, or other corporate actions.
4. Test the apparent reading against a known corporate-action boundary: determine whether the historical values shown by the provider preserve original nominal prices or have been restated. A qualifier such as “without stock split adjustment” may describe the provider's display convention rather than instructing a conversion.
5. Obtain the relevant historical observations directly from the provider if possible. If its interface is dynamic, inspect supported endpoints or a data download; use an independent source only to corroborate, not replace, the provider.
6. Calculate the earliest qualifying calendar period using the requested metric. Check every earlier period explicitly and distinguish an intraday high from a closing-price crossing.
7. Before reporting, perform a semantic cross-check: calculate the result under both plausible adjustment conventions and resolve the ambiguity using the provider evidence. If only a bare year is requested, return only that year.
