"""WESO test suite.

Each test pins down a claim the documentation makes. If a change to the kernel
breaks one of these, either the change is wrong or the docs need to change too.

    python -m pytest -v
"""
import sys
from datetime import date
from pathlib import Path

import pytest
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from wesotools import WESO, exposure, load, load_jsonld, query, validate  # noqa: E402

EX = "https://example.org/fleet/"
AS_OF = date(2026, 9, 7)
EXAMPLES = sorted((ROOT / "examples").glob("*.ttl"))
CORE = ROOT / "ontology" / "weso-core.ttl"


# --- the ontology itself -------------------------------------------------------

def test_core_parses():
    assert len(Graph().parse(CORE, format="turtle")) > 100


def test_every_kernel_term_is_documented():
    """Contributors must give every class a label and a definition or scope note,
    and every property a label. This keeps the kernel readable for newcomers."""
    g = Graph().parse(CORE, format="turtle")
    missing = []
    for cls in g.subjects(RDF.type, OWL.Class):
        if not str(cls).startswith(str(WESO)):
            continue
        if not g.value(cls, RDFS.label):
            missing.append(f"{cls} has no rdfs:label")
        if not (g.value(cls, SKOS.definition) or g.value(cls, SKOS.scopeNote)):
            missing.append(f"{cls} has no skos:definition or skos:scopeNote")
    for kind in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):
        for p in g.subjects(RDF.type, kind):
            if str(p).startswith(str(WESO)) and not g.value(p, RDFS.label):
                missing.append(f"{p} has no rdfs:label")
    assert not missing, "\n".join(missing)


def test_no_object_property_points_at_a_class():
    """ADR-0008: pointers from individuals to classes are annotation properties.
    An object property with range owl:Class would push the kernel out of OWL 2 DL."""
    g = Graph().parse(CORE, format="turtle")
    offenders = [p for p in g.subjects(RDF.type, OWL.ObjectProperty)
                 if (p, RDFS.range, OWL.Class) in g]
    assert not offenders


# --- examples conform --------------------------------------------------------------

@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_examples_conform_without_warnings(path):
    ok, results = validate(load(path))
    assert ok, results
    assert not results, results


# --- shapes catch what they claim to catch --------------------------------------------

@pytest.mark.parametrize(
    "fixture, shape_fragment",
    [
        ("rds-tag-names-a-unit.ttl", "DesignationTargetShape"),
        ("part-number-names-a-unit.ttl", "DesignationTargetShape"),
        ("wrong-function-in-slot.ttl", "OccupancyShape"),
        ("two-units-one-slot.ttl", "OccupancyShape"),
        ("occupancy-ends-before-start.ttl", "OccupancyShape"),
    ],
)
def test_invalid_fixture_is_rejected(fixture, shape_fragment):
    ok, results = validate(load(ROOT / "tests" / "fixtures" / fixture))
    assert not ok
    assert any(shape_fragment in r["shape"] and r["severity"] == "Violation" for r in results)


def test_scheme_without_contract_warns_but_conforms():
    ok, results = validate(load(ROOT / "tests" / "fixtures" / "scheme-without-contract.ttl"))
    assert ok
    assert [r["severity"] for r in results] == ["Warning"]


# --- the blade example: the numbers in docs/worked-examples.md ------------------------

@pytest.fixture(scope="module")
def blades():
    return load(ROOT / "examples" / "blade-replacement.ttl")


def test_blade_exposure_is_counted_per_position(blades):
    e = exposure(blades, AS_OF)[EX + "pk-blade"]
    assert e.positions == 3          # not 1 turbine
    assert e.occupancies == 4        # 3 originals + 1 replacement
    assert e.failures == 1
    assert e.years == pytest.approx(30.88, abs=0.01)   # not 10.3 turbine-years


def test_original_and_replacement_are_derived_not_asserted(blades):
    roles = {str(r.item).removeprefix(EX): str(r.role)
             for r in query(blades, "original-vs-replacement")}
    assert roles == {"blade-sn-1001": "original", "blade-sn-1002": "original",
                     "blade-sn-1003": "original", "blade-sn-4417": "replacement"}
    assert not list(blades.subjects(RDF.type, WESO.OccupancyRole))


