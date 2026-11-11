"""Small helpers for working with WESO from Python.

    from wesotools import load, validate, exposure

load()      parses a Turtle file and follows owl:imports using local copies
            (the same mapping as ontology/catalog-v001.xml), so nothing is
            fetched from the web.
validate()  runs the core SHACL shapes and returns (conforms, results).
exposure()  sums position-time per position kind as of a given date.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from xml.etree import ElementTree

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import OWL, RDF

ROOT = Path(__file__).resolve().parent.parent
WESO = Namespace("https://w3id.org/ontoforge/weso/")
SH = Namespace("http://www.w3.org/ns/shacl#")
CATALOG = ROOT / "ontology" / "catalog-v001.xml"
SHAPES = ROOT / "shapes" / "weso-core-shapes.ttl"
QUERIES = ROOT / "examples" / "queries"


def _catalog() -> dict[str, Path]:
    """Read ontology/catalog-v001.xml into {IRI: local file}."""
    ns = {"c": "urn:oasis:names:tc:entity:xmlns:xml-catalog"}
    tree = ElementTree.parse(CATALOG)
    base = CATALOG.parent
    mapping = {
        el.get("name"): (base / el.get("uri")).resolve()
        for el in tree.getroot().findall("c:uri", ns)
    }
    # Examples import each other by their ontology IRI.
    for ttl in (ROOT / "examples").glob("*.ttl"):
        mapping[f"https://example.org/fleet/{ttl.stem}"] = ttl
    return mapping


def load(*paths: str | Path, follow_imports: bool = True) -> Graph:
    """Parse files into one graph, resolving owl:imports from local copies."""
    mapping = _catalog()
    g = Graph()
    seen: set[Path] = set()
    queue = [Path(p).resolve() for p in paths]
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        fmt = "xml" if path.suffix == ".owl" else "turtle"
        part = Graph().parse(path, format=fmt)
        g += part
        if follow_imports:
            for iri in part.objects(None, OWL.imports):
                local = mapping.get(str(iri))
                if local is None:
                    raise FileNotFoundError(f"No local copy for import {iri} (from {path})")
                queue.append(local)
    for prefix, ns in Graph().parse(paths[0], format="turtle").namespaces():
        g.bind(prefix, ns)
    return g


CONTEXT = ROOT / "ontology" / "weso-context.jsonld"


def load_jsonld(path: str | Path, into: Graph | None = None) -> Graph:
    """Parse a JSON-LD document that uses the WESO context, offline.

    The published context IRI is replaced by the local file, so nothing is
    fetched from the web.
    """
    import json

    doc = json.loads(Path(path).read_text())
    local = json.loads(CONTEXT.read_text())["@context"]
    ctx = doc.get("@context")
    ctx = ctx if isinstance(ctx, list) else [ctx]
    doc["@context"] = [local if c == "https://w3id.org/ontoforge/weso/context.jsonld" else c for c in ctx]
    g = into if into is not None else Graph()
    g.parse(data=json.dumps(doc), format="json-ld")
    return g


def validate(data: Graph) -> tuple[bool, list[dict]]:
    """Run core shapes. Returns (no violations, list of results)."""
    from pyshacl import validate as shacl_validate

    shapes = Graph().parse(SHAPES, format="turtle")
    _, report, _ = shacl_validate(
        data, shacl_graph=shapes, inference="none", advanced=True, allow_warnings=True
    )
    results = []
    for r in report.subjects(RDF.type, SH.ValidationResult):
        results.append(
            {
                "severity": str(report.value(r, SH.resultSeverity)).split("#")[-1],
                "focus": str(report.value(r, SH.focusNode)),
                "shape": str(report.value(r, SH.sourceShape)),
                "message": str(report.value(r, SH.resultMessage)),
            }
        )
    no_violations = not any(r["severity"] == "Violation" for r in results)
    return no_violations, results


def query(g: Graph, name: str, **bindings):
    text = (QUERIES / f"{name}.rq").read_text()
    init = {k: (URIRef(v) if isinstance(v, str) and v.startswith("http") else v)
            for k, v in bindings.items()}
    return g.query(text, initBindings=init or None)


@dataclass
class KindExposure:
    kind: str
    positions: int
    occupancies: int
    years: float
    failures: int


def _as_date(value) -> date:
    return value.date() if hasattr(value, "date") else value


def exposure(g: Graph, as_of: date) -> dict[str, KindExposure]:
    """Position-years and failures per position kind.

    Exposure is summed over occupancies, so a replacement adds time to the same
    position rather than adding a new member to the population.
    """
    acc: dict[str, dict] = defaultdict(lambda: {"pos": set(), "occ": 0, "days": 0, "fail": 0})
    for row in query(g, "exposure"):
        a = acc[str(row.kind)]
        a["pos"].add(str(row.pos))
        a["occ"] += 1
        start = _as_date(row.start.toPython())
        end = _as_date(row.end.toPython()) if row.end is not None else as_of
        a["days"] += (min(end, as_of) - start).days
        a["fail"] += int(row.failures)
    return {
        k: KindExposure(k, len(v["pos"]), v["occ"], v["days"] / 365.25, v["fail"])
        for k, v in acc.items()
    }


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: python scripts/validate.py FILE.ttl [FILE.ttl ...]")
        return 2
    g = load(*argv)
    ok, results = validate(g)
    for r in results:
        print(f"[{r['severity']}] {r['message']}")
    print(f"{len(g)} triples, {'conforms' if ok else 'DOES NOT CONFORM'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
