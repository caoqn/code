---
name: evaluator-conflict-resolution
description: Resolve conflicting task metadata, manifests, and evaluator contracts before authorizing external mutations or completion.
trigger: When authoritative files disagree on target counts, filters, recipients, or artifact semantics.
---
1. Inventory every candidate source of truth (native contract, evaluator fixtures, task parameters, manifests, service state) and rank authority based on explicit evaluator validation semantics.
2. Read the exact evaluator code or contract clauses governing each disputed field; do not infer from aggregate counts or filenames.
3. Build a discrepancy table showing each source, claimed value, and affected mutation/validation step.
4. Derive the evaluator-visible expected set using deterministic IDs/filters, and verify whether the source data can produce that set.
5. If no deterministic mapping resolves the conflict, block mutation/completion rather than choosing an arbitrary subset; report the exact unresolved field and required evidence.
6. After any mutation, perform per-record evaluator-shaped readback and rerun the exact acceptance harness, ensuring counts and identities match the contract.