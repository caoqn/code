---
name: historical-transit-stop-verification
description: Verify a historical transit route's intermediate-stop count using dated schedules and route topology.
trigger: When a question asks how many stations or stops lie between two points on a transit service at a specified date.
---
1. Parse the date, route/branch, direction, endpoints, and whether the requested count excludes endpoints. Distinguish stations on the route from stops made by a particular express trip.
2. Locate the timetable or map effective on that date. Prefer operator-hosted historical material; if unavailable, use a preserved operator timetable and record its effective dates.
3. Extract the ordered station sequence from the origin through the destination. Confirm the direction and branch junctions, since a line may have alternative terminals or short turns.
4. List every station strictly after the origin and strictly before the destination, then count the list. Do not infer a count from zone numbers, travel time, or a contemporary route map without checking date applicability.
5. Cross-check the sequence with an independent route/station list or a second schedule. Reconcile schedule changes that occur within the named month or date range.
6. Report the number in the exact requested format. Retain a compact station list and dated-source URL as audit evidence, while clearly noting if the result is a topology count rather than a train-specific calling pattern.
