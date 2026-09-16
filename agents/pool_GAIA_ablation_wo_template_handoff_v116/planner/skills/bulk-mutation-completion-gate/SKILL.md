---
name: bulk-mutation-completion-gate
description: Complete large cross-system mutations reliably when each item needs explicit API operations
trigger: When a task requires updating or notifying many records through external tools
---
1. Establish the authoritative target set and expected count from the strongest source; reconcile discrepancies before mutation.
2. Inspect API semantics with a tiny canary, including whether ranges are shifted, writes append, or responses truncate.
3. Choose a deterministic batching strategy that the tool actually supports. If an operation is per-item only, execute the full loop rather than stopping after a few examples.
4. Maintain a manifest with each item’s pending/completed/verified status and checkpoint after bounded batches.
5. After every batch, independently read back aggregate count and representative item payloads; investigate any offset or truncation before advancing.
6. Do not accept “too many manual calls” or partial progress as completion while budget remains; delegate execution or use supported batch endpoints.
7. Before finalizing, require expected==completed==verified, zero pending/duplicates/extras, and authoritative readback of the final state. If impossible, report partial status explicitly rather than implying success.