# ADR-0001: RDS function-aspect designations name positions, not functions

**Status:** Accepted

## Context
IEC 81346 calls its `=` aspect the "function" aspect. BFO has a category called *function*. The obvious mapping is to treat `=A1=JF2` as naming a BFO function. Many attempts do.

## Decision
A function-aspect designation names a **component position** — a node in a function-oriented breakdown. It does not name a BFO function or role.

Three tests rule out a BFO function:
1. The designation can be assigned before any hardware exists. A BFO function needs a material bearer.
2. It is relative to a system and a hierarchy: `=JF2` means what it does because of what it sits under. A bearing's capacity to carry load doesn't depend on which turbine it is in.
3. Move a gearbox from `=A1=JF2` of one turbine to the same designation in another: its BFO function is unchanged, its designation has changed. Anything that changes independently of the physical makeup is not grounded in it.

WESO keeps three things apart: the function borne by the item (`ComponentFunction`), the slot (`ComponentPosition`, which the designation names), and the role the item has while in the slot (`OccupancyRole`). A position kind *prescribes* a function type; the occupant must *bear* it.

## Consequences
- Domain ontologies must not import an RDS breakdown as a class hierarchy.
- The prescribe/bear pair gives a check no source system can perform on its own, because none separates slot from occupant.
- Users familiar with RDS need the distinction explained; [core-concepts.md](../core-concepts.md) does this with the org chart analogy.
