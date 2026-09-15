---
name: endpoint-change-checklist
description: Safe workflow for adding a web API endpoint to an existing service
trigger: When implementing or modifying an HTTP endpoint in a repository with multiple routers
---
1. Identify the authoritative application wiring and enumerate every router that could expose the requested path.
2. Inspect one or two neighboring endpoint modules for dependency, response, naming, and error-handling conventions.
3. Capture the contract explicitly: HTTP method, full mounted path, status code, exact response shape, authentication/rate-limit requirements, and documentation location.
4. Prefer the smallest additive change: add a focused module or route and avoid replacing existing integration files unless required.
5. Check for duplicate prefixes and dynamic discovery behavior; ensure the route is mounted exactly once by the real app entry point.
6. Update the API documentation with request, response, auth requirements, and changelog details while preserving unrelated content.
7. Run lightweight syntax/static checks and inspect generated artifacts; remove cache files before handoff.
8. Ask a verifier to check route resolution, exact payload, dependencies, docs, and artifact placement once, then report completion.