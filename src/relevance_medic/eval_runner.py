
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path

from .pipeline import diagnose_incident
from .utils import load_jsonl

def main() -> None:
    parser = argparse.ArgumentParser(description="Run simple eval over labeled incidents.")
    parser.add_argument("incidents_path")
    parser.add_argument("expected_path")
    args = parser.parse_args()

    incidents = {row["incident_id"]: row for row in load_jsonl(Path(args.incidents_path))}
    expected = load_jsonl(Path(args.expected_path))

    total = len(expected)
    class_matches = 0
    abstain_matches = 0
    predicted_counter = Counter()
    expected_counter = Counter()
    rows = []

    for exp in expected:
        incident = incidents[exp["incident_id"]]
        result = diagnose_incident(incident)
        class_ok = result["failure_class"] == exp["expected_failure_class"]
        abstain_ok = (result["status"] == "abstained") == exp["should_abstain"]
        class_matches += int(class_ok)
        abstain_matches += int(abstain_ok)
        predicted_counter[result["failure_class"]] += 1
        expected_counter[exp["expected_failure_class"]] += 1
        rows.append({
            "incident_id": exp["incident_id"],
            "predicted": result["failure_class"],
            "expected": exp["expected_failure_class"],
            "status": result["status"],
            "class_ok": class_ok,
            "abstain_ok": abstain_ok,
        })

    summary = {
        "total_cases": total,
        "classification_accuracy": round(class_matches / total, 3) if total else 0.0,
        "abstention_accuracy": round(abstain_matches / total, 3) if total else 0.0,
        "predicted_distribution": dict(predicted_counter),
        "expected_distribution": dict(expected_counter),
        "rows": rows,
    }
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
