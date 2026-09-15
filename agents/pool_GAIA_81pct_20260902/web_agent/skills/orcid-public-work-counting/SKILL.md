---
name: orcid-public-work-counting
description: Count works before a date on publicly accessible ORCID records while matching the record UI's grouping and date semantics.
trigger: When a question identifies people through ORCID IDs and asks for a work count, date-filtered count, or an aggregate of those counts.
---
1. Extract every explicitly identified ORCID iD and record whether the task permits discovering additional people or profiles.
2. Load the public ORCID record and its public works endpoint with JSON content negotiation. Preserve the retrieval time and endpoint because ORCID records are mutable.
3. Establish the counting unit from the wording. ORCID's `group` array represents identifier-grouped works as presented in the public record; `work-summary` entries are sources or versions inside one displayed group. Do not silently substitute raw summaries for displayed works.
4. Establish the date rule before counting. For each group, inspect the preferred/displayed summary (using the documented display ordering) and its publication date. Treat an absent publication date as uncountable rather than inferring it from metadata unless the question directs otherwise.
5. Independently reproduce the exact public-page count where possible (rendered UI, public UI data request, or a saved accessible representation). The API and UI can have visibility, caching, pagination, ordering, and version differences; do not assume an API aggregate exactly equals the question's intended page count.
6. Produce an audit table with profile URL, total displayed groups, qualifying groups, undated groups, counting unit, and date field used. For groups with multiple summaries having divergent dates, state the selected displayed-summary rule.
7. Before calculating an average, reconcile any mismatch with an independently obtained expected/intermediate count by inspecting pagination, visibility, inferred date handling, and scope of people. Report only a result supported by the same representation named in the prompt.
