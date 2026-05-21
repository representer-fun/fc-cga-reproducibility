# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v4_repaired_audit`
Generated: 2026-05-20 17:59:20 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      0 |                1 | 0.980495 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      2 |                1 | 0.979511 |             0.995122 |         0.953659 |
| amlnet    | lightgbm   | hard_projected_v2               |      0 |                1 | 0.979199 |             0.990244 |         0.953659 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      0 |                1 | 0.978852 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | hard_projected_v2               |      2 |                1 | 0.978361 |             0.997561 |         0.95122  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |                1 | 0.97787  |             0.995122 |         0.95122  |
| amlnet    | lightgbm   | typology_projected_v2           |      0 |                1 | 0.977841 |             0.995122 |         0.953659 |
| amlnet    | lightgbm   | typology_projected_v2           |      2 |                1 | 0.977418 |             0.995122 |         0.95122  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      1 |                1 | 0.97709  |             0.992683 |         0.953659 |
| amlnet    | xgboost    | feature_noise_repaired_v2       |      2 |                1 | 0.976401 |             0.992683 |         0.953659 |
| amlnet    | xgboost    | mixup_v2                        |      0 |                1 | 0.975966 |             0.992683 |         0.953659 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      0 |                1 | 0.975885 |             0.992683 |         0.95122  |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.56181   |             0           |           0          |        0.557055 |          0.949612 |
| edge_rewire_v2                  |           0.178286  |             0           |           0          |        1.30039  |          0.949612 |
| feature_noise_repaired_v2       |           1.98158   |             0           |           0          |        2.04599  |          0.950138 |
| feature_noise_v2                |           2.43065   |             0.582372    |           0.3473     |        2.08259  |          0.391295 |
| hard_projected_v2               |           6.21466   |             0           |           0          |        0.530101 |          0.949612 |
| mixup_repaired_v2               |           1.47977   |             0           |           0          |        1.0822   |          0.949612 |
| mixup_v2                        |           1.28777   |             0.000225225 |           0.00023189 |        1.0822   |          0.949387 |
| none                            |         nan         |           nan           |         nan          |      nan        |        nan        |
| plausible_hard_projected_v2     |           5.16055   |             0           |           0          |        0.301893 |          0.949612 |
| plausible_typology_projected_v2 |           5.70611   |             0           |           0          |        0.292291 |          0.949612 |
| random_feasible_v2              |           0.0312528 |             0           |           0          |        1.30274  |          0.949612 |
| smote_repaired_v2               |           0.265202  |             0           |           0          |        1.46006  |          0.949612 |
| smote_v2                        |           0.277121  |             0           |           0          |        1.46006  |          0.949612 |
| typology_projected_v2           |           7.04704   |             0           |           0          |        0.515501 |          0.949612 |