def test_blade_positions_differ_only_by_designation(blades):
    """The three blade slots carry identical facts apart from labels; only the
    designations that point at them tell them apart (docs/core-concepts.md)."""
    def facts(pos):
        return {(p, o) for p, o in blades.predicate_objects(URIRef(EX + pos)) if p != RDFS.label}
    assert facts("pos-T07-blade-A") == facts("pos-T07-blade-B") == facts("pos-T07-blade-C")


@pytest.mark.parametrize("string, expected_target, expected_kind", [
    ("-A1-RB2", "pos-T07-blade-B", "ComponentPosition"),
    ("=A1=RB1=RB2", "pos-T07-blade-B", "ComponentPosition"),
    ("ACME-B73P-4417", "blade-sn-4417", "ComponentUnit"),
])
def test_designation_resolution(blades, string, expected_target, expected_kind):
    rows = list(query(blades, "resolve-designation", string=Literal(string)))
    assert len(rows) == 1
    assert str(rows[0].target) == EX + expected_target
    assert str(rows[0].kindOfThing) == str(WESO) + expected_kind


# --- the planet bearing example ---------------------------------------------------------

@pytest.fixture(scope="module")
def gearbox():
    return load(ROOT / "examples" / "planet-bearing.ttl")


def test_planet_bearing_multiplicity(gearbox):
    e = exposure(gearbox, AS_OF)[EX + "pk-planet-bearing"]
    assert e.positions == 3
    assert e.occupancies == 4
    assert e.failures == 1


def test_rds_aspects_land_on_different_primitives(gearbox):
    targets = {}
    for d in gearbox.subjects(WESO.fromScheme,
                              URIRef("https://w3id.org/ontoforge/weso/align/rds-wtg/scheme")):
        label = str(gearbox.value(d, RDFS.label))
        target = gearbox.value(d, WESO.designates)
        targets[label[:2] if label.startswith("++") else label[0]] = set(gearbox.objects(target, RDF.type))
    assert WESO.ComponentPosition in targets["="]
    assert WESO.ComponentPosition in targets["-"]
    assert WESO.ComponentPosition in targets["+"]
    assert WESO.Space in targets["++"]


def test_same_shape_string_resolves_by_scheme(gearbox):
    """A part number names a model; a serial names a unit."""
    part = list(query(gearbox, "resolve-designation", string=Literal("GB4200-PLB-225")))
    serial = list(query(gearbox, "resolve-designation", string=Literal("88113")))
    assert str(part[0].kindOfThing) == str(WESO.ComponentModel)
    assert str(serial[0].kindOfThing) == str(WESO.ComponentUnit)


# --- external vocabularies are optional -------------------------------------------------

def test_reporting_labels_do_not_change_results():
    """ADR-0003: aggregation runs on WESO's own position kinds. Loading an
    external reporting vocabulary adds labels and changes nothing else."""
    plain = exposure(load(ROOT / "examples" / "planet-bearing.ttl"), AS_OF)
    labelled_graph = load(ROOT / "examples" / "planet-bearing-reporting-labels.ttl")
    assert exposure(labelled_graph, AS_OF) == plain
    labels = {str(r.kind).removeprefix(EX): r.label for r in query(labelled_graph, "export-with-reporting-labels")}
    assert str(labels["pk-planet-bearing"]).endswith("GearboxBearingPlanet")


# --- JSON-LD for APIs -------------------------------------------------------------------

def test_jsonld_update_merges_and_conforms():
    """An API payload in JSON-LD (a blade swap on position C) merges into the
    Turtle example, validates, and moves the numbers the way it should."""
    g = load(ROOT / "examples" / "blade-replacement.ttl")
    load_jsonld(ROOT / "examples" / "json-ld" / "blade-swap-event.jsonld", into=g)
    ok, results = validate(g)
    assert ok and not results, results
    e = exposure(g, AS_OF.replace(month=12, day=31))[EX + "pk-blade"]
    assert (e.positions, e.occupancies) == (3, 5)
    roles = {str(r.item).removeprefix(EX): str(r.role) for r in query(g, "original-vs-replacement")}
    assert roles["blade-sn-5120"] == "replacement"
