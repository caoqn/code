---
name: dated-transit-stop-count
description: Verify a historical transit-line stop count from authoritative schedules or maps.
trigger: When asked to count stations or stops between named transit endpoints as of a specified date.
---
1. Parse the date, route, endpoints, direction, and whether endpoints must be excluded. Distinguish a request about the route's complete station sequence from one about a particular trip.
2. Search the operator's official route page and dated timetable/map first. Confirm the effective date printed on the document, rather than relying on a page's current content or search snippet.
3. If the official historical page no longer renders trip data, locate an archived copy of the operator's dated PDF; preserve both the canonical official route URL and the archive URL where possible.
4. Extract the station names in travel order. Check separate weekday/weekend tables and branch services for skipped or conditional stops.
5. Count only the entries strictly after the origin and strictly before the destination. State the full sequence and identify exactly which entries were counted.
6. If the schedule contains service variants, report the route-level count only when the question asks about the line/map; otherwise name the chosen train or pattern and explain any differing counts.
7. Cite the dated source URL and quote its effective date and decisive station rows. Do not present third-party archival hosting as operator authority without that caveat.
