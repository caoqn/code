---
name: cross-file-contract-reconciliation
description: Keep schemas, services, and endpoints aligned during concurrent multi-file implementation.
trigger: When implementing or modifying a feature spanning request/response models, service methods, and routes.
---
1. Build a matrix of required files, public symbols, method signatures, route paths, status codes, and response fields before editing.
2. Read the complete current versions of every target file and preserve existing behavior unless explicitly replaced by the contract.
3. Update service return shapes and response schemas together; grep every producer and consumer of changed fields.
4. After each edit, immediately reread the entire modified block and verify file size and key symbols.
5. Run static compilation across the whole output tree and perform import/introspection checks where dependencies permit.
6. Inspect final git diff/status and file inventory for missing, truncated, or concurrently overwritten artifacts.
7. Report dependency limitations separately from source-level verification; never treat compilation alone as endpoint contract proof.