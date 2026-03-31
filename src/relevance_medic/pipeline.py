
from __future__ import annotations
from typing import Any

from .logic import should_abstain, classify_failure, recommended_actions, regression_tests
from .validator import validate_incident, validate_diagnosis

def diagnose_incident(incident: dict[str, Any]) -> dict[str, Any]:
    validate_incident(incident)

    abstain, missing = should_abstain(incident)
    if abstain:
        diagnosis = {
            "incident_id": incident["incident_id"],
            "status": "abstained",
            "confidence_band": "low",
            "failure_class": "mixed_or_unclear",
            "evidence_used": [],
            "missing_evidence": missing,
            "recommended_actions": [
                "Gather before/after search result snapshots",
                "Attach release context for recent search-related changes",
                "Re-run diagnosis after evidence is complete",
            ],
            "regression_tests": [],
        }
        validate_diagnosis(diagnosis)
        return diagnosis

    label, confidence, evidence = classify_failure(incident)
    diagnosis = {
        "incident_id": incident["incident_id"],
        "status": "diagnosed",
        "confidence_band": confidence,
        "failure_class": label,
        "evidence_used": evidence,
        "missing_evidence": missing,
        "recommended_actions": recommended_actions(label),
        "regression_tests": regression_tests(incident, label),
    }
    validate_diagnosis(diagnosis)
    return diagnosis
