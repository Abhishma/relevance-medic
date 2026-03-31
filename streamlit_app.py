
from __future__ import annotations
import json
from pathlib import Path
import streamlit as st

from relevance_medic.pipeline import diagnose_incident
from relevance_medic.utils import load_json, load_jsonl

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "examples"
SYNTH_DIR = ROOT / "data" / "synthetic"

st.set_page_config(page_title="Relevance Medic", layout="wide")
st.title("Relevance Medic")
st.caption("AI-assisted ecommerce search incident diagnostics with abstention and regression tests.")

example_files = sorted([p.name for p in DATA_DIR.glob("*.json")])

with st.sidebar:
    st.header("Load incident")
    selected = st.selectbox("Example incident", example_files, index=0 if example_files else None)
    load_btn = st.button("Load example")
    st.markdown("---")
    st.markdown("**Demo framing**")
    st.markdown("- Diagnosis, not chat")
    st.markdown("- Evidence before confidence")
    st.markdown("- Abstain when under-informed")
    st.markdown("- Human review before fixes")

incident = None
if load_btn and selected:
    incident = load_json(DATA_DIR / selected)
elif selected:
    incident = load_json(DATA_DIR / selected)

col1, col2 = st.columns([1,1])

with col1:
    st.subheader("Incident input")
    if incident:
        st.json(incident)
    else:
        st.info("No incident loaded.")

with col2:
    st.subheader("Diagnosis output")
    if incident:
        diagnosis = diagnose_incident(incident)
        st.json(diagnosis)

        if diagnosis["status"] == "abstained":
            st.warning("System abstained. This is intentional when evidence is incomplete.")
        else:
            st.success(f"Diagnosed as: {diagnosis['failure_class']}")

        st.markdown("### Portfolio interpretation")
        if diagnosis["status"] == "abstained":
            st.write("This refusal is a feature. It shows the system has boundaries and does not fake certainty.")
        else:
            st.write("This output is designed to reduce triage ambiguity and create reusable incident discipline.")
    else:
        st.info("Load an incident to view diagnosis.")

st.markdown("---")
st.subheader("Quick evaluation snapshot")
if st.button("Run eval on synthetic set"):
    incidents = SYNTH_DIR / "incidents.jsonl"
    expected = SYNTH_DIR / "expected_labels.jsonl"
    inc_rows = {row["incident_id"]: row for row in load_jsonl(incidents)}
    exp_rows = load_jsonl(expected)

    total = len(exp_rows)
    class_ok = 0
    abstain_ok = 0
    results = []
    for exp in exp_rows:
        pred = diagnose_incident(inc_rows[exp["incident_id"]])
        ck = pred["failure_class"] == exp["expected_failure_class"]
        ak = (pred["status"] == "abstained") == exp["should_abstain"]
        class_ok += int(ck)
        abstain_ok += int(ak)
        results.append({
            "incident_id": exp["incident_id"],
            "predicted": pred["failure_class"],
            "expected": exp["expected_failure_class"],
            "status": pred["status"],
            "class_ok": ck,
            "abstain_ok": ak
        })

    metric1, metric2 = st.columns(2)
    metric1.metric("Classification accuracy", f"{class_ok/total:.0%}")
    metric2.metric("Abstention accuracy", f"{abstain_ok/total:.0%}")
    st.dataframe(results, use_container_width=True)
