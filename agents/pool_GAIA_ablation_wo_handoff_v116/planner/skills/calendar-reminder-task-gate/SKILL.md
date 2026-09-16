---
name: calendar-reminder-task-gate
description: Reliable workflow for deriving and validating calendar reminders from email deadlines
trigger: When asked to create calendar reminders based on a mailbox and attachment list
---
1. Read the attachment/list and enumerate the complete target population; establish a stable key such as conference code plus track.
2. Retrieve all relevant mailbox pages, not only the first search page. Parse every deadline notice and explicitly resolve extensions, corrections, and conflicting notices according to the authoritative/latest-deadline rule.
3. Authenticate the calendar account before any list or mutation. List the full relevant date range and reconcile existing events by stable key, time, and summary; handle duplicates before creating new events.
4. Determine the exact calendar API payload schema and evaluator-visible fields. Preserve required title/summary wording, start/end structure, timezone, description, and reminder settings; do not assume that matching times alone is sufficient.
5. Create one canary event and read it back end-to-end. Verify its exact fields against the expected contract before bulk creation.
6. Create remaining events in bounded batches, recording IDs and source mappings in a manifest. Never recreate successful mutations because of delayed responses.
7. Independently list and read back every resulting event. Check count, uniqueness, stable key, exact deadline-minus-offset arithmetic, timezone, title/summary, and all evaluator-relevant fields. Compare artifact deadline fields to event times and source notices.
8. Correct any discrepancies with update operations, then rerun the complete readback and synchronize manifest, parameters, verification report, and completion gate. Only finalize when expected equals verified and all failure/duplicate/extra/unverified counts are zero.