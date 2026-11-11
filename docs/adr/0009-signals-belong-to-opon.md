# ADR-0009: Signals belong to OpOn; sensor positions stay in WESO

**Status:** Accepted

## Context
Binding a SCADA tag (IEC 61400-25) to a component showed that a tag names neither a component nor a position: it names a measurement channel, which links an observed quality, the thing bearing that quality, and the sensor's own slot.

## Decision
Measurement channels, observed qualities and signal bindings live in the Operations Ontology (OpOn). WESO provides positions for OpOn to point at. Sensors remain in WESO's position tree, because OpOn must distinguish the sensor's slot from the measured item's slot.

## Consequences
- WESO's scope stays physical and configurational.
- Two generalisations motivated by this work stay in WESO because they hold without signals: `PortionOfMaterial` (oil has a lifecycle whether or not it is measured) and compound keys on projection rules.
