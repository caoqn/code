---
name: minimal-patch-feature-audit
description: Implement cross-layer feature flags while preserving existing code and validating signed payload and inbound processing paths.
trigger: When adding metadata or options that must flow through creation, cryptographic signing, and event verification.
---
1. Identify the canonical creation API and grep all callers before changing its signature; add new parameters as trailing defaults.
2. Trace the complete data lifecycle: creation payload, canonical serialization, signing invocation, transport envelope, signature verification, and post-verification handling.
3. Apply additive minimal patches to the existing implementation rather than rewriting or compressing modules; preserve constructors, routes, and unrelated behavior.
4. Ensure the new field is included in the exact bytes/message passed to cryptographic signing, and add a compatibility default when parsing older payloads.
5. In inbound handlers, distinguish raw/unverified data from verified payload; extract metadata only after successful verification and log using the module's established logger with exact required text.
6. Independently inspect every changed artifact, grep acceptance literals, compile changed modules, and remove generated caches before submission.
