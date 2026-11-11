# ADR-0008: Stay in OWL 2 DL; put "must" in SHACL

**Status:** Accepted

## Context
Running ROBOT's profile check and HermiT over the examples found three ways the drafts left OWL 2 DL:
1. Function *individuals* were used in `owl:someValuesFrom`, which needs a class.
2. Object properties pointed from individuals to classes (`prescribesFunction`, `projectsOnto` with range `owl:Class`).
3. `xsd:date` is not in the OWL 2 datatype map; declaring it makes its literals illegal.

## Decision
- Function types are classes; each item bears its own function instance.
- Pointers from an individual to a class are **annotation properties** (`prescribesFunction`, `projectsOnto`, `modelOfType`).
- Dates are `xsd:dateTime`.
- Rules that must *flag* bad data are written in SHACL, because OWL's open-world semantics never reports a missing fact as an error. The admissibility check is a SHACL-SPARQL constraint.
- CI checks the kernel, alignments and every example for OWL 2 DL, consistency and satisfiability.

## Consequences
- Any OWL 2 DL reasoner works on WESO and its examples.
- The reasoner does not enforce admissibility; the shapes do. This is honest: OWL would only ever infer, not reject.
- Contributors writing `"2024-06-11"^^xsd:date` will see CI fail; the error message is the hint.
