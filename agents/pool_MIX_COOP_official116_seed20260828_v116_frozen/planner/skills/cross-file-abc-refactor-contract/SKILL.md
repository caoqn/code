---
name: cross-file-abc-refactor-contract
description: Safely introduce a shared abstract strategy base across heterogeneous implementations while preserving APIs.
trigger: When a task requests a new ABC and migration of multiple existing strategy classes.
---
1. Inventory every target class, constructor signature, execution method, and existing helper; record behavior that must remain unchanged.
2. Build a literal requirement matrix for base class name, constructor parameters, helper signature, abstract methods, return annotations, inheritance, and exports.
3. Implement the new ABC first with exactly the requested signatures; retain compatibility aliases only when existing package APIs require them.
4. Update each concrete class with explicit super calls and exact abstract method implementations. Do not add placeholder implementations that silently return empty data.
5. Preserve strategy-specific execution semantics by adapting existing primary methods rather than replacing them with generic stubs.
6. Validate wallet-manager lookup behavior using realistic manager and wallet doubles, including insufficient, exact, absent, and malformed balances.
7. Grep all old class/method names and callers, inspect exports, and compile/import the canonical source tree.
8. Run direct instantiation/introspection checks for every concrete class and assert abstract classes remain abstract; remove caches and verify final artifact paths.