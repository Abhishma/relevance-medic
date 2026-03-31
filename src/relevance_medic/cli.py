
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .pipeline import diagnose_incident
from .utils import load_json

def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose an ecommerce search incident.")
    parser.add_argument("incident_path", help="Path to incident JSON file")
    args = parser.parse_args()

    incident = load_json(Path(args.incident_path))
    result = diagnose_incident(incident)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
