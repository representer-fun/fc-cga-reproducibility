# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_label_scarcity`
Generated: 2026-05-19 14:07:40 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation          |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | boundary_projected_v2 |      1 |                1 | 0.978987 |             0.990244 |         0.953659 |
| amlnet    | lightgbm   | adv_no_projection_v2  |      2 |                1 | 0.978965 |             0.997561 |         0.94878  |
| amlnet    | lightgbm   | hard_projected_v2     |      0 |                1 | 0.977536 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | adv_no_projection_v2  |      0 |                1 | 0.977516 |             0.995122 |         0.94878  |
| amlnet    | lightgbm   | hard_projected_v2     |      1 |                1 | 0.977327 |             0.990244 |         0.94878  |
| amlnet    | xgboost    | adv_no_projection_v2  |      2 |                1 | 0.977254 |             0.997561 |         0.94878  |
| amlnet    | lightgbm   | adv_no_projection_v2  |      1 |                1 | 0.977205 |             0.995122 |         0.94878  |
| amlnet    | lightgbm   | boundary_projected_v2 |      2 |                1 | 0.976406 |             0.990244 |         0.94878  |
| amlnet    | xgboost    | random_feasible_v2    |      0 |                1 | 0.976392 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | hard_projected_v2     |      2 |                1 | 0.976248 |             0.990244 |         0.94878  |
| amlnet    | lightgbm   | boundary_projected_v2 |      0 |                1 | 0.976216 |             0.990244 |         0.95122  |
| amlnet    | xgboost    | adv_no_projection_v2  |      1 |                1 | 0.976015 |             0.995122 |         0.94878  |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection_v2  |           3.23592   |                0.973882 |             0.484807 |        0.738147 |         0.0261185 |
| boundary_projected_v2 |           8.57685   |                0        |             0        |        0.704855 |         0.939883  |
| hard_projected_v2     |           8.60222   |                0        |             0        |        0.707719 |         0.939883  |
| none                  |         nan         |              nan        |           nan        |      nan        |       nan         |
| random_feasible_v2    |           0.0582005 |                0        |             0        |        1.34156  |         0.939883  |
