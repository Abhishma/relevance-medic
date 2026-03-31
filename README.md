# Relevance Medic

AI-assisted diagnosis for ecommerce search failures — with evidence, abstention, and regression test generation.

## Why this exists

Search incidents are messy. A stakeholder says "search is broken," support shares screenshots,
engineering checks logs, and product guesses whether it is ranking, taxonomy, synonyms, inventory,
filters, or merchandising rules. Most teams do not have a consistent diagnostic language.

This workflow is informed by real ecommerce search incident patterns observed across multi-brand D2C platforms,
where the recurring failure is not a lack of data but a lack of structured diagnostic language.

**Relevance Medic** turns search complaints into a structured incident review:
- likely failure pattern
- evidence used
- missing evidence
- confidence band
- minimal fix options
- regression tests to add
- abstention when the system is under-informed

This is intentionally **not** a chatbot. It is a workflow tool for reducing ambiguity in ecommerce search operations.

## What it does

Input:
- incident narrative
- before/after result snapshots
- query-level metrics
- facet/filter context
- release metadata

Output:
- failure classification
- evidence-backed hypothesis
- missing-evidence checklist
- low-risk fix suggestions
- regression queries and expected result checks
- abstention when confidence is weak

## What it does not do

- It does not auto-edit ranking rules
- It does not auto-ship fixes
- It does not pretend certainty where evidence is thin

## Run

```bash
pip install -r requirements.txt
python -m relevance_medic.cli data/examples/incident_001.json
python -m relevance_medic.eval_runner data/synthetic/incidents.jsonl data/synthetic/expected_labels.jsonl
streamlit run streamlit_app.py
```

## Suggested demo flow

1. Open the Streamlit app
2. Load `INC-001` for a confident diagnosis
3. Load `INC-003` for an abstention case
4. Run the eval harness and show accuracy and abstention behavior
5. Explain why the system refuses when key evidence is missing

## Design choices

- **Constrained taxonomy, not open-ended prose** — the failure taxonomy is bounded and auditable by design. A constrained heuristic classifier is safer in a reviewer workflow than a model that generates plausible but unverifiable diagnoses.
- **v1 uses keyword-based heuristic classification** — this is intentional. It is transparent, evaluable, and directly auditable. The upgrade path to scored retrieval or a model-assisted classifier is documented in Known Limitations.
- Evidence-linked outputs — every classification cites the evidence that triggered it
- Explicit abstention when key evidence is missing — the system refuses rather than guesses
- Minimal, testable recommendations — human review remains mandatory

## Repo structure

- `src/relevance_medic/` — core implementation
- `data/` — example and synthetic incidents
- `schemas/` — input/output JSON schemas
- `eval/` — rubric and evaluation harness
- `demo/` — sample reports

## Portfolio point

This repo is about diagnostics over AI theater. The PM design decisions are the artifact: what inputs are required, what outputs are structured, where the system stops, and how you evaluate it.

## v2 additions

This version adds:
- a minimal Streamlit review UI
- richer synthetic gold cases
- explicit refusal and abstention scenarios
- cleaner evaluation workflow
- screenshot-friendly output for portfolio presentation

## Known limitations

- v2 uses a bounded heuristic classifier, not a production-grade relevance diagnosis engine
- synthetic incidents are realistic but still simulated
- the system is strongest at triage structure, not root-cause certainty
- recommendations are intentionally low-risk and generic enough for human review
- next upgrade: replace heuristics with scored retrieval and a rule layer, add 20+ realistic incidents, add HTML report export

## Where automation stops

- no ranking rule changes are executed automatically
- no fixes are pushed automatically
- every recommendation requires human review
- abstention is expected when evidence is incomplete

## Trust boundary

This project is decision support, not automation. It produces structured outputs for human review and abstains when core evidence is missing.
