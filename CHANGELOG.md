# Changelog

All notable changes to WESO. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [semantic versioning](GOVERNANCE.md#stability-and-versioning).

## [Unreleased]

## [0.1.0] - 2026-11-10

First public draft.

### Added
- Core kernel (`ontology/weso-core.ttl`): physical layer (physical item, component unit, population item, portion of material, component type, component model), position layer (position kind, component position, space, four decomposition relations), function and role, lifecycle (occupancy and events), designation layer, comparability (granularity, attribution scope, reporting labels), projection contract.
- SHACL shapes: designation provenance, projection-contract conformance, occupancy integrity, no overlapping units, function admissibility, model/item mass separation.
- RDS for WTG alignment module with projection rules for all four aspects.
- Examples: blade replacement, planet bearing, optional reporting labels, JSON-LD payload.
- SPARQL queries: exposure, original vs replacement, designation resolution, labelled export.
- Test suite and failing fixtures; OWL 2 DL / HermiT check over kernel, alignment and examples.
- Documentation and ten decision records.
