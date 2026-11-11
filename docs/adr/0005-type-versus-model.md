# ADR-0005: Component type and component model are separate

**Status:** Accepted

## Context
`ComponentType` was a subclass of BFO *object*. That entailed that the model "B-73P" was made of matter, had a location, and would be summed alongside its own instances in a fleet mass total. It also held two different things: a functional kind and a catalogue entry.

## Decision
- A **component type** is a kind, defined by function. It is written as an OWL class; units are `rdf:type` of it.
- A **component model** is a product specification — part number, revision, manufacturer, nominal mass — and is an information content entity. Units `conformsTo` it.

## Consequences
- Catalogue mass (`nominalMassKg`, on the model) and measured mass (`hasMassKg`, on the item) cannot be confused; a shape rejects measured mass on a model.
- A model can be revised or withdrawn without its installed units being affected.
- "Model" is reserved for the catalogue sense, avoiding the clash with simulation and CAD models common in the same teams.
