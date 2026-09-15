---
name: historical-link-distance
description: Determine minimum hyperlink distance between dated versions of encyclopedia pages
trigger: When asked for shortest clickable-link path between pages as of a historical cutoff date
---
1. Resolve the exact page titles and define the cutoff timestamp (usually end-of-day in the requested timezone/UTC assumption).
2. Query the revision API for each page using a timestamp-bounded latest revision; record revision IDs and timestamps as evidence.
3. Extract namespace-0 wikilinks from wikitext, excluding fragments and non-page namespaces, and normalize redirects/title capitalization as needed.
4. First test whether the source directly links to the target; if so the answer is one (or zero when source equals target).
5. For larger distances, perform bidirectional BFS over page links, fetching dated revisions for discovered pages and caching results. Confirm every edge in the resulting path from the corresponding historical wikitext.
6. Establish minimality by exhausting all paths of shorter depth (BFS frontier intersection), and report the path, revision evidence, and final count in the requested format.