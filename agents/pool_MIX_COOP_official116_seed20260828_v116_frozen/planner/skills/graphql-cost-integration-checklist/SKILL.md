---
name: graphql-cost-integration-checklist
description: Implement and verify AST-based GraphQL query cost limits across configuration, validation, and web integration.
trigger: When adding GraphQL query complexity or cost analysis to an existing service.
---
1. Inventory the authoritative GraphQL stack (Graphene/graphql-core, Strawberry, or other) and inspect the actual router/execution API for validation-rule hooks rather than assuming a parameter name.
2. Define configuration with a typed positive integer default and deterministic environment precedence; expose both settings-object and module-level access only when callers require them.
3. Implement a graphql-core ValidationRule that computes each operation independently, traverses fields, inline fragments, fragment spreads with cycle protection, and derives parent type names from schema metadata.
4. Apply field base costs and explicit expensive-field overrides; parse literal pagination arguments safely and multiply the intended subtree according to the requirement.
5. Emit one GraphQLError per over-limit operation with exact user-facing wording and useful extensions; preserve normal validation behavior.
6. Integrate the rule through the framework's supported hook. If the framework lacks native support, add a custom validation/execution wrapper instead of silently skipping enforcement.
7. Add tests for simple pass, deep nesting rejection, low and high pagination multipliers, fragments, aliases, and exact error text.
8. Compile all submitted files, run focused tests with dependencies installed, and inspect the final diff for duplicate declarations, stale imports, and unsupported integration paths.