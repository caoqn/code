---
name: historical-wikipedia-verification
description: Verify historical Wikipedia lists and nomination metadata reliably using primary page archives and structured API access.
trigger: When asked to identify an item and contributor from a dated Wikipedia promotion, nomination, or archive list.
---
1. Identify the likely canonical list page and the relevant dated section.
2. Retrieve page wikitext through the MediaWiki API when normal page fetching is blocked or rate-limited.
3. Search the dated section for the target topic/category and extract the exact item and contributor fields.
4. Open the individual archived discussion via API and verify its closure/promotion timestamp and explicit nominator line.
5. Cross-check both sources for agreement; distinguish promoter/reviewer from nominator.
6. Report the exact requested output string, preserving username spelling and avoiding extra names when the format is strict.
