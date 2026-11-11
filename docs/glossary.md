# Glossary

One line each. Fuller explanations in [core-concepts.md](core-concepts.md).

| Term | Meaning |
|---|---|
| **Alignment module** | A small file declaring how one designation scheme projects onto WESO. |
| **Attribution scope** | What a failure recorded at a position is taken to cover (unit alone, unit with interfaces, whole assembly). |
| **BFO** | Basic Formal Ontology, the ISO/IEC 21838-2 top-level ontology WESO is aligned to. |
| **Component function** | What an item can do because of how it is built. Borne by the item; unchanged if it is moved. |
| **Component model** | A manufacturer's product specification: part number, revision, nominal mass. Information, not matter. |
| **Component position** | A slot in one particular machine, e.g. blade position B of T07. Persists while its occupants change. |
| **Component type** | A kind of physical item defined by its function, e.g. blade. Written as an OWL class. |
| **Component unit** | One physical thing tracked individually, usually by serial number. |
| **Designation** | A string from a source system plus the scheme it came from. |
| **Designation scheme** | Anything that issues identifiers: a standard, a serial register, a tag convention. |
| **Exposure / position-time** | Total time positions of a kind were occupied; the denominator for failure rates. |
| **Granularity scale** | A scheme's own ordered set of breakdown levels. Not assumed comparable to other schemes'. |
| **OpOn** | Operations Ontology: signals, channels, measurements. Points into WESO positions. |
| **Occupancy role** | What an item is in virtue of its history: original, replacement, spare. Derived, not asserted. |
| **Physical item** | Any material thing that can fill a position: a component unit, a population item, or a portion of material. |
| **Population item** | A set of things tracked as a set: the bolts of a flange. |
| **Portion of material** | Stuff tracked by amount: the oil in a gearbox. |
| **Position kind** | The generic slot across machines, e.g. "blade position". WESO's counting key. |
| **Position occupancy** | A record that one item filled one position from one date to another. |
| **Projection rule** | A scheme's declaration of what kind of WESO thing its designations name. |
| **Punning** | Using one IRI as both a class and an individual. Allowed in OWL 2 DL; avoided by default in WESO. |
| **Reporting label** | An external category attached to a position kind for labelling exports. Never used in calculations. |
| **SHACL** | W3C language for validating RDF data. WESO's checks are SHACL shapes. |
| **Space** | A region in or around a turbine: nacelle, hub interior. The only genuinely spatial WESO class. |
| **WEO** | Wind Energy Ontology: the domain layer that adds kinds of component, function types and a position kind library. |
