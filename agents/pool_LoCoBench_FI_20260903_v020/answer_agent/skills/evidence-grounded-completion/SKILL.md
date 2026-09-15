---
name: evidence-grounded-completion
description: Produce reliable completion summaries for multi-file engineering tasks
trigger: When preparing the final response after teammates implement and verify a solution
---
1. Collect the latest coordinator and verifier messages, preferring explicit artifact listings over inferred filenames.
2. Cross-check that every required deliverable category is represented (implementation, integration, tests, configuration) and note any missing evidence.
3. Separate verification types: compilation, tests, static review, and artifact cleanliness; report only those explicitly confirmed.
4. Resolve conflicting or stale status updates by requesting one canonical confirmation rather than repeating multiple summaries.
5. Emit exactly the required response prefix and a concise summary of implemented behavior plus supported verification claims.
6. Do not include source code, speculative quality claims, or details unsupported by the evidence packet.