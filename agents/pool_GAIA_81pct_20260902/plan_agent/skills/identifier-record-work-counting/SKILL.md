---
name: identifier-record-work-counting
description: Count dated works from researcher-identifier records referenced in an attachment and calculate an aggregate without conflating API representations.
trigger: When a task provides identifiers or a structured bibliographic file and asks for counts of works before or after a date on public researcher profiles.
---
1. Read the attachment completely and build a table of every person, every identifier URL, their role, and whether an identifier is actually present. Establish the exact population and denominator from the wording before collecting counts.
2. Identify the named identification service and inspect both its public record page and its official API/documentation. Do not assume that an API list, a group, or a summary matches the page's displayed unit.
3. Obtain the full record data and retain, for each displayed work candidate, all relevant date fields: publication date, created date, last-modified date, and any preferred/representative record date. Determine from the public page and service documentation which field supplies the date visible to a reader.
4. Explicitly test competing interpretations: raw records versus displayed groups; publication dates versus contribution/indexing dates; and inclusion versus exclusion of missing dates. Reconcile duplicates and alternative versions using a sample of records from each grouping type.
5. Make a reproducible per-person count table under every plausible interpretation. If the requested wording is tied to pages, prioritize what is visibly presented there, but require direct evidence that the API projection precisely reproduces it.
6. Have an independent reviewer use a separate extraction route or independently inspect representative page entries. Do not accept two analyses that use the same endpoint and assumptions as independent confirmation.
7. Calculate the aggregate only after resolving the semantic choice. Send the final evidence packet with population, per-person counts, selected data/date field, arithmetic, and strict output format.
