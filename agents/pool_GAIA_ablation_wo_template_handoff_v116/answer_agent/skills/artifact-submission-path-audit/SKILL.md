---
name: artifact-submission-path-audit
description: Verify generated artifacts are written to the evaluator-visible submission directory and not merely source, groundtruth, or staging directories
trigger: When a task requires creating or modifying files that an external evaluator will load from a workspace
---
1. Read the native contract, task parameters, and evaluator instructions to identify the exact required relative output path(s).
2. Enumerate candidate directories (submission/agent workspace, source, staging, and groundtruth) and resolve their absolute paths.
3. Require the producer to write the artifact directly into the evaluator's submission path; do not infer that a similarly named path is equivalent.
4. Confirm existence, file type, size, and expected structure at the exact submission path.
5. Perform readback validation from that exact path, including headers, row counts, ordering, uniqueness, and required field semantics.
6. If a reference or groundtruth artifact exists, compare contents as needed, but never treat equality in the reference directory as proof of submission.
7. Before final response, inspect the evaluator log or run its check to ensure it opens the same absolute path; report any path mismatch as a blocking failure.
