# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v3_heldout_structuring`
Generated: 2026-05-19 19:37:43 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation       |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:-------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | xgboost    | random_feasible_v2 |      1 |                1 | 0.760743 |                    1 |         0.645833 |
| amlnet    | xgboost    | random_feasible_v2 |      0 |                1 | 0.719431 |                    1 |         0.541667 |
| amlnet    | xgboost    | none               |      0 |                1 | 0.666075 |                    1 |         0.5      |
| amlnet    | lightgbm   | none               |      2 |                1 | 0.66568  |                    1 |         0.375    |
| amlnet    | xgboost    | random_feasible_v2 |      2 |                1 | 0.659797 |                    1 |         0.479167 |
| amlnet    | lightgbm   | none               |      1 |                1 | 0.650212 |                    1 |         0.375    |
| amlnet    | xgboost    | none               |      2 |                1 | 0.633772 |                    1 |         0.458333 |
| amlnet    | xgboost    | none               |      1 |                1 | 0.620819 |                    1 |         0.4375   |
| amlnet    | lightgbm   | random_feasible_v2 |      1 |                1 | 0.618359 |                    1 |         0.375    |
| amlnet    | lightgbm   | random_feasible_v2 |      0 |                1 | 0.592194 |                    1 |         0.375    |
| amlnet    | lightgbm   | random_feasible_v2 |      2 |                1 | 0.584136 |                    1 |         0.375    |
| amlnet    | lightgbm   | none               |      0 |                1 | 0.566063 |                    1 |         0.375    |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           4.56073   |                       0 |                    0 |        0.616799 |          0.948944 |
| hard_projected_v2               |           8.95636   |                       0 |                    0 |        0.481719 |          0.948944 |
| none                            |         nan         |                     nan |                  nan |      nan        |        nan        |
| plausible_hard_projected_v2     |           8.31152   |                       0 |                    0 |        0.334959 |          0.948944 |
| plausible_typology_projected_v2 |           8.52295   |                       0 |                    0 |        0.334105 |          0.948944 |
| random_feasible_v2              |           0.0187836 |                       0 |                    0 |        2.02965  |          0.948944 |
| typology_projected_v2           |           9.15787   |                       0 |                    0 |        0.471941 |          0.948944 |
