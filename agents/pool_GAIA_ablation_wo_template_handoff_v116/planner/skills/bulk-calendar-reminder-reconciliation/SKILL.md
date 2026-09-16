---
name: bulk-calendar-reminder-reconciliation
description: Reliable workflow for creating many calendar reminders from authoritative messages while avoiding duplicates and preserving exact payloads.
trigger: When deriving and creating multiple calendar events from email or other deadline sources.
---
1. Enumerate the complete authoritative population and assign each item a stable ID, deduplicating by logical target (for example conference and track), not message ID.
2. Resolve the latest applicable deadline by comparing all matching notices; extensions supersede original deadlines. Record timezone and transformation (such as reminder offset) explicitly.
3. Read the calendar over the full relevant range before mutation and confirm baseline conflicts or pre-existing matching events.
4. Define non-overlapping mutation ownership ranges before delegating. Maintain a shared manifest mapping every target to exactly one owner and pending/completed status.
5. Use one canonical payload schema for summary, description, start, end, and timezone. Run a canary creation and readback before bulk creation.
6. Execute bounded batches, recording returned event IDs immediately. If overlap occurs, stop further writes and delete only verified duplicates, retaining one canonical event per target.
7. Independently list the full calendar range after writes. Reconcile expected versus actual targets, checking exact title, description, start/end, timezone, duplicate count, and unintended extras.
8. Update the manifest and completion contract only after authoritative readback proves every target verified and no pending, failed, duplicate, or extra items remain.