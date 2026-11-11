# Worked examples

Both examples are runnable Turtle files in [`examples/`](../examples). Every number on this page is checked by the test suite, so if this page and the code disagree, the tests fail.

## 1. Blade replacement — [`blade-replacement.ttl`](../examples/blade-replacement.ttl)

**Story.** Turbine T07 was commissioned on 20 May 2016 with three ACME B-73P blades. On 11 June 2024 the blade in position B failed and was removed; a new B-73P went in on 18 June. The other two are still the originals. Figures are taken as of 7 September 2026.

### What gets modelled

| Thing | WESO class | How many |
|---|---|---|
| Aerodynamic torque function | function type (`owl:Class` under `ComponentFunction`) | 1 class |
| Blade | component type (`owl:Class` under `ComponentUnit`) | 1 class |
| ACME B-73P rev C | `ComponentModel` | 1 |
| Blade position (fleet-wide) | `PositionKind` | 1 |
| Blade positions A, B, C on T07 | `ComponentPosition` | 3 |
| Physical blades | instances of `Blade` | 4 |
| Which blade was where, when | `PositionOccupancy` | 4 |
| RDS tags and serial numbers | `Designation` | 10 |

### Things worth noticing

**The three positions are identical.** Same kind, same turbine, same parent, same prescribed function. Strip the labels and nothing distinguishes them except the designations pointing at them — and the RDS guideline itself says its counting numbers carry no meaning. That is not a gap in the model; it is the model reporting accurately that the only difference between blade 1 and blade 2 is a convention. (Test: `test_blade_positions_differ_only_by_designation`.)

**Two designations, one position, two trees.** Blade B is both `=A1=RB1=RB2` (function aspect, nested under the rotor system) and `-A1-RB2` (product aspect, directly under the turbine). Both resolve to the same position.

**Nobody wrote "replacement".** Serial 4417 is a replacement because an earlier occupancy of position B exists. The query [`original-vs-replacement.rq`](../examples/queries/original-vs-replacement.rq) derives it.

**Catalogue mass and real mass are separate.** The model says 27 500 kg. Each blade carries its own weighed figure.

### What it contributes to fleet statistics

| | Value |
|---|---|
| Blade positions | 3 |
| Occupancies | 4 |
| Exposure | 10.30 + 8.06 + 2.22 + 10.30 = **30.88 position-years** |
| Failures | 1 |

The two tempting alternatives are both wrong:

- *Turbine-years* (10.3) charges one turbine's time against three blades and overstates the blade failure rate threefold.
- *Unit count* (4) lets the replacement inflate the population to four blade-lives on a three-blade machine.

Run it yourself:

```python
# from the repository root
import sys; sys.path.insert(0, "scripts")
from datetime import date
from wesotools import load, exposure
g = load("examples/blade-replacement.ttl")
exposure(g, date(2026, 9, 7))["https://example.org/fleet/pk-blade"]
# KindExposure(positions=3, occupancies=4, years=30.88..., failures=1)
```

## 2. Planet bearing — [`planet-bearing.ttl`](../examples/planet-bearing.ttl)

**Story.** T07's gearbox, an ACME GB-4200 (serial 000-00-125), has a planetary stage with three planet bearings. The bearing in position 2 failed on 30 August 2023 and was replaced on 4 September. The gearbox oil was changed in March 2024.

### Things worth noticing

**All four RDS aspects, four different landing places.**

| Designation | Aspect | Names |
|---|---|---|
| `=A1=JF2` | function | the gearbox position |
| `-A1-JF1` | product | the same gearbox position |
| `+A1+JF1` | host | the gearbox position, as host of the bearings |
| `++A1++LA1` | site | the nacelle — a space |

The gear system is `JF2` in one tree and `JF1` in the other. If the aspects were just different prefixes on one identifier, the numbers would agree. They don't, which is why WESO keeps a separate parent link per tree.

**Same-looking strings, different targets.** `GB4200-PLB-225` comes from ACME's parts catalogue and names a component model. `88113` comes from ACME's serial register and names one bearing. The scheme decides; `resolve-designation.rq` shows it. (Test: `test_same_shape_string_resolves_by_scheme`.)

**Depth beyond the standard.** RDS for WTG standardises the gear system down to its bearing system. The planet bearing tags go two levels deeper using a (hypothetical) manufacturer extension. Each designation records its depth, so a consumer can tell standardised from extended.

**Multiplicity.** Three planet bearing positions per gearbox. A per-turbine count would miss two thirds of the exposure.

**Shared oil.** One oil charge fills one position, but every bearing in the gearbox depends on it. Failures across the three bearing positions are therefore correlated — pooling them as independent observations understates the uncertainty. WESO makes the dependency visible; quantifying it is an analysis task.

### Optional: labelling results for an external scheme

[`planet-bearing-reporting-labels.ttl`](../examples/planet-bearing-reporting-labels.ttl) attaches categories from the Reliawind component taxonomy to the position kinds, so results can be exported under those names. The test `test_reporting_labels_do_not_change_results` loads the example with and without this file and checks that every number is identical. The external vocabulary is a label on the output, never an input to the calculation.

## 3. Mistakes the shapes catch — [`tests/fixtures/`](../tests/fixtures)

Each fixture is a small, deliberately wrong addition to one of the examples. All must fail validation.

| Fixture | The mistake |
|---|---|
| `rds-tag-names-a-unit.ttl` | An RDS tag mapped onto a serialised blade instead of its slot |
| `part-number-names-a-unit.ttl` | A catalogue part number mapped onto one physical bearing |
| `wrong-function-in-slot.ttl` | A gearbox recorded as occupying a blade position |
| `two-units-one-slot.ttl` | A second blade in a slot whose original was never removed |
| `occupancy-ends-before-start.ttl` | End date before start date |
| `scheme-without-contract.ttl` | A scheme with no projection rules — accepted, with a warning |
