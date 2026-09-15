---
name: artifact-contract-audit
description: Perform a concise final audit of generated software artifacts against exact API and persistence contracts.
trigger: When reviewing a completed multi-file implementation before submission
---
1. Enumerate the output tree and verify every explicitly requested file/path; flag unexpected generated artifacts such as caches.
2. Build a checklist of exact symbols, endpoint methods/paths, status codes, payload field names, and persistence locations.
3. Inspect canonical implementation entrypoints plus compatibility modules to ensure there is one consistent public contract.
4. Check at least one malformed input, missing-resource path, empty-data case, and serialization round-trip statically or via existing tests.
5. Run one lightweight syntax/import check, then clean any artifacts it generated.
6. Report PASS/BLOCKER/NON-BLOCKING findings once, quoting concrete file evidence and distinguishing untested runtime behavior.