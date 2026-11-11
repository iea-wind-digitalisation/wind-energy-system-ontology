# ADR-0010: Occupancy is a first-class record

**Status:** Accepted

## Context
"Which item was in which slot, when" could be stored as dates on the item, dates on the position, or as its own record.

## Decision
`PositionOccupancy` is its own entity, linking one occupied position, one occupant and an interval. Events (installation, removal, failure) attach to occupancies.

## Consequences
- Exposure is position-time: the sum of occupancy intervals per position kind. Replacements extend a position's record instead of enlarging the population; multiplicity (three blades) is kept.
- Original and replacement are derived from the record, not asserted.
- A shape can detect two units in one slot at once.
- Whether an occupancy is best modelled as a BFO process is open (open question 5).
