# Repaired Baselines On Held-Out Layering

Tests whether post-hoc repair is enough to match typology-aware projected counterfactuals under the main positive shift.

| Detector   | Method                 | AUPRC           |   Δ vs no aug. |   Seeds |
|:-----------|:-----------------------|:----------------|---------------:|--------:|
| lightgbm   | No aug.                | 0.932 ± 0.001   |          0     |      10 |
| lightgbm   | Feature noise          | 0.933 ± 0.002   |          0.001 |      10 |
| lightgbm   | Feature noise + repair | 0.928 ± 0.010   |         -0.004 |      10 |
| lightgbm   | SMOTE                  | 0.930 ± 0.002   |         -0.002 |      10 |
| lightgbm   | SMOTE + repair         | 0.932 ± 0.002   |          0     |      10 |
| lightgbm   | Mixup                  | 0.944 ± 0.002   |          0.012 |      10 |
| lightgbm   | Mixup + repair         | 0.934 ± 0.005   |          0.003 |      10 |
| lightgbm   | Random feasible        | 0.934 ± 0.002   |          0.002 |      10 |
| lightgbm   | Hard projected         | 0.946 ± 0.001   |          0.014 |      10 |
| lightgbm   | Plausible hard         | 0.947 ± 0.002   |          0.015 |      10 |
| lightgbm   | Curriculum projected   | 0.945 ± 0.003   |          0.013 |      10 |
| lightgbm   | Typology projected     | 0.947 ± 0.002   |          0.016 |      10 |
| lightgbm   | Plausible typology     | 0.946 ± 0.003   |          0.014 |      10 |
| xgboost    | No aug.                | 0.927 ± 9.7e-04 |          0     |      10 |
| xgboost    | Feature noise          | 0.929 ± 0.002   |          0.001 |      10 |
| xgboost    | Feature noise + repair | 0.928 ± 0.008   |          0.001 |      10 |
| xgboost    | SMOTE                  | 0.929 ± 0.001   |          0.002 |      10 |
| xgboost    | SMOTE + repair         | 0.930 ± 0.002   |          0.002 |      10 |
| xgboost    | Mixup                  | 0.941 ± 0.004   |          0.013 |      10 |
| xgboost    | Mixup + repair         | 0.933 ± 0.005   |          0.006 |      10 |
| xgboost    | Random feasible        | 0.932 ± 0.002   |          0.004 |      10 |
| xgboost    | Hard projected         | 0.945 ± 0.003   |          0.018 |      10 |
| xgboost    | Plausible hard         | 0.945 ± 0.002   |          0.018 |      10 |
| xgboost    | Curriculum projected   | 0.946 ± 0.003   |          0.018 |      10 |
| xgboost    | Typology projected     | 0.942 ± 0.005   |          0.014 |      10 |
| xgboost    | Plausible typology     | 0.941 ± 0.004   |          0.013 |      10 |
