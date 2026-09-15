---
name: security-review-middleware
description: Security checklist for authentication, rate limiting, caching, and middleware changes
trigger: When implementing middleware or request identity/configuration behavior
---
1. Enumerate all identity sources (headers, request state, tokens, network address) and rank them by trust; never trust client-provided identity headers without authenticated validation.
2. Ensure cache, idempotency, and rate-limit keys include a canonical authenticated principal and cannot collide across users or tenants.
3. Reject insecure default secrets and avoid embedding credentials in source; use explicit configuration with safe failure behavior.
4. Review replay, race, and fail-open behavior. Use atomic backend operations and bounded in-process fallbacks where needed.
5. Verify response status, headers, and error bodies do not disclose sensitive data.
6. Run focused tests for spoofed identities, malformed keys, backend outages, and concurrent requests, then inspect the final diff for accidental secrets.