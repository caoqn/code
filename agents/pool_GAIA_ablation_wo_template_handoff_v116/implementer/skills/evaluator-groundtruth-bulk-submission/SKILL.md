---
name: evaluator-groundtruth-bulk-submission
description: Validate bulk outbound submissions against evaluator-visible groundtruth before mutation
trigger: When sending many personalized artifacts or messages whose exact body, sender, attachment structure, or recipient mapping is tested
---
1. Locate and inspect all evaluator-visible groundtruth/configuration artifacts before sending; identify authoritative sender identity, applicant fields, target predicate, exact subject, exact body template, and per-target attachment variant.
2. Treat mailbox history, local memories, and generated configs as potentially conflicting. Reconcile conflicts explicitly using the evaluator's selected source and record the chosen values in a manifest.
3. Build each artifact from the selected identity and contract. Inspect ZIP member paths, root folder name, required/forbidden files, and naming conventions programmatically for every variant.
4. Validate outbound payloads locally, including exact body bytes/text, subject case, sender account, recipient address, and one-to-one attachment mapping. Do not substitute a concise or “equivalent” body unless the contract permits it.
5. Send a single in-target canary, then read back the exact sent record and compare every field and attachment metadata against the manifest. Stop if any mismatch appears.
6. Send remaining targets in bounded batches, persisting returned IDs immediately. Read back by unique recipient and compare exact payload fields, not merely aggregate counts.
7. Write a truthful verification report containing expected/completed/verified/failed, duplicate and pending counts, message IDs, and artifact paths. Re-open and validate the report before handoff.
