---
name: validation-contract-audit
description: Checklist for implementing validation and quarantine changes while preserving exact contracts
trigger: When adding validators, tuple-return APIs, failure routing, or dead-letter/quarantine handling
---
1. Extract exact return tuple order, types, and success/failure sentinels from the task and existing callers.
2. Search all validators and callers for parallel success paths; ensure every success path uses the same sentinel values.
3. Preserve existing exceptions, metrics, artifacts, and public aliases while introducing the new helper.
4. Validate malformed input and edge cases explicitly, including empty records and invalid ranges.
5. Ensure failed records are routed before downstream processing and include the required reason metadata in the serialized payload.
6. Verify producer/consumer lifecycle ordering: publish, flush, then close under guarded cleanup.
7. Run syntax checks, grep for contract literals, inspect artifacts, and remove generated caches before finalizing.