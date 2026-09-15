---
name: graphql-validation-integration
description: Robust workflow for adding AST-based GraphQL validation to an existing service
trigger: When implementing query complexity, depth, authorization, or other document validation
---
1. Enumerate every GraphQL schema/router/view in the repository and identify the canonical application factory plus duplicate or legacy entry points.
2. Capture the validation contract precisely: per-field costs, special field/type rules, argument multipliers, variable handling, fragment behavior, threshold comparison, and exact error text/status semantics.
3. Implement a pure AST cost function independently of framework hooks so it can be unit-tested with parsed documents.
4. Add a graphql-core ValidationRule that reports errors during validation; avoid relying solely on post-validation exceptions that may become HTTP 500 responses.
5. Integrate through the framework's documented validation/extension lifecycle, confirming when the parsed document and variable values are available and ensuring rejected operations produce top-level GraphQL errors.
6. Resolve literal and variable argument values when possible; define safe behavior for missing, invalid, negative, or excessively large values.
7. Test nested selections, aliases, fragments, multiple operations, special fields, literal multipliers, variable multipliers, under-limit queries, and over-limit queries with exact error assertions.
8. Run syntax checks on every changed source file and inspect file boundaries for accidental markdown fences or generated cache artifacts before handoff.