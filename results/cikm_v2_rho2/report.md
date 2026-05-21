# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_rho2`
Generated: 2026-05-19 16:02:16 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation          |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | hard_projected_v2     |      1 |                1 | 0.978574 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | boundary_projected_v2 |      1 |                1 | 0.978209 |             0.990244 |         0.953659 |
| amlnet    | lightgbm   | boundary_projected_v2 |      0 |                1 | 0.978131 |             0.992683 |         0.953659 |
| amlnet    | lightgbm   | hard_projected_v2     |      0 |                1 | 0.977719 |             0.992683 |         0.953659 |
| amlnet    | lightgbm   | hard_projected_v2     |      2 |                1 | 0.977465 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | boundary_projected_v2 |      2 |                1 | 0.97697  |             0.987805 |         0.94878  |
| amlnet    | xgboost    | random_feasible_v2    |      1 |                1 | 0.973465 |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | random_feasible_v2    |      1 |                1 | 0.973408 |             0.990244 |         0.94878  |
| amlnet    | xgboost    | random_feasible_v2    |      0 |                1 | 0.973217 |             0.992683 |         0.95122  |
| amlnet    | xgboost    | random_feasible_v2    |      2 |                1 | 0.973058 |             0.990244 |         0.953659 |
| amlnet    | lightgbm   | random_feasible_v2    |      2 |                1 | 0.972049 |             0.987805 |         0.953659 |
| amlnet    | lightgbm   | random_feasible_v2    |      0 |                1 | 0.971354 |             0.985366 |         0.95122  |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| boundary_projected_v2 |           7.32138   |                       0 |                    0 |        0.516783 |          0.949868 |
| hard_projected_v2     |           7.33831   |                       0 |                    0 |        0.517497 |          0.949868 |
| random_feasible_v2    |           0.0317335 |                       0 |                    0 |        1.29798  |          0.949868 |
