---
name: concurrent-artifact-finalization-audit
description: Verify final generated artifacts when multiple agents may edit the same tree concurrently
trigger: When implementation and verification occur in parallel and reports may describe stale file contents
---
1. Treat every teammate completion report as provisional until independently re-reading the exact final files.
2. Enumerate the evaluator-visible output tree and compare it with the required artifact list; detect files that appeared, disappeared, or were replaced during concurrent edits.
3. Re-read public schemas, service return values, and route handlers together; compare serialized field names and shapes directly rather than inferring compatibility from class names.
4. Run compilation after the final reread, then perform dependency-aware import or focused runtime checks where dependencies exist.
5. If snapshots disagree, report the timestamp/order and current authoritative contents; do not silently repair or accept stale claims.
6. Distinguish confirmed compilation from unexecuted runtime behavior and preserve unresolved mismatches in the final evidence report.