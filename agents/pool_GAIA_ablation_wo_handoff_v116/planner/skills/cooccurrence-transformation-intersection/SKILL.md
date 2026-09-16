---
name: cooccurrence-transformation-intersection
description: Resolve compound questions that combine database filters, enzyme transformations, and shared gene-chemical co-occurrence rankings.
trigger: When a question asks for a filtered database compound and then asks about shared co-occurrences across multiple transformations.
---
1. Use the authoritative database query or downloadable dataset to identify every compound satisfying all numeric filters; do not stop at a plausible candidate.
2. Enumerate the exact enzyme transformation records for the selected compound, including transformation type, enzyme/gene entities, and successor compounds. Treat “two possible transformations” as the two records/branches explicitly shown by the source, not as a guessed metabolic pathway.
3. For each transformation branch, retrieve its gene-chemical co-occurrence set from the specified database panel/API. Distinguish genes from chemicals and preserve PubChem CIDs.
4. Compute the set intersection of chemical co-occurrences between the two branches. Do not substitute pathway metabolites, enzyme substrates, or downstream products for co-occurrence neighbors.
5. Retrieve molecular weights for every intersecting CID via the same authoritative property service, then select the maximum numerically (checking ties and missing values).
6. Independently verify the transformation identities, intersection membership, and weight ordering with a second query or agent before producing the concise CID-only answer.