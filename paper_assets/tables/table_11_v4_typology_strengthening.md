# V4 Typology Strengthening

AUPRC mean ± std. Layering uses 10 seeds; structuring/integration use 5 seeds.

| Held-out typology   | Detector   | No aug.       | Random feasible   | Hard projected   | Plausible hard   | Curriculum projected   | Typology projected   | Plausible typology   | Best method          |   Best Δ vs no aug. |   Seeds |
|:--------------------|:-----------|:--------------|:------------------|:-----------------|:-----------------|:-----------------------|:---------------------|:---------------------|:---------------------|--------------------:|--------:|
| integration         | lightgbm   | 0.000 ± 0.000 | 0.000 ± 0.000     | 0.000 ± 0.000    | 0.000 ± 0.000    | 0.000 ± 0.000          | 0.000 ± 0.000        | 0.000 ± 0.000        | No aug.              |               0     |       5 |
| integration         | xgboost    | 0.000 ± 0.000 | 0.000 ± 0.000     | 0.000 ± 0.000    | 0.001 ± 0.000    | 0.000 ± 0.000          | 0.000 ± 0.000        | 0.001 ± 0.000        | Plausible hard       |               0     |       5 |
| layering            | lightgbm   | 0.932 ± 0.001 | 0.934 ± 0.002     | 0.946 ± 0.001    | 0.947 ± 0.002    | 0.945 ± 0.003          | 0.947 ± 0.002        | 0.946 ± 0.003        | Typology projected   |               0.016 |      10 |
| layering            | xgboost    | 0.927 ± 0.001 | 0.932 ± 0.002     | 0.945 ± 0.003    | 0.945 ± 0.002    | 0.946 ± 0.003          | 0.942 ± 0.005        | 0.941 ± 0.004        | Curriculum projected |               0.018 |      10 |
| structuring         | lightgbm   | 0.618 ± 0.041 | 0.593 ± 0.022     | 0.390 ± 0.003    | 0.386 ± 0.003    | 0.387 ± 0.006          | 0.386 ± 0.002        | 0.386 ± 0.002        | No aug.              |               0     |       5 |
| structuring         | xgboost    | 0.625 ± 0.029 | 0.709 ± 0.037     | 0.387 ± 0.006    | 0.393 ± 0.005    | 0.386 ± 0.007          | 0.386 ± 0.004        | 0.392 ± 0.007        | Random feasible      |               0.084 |       5 |
