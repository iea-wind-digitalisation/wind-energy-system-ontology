# Architecture decision records

Each file records one design decision: the context, what was decided, and what it costs. They are short on purpose.

**To challenge a decision**, open an issue that names the ADR and gives a counter-example — a real situation the decision handles badly. If the outcome changes, a new ADR supersedes the old one; old ones are never deleted.

| # | Decision | Status |
|---|---|---|
| [0001](0001-rds-function-is-not-bfo-function.md) | RDS function-aspect designations name positions, not functions | Accepted |
| [0002](0002-positions-are-information.md) | Positions are information entities, not sites or objects | Accepted, under review |
| [0003](0003-position-kind-is-the-counting-key.md) | Position kind is the native aggregation key | Accepted |
| [0004](0004-three-kinds-of-physical-item.md) | Three kinds of physical item | Accepted |
| [0005](0005-type-versus-model.md) | Component type and component model are separate | Accepted |
| [0006](0006-no-punning-by-default.md) | Component types are plain OWL classes; no punning by default | Accepted |
| [0007](0007-function-is-the-only-occupancy-constraint.md) | Function is the only occupancy constraint; no nominal type on positions | Accepted |
| [0008](0008-staying-in-owl2-dl.md) | Stay in OWL 2 DL; put "must" in SHACL | Accepted |
| [0009](0009-signals-belong-to-opon.md) | Signals belong to OpOn; sensor positions stay in WESO | Accepted |
| [0010](0010-occupancy-is-reified.md) | Occupancy is a first-class record | Accepted |

Template: copy any file, keep the four headings.
