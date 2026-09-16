---
name: historical-market-threshold-validation
description: Determine the first year a security crossed a price threshold using a named finance provider's historical data.
trigger: When asked for the first year a stock or asset went above/below a price according to a specific finance site.
---
1. Identify the provider's exact historical-data interface and whether values are split-adjusted, dividend-adjusted, or nominal; verify from provider documentation or UI metadata.
2. Clarify the threshold metric: intraday high, low, closing price, or any traded price, and whether “year” means calendar year of first qualifying observation.
3. Retrieve data spanning the instrument's entire history from the provider when possible; avoid relying solely on secondary narratives.
4. If the provider only exposes adjusted data, reconstruct nominal values using all relevant corporate-action ratios and document the transformation.
5. Compute the earliest qualifying date/year directly, checking boundary observations around the crossing and ensuring no earlier year qualifies.
6. Cross-check with an independent historical source or contemporaneous report, while preserving the provider-specific interpretation.
7. Return only the requested year/value in the strict output format.