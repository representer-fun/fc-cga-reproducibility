# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_heldout_layering`
Generated: 2026-05-19 15:04:29 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation          |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | hard_projected_v2     |      0 |                1 | 0.953937 |             0.965616 |         0.936963 |
| amlnet    | xgboost    | adv_no_projection_v2  |      0 |                1 | 0.953329 |             0.974212 |         0.934097 |
| amlnet    | lightgbm   | hard_projected_v2     |      2 |                1 | 0.95136  |             0.95702  |         0.936963 |
| amlnet    | lightgbm   | boundary_projected_v2 |      2 |                1 | 0.951189 |             0.95702  |         0.936963 |
| amlnet    | lightgbm   | boundary_projected_v2 |      0 |                1 | 0.95115  |             0.95702  |         0.942693 |
| amlnet    | lightgbm   | adv_no_projection_v2  |      0 |                1 | 0.950896 |             0.979943 |         0.934097 |
| amlnet    | xgboost    | hard_projected_v2     |      1 |                1 | 0.950772 |             0.959885 |         0.942693 |
| amlnet    | lightgbm   | adv_no_projection_v2  |      1 |                1 | 0.950021 |             0.974212 |         0.931232 |
| amlnet    | xgboost    | hard_projected_v2     |      0 |                1 | 0.949855 |             0.95702  |         0.934097 |
| amlnet    | xgboost    | boundary_projected_v2 |      1 |                1 | 0.949826 |             0.95702  |         0.936963 |
| amlnet    | xgboost    | boundary_projected_v2 |      0 |                1 | 0.949688 |             0.95702  |         0.934097 |
| amlnet    | xgboost    | adv_no_projection_v2  |      2 |                1 | 0.948008 |             0.965616 |         0.934097 |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection_v2  |             4.3185  |                0.965657 |             0.487791 |         1.20657 |         0.0343434 |
| boundary_projected_v2 |             9.93164 |                0        |             0        |         1.36609 |         0.95      |
| hard_projected_v2     |            10.0366  |                0        |             0        |         1.35413 |         0.95      |
| none                  |           nan       |              nan        |           nan        |       nan       |       nan         |
