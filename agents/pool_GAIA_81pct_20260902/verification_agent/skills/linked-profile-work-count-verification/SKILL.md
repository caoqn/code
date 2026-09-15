---
name: linked-profile-work-count-verification
description: Verify an average number of historical works across public researcher-identifier profiles named in a structured attachment.
trigger: When a task extracts researcher IDs from an attachment and asks to count profile works before a date or average the counts.
---
1. Parse the attachment and enumerate only people with an explicit identification URL/ID; preserve the role and exact identifier for each.
2. Determine the target service and inspect the public profile page, not merely a generic search result. Record whether the requested unit is visible work cards, unique/grouped works, or underlying source records.
3. Treat a machine API as supporting evidence, not an automatic substitute for the page: establish whether its list is grouped/deduplicated and which date field the page uses for the displayed publication date.
4. For every profile, enumerate the qualifying visible works and retain titles plus displayed dates (or a reproducible endpoint/page citation). Explicitly resolve missing dates, duplicate groups, private/empty profiles, and dates differing across metadata sources.
5. Cross-check each count by a second method, such as pagination totals plus a year-filtered manual enumeration, or details retrieved for all individual records. Do not count from an API summary's first entry unless verified as the profile's displayed work and date.
6. Establish the denominator from the wording: normally every explicitly identified person is included, including a person with zero qualifying works. State an alternative only if the prompt says to exclude a category.
7. Add counts, divide by the justified denominator, and report the requested numerical precision only. Send the lead the per-profile counts, sum, denominator, URL evidence, and any unresolved display/API mismatch.
