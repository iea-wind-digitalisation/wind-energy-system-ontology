# ADR-0003: Position kind is the native aggregation key

**Status:** Accepted

## Context
Early versions grouped reliability statistics by a concept from an external failure-statistics vocabulary. That made WESO's core computation depend on a vocabulary it was meant to bridge, and on boundaries drawn by someone else without being declared.

## Decision
Statistics are grouped by `PositionKind`, WESO's own class. External categories attach through `weso:hasReportingLabel` and are joined after the computation, as labels on the output.

## Consequences
- Removing every external vocabulary leaves every number unchanged. The test suite checks this.
- Pooling data across organisations requires a shared position kind library; WEO is the expected home.
- `AttributionScope` on the position kind makes export to a foreign category a checkable step.
