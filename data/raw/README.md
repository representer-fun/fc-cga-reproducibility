# Raw Data

The artifact includes experiment-ready processed data in `data/processed/`.
The original raw public downloads are not committed because the two largest
CSV files are each roughly 690 MB. To rebuild the processed Parquet files from
raw sources, place the downloads at these paths:

```text
data/raw/AMLNet_August_2025.csv
data/raw/ellipticpp/txs_features.csv
data/raw/ellipticpp/txs_classes.csv
data/raw/ellipticpp/txs_edgelist.csv
external/TransXion/data/tx.csv
external/TransXion/data/person.csv
external/TransXion/data/merchant.csv
```

Sources:

- AMLNet: https://doi.org/10.5281/zenodo.16736515
- TransXion: https://github.com/chaos-max/TransXion
- Elliptic++: https://huggingface.co/datasets/AI4FinTech/ellipticpp and https://github.com/git-disl/EllipticPlusPlus

After placing raw files, run:

```bash
python3 code/flow_experiment.py prepare
```

For ordinary paper reproduction this step is not required, because
`data/processed/` is already included.
