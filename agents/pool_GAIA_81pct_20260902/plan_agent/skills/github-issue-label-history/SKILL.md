---
name: github-issue-label-history
description: Determine the exact date a label was applied to the correct GitHub issue when a question combines repository scope, issue status, and chronological criteria.
trigger: When a question asks when a GitHub label was added to an issue selected by filters such as component, status, or oldest/newest.
---
1. Translate every phrase in the question into a GitHub search constraint: repository, issue versus pull request, open/closed state, each applicable label, and chronological ordering.
2. Use the GitHub issue search API with all relevant labels, sorting by issue creation when identifying the oldest or newest qualifying issue. Record the complete candidate set or enough ordered results to establish the target.
3. Inspect the selected issue metadata to confirm its status and labels, and distinguish its creation/closure dates from label-change dates.
4. Query the issue events or timeline endpoint and locate the `labeled` event for the requested label. Use that event timestamp, not the issue creation timestamp, unless evidence directly establishes they coincide.
5. Account for renamed labels by matching historical and current label identities; report the event date associated with the requested label concept.
6. Independently cross-check the filter interpretation, especially whether a phrase names a component label rather than merely text occurring in title/body.
7. Convert the verified timestamp to the requested date format and provide only that value when the required answer is strict short form.
