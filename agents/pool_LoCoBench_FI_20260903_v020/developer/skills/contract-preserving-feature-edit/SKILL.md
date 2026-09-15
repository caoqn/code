---
name: contract-preserving-feature-edit
description: Safely add cross-cutting metadata to context-derived services
trigger: When extending existing models, payloads, or signing flows without breaking compatibility
---
1. Copy complete canonical source artifacts before editing; never rewrite from memory.
2. Identify every parser, constructor, serializer, logger, and signer handling the affected object.
3. Add new fields only with trailing defaults and parse optional wire values conservatively.
4. Preserve optional dependencies, lifecycle methods, and alternate entrypoints exactly.
5. For signed payloads, define one deterministic canonical serialization and include all security-relevant metadata before signing.
6. Add a safe extraction/verification path for incoming payloads; distinguish absent metadata from malformed values.
7. Run syntax checks, inspect the diff for accidental deletions or formatting fences, and remove generated cache artifacts.
8. Perform one focused contract review covering backward compatibility, exact logs, payload keys, and integration reachability.