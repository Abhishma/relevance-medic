
from relevance_medic.pipeline import diagnose_incident

def test_abstain_on_missing_before_results():
    incident = {
        "incident_id": "T-1",
        "narrative": "Search seems wrong",
        "queries": [{"query_text": "blue sofa", "before_results": [], "after_results": ["x"]}],
        "metrics_snapshot": {"ctr_delta_pct": -2.0, "conversion_delta_pct": 0.0, "zero_result_rate_delta_pct": 0.0},
        "release_context": "",
        "facet_context": ""
    }
    result = diagnose_incident(incident)
    assert result["status"] == "abstained"

def test_detect_attribute_mismatch():
    incident = {
        "incident_id": "T-2",
        "narrative": "Search for wool rug returns cotton rugs after catalog sync",
        "queries": [{"query_text": "wool rug", "before_results": ["wool rug A"], "after_results": ["cotton rug B"]}],
        "metrics_snapshot": {"ctr_delta_pct": -12.0, "conversion_delta_pct": -4.0, "zero_result_rate_delta_pct": 0.0},
        "release_context": "catalog sync overnight",
        "facet_context": "material facet inconsistent"
    }
    result = diagnose_incident(incident)
    assert result["failure_class"] == "attribute_mismatch"
