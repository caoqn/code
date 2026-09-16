---
name: entity-filter-intersection-validation
description: Reliably solve multi-constraint entity identification and downstream intersection questions from structured databases
trigger: When a task asks to filter database entities by properties and then derive transformations, co-occurrences, or an extremum
---
1. Parse the request into explicit stages: candidate filtering, classification membership, relationship extraction, and final extremum/intersection.
2. Build the candidate set from the named source or classification first; do not assume that a chemically plausible compound is in the requested class.
3. Retrieve every requested property using the source's canonical record/API and record identifiers, units, and release/version.
4. For downstream transformations, enumerate only relationships explicitly listed by the requested source or study. Keep inferred biochemical plausibility separate from observed records.
5. If the question asks for shared gene–chemical co-occurrences, obtain the gene sets for each relevant chemical and compute the literal intersection; do not substitute enzyme names based on general metabolism knowledge.
6. For “heaviest” or another extremum, define the comparison universe exactly (all returned related compounds, intersection members, or transformed products) and compare numeric values from records, not memory.
7. Verify the final identifier by independently querying its record and checking that it satisfies the stated relationship and extremum; report uncertainty when source access is incomplete.