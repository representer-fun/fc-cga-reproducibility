# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_rho`
Generated: 2026-05-19 15:46:47 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation          |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | hard_projected_v2     |      0 |                1 | 0.981915 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | boundary_projected_v2 |      0 |                1 | 0.980863 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | hard_projected_v2     |      1 |                1 | 0.97935  |             0.995122 |         0.94878  |
| amlnet    | lightgbm   | boundary_projected_v2 |      2 |                1 | 0.978409 |             0.995122 |         0.95122  |
| amlnet    | lightgbm   | hard_projected_v2     |      2 |                1 | 0.978227 |             0.995122 |         0.953659 |
| amlnet    | lightgbm   | boundary_projected_v2 |      1 |                1 | 0.977259 |             0.992683 |         0.95122  |
| amlnet    | xgboost    | hard_projected_v2     |      1 |                1 | 0.974153 |             0.990244 |         0.94878  |
| amlnet    | lightgbm   | random_feasible_v2    |      2 |                1 | 0.974107 |             0.992683 |         0.953659 |
| amlnet    | xgboost    | boundary_projected_v2 |      2 |                1 | 0.974075 |             0.990244 |         0.94878  |
| amlnet    | xgboost    | random_feasible_v2    |      2 |                1 | 0.973961 |             0.990244 |         0.95122  |
| amlnet    | xgboost    | random_feasible_v2    |      0 |                1 | 0.973316 |             0.990244 |         0.94878  |
| amlnet    | xgboost    | boundary_projected_v2 |      1 |                1 | 0.973267 |             0.990244 |         0.94878  |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| boundary_projected_v2 |           7.26909   |                       0 |                    0 |        0.502916 |          0.949576 |
| hard_projected_v2     |           7.2837    |                       0 |                    0 |        0.506196 |          0.949576 |
| random_feasible_v2    |           0.0329469 |                       0 |                    0 |        1.33314  |          0.949576 |
