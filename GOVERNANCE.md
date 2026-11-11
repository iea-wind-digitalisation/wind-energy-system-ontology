# Governance

WESO is developed in the open alongside the Wind Energy Ontology (WEO) and the Operations Ontology (OpOn) efforts. This document is deliberately light and will grow with the community.

## Roles

- **Contributors** — anyone who opens an issue or pull request.
- **Maintainers** — review and merge pull requests, triage issues, cut releases. Listed in [MAINTAINERS.md](MAINTAINERS.md).

## How decisions are made

- **Docs, examples, tests, alignment modules:** one maintainer approval.
- **Kernel changes** (`ontology/weso-core.ttl`, `shapes/`): two maintainer approvals and an ADR. The PR stays open at least one week so that people working on WEO and OpOn can comment.
- **Disagreements** are settled by counter-example where possible: the option that handles more real cases wins. Where that doesn't settle it, maintainers decide by consensus and record the reasoning in an ADR.

## Stability and versioning

Semantic versioning on the kernel:

- **Patch** — documentation, labels, definitions, examples.
- **Minor** — new terms; nothing existing changes meaning.
- **Major** — a term is removed, renamed, or changes meaning.

Before 1.0.0, minor versions may also break things; the CHANGELOG says so when they do. Removed terms are marked `owl:deprecated true` for at least one minor release before deletion.
