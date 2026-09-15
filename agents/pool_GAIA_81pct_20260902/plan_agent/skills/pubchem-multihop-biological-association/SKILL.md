---
name: pubchem-multihop-biological-association
description: Solve PubChem questions that combine compound-property filtering, biological transformations, and shared gene–chemical association ranking.
trigger: When a question asks to filter PubChem compounds and traverse transformation or gene-chemical relationship data to identify a ranked related compound.
---
1. Parse every initial compound constraint exactly, including the classification/source collection, property inequalities, and whether values are computed or displayed.
2. Obtain the candidate set through an official PubChem query/API or downloaded database data, then make a table of CID, name, and every specified property. Confirm that the selected candidate belongs to the required classification.
3. Find the biological transformation section for that exact CID and enumerate each transformation stated or implied by the wording. Preserve reaction direction, enzyme identity, product CID, and source links.
4. For each transformed chemical, retrieve its gene–chemical co-occurrence set from the relevant PubChem/NCATS relationship source. Normalize gene and chemical identifiers before intersecting; do not substitute merely related genes, enzymes, or pathways.
5. Enumerate the intersection, retrieve molecular weights for every chemical in it from PubChem, and rank numerically. Resolve salts, stereoisomers, and duplicate names by CID.
6. Independently validate the final CID through a distinct source or endpoint and verify the question asks for the related compound rather than the original filtered compound.
7. Report only the requested identifier in the required short-answer format, while retaining URLs and the calculation table as evidence for the final synthesis agent.