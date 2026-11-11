# Open questions

The kernel is a draft. These are the issues known to be unresolved, roughly in order of how much they would change. Each should become a GitHub issue; discussion belongs there, and the outcome becomes a decision record in [`adr/`](adr/).

## Modelling

### 1. Positions nested under swappable units
A planet bearing position sits inside a gearbox. If the whole gearbox is swapped, does the bearing position stay with the turbine (as the RDS tag, which is turbine-relative, suggests) or travel with the gearbox (as the bearing's actual history does)? The examples attach it to the turbine. Getting this wrong misattributes exposure for any component inside a unit that is itself exchanged — gearboxes, pitch systems, generators.

### 2. Design baseline (configuration module)
What a given turbine model specifies for each slot — the specified model, approved alternates, how many such slots, from which serial onward — is design data, identical across a fleet. It is deliberately not in the core ([ADR-0007](adr/0007-function-is-the-only-occupancy-constraint.md)). It needs its own module: likely a *design position* level between position kind and component position, with `specifiedModel`, `approvedModel` (plural), multiplicity and effectivity. This is also where as-designed versus as-built deviation becomes expressible.

### 3. Refurbishment and provenance
Original and replacement derive cleanly from the occupancy record. Refurbished units don't: a bearing reinstalled under its original serial with new rollers is neither. A provenance chain on the unit (built, refurbished on date X with these items replaced, ...) is probably the answer, rather than more role values.

### 4. Population items in positions
A flange holds about a hundred bolts; one occupancy record with `occupantQuantity` is a placeholder. Partial replacement (twelve bolts renewed) is not yet expressible.

## Anchoring

### 5. Is an occupancy a process?
`PositionOccupancy` is a BFO process. It is arguably a state — nothing unfolds. The alternative is a relation qualified by a temporal region. Process is simpler and works; whether it survives review by BFO specialists is open.

### 6. BFO parents for population items and portions of material
Population items are probably *object aggregates*. Portions of material are a known difficult case in BFO; *fiat object part* fits poorly. Both currently sit directly under material entity.

### 7. Positions as information entities
`ComponentPosition` sits under *information content entity* and `PositionKind` under *directive information entity*. The most mature prior art (ISO 15926) treats the functional location as a physical object instead — possible only because it is four-dimensional. The argument for WESO's choice is in [ADR-0002](adr/0002-positions-are-information.md); it should be reviewed against IOF's treatment.

## Comparability

### 8. Comparing granularity across schemes
Granularity scales are scheme-local. Is any cross-scheme `finerThan` assertion defensible (e.g. ISO 14224 *maintainable item* vs RDS depth 3), or should comparison always be refused?

### 9. Attribution scope vocabulary
The class exists but has no agreed values. They should come from how ISO 14224 and established reporting schemes actually draw failure boundaries, not from first principles.

## Interfaces

### 10. Emitting designations
Counting numbers carry no meaning, so a system that generates designations must store them per position. Should WESO define how (a scheme-scoped index on the position), or leave it to applications? Only matters for systems that emit, not those that parse.

### 11. Compound keys in practice
Projection rules accept several source constructs. Whether real IEC 61400-25 data objects carry enough information to resolve, say, gearbox versus main bearing, or whether that must come from the manufacturer's configuration, has not been checked against the standard's tables.
