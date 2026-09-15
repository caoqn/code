---
name: historical-wikipedia-link-distance-verification
description: Verify a claimed shortest path in English Wikipedia using the revisions that existed at a stated historical cutoff.
trigger: When a task asks for the number of clickable Wikipedia links between articles as of a past date.
---
1. Specify the cutoff precisely, the source and target titles, and link-count convention: count hyperlink traversals, not pages visited.
2. Use the MediaWiki Action API to retrieve the latest revision at or before the cutoff for the source, target, and each proposed intermediate page: set revision start just after the cutoff, use older direction, and request revision id, timestamp, and wikitext.
3. Extract source-page internal main-namespace links from historical wikitext. Test for a direct target link first; if present, the answer is one link.
4. For each plausible source neighbor, retrieve its same-cutoff revision and inspect its full wikitext for a target link. Prefer automated exact target-title matching but manually confirm the resulting wikilink syntax and its effective destination, including piped links.
5. A two-hop route is provably shortest once the direct-link check is negative and a source neighbor has a target link. For longer distances, run a breadth-first search over historical outgoing links, caching revisions and normalizing redirects/title variants; retain predecessor edges.
6. Report the number, exact page-title path, revision IDs/timestamps, and source URLs to the requester. State scope assumptions where material: ordinary article hyperlinks, namespace filtering, redirects, and whether links inside templates are treated as clickable.
7. For a strict final response, separately send the requested bare number/string and keep evidence only in the supporting report.
