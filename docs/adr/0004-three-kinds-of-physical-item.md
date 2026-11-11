# ADR-0004: Three kinds of physical item

**Status:** Accepted

## Context
Only serialised units could originally occupy positions. Oil, grease, bolt sets and bearing rollers had nowhere to go, so oil changes needed special handling and sub-unit refurbishment was invisible.

## Decision
`PhysicalItem` (BFO material entity) with three subclasses, distinguished by how identity is tracked — not by phase or by serial number:
- `ComponentUnit` — one thing, tracked individually (BFO object);
- `PopulationItem` — many things, tracked as a set;
- `PortionOfMaterial` — merges and splits, tracked by amount.

Material entity is the only BFO level all three share, which fixes the parent's position.

## Consequences
- An oil change is an ordinary occupancy transition.
- Replaced mass can be computed honestly (a roller renewal is not a whole bearing).
- A shared lubricant makes failures at several positions correlated, and that becomes visible.
- BFO parents for the latter two are open (open question 6).
