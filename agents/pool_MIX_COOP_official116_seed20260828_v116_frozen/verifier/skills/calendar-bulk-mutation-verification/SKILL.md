---
name: calendar-bulk-mutation-verification
description: Safely create and reconcile batches of calendar records from authoritative source data.
trigger: When creating or updating multiple calendar events from emails, documents, or manifests.
---
1. Derive the complete authoritative target set and expected count before any mutation; preserve stable IDs and source evidence.
2. Query the calendar over the full relevant date range and build an identity map using normalized code/track, start, end, and summary.
3. Coordinate ownership so each target has exactly one writer; do not create an event until checking whether another worker already owns or created it.
4. Confirm the exact payload contract, especially summary format, timezone, start, end, and duration, before creating records. Never guess duration when a deadline interval is specified.
5. Create only missing records, recording returned IDs immediately.
6. Perform a fresh paginated readback and reconcile every expected target: missing, duplicate, unintended extra, summary, description, start, end, and timezone.
7. If duplicates arise, delete only the known duplicate IDs, then re-read the affected range and report concrete counts and IDs.