---
name: structured-schedule-reconciliation
description: Reconcile event schedules from multiple structured sources, identify exclusions, and verify a completed tabular artifact.
trigger: When compiling a schedule or roster from configuration files, announcements, messages, and a reference workbook.
---
1. Inventory all candidate source files and inspect their schemas before extracting records.
2. Define the population key (usually a normalized course/event code) and deduplicate suffix variants or display-name variants using that key.
3. Parse each source for explicit inclusion statements and explicit exclusions; treat statements such as “no final exam” as authoritative exclusions.
4. Merge records from complementary sources, assigning provenance per row (for example, announcement versus email), and flag conflicts rather than silently overwriting.
5. Normalize dates, times, durations, names, emails, and locations while preserving source wording where the output schema requires it.
6. Sort by the requested temporal key and compare row count, unique keys, headers, and cell values against any reference artifact.
7. Report coverage, excluded records, unresolved/TBD records, duplicates, and source limitations (such as empty local API stores) separately from directly observed evidence.