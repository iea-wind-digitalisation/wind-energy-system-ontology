# ADR-0002: Positions are information entities, not sites or objects

**Status:** Accepted, under review (see open question 7)

## Context
A slot persists while everything in it is replaced, and can be empty. Something must ground its identity. Candidates: the material (fails — total replacement is normal), a place (BFO *site*), a role borne by the occupant, or a record.

## Decision
`ComponentPosition` is an information content entity; `PositionKind` is a directive information entity.

- **Not a site:** blade 1 and blade 2 sweep through each other's regions continuously. What separates them is a convention, not a location. The RDS guideline states its counting numbers carry no meaning.
- **Not a role:** a role needs a bearer, so an empty slot could not exist, and slots could not be counted across a fleet — which removes the denominator of every reliability statistic.
- **Not a physical object (as in ISO 15926):** that works only in a four-dimensional ontology, where an object can have temporal parts of different matter. BFO is three-dimensional.

What remains is a record: a slot exists because a configuration says so, like a seat on a seating plan or a functional location in a maintenance system.

## Consequences
- The genuinely spatial part of RDS (the `++` aspect) gets its own class, `Space`, under BFO *site*.
- Physical relations (contact, containment) belong between occupants, not between positions.
- BFO specialists may object; the blade-1/blade-2 case is the argument to engage with.
