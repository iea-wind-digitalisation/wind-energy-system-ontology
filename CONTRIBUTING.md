# Contributing to WESO

Thanks for considering it. At this stage the most valuable contributions are **counter-examples**: a real situation from a turbine, a fleet or a dataset that the kernel handles badly. A good counter-example is worth more than a new class.

## Ways to contribute

| You want to… | Do this |
|---|---|
| Ask how to model something | Open a *Modelling question* issue |
| Challenge a design decision | Open an issue naming the ADR (e.g. "ADR-0002") with a counter-example |
| Propose a new kernel term | Open a *New term* issue first — see the bar below |
| Connect a designation scheme | Open a *New alignment* issue, then a PR using `alignments/_template/` |
| Fix docs, examples, tests | Open a PR directly |

## The bar for adding to the kernel

The kernel stays small on purpose. A new class or property goes into `ontology/weso-core.ttl` only if:

1. a **competency question** needs it — a concrete question someone wants answered that the kernel cannot answer without it;
2. it **cannot live in a domain ontology or extension** instead (most things belong in WEO, OpOn, or an extension module);
3. it comes with a **label and definition**, an **example** using it, and a **fixture** showing what it rules out, where relevant;
4. the PR adds or updates an **ADR** if it changes a decision.

## Conventions

- Classes `UpperCamelCase`, properties `lowerCamelCase`, under `https://w3id.org/ontoforge/weso/`.
- Every class: `rdfs:label` (lowercase, `@en`) and `skos:definition` or `skos:scopeNote`. Every property: `rdfs:label`. Tests enforce this.
- Definitions are one sentence, genus–differentia where possible, readable without ontology training.
- Pointers from an individual to a class are annotation properties ([ADR-0008](docs/adr/0008-staying-in-owl2-dl.md)).
- Dates are `xsd:dateTime`, not `xsd:date`.
- Rules that should reject bad data go in `shapes/`, not as OWL axioms.
- Example instance data uses `https://example.org/fleet/`. Never put instance data in the WESO namespace.

## Before you open a PR

```bash
pip install -r requirements.txt
python -m pytest -v
ROBOT_JAR=path/to/robot.jar scripts/check-owl.sh   # if you changed any .ttl
```

CI runs both on every PR. A PR that changes behaviour should change a test.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
