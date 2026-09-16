---
name: ccs2-parser-contract-validation
description: Validate protocol-specific vehicle parsers against exact response schemas and public attribute contracts
trigger: When fixing parsing for a new protocol or model-year response format
---
1. Inventory every public Vehicle attribute and identify exact naming conventions already used by the library; do not add speculative aliases until contract evidence supports them.
2. Locate the exact protocol dispatch method and construct a temporary fixture matching realistic response nesting from issue data, fixtures, or upstream tests.
3. Before editing, invoke the parser on the fixture and record each target field's baseline value and type (including tuple-vs-scalar behavior).
4. Implement mappings using the exact response keys and preserve established enum conversion semantics; avoid broad guessed fallback paths that can mask schema errors.
5. For numeric fields, define explicit handling for null, negative, ratio, integer, and out-of-range values according to the requirement, preserving expected output types.
6. Build a behavior matrix covering each requested positive field, null/negative boundaries, malformed values, and unaffected legacy protocol paths.
7. Run the temporary reproduction before and after the patch, then run all nearest visible tests and inspect the final diff for only intended source files.
8. If hidden-like tests still fail, prioritize reading their fixture structure and expected attribute names over adding more speculative aliases.