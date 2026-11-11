# ADR-0007: Function is the only occupancy constraint; no nominal type on positions

**Status:** Accepted

## Context
Earlier versions attached an "expected type" to positions or position kinds. Read as a constraint it duplicated the function check; read as information it was design data (what the W4200 turbine model specifies) sitting in a layer meant to be design-neutral.

## Decision
A position kind prescribes a **function type**. An occupant is admissible if it bears that function. There is no type or model attached to a position in the core.

- What sits in a position is a fact about the occupant, reachable through the occupancy.
- What a turbine model specifies for a slot belongs in a configuration module (open question 2).

## Consequences
- A valid substitute from another manufacturer passes the check.
- Legitimate retrofits are not flagged as violations.
- As-designed versus as-built comparison waits for the configuration module.
