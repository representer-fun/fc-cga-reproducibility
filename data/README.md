# Data Included in This Artifact

This repository includes the processed feature tables used by the experiments.
They are stored as Parquet files under `data/processed/` and tracked with Git
LFS where needed.

```text
data/processed/
  amlnet/
    features.parquet
    meta.parquet
    summary.json
  transxion/
    features.parquet
    meta.parquet
    summary.json
  ellipticpp/
    features.parquet
    meta.parquet
    summary.json
```

Dataset summaries:

| Dataset | Rows | Features | Positives | Role |
|---|---:|---:|---:|---|
| AMLNet | 1,090,172 | 42 | 1,745 | Main held-out typology transfer benchmark |
| TransXion | 3,029,170 | 83 | 4,641 | In-distribution and label-scarcity validation |
| Elliptic++ | 46,564 | 185 | 4,545 | External robustness check without validity-audit claims |

The raw public downloads are documented in `data/raw/README.md`. The processed
tables are sufficient for rerunning the paper experiments and analyses.
