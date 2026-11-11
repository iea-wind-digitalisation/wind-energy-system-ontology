# Alignment with standards and other semantic artefacts

WESO's purpose is to connect things. This page explains *how* it connects to each kind of artefact, and why the connections are kept deliberately different from each other.

## Four kinds of link

The single most important rule: **do not use one kind of link for everything.** Most alignment problems in this space come from expressing every relationship as `skos:exactMatch` or `rdfs:subClassOf`.

| Link | Used for | Mechanism | What it claims |
|---|---|---|---|
| **Projection** | Designation schemes — anything that issues identifiers | `ProjectionRule` in an alignment module | "Strings of this form name this kind of WESO thing" |
| **Specialisation** | Ontologies that build on WESO (WEO, OpOn, extensions) | `rdfs:subClassOf` WESO classes | "This is a more specific kind of that" |
| **Reporting label** | Reporting categories — statistical buckets | `weso:hasReportingLabel` on a position kind | "Their bucket counts the same population as our position kind" |
| **Concept mapping** | Thesauri and taxonomies published in SKOS | `skos:*Match` from an optionally punned component type | Whatever SKOS mapping properties claim — loosely, "similar concept" |

Each answers a different question, and confusing them causes specific damage:

- Using **specialisation** for a designation standard turns a tree of slots into a tree of kinds, so "main bearing system" becomes a kind of thing rather than a place in a turbine.
- Using a **concept mapping** for a reporting category hides the question that matters for statistics: do both sides count the same population, with the same boundaries?
- Using a **reporting label** inside a calculation lets an external category decide which rows are counted, and the result silently depends on how that category was drawn.

## Designation standards

### IEC 81346 and the RDS family (RDS-PP, RDS-PS, RDS for WTG)

The reference designation system is the main reason WESO exists. Its aspects are views on the same object, and each lands on a different primitive:

| Aspect | Prefix | Lands on |
|---|---|---|
| Function | `=` | `ComponentPosition` (functional parent chain) |
| Product | `-` | `ComponentPosition` (assembly parent chain) |
| Host of installation | `+` | `ComponentPosition` (as `hostedBy`) |
| Site of installation | `++` | `Space` |

No aspect ever names a physical unit. The function aspect does not name a BFO function ([ADR-0001](adr/0001-rds-function-is-not-bfo-function.md)). The generic breakdown structures published in the guidelines are *position kinds*; an operator's tag list is *component positions*.

Status: RDS for WTG has an alignment module ([`alignments/rds-wtg/`](../alignments/rds-wtg)). RDS-PP and RDS-PS follow the same pattern and are wanted.

### IEC 61400-25 (SCADA information model)

Not a component designation at all: a tag names a measurement channel. The binding lives in OpOn ([ADR-0009](adr/0009-signals-belong-to-opon.md)), pointing at WESO positions. One finding matters for WESO itself: a logical node can span positions that RDS splits, so resolving a position needs the logical node *and* the data object together. Projection rules support compound keys for this reason.

### ISO 14224 (reliability and maintenance data)

Its taxonomy levels (equipment unit, subunit, maintainable item, part) are a **granularity scale**, local to ISO 14224. Its equipment classes are **reporting labels** on position kinds. Its boundary definitions are the natural source for **attribution scope** values, which WESO has not fixed yet ([open question](open-questions.md)).

### Manufacturer and operator schemes

Part catalogues, serial registers and in-house tag conventions are designation schemes like any other. Each needs a projection rule — usually one line. The examples show both a parts scheme (→ `ComponentModel`) and a serial scheme (→ `ComponentUnit`).

## Upper and mid-level ontologies

### BFO 2020

WESO is aligned to BFO 2020 (ISO/IEC 21838-2). The imported file is the official `bfo-core.owl`. Choices worth knowing:

- Physical items are material entities; component units are objects.
- Positions are information content entities, not sites ([ADR-0002](adr/0002-positions-are-information.md)).
- Spaces (the `++` aspect) are sites.
- Component functions are BFO functions; occupancy roles are BFO roles.
- Component types are OWL classes, not instances of a BFO category ([ADR-0006](adr/0006-no-punning-by-default.md)).

### IAO

Two IAO terms are used — *information content entity* and *directive information entity* — imported as a minimal extract.

### IOF Core and IOF Maintenance

The Industrial Ontology Foundry's maintenance reference ontology is WESO's nearest architectural sibling: BFO-aligned, deliberately small, extended by application modules. IOF's pattern of a material artifact whose function is prescribed by a design specification corresponds to WESO's position kind prescribing a function type. Formal alignment to IOF Core is planned, not done.

## Prior art in other industries

The slot-versus-occupant problem is old. Two traditions solved it independently, and WESO borrows from both while differing in one important way.

**ISO 15926 (process industry) and its successor the Industrial Data Ontology.** Its standard example is a heat exchanger *tag* that keeps its identity while the physical exchanger installed at it is removed and replaced — the same structure as WESO's position and unit. The Industrial Data Ontology states coherence with IEC 81346. The difference is philosophical: ISO 15926 is four-dimensional, so a tag can be a physical thing whose temporal parts are made of different steel. BFO is three-dimensional, which is why WESO models the slot as information and makes the occupancy an explicit record.

**PLCS, ISO 10303-239 (aerospace and defence logistics).** Records, for each position, the parts that may be fitted, the part currently fitted, and the history of parts previously fitted — WESO's position, design baseline and occupancy. It is an EXPRESS information model rather than an ontology.

**What WESO adds.** Both traditions assume one authority: a reference library everyone maps into, or one configuration owner. WESO is built for the case where several schemes are each authoritative for their own question and none is in charge — hence projection contracts, scheme-local granularity and attribution scope, instead of a master model.

## SKOS vocabularies and thesauri

Many useful wind energy vocabularies are published in SKOS — component lists, failure taxonomies, inspection terminologies. WESO can use them without depending on them:

- If the vocabulary is used for **counting** (a failure-statistics category), attach it as a reporting label. See [`examples/planet-bearing-reporting-labels.ttl`](../examples/planet-bearing-reporting-labels.ttl).
- If you want **concept mappings** to a component type, assert that type additionally as an individual (punning) and map it with `skos:exactMatch` or `skos:closeMatch`. This is opt-in per type; nothing in WESO's core depends on it, and a reasoner will not connect the mapping to the class.
- **Never** subclass WESO classes under a SKOS hierarchy, or vice versa. A `skos:broader` tree typically mixes "is a kind of" with "is a part of", and inheriting it as `rdfs:subClassOf` turns parts into kinds.

## Writing an alignment module

1. Copy [`alignments/_template/`](../alignments/_template).
2. Declare the scheme as a `weso:DesignationScheme`.
3. For each kind of identifier the scheme issues, write a `weso:ProjectionRule` saying which WESO class it names. If two pieces of an identifier only together determine the target, give the rule several `weso:sourceConstruct` values.
4. If the scheme has a notion of depth or level, declare a `weso:GranularityScale` with its levels. Do not assert `finerThan` against another scheme's levels unless you can argue it in the pull request.
5. Add an example and a fixture that must fail (a designation from your scheme naming the wrong kind of thing).
6. Open a pull request using the *new alignment* template.
