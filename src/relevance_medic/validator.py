
from __future__ import annotations
from pathlib import Path
from jsonschema import validate

from .utils import load_json

ROOT = Path(__file__).resolve().parents[2]

def validate_incident(incident: dict) -> None:
    schema = load_json(ROOT / "schemas" / "incident_input.schema.json")
    validate(instance=incident, schema=schema)

def validate_diagnosis(diagnosis: dict) -> None:
    schema = load_json(ROOT / "schemas" / "diagnosis_output.schema.json")
    validate(instance=diagnosis, schema=schema)
