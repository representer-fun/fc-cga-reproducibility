# Codebase Map

## Core Runners

`flow_experiment.py`

- Data discovery.
- Canonicalization.
- Feature engineering.
- Baseline training.
- Metrics and reports.

`cikm_extended_experiment.py`

- Extended CIKM runner.
- Repaired augmentations.
- Ledger-conserving counterfactual generation.
- Held-out typology splits.
- Few-shot held-out positives.
- Cold-start/new-pair subsets.
- Prediction saving.
- PyG SAGE/GAT.

## Analysis Scripts

`cikm_result_analysis.py`

- Combines results across runs.
- Builds claim audits.
- Computes aggregate predictive and validity summaries.

`cikm_strengthening_analysis.py`

- v4 strengthening tables and figures.

`cikm_mechanism_analysis.py`

- Generated-example mechanism analysis: support distance, profile drift,
  detector hardness.

`cikm_final_analysis.py`

- Final paper tables and figures:
  alert budgets, bootstrap, repaired baselines, few-shot, temporal buckets,
  counterparty shift, graph confirmation, failure modes.

`make_cikm_paper_assets.py`

- Broad paper asset generation into `paper/`.

## Run Scripts

`run_cikm_final_experiments.sh`

- The final 927-job suite.
- This is the last complete experimental run.

`check_cikm_final_progress.sh`

- Progress monitor for the final suite.

## Outputs

`results/`

- Compact CSV/Markdown summaries.

`paper/`

- Full generated paper assets.

`final_paper_package/`

- Curated writing package.
