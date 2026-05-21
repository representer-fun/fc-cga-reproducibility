# Reproducibility And Commands

## Environment

The final experiments were run on a machine with:

- 16 vCPUs.
- 120 GB RAM.
- CPU execution, no GPU.

Install dependencies:

```bash
pip install -r requirements.txt
```

Some graph experiments require PyTorch and PyG packages in the environment.

## Data Preparation

Raw data is not committed. See `../REPRODUCE_FROM_SCRATCH.md` for the exact
expected raw-data paths and source pages.

Prepared feature caches are available in the release assets:

- <https://github.com/representer-fun/fc-cga-reproducibility>

After placing the raw files, or instead of using the prepared cache, prepare
processed features with:

```bash
python3 flow_experiment.py schema
python3 flow_experiment.py prepare
```

Processed data is written under `data/processed/`, which is ignored by git.

## Final Experiment Suite

Completed run artifacts are available as split release zip parts:

- `run_artifacts.zip.part-00`
- `run_artifacts.zip.part-01`
- `run_artifacts.zip.part-02`

Reconstruct with:

```bash
cat run_artifacts.zip.part-* > run_artifacts.zip
unzip run_artifacts.zip
```

Run:

```bash
nohup env \
  FLOW_FRAUD_WORKERS=4 \
  FLOW_FRAUD_THREADS=3 \
  FLOW_FRAUD_GRAPH_WORKERS=2 \
  FLOW_FRAUD_GRAPH_THREADS=3 \
  FLOW_FRAUD_FINAL_BOOT=200 \
  bash run_cikm_final_experiments.sh \
  >> runs/logs/cikm_final_active.log 2>&1 < /dev/null &
```

Check:

```bash
./check_cikm_final_progress.sh
```

Completed status:

```text
927/927 jobs, 0 errors
```

## Regenerate Paper Assets

```bash
python3 make_cikm_paper_assets.py
python3 cikm_final_analysis.py --n-boot 200
```

## Important Outputs

- `paper/tables/`
- `paper/figures/`
- `results/cikm_final_analysis/`
- `results/cikm_final_synthesis/`
- `final_paper_package/`

## What Is Not Tracked

The following are intentionally excluded:

- Raw datasets.
- Processed parquet data.
- External downloaded repositories.
- `runs/` logs and prediction archives.
- Trained model objects.
- Python caches.
