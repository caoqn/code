---
name: bulk-artifact-mutation-verification
description: Safely create and verify many recipient-specific artifacts and external mutations
trigger: When a task requires generating per-target archives/files and performing one external operation per target
---
1. Reconcile the authoritative target list and assign each target a stable ID before any mutation.
2. Build a manifest containing target, artifact path, payload summary, and pending status.
3. Generate artifacts deterministically from shared source material, applying target-specific schemas or structures.
4. Validate every artifact opens successfully and contains exactly the intended files, with no generated metadata or extras.
5. Test one mutation with an absolute artifact path and record its authoritative response before batching.
6. Batch only remaining targets, preserving response IDs and never retrying successful targets.
7. Read back authoritative external state and compare recipient, payload, attachment, and counts against the manifest.
8. Update completion status only from direct evidence; report expected, completed, verified, failed, remaining, duplicate, and unverified counts.