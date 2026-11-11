#!/usr/bin/env bash
# Check that the kernel and every example are valid OWL 2 DL, logically
# consistent, and free of unsatisfiable classes. Requires Java and ROBOT.
#
#   ROBOT_JAR=/path/to/robot.jar scripts/check-owl.sh
#
# CI downloads ROBOT automatically (.github/workflows/ci.yml).
set -euo pipefail
cd "$(dirname "$0")/.."
JAR="${ROBOT_JAR:-robot.jar}"
OUT=$(mktemp -d)
status=0

check () {
  local catalog=$1 name=$2; shift 2
  local ROBOT="java -jar $JAR --catalog $catalog"
  printf '%-48s' "$name"
  if ! $ROBOT merge "$@" validate-profile --profile DL -o "$OUT/$name.profile.txt" >/dev/null 2>&1; then
    echo "NOT OWL 2 DL"; sed -n '1,15p' "$OUT/$name.profile.txt"; status=1; return
  fi
  if ! $ROBOT merge "$@" reason --reasoner hermit --equivalent-classes-allowed asserted-only \
        -o "$OUT/$name.reasoned.owl" >"$OUT/$name.reason.log" 2>&1; then
    echo "REASONER FAILED"; tail -5 "$OUT/$name.reason.log"; status=1; return
  fi
  echo "ok (DL, consistent, all classes satisfiable)"
}

check ontology/catalog-v001.xml           weso-core -i ontology/weso-core.ttl
check alignments/rds-wtg/catalog-v001.xml rds-wtg   -i alignments/rds-wtg/rds-wtg.ttl
for ex in examples/*.ttl; do
  check examples/catalog-v001.xml "$(basename "$ex" .ttl)" -i "$ex"
done
exit $status
