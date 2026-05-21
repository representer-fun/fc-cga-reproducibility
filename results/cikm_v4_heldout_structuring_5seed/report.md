# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v4_heldout_structuring_5seed`
Generated: 2026-05-20 18:24:34 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation       |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:-------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | xgboost    | random_feasible_v2 |      1 |                1 | 0.760743 |                    1 |         0.645833 |
| amlnet    | xgboost    | random_feasible_v2 |      0 |                1 | 0.719431 |                    1 |         0.541667 |
| amlnet    | xgboost    | random_feasible_v2 |      4 |                1 | 0.709475 |                    1 |         0.541667 |
| amlnet    | xgboost    | random_feasible_v2 |      3 |                1 | 0.694682 |                    1 |         0.520833 |
| amlnet    | xgboost    | none               |      0 |                1 | 0.666075 |                    1 |         0.5      |
| amlnet    | lightgbm   | none               |      2 |                1 | 0.66568  |                    1 |         0.375    |
| amlnet    | xgboost    | random_feasible_v2 |      2 |                1 | 0.659797 |                    1 |         0.479167 |
| amlnet    | lightgbm   | none               |      1 |                1 | 0.650212 |                    1 |         0.375    |
| amlnet    | xgboost    | none               |      2 |                1 | 0.633772 |                    1 |         0.458333 |
| amlnet    | xgboost    | none               |      1 |                1 | 0.620819 |                    1 |         0.4375   |
| amlnet    | lightgbm   | random_feasible_v2 |      1 |                1 | 0.618359 |                    1 |         0.375    |
| amlnet    | xgboost    | none               |      4 |                1 | 0.616679 |                    1 |         0.395833 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           4.61228   |                       0 |                    0 |        0.616362 |          0.948944 |
| hard_projected_v2               |           9.04985   |                       0 |                    0 |        0.466617 |          0.948944 |
| none                            |         nan         |                     nan |                  nan |      nan        |        nan        |
| plausible_hard_projected_v2     |           8.45571   |                       0 |                    0 |        0.333987 |          0.948944 |
| plausible_typology_projected_v2 |           8.62817   |                       0 |                    0 |        0.335528 |          0.948944 |
| random_feasible_v2              |           0.0159973 |                       0 |                    0 |        2.02357  |          0.948944 |
| typology_projected_v2           |           9.23589   |                       0 |                    0 |        0.461529 |          0.948944 |
