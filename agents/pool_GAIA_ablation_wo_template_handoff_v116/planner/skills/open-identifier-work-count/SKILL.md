---
name: open-identifier-work-count
description: Determine averages of dated works from public researcher/contributor identification pages named or implied by an attachment.
trigger: When an attachment lists people and asks for average works on open identification pages.
---
1. Parse the attachment and enumerate every person, not only those with explicit identifier fields.
2. For each person, search authoritative open researcher/contributor registries to locate a matching public profile; document identity disambiguation using affiliation, name, and source context.
3. Use the profile's displayed work records or official API representation. Prefer the page's deduplicated/grouped work count over raw duplicate summary entries, and define pre-cutoff as publication year earlier than the stated cutoff.
4. Include all people for whom an open identification page can be established; do not silently exclude people merely because the attachment omitted an identifier.
5. Treat undated works consistently (exclude from pre-cutoff unless the source explicitly dates them), record zero for profiles with no works, and compute sum divided by the complete identified-person denominator.
6. Independently verify each profile match and arithmetic, then round only as requested (for example, one decimal place if the expected answer format implies it).