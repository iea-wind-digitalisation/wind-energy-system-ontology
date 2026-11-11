# Publishing

WESO's namespace is `https://w3id.org/ontoforge/weso/`. [w3id.org](https://w3id.org) provides permanent identifiers by redirect; the redirect rules live in the `perma-id/w3id.org` repository and are changed by pull request.

`w3id.htaccess` is a draft for that pull request. Before submitting, replace `OWNER` with the GitHub account that will host this repository, and decide where rendered documentation will live (GitHub Pages is assumed).

## Release checklist

1. Update `owl:versionIRI` and `owl:versionInfo` in `ontology/weso-core.ttl`.
2. Move the `[Unreleased]` section of `CHANGELOG.md` under the new version.
3. Update `version` and `date-released` in `CITATION.cff`.
4. Tag the release (`v0.2.0`) and attach `weso-core.ttl` and a merged `weso-full.owl`:
   `java -jar robot.jar --catalog ontology/catalog-v001.xml merge -i ontology/weso-core.ttl -o weso-full.owl`
