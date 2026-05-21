# Paired Bootstrap Significance On Held-Out Layering

Prediction-level bootstrap with 200 resamples per seed, summarized across seeds.

| Detector   | Target               | Baseline       |   Mean ΔAUPRC |   Mean bootstrap low |   Mean bootstrap high |   Seed win rate |   Seeds |
|:-----------|:---------------------|:---------------|--------------:|---------------------:|----------------------:|----------------:|--------:|
| lightgbm   | Random feasible      | No aug.        |         0.002 |               -0.001 |                 0.006 |             1   |      10 |
| lightgbm   | Random feasible      | SMOTE + repair |         0.002 |               -0.002 |                 0.007 |             0.9 |      10 |
| lightgbm   | SMOTE + repair       | No aug.        |         0     |               -0.003 |                 0.003 |             0.6 |      10 |
| lightgbm   | Hard projected       | No aug.        |         0.014 |                0.005 |                 0.024 |             1   |      10 |
| lightgbm   | Hard projected       | SMOTE + repair |         0.014 |                0.005 |                 0.024 |             1   |      10 |
| lightgbm   | Plausible hard       | No aug.        |         0.015 |                0.007 |                 0.025 |             1   |      10 |
| lightgbm   | Plausible hard       | SMOTE + repair |         0.015 |                0.006 |                 0.025 |             1   |      10 |
| lightgbm   | Curriculum projected | No aug.        |         0.013 |                0.006 |                 0.023 |             1   |      10 |
| lightgbm   | Curriculum projected | SMOTE + repair |         0.013 |                0.005 |                 0.023 |             1   |      10 |
| lightgbm   | Typology projected   | No aug.        |         0.016 |                0.007 |                 0.025 |             1   |      10 |
| lightgbm   | Typology projected   | SMOTE + repair |         0.015 |                0.007 |                 0.025 |             1   |      10 |
| lightgbm   | Plausible typology   | No aug.        |         0.014 |                0.006 |                 0.024 |             1   |      10 |
| lightgbm   | Plausible typology   | SMOTE + repair |         0.014 |                0.006 |                 0.024 |             1   |      10 |
| xgboost    | Random feasible      | No aug.        |         0.004 |                0.001 |                 0.008 |             1   |      10 |
| xgboost    | Random feasible      | SMOTE + repair |         0.002 |               -0.001 |                 0.005 |             0.9 |      10 |
| xgboost    | SMOTE + repair       | No aug.        |         0.002 |               -0     |                 0.005 |             1   |      10 |
| xgboost    | Hard projected       | No aug.        |         0.018 |                0.008 |                 0.028 |             1   |      10 |
| xgboost    | Hard projected       | SMOTE + repair |         0.015 |                0.007 |                 0.026 |             1   |      10 |
| xgboost    | Plausible hard       | No aug.        |         0.018 |                0.008 |                 0.029 |             1   |      10 |
| xgboost    | Plausible hard       | SMOTE + repair |         0.015 |                0.007 |                 0.025 |             1   |      10 |
| xgboost    | Curriculum projected | No aug.        |         0.018 |                0.01  |                 0.028 |             1   |      10 |
| xgboost    | Curriculum projected | SMOTE + repair |         0.016 |                0.008 |                 0.024 |             1   |      10 |
| xgboost    | Typology projected   | No aug.        |         0.014 |                0.004 |                 0.026 |             1   |      10 |
| xgboost    | Typology projected   | SMOTE + repair |         0.012 |                0.003 |                 0.022 |             1   |      10 |
| xgboost    | Plausible typology   | No aug.        |         0.013 |                0.002 |                 0.025 |             1   |      10 |
| xgboost    | Plausible typology   | SMOTE + repair |         0.011 |                0.001 |                 0.022 |             1   |      10 |
