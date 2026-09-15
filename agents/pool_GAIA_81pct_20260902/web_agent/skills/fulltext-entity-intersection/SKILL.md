---
name: fulltext-entity-intersection
description: Extract and intersect entities across multiple cited scientific papers while excluding bibliographies and resolving species-level naming.
trigger: When a question asks which named entities (especially animals) occur in the bodies of several papers and in a third source.
---
1. Identify each target paper from authoritative metadata (publisher, PubMed, PMC, DOI) and record direct full-text URLs.
2. Retrieve machine-readable full text (XML/HTML/PDF text), remove reference-list and bibliography sections before searching.
3. Search broadly for taxonomic and common-name variants (singular/plural, genus/species, collective terms), then inspect each match in context to distinguish actual body mentions from author names, affiliations, captions, and citations.
4. Normalize mentions to the requested semantic level: map variants such as “ob/ob hyperphagic mice” to mice, but do not automatically treat generic “animals” or “humans” as a species unless the question explicitly allows it.
5. Build one set per paper and compute the intersection; verify each surviving entity appears in all required bodies, including the exact third study cited by the relevant Wikipedia page.
6. Prefer the answer format requested (e.g., lowercase comma-separated names), and provide evidence URLs/quotes to the coordinator while keeping the final output minimal.