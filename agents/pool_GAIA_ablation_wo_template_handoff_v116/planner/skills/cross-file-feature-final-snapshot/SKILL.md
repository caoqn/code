---
name: cross-file-feature-final-snapshot
description: Contract-first workflow for implementing repository features across schemas, services, routes, auditing, and documentation while preventing concurrent-edit drift.
trigger: When a feature request spans multiple source layers and requires exact public fields, endpoint behavior, and documentation.
---
1. Build a requirement-to-file/symbol matrix before editing, including exact request/response fields, status codes, exception mappings, persistence transitions, audit payload, and documentation location.
2. Identify the canonical source tree and inspect existing callers, schemas, service abstractions, repositories, audit APIs, and router registration before delegating implementation.
3. Assign one owner for edits to canonical files; prohibit parallel agents from overwriting those files. Use other agents for independent inventory or review only.
4. After implementation, read back every evaluator-visible file from disk. Compare schema fields to the service return object and route response model literally, not semantically.
5. Run compile/static checks and targeted behavioral stubs for success, missing resource, invalid state, excessive amount, full refund, partial refund, and audit invocation.
6. Remove generated caches and unrelated/duplicate artifacts, then run a final filesystem inventory and diff-scope audit.
7. Report dependency-limited runtime tests explicitly, but do not treat compile success as proof of cross-file integration.