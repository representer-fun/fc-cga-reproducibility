# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_heldout_structuring`
Generated: 2026-05-19 15:11:00 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation         |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:---------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | xgboost    | none                 |      0 |                1 | 0.666075 |             1        |         0.5      |
| amlnet    | lightgbm   | none                 |      2 |                1 | 0.66568  |             1        |         0.375    |
| amlnet    | lightgbm   | none                 |      1 |                1 | 0.650212 |             1        |         0.375    |
| amlnet    | xgboost    | none                 |      2 |                1 | 0.633772 |             1        |         0.458333 |
| amlnet    | xgboost    | none                 |      1 |                1 | 0.620819 |             1        |         0.4375   |
| amlnet    | lightgbm   | none                 |      0 |                1 | 0.566063 |             1        |         0.375    |
| amlnet    | xgboost    | adv_no_projection_v2 |      2 |                1 | 0.399126 |             1        |         0.375    |
| amlnet    | xgboost    | adv_no_projection_v2 |      1 |                1 | 0.397359 |             1        |         0.375    |
| amlnet    | lightgbm   | adv_no_projection_v2 |      2 |                1 | 0.395089 |             1        |         0.375    |
| amlnet    | xgboost    | adv_no_projection_v2 |      0 |                1 | 0.394322 |             0.979167 |         0.375    |
| amlnet    | lightgbm   | adv_no_projection_v2 |      0 |                1 | 0.391592 |             1        |         0.375    |
| amlnet    | lightgbm   | hard_projected_v2    |      1 |                1 | 0.389928 |             1        |         0.375    |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection_v2  |             3.96038 |                0.966828 |             0.452778 |        0.530718 |         0.0331719 |
| boundary_projected_v2 |            10.2029  |                0        |             0        |        0.438011 |         0.949802  |
| hard_projected_v2     |            10.223   |                0        |             0        |        0.44321  |         0.949802  |
| none                  |           nan       |              nan        |           nan        |      nan        |       nan         |
