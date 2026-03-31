
from __future__ import annotations

SUPPORTED_FAILURE_CLASSES = {
    "taxonomy_leakage": {
        "keywords": ["category", "taxonomy", "wrong category", "kids", "women", "men"],
        "actions": [
            "Review taxonomy mappings for top shifted results",
            "Add intent guardrails for category-sensitive queries",
            "Test category-restricted regression queries before rollout",
        ],
    },
    "attribute_mismatch": {
        "keywords": ["material", "color", "size", "attribute", "catalog sync", "cotton", "wool"],
        "actions": [
            "Audit attribute population for affected products",
            "Rebuild affected filter facets after attribute correction",
            "Run material-sensitive regression checks",
        ],
    },
    "synonym_gap": {
        "keywords": ["synonym", "alias", "spelling", "typo"],
        "actions": [
            "Inspect synonym dictionary changes for impacted terms",
            "Add missing synonym mappings only for validated query intents",
            "Run regression checks across common spelling variants",
        ],
    },
    "ranking_override_conflict": {
        "keywords": ["boost", "merchandising", "override", "rule", "rules deploy"],
        "actions": [
            "Review recent ranking or merchandising overrides",
            "Reduce broad overrides affecting intent-sensitive terms",
            "Validate top-result shifts with a focused regression set",
        ],
    },
    "inventory_bleed": {
        "keywords": ["inventory", "out of stock", "availability", "bleed"],
        "actions": [
            "Check inventory feed freshness and availability joins",
            "Verify out-of-stock suppression logic",
            "Add regression queries for in-stock ranking expectations",
        ],
    },
    "filter_logic_issue": {
        "keywords": ["filter", "facet", "refine", "logic"],
        "actions": [
            "Review filter defaults and facet application order",
            "Verify hidden filters after recent release changes",
            "Test affected queries with and without default filters",
        ],
    },
    "zero_result_spike": {
        "keywords": ["zero results", "returns zero", "no results", "0 results"],
        "actions": [
            "Review exact-match and filter interactions for affected queries",
            "Check recent changes to default availability constraints",
            "Add zero-result monitoring queries to regression coverage",
        ],
    },
    "mixed_or_unclear": {
        "keywords": [],
        "actions": [
            "Gather before/after result snapshots",
            "Collect release context and query-level metrics",
            "Escalate for human review once evidence is complete",
        ],
    },
}
