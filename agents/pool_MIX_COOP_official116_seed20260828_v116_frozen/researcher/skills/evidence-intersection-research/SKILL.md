---
name: evidence-intersection-research
description: Efficiently identify entities in scholarly sources and compute intersections with a comparison study
trigger: When a question asks which animals, organisms, or other named entities occur across multiple papers
---
1. Resolve ambiguous names by searching exact author combinations and the target taxon; confirm the genus/species from an authoritative paper or database.
2. Locate open full text through Europe PMC/PMC or the publisher, preferring primary article text over search snippets.
3. Extract article text programmatically when practical, then search targeted terms and inspect surrounding context to distinguish main text from references and bibliography.
4. Build a normalized list of entities for each requested paper, preserving exact taxonomic names where stated and noting broader categories separately.
5. Extract the comparison study’s entities independently; distinguish study participants from preclinical models and from incidental mentions in background/references.
6. Compute the intersection conservatively using only directly observed, non-bibliographic mentions unless the question explicitly includes references. Report uncertainty for inferred or contextual entities.
7. Send the concise intersection and source URLs to the lead, including the evidence passages or section context needed for verification.