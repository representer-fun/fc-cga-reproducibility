# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_ablations`
Generated: 2026-05-19 14:58:11 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation      |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | v2_no_ledger      |      1 |                1 | 0.980191 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | v2_no_ledger      |      0 |                1 | 0.979753 |             0.995122 |         0.94878  |
| amlnet    | lightgbm   | v2_no_profile     |      0 |                1 | 0.979689 |             0.995122 |         0.953659 |
| amlnet    | lightgbm   | v2_no_ledger      |      2 |                1 | 0.978878 |             0.997561 |         0.94878  |
| amlnet    | xgboost    | v2_no_profile     |      2 |                1 | 0.978268 |             0.992683 |         0.94878  |
| amlnet    | lightgbm   | v2_no_profile     |      2 |                1 | 0.978262 |             0.995122 |         0.95122  |
| amlnet    | lightgbm   | hard_projected_v2 |      0 |                1 | 0.977922 |             0.992683 |         0.95122  |
| amlnet    | xgboost    | v2_no_ledger      |      1 |                1 | 0.977837 |             0.992683 |         0.95122  |
| amlnet    | xgboost    | v2_no_ledger      |      2 |                1 | 0.977598 |             0.992683 |         0.94878  |
| amlnet    | xgboost    | v2_no_temporal    |      2 |                1 | 0.977584 |             0.995122 |         0.94878  |
| amlnet    | lightgbm   | hard_projected_v2 |      1 |                1 | 0.977479 |             0.990244 |         0.94878  |
| amlnet    | lightgbm   | v2_no_temporal    |      0 |                1 | 0.976946 |             0.990244 |         0.95122  |

## Counterfactual Validity

| augmentation       |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:-------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| hard_projected_v2  |           7.31141   |                0        |             0        |        0.504252 |         0.949603  |
| random_feasible_v2 |           0.0310476 |                0        |             0        |        1.31052  |         0.949603  |
| v2_amount_only     |           0.641229  |                0        |             0        |        0.386806 |         0.949603  |
| v2_no_hard         |           0.0434035 |                0        |             0        |        1.32503  |         0.949603  |
| v2_no_ledger       |           2.46542   |                0.968743 |             0.458543 |        0.673569 |         0.0312574 |
| v2_no_profile      |           2.92748   |                0        |             0        |        0.657251 |         1         |
| v2_no_temporal     |           2.01581   |                0        |             0        |        0.464932 |         0.949603  |
| v2_topology_only   |           1.27169   |                0        |             0        |        0.447996 |         0.953302  |
