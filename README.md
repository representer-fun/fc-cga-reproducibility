# FC-CGA Anonymous Reproducibility Artifact

This is the anonymous reproducibility artifact for the CIKM submission
*Flow-Constrained Counterfactual Graph Augmentation for Robust Transaction Fraud
Detection*. It contains the experiment code, processed datasets, run scripts,
cached seed-level outputs, processed result tables, plotting scripts, and the
anonymous paper source snapshot needed to reproduce the empirical claims.

Canonical artifact URL:

```text
https://github.com/representer-fun/fc-cga-reproducibility
```

The repository is prepared for double-blind review. It intentionally does not
contain author names, affiliations, private credentials, trained model weights,
or local machine paths.

## What Is Included

```text
.
├── code/                         # Python experiment and analysis code
├── scripts/                      # Shell entrypoints and progress checkers
├── data/
│   ├── processed/                # Included experiment-ready Parquet data
│   └── raw/README.md             # Raw public download locations
├── cached_seed_outputs/runs/     # Compact per-seed results/validity JSONL
├── results/                      # Processed CSV/Markdown result summaries
├── paper_assets/                 # Tables, figures, and result notes for paper writing
├── paper/                        # Anonymous paper source snapshot and figures
├── docs/                         # Manifest/model-artifact notes
└── requirements.txt
```

The included processed data are the same feature and metadata tables used by
the final experiments:

| Dataset | Rows | Features | Positives | Used For |
|---|---:|---:|---:|---|
| AMLNet | 1,090,172 | 42 | 1,745 | Main held-out layering, typology boundaries, alert budgets, few-shot, temporal, new-pair slices |
| TransXion | 3,029,170 | 83 | 4,641 | In-distribution and label-scarcity checks |
| Elliptic++ | 46,564 | 185 | 4,545 | External predictive sanity check |

The raw public sources are documented in `data/raw/README.md`. Rebuilding from
raw is optional because the processed Parquet tables are committed in this
artifact.

## Environment

The experiments were run on a CPU machine. GPU is not required for the
boosted-tree experiments that support the main paper claim. The graph neural
checks can run on CPU, but are slower and require PyTorch/PyG-compatible
packages.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Optional for graph neural detector checks:

```bash
pip install torch-geometric
```

## Fast Verification From Cached Outputs

The cached seed-level outputs are stored outside `runs/` so the repository does
not look like an active work directory. Restore them with:

```bash
bash scripts/restore_cached_seed_outputs.sh
```

Then check the final experiment suite:

```bash
bash scripts/check_cikm_final_progress.sh
```

Expected final-suite completion is:

```text
CIKM final total: 927/927 = 100.0% | errors=0
```

Earlier strengthening suites can be checked similarly:

```bash
bash scripts/check_cikm_strengthening_progress.sh
bash scripts/check_cikm_v3_progress.sh
```

The reviewer-facing outputs used by the paper are already materialized in:

```text
paper_assets/tables/
paper_assets/figures/
paper_assets/results/
results/cikm_final_analysis/
results/cikm_v4_strengthening/
results/cikm_v4_mechanism/
results/cikm_final_synthesis/
```

## Reproducing the Paper Tables and Figures

To regenerate the paper-facing tables and figures from the included processed
results:

```bash
python3 code/make_cikm_paper_assets.py
python3 code/cikm_strengthening_analysis.py
python3 code/cikm_mechanism_analysis.py
python3 code/cikm_final_analysis.py --n-boot 200
```

The anonymous paper source snapshot is in `paper/`. To rebuild the PDF:

```bash
cd paper
make anon
```

The main paper figures correspond to:

```text
paper/figures/fig_07_layering_10seed_delta_ci.*
paper/figures/fig_08_effect_scope_map.*
paper/figures/fig_09_amount_alignment.*
```

## Full Experiment Rerun

The full rerun uses the included `data/processed/` tables. On a 16-vCPU CPU
machine, use multiprocessing with conservative per-worker thread counts:

```bash
mkdir -p runs/logs
nohup env \
  FLOW_FRAUD_WORKERS=4 \
  FLOW_FRAUD_THREADS=3 \
  FLOW_FRAUD_GRAPH_WORKERS=2 \
  FLOW_FRAUD_GRAPH_THREADS=3 \
  FLOW_FRAUD_FINAL_BOOT=200 \
  bash scripts/run_cikm_final_experiments.sh \
  > runs/logs/cikm_final_active.log 2>&1 < /dev/null &
```

Progress:

```bash
bash scripts/check_cikm_final_progress.sh
tail -n 40 runs/logs/cikm_final_active.log
```

The broader strengthening suite can be launched with:

```bash
nohup env \
  FLOW_FRAUD_WORKERS=4 \
  FLOW_FRAUD_THREADS=3 \
  bash scripts/run_cikm_strengthening.sh \
  > runs/logs/cikm_strengthening_active.log 2>&1 < /dev/null &
```

The earlier v3 audit/transfer suite can be launched with:

```bash
nohup env \
  FLOW_FRAUD_WORKERS=4 \
  FLOW_FRAUD_THREADS=3 \
  bash scripts/run_cikm_v3_fast.sh \
  > runs/logs/cikm_v3_active.log 2>&1 < /dev/null &
```

Fresh reruns may create prediction arrays, logs, and model artifacts under
`runs/`; these are intentionally ignored by Git. The committed
`cached_seed_outputs/` directory contains compact JSONL outputs sufficient to
audit completed jobs and inspect seed-level metrics.

## Main Experimental Map

The core claim is evaluated on AMLNet held-out layering. All layering positives
are removed from training, counterfactual examples are generated from the
remaining positives, and evaluation is restricted to the held-out layering
positives in the test period. The principal comparisons are:

- no augmentation,
- repaired feature-space baselines such as SMOTE+repair and mixup+repair,
- valid but non-hard random feasible augmentation,
- hard projected counterfactuals,
- plausible/curriculum/typology projected variants.

Additional experiments test whether the effect persists under low-FPR alert
budgets, top-k precision, few-shot target labels, temporal slices, unseen
counterparty pairs, non-layering typologies, graph neural detectors, and
constraint ablations. The paper deliberately treats non-layering and graph
detector results as boundary evidence rather than a universal-success claim.

## Rebuilding Processed Data From Raw

This is optional because `data/processed/` is included. If desired, download
the raw public sources listed in `data/raw/README.md`, place them at the
documented paths, and run:

```bash
python3 code/flow_experiment.py prepare
```

Schema inspection:

```bash
python3 code/flow_experiment.py schema
```

## Notes on Omitted Artifacts

The repository includes processed data and seed-level outputs, but omits:

- trained model binaries,
- prediction `.npz` arrays from fresh reruns,
- raw multi-hundred-megabyte CSV downloads,
- local logs and temporary scratch files.

These omissions keep the artifact cloneable while preserving the data and
outputs needed for reproduction.
