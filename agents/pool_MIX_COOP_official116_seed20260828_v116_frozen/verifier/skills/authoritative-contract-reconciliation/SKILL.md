---
name: authoritative-contract-reconciliation
description: Reconcile conflicting task metadata, generated manifests, and evaluator-visible groundtruth before mutation or sign-off.
trigger: When task parameters, contracts, manifests, or service state disagree on counts, filters, ordering, or payloads.
---
1. Inventory every task-visible artifact and extract each claimed criterion, count, identity list, ordering rule, and payload field into a comparison table.
2. Identify the authority hierarchy: explicit evaluator/groundtruth metadata and task instructions outrank stale workflow contracts or intermediate manifests; live service readback outranks teammate summaries.
3. Reconstruct the target set from primary records programmatically, preserving stable IDs and documenting exclusions.
4. Resolve conflicts by querying the authoritative source or evaluator fixture; never average, guess, or silently choose one value.
5. Before mutation, record the resolved contract and expected counts in the manifest; after mutation, reconcile every identity and payload field against it.
6. Report unresolved conflicts as blocking and avoid claiming completion until counts, ordering, and per-record evidence all agree.