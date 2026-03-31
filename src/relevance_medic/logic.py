
from __future__ import annotations
from collections import Counter
from typing import Any

from .taxonomy import SUPPORTED_FAILURE_CLASSES

def _text_blob(incident: dict[str, Any]) -> str:
    parts = [
        incident.get("narrative", ""),
        incident.get("release_context", ""),
        incident.get("facet_context", ""),
    ]
    for q in incident.get("queries", []):
        parts.append(q.get("query_text", ""))
        parts.extend(q.get("before_results", []) or [])
        parts.extend(q.get("after_results", []) or [])
    return " ".join(parts).lower()

def detect_missing_evidence(incident: dict[str, Any]) -> list[str]:
    missing = []
    queries = incident.get("queries", [])
    if not queries:
        missing.append("No query examples provided")
    else:
        if any(not q.get("before_results") for q in queries):
            missing.append("Missing before-results snapshot for one or more queries")
        if any(q.get("after_results") is None for q in queries):
            missing.append("Missing after-results snapshot for one or more queries")
    if not incident.get("release_context"):
        missing.append("Missing release context")
    return missing

def should_abstain(incident: dict[str, Any]) -> tuple[bool, list[str]]:
    missing = detect_missing_evidence(incident)
    if any("before-results" in m for m in missing):
        return True, missing
    return False, missing

def classify_failure(incident: dict[str, Any]) -> tuple[str, str, list[str]]:
    blob = _text_blob(incident)
    scores: Counter[str] = Counter()
    evidence: list[str] = []

    ctr = incident.get("metrics_snapshot", {}).get("ctr_delta_pct", 0)
    zero_results = incident.get("metrics_snapshot", {}).get("zero_result_rate_delta_pct", 0)

    for label, cfg in SUPPORTED_FAILURE_CLASSES.items():
        for kw in cfg["keywords"]:
            if kw in blob:
                scores[label] += 2

    if zero_results >= 20:
        scores["zero_result_spike"] += 4
        evidence.append(f"Zero-result rate increased by {zero_results}%")
    if "kids" in blob and "kurta" in blob:
        scores["ranking_override_conflict"] += 2
        scores["taxonomy_leakage"] += 1
        evidence.append("Results appear contaminated by kids-category items for an adult-intent query")
    if "catalog sync" in blob or "attribute" in blob or ("wool" in blob and "cotton" in blob):
        scores["attribute_mismatch"] += 3
        evidence.append("Catalog/attribute signals suggest mismatched product attributes")
    if "synonym" in blob or "alias" in blob:
        scores["synonym_gap"] += 3
        evidence.append("Recent synonym change mentioned for the affected query family")
    if "inventory" in blob or "out-of-stock" in blob or "availability badges stale" in blob:
        scores["inventory_bleed"] += 3
        evidence.append("Inventory freshness or availability suppression appears inconsistent")
    if "merchandising" in blob or "boost" in blob or "rules deploy" in blob:
        scores["ranking_override_conflict"] += 3
        evidence.append("Recent merchandising or ranking rule change mentioned")
    if ctr <= -10:
        evidence.append(f"CTR declined by {abs(ctr)}%")

    if not scores:
        return "mixed_or_unclear", "low", evidence

    top_two = scores.most_common(2)
    top_label, top_score = top_two[0]
    if len(top_two) > 1 and top_two[0][1] - top_two[1][1] <= 1:
        return "mixed_or_unclear", "low", evidence

    confidence = "high" if top_score >= 6 else "medium"
    return top_label, confidence, evidence

def recommended_actions(label: str) -> list[str]:
    return SUPPORTED_FAILURE_CLASSES.get(label, SUPPORTED_FAILURE_CLASSES["mixed_or_unclear"])["actions"]

def regression_tests(incident: dict[str, Any], label: str) -> list[str]:
    qs = [q.get("query_text", "") for q in incident.get("queries", []) if q.get("query_text")]
    tests = []
    for q in qs[:3]:
        tests.append(f"Verify '{q}' top results align with intended product type after fix")
    if label == "attribute_mismatch":
        tests.append("Verify material-sensitive queries do not surface attribute-conflicting products")
    elif label == "ranking_override_conflict":
        tests.append("Verify merchandising overrides do not outrank core-intent products for protected queries")
    elif label == "zero_result_spike":
        tests.append("Verify affected queries return at least 3 relevant results without hidden filter leakage")
    return tests
