---
name: historical-link-path-research
description: Determine shortest hyperlink paths between dated encyclopedia pages and support the result with historical revision evidence
trigger: When asked for a minimum click/link path between pages as of a specified date
---
1. Resolve each requested page title through the site/API, including redirects and disambiguation; record canonical titles.
2. Obtain page revisions nearest but not later than the target date, preferring official revision APIs. Record revision IDs and timestamps.
3. Extract outgoing links from those historical revisions. For a candidate intermediate page, retrieve its revision nearest the date as well and verify the outgoing link to the destination in wikitext or parsed links.
4. Establish the path length by checking for a direct source-to-destination link first. If absent, test one-intermediate candidates (prefer links semantically suggested by page content), then broader breadth-first search as needed.
5. Count clicks explicitly: each traversed hyperlink, including the destination, is one click; do not count the starting page.
6. Report the exact page sequence, click count, revision timestamps/IDs, and direct evidence URLs. Distinguish observed revision content from inference about minimality, and state any API or snapshot limitations.