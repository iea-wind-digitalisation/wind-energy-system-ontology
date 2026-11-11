# ADR-0006: Component types are plain OWL classes; no punning by default

**Status:** Accepted (supersedes an earlier decision to pun all types)

## Context
To make component types targets for `skos:exactMatch`, they were once asserted both as classes and as individuals (punning). That put an external-vocabulary convenience on the critical path of the core.

## Decision
Component types are plain OWL classes. `weso:ComponentType` is kept as a documentation anchor. A type that genuinely needs a SKOS mapping may additionally be punned — opt-in, per type, outside the core.

## Consequences
- The kernel and its examples carry no punning.
- SKOS alignment is still possible, but nothing depends on it.
- Where punning is used, a reasoner treats the class and the individual as unrelated: `skos:broader` between punned types implies no subclass relation.
