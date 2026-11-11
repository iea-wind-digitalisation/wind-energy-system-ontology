"""Validate WESO data against the core shapes.

    python scripts/validate.py examples/blade-replacement.ttl
    python scripts/validate.py my-fleet.ttl

owl:imports are resolved from local copies; include the WESO import in your
file (or pass weso-core.ttl alongside it) so subclass reasoning is available.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wesotools import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
