---
name: github-issue-label-timeline-research
description: Identify the oldest issue matching repository/component labels and determine the historical date a target label was applied.
trigger: When a question asks when a label was added to the oldest issue matching GitHub repository and component/state criteria.
---
1. Resolve the repository's exact label names first, including numbered or renamed variants; do not assume the prose label string is the current API name.
2. Query GitHub issue search or the issues listing with repository, issue/closed-state, and all required labels. Sort by creation date (and independently inspect closure dates if “oldest” could be ambiguous).
3. Enumerate all matching candidates and record issue number, title, creation and closure timestamps, and current labels.
4. For the oldest candidate, inspect its timeline (API, embedded page data, or HTML) and locate the LabeledEvent whose label name matches the target or historical predecessor. Record the event timestamp, not merely the issue or closure date.
5. If labels were renamed, document the historical/current names and confirm they refer to the same label via IDs or timeline evidence.
6. Convert the event timestamp to the requested date format, preserving the repository's displayed timezone/date semantics, and have an independent source or second candidate check confirm minimality.
7. Return only the requested concise answer after validating the exact output contract.