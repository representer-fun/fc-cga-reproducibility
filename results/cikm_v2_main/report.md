# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_main`
Generated: 2026-05-19 11:32:16 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation          |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | adv_no_projection_v2  |      1 |                1 | 0.980191 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | adv_no_projection_v2  |      0 |                1 | 0.979753 |             0.995122 |         0.94878  |
| amlnet    | lightgbm   | adv_no_projection_v2  |      2 |                1 | 0.978878 |             0.997561 |         0.94878  |
| amlnet    | lightgbm   | hard_projected_v2     |      0 |                1 | 0.977922 |             0.992683 |         0.95122  |
| amlnet    | xgboost    | adv_no_projection_v2  |      1 |                1 | 0.977837 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | boundary_projected_v2 |      0 |                1 | 0.977835 |             0.992683 |         0.95122  |
| amlnet    | xgboost    | adv_no_projection_v2  |      2 |                1 | 0.977598 |             0.992683 |         0.94878  |
| amlnet    | lightgbm   | boundary_projected_v2 |      2 |                1 | 0.977559 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | hard_projected_v2     |      1 |                1 | 0.977479 |             0.990244 |         0.94878  |
| amlnet    | lightgbm   | boundary_projected_v2 |      1 |                1 | 0.977312 |             0.987805 |         0.946341 |
| amlnet    | lightgbm   | hard_projected_v2     |      2 |                1 | 0.976619 |             0.992683 |         0.953659 |
| amlnet    | xgboost    | none                  |      2 |                1 | 0.974561 |             0.990244 |         0.95122  |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection_v2  |           2.60103   |                0.969481 |             0.460565 |        0.676679 |         0.0305188 |
| boundary_projected_v2 |           7.59103   |                0        |             0        |        0.484085 |         0.949603  |
| hard_projected_v2     |           7.60889   |                0        |             0        |        0.485568 |         0.949603  |
| none                  |         nan         |              nan        |           nan        |      nan        |       nan         |
| random_feasible_v2    |           0.0738796 |                0        |             0        |        1.31052  |         0.949603  |
