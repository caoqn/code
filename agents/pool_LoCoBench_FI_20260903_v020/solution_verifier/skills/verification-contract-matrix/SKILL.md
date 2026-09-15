---
name: verification-contract-matrix
description: Build a compact evidence matrix for verifying feature submissions across artifacts, behavior, compatibility, and robustness.
trigger: When reviewing a multi-file implementation against a broad or ambiguous requirement
---
1. Enumerate every required output artifact and map each to the requirement it satisfies.
2. Extract exact behavioral contracts, including fields, defaults, serialization, logging, errors, and integration points.
3. For each contract, inspect both the producer and every consumer/caller; distinguish helper availability from actual runtime wiring.
4. Check backward compatibility by locating existing constructors, public methods, and call sites before approving additive fields or signatures.
5. Inspect at least one malformed-input and missing/unknown-value path, and record whether behavior is explicit or merely assumed from transport conventions.
6. Run one static syntax/import check, then remove generated caches and re-enumerate artifacts.
7. Send one prioritized report with PASS, BLOCKER, and CAVEAT sections, quoting concrete evidence and noting unexecuted runtime tests.