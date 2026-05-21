# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/external_robustness`
Generated: 2026-05-19 05:32:13 UTC

## Top Predictive Runs

| dataset    | detector   | augmentation   |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:-----------|:-----------|:---------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| ellipticpp | lightgbm   | ours           |      2 |                1 | 0.572055 |             0.489362 |         0.50591  |
| ellipticpp | lightgbm   | ours           |      0 |                1 | 0.565973 |             0.49409  |         0.515366 |
| ellipticpp | lightgbm   | ours           |      1 |                1 | 0.56508  |             0.49409  |         0.510638 |
| ellipticpp | lightgbm   | none           |      0 |                1 | 0.564187 |             0.489362 |         0.515366 |
| ellipticpp | lightgbm   | none           |      2 |                1 | 0.564    |             0.49409  |         0.508274 |
| ellipticpp | lightgbm   | none           |      1 |                1 | 0.562864 |             0.49409  |         0.503546 |
| ellipticpp | xgboost    | none           |      0 |                1 | 0.556579 |             0.484634 |         0.508274 |
| ellipticpp | xgboost    | ours           |      2 |                1 | 0.555978 |             0.486998 |         0.501182 |
| ellipticpp | xgboost    | ours           |      1 |                1 | 0.555035 |             0.489362 |         0.503546 |
| ellipticpp | xgboost    | none           |      2 |                1 | 0.554563 |             0.49409  |         0.508274 |
| ellipticpp | xgboost    | none           |      1 |                1 | 0.553367 |             0.491726 |         0.503546 |
| ellipticpp | xgboost    | ours           |      0 |                1 | 0.552288 |             0.484634 |         0.50591  |

## Counterfactual Validity

| augmentation   |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:---------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| none           |       nan           |                     nan |                  nan |           nan   |        nan        |
| ours           |         2.47283e-06 |                       0 |                    0 |         71797.6 |          0.949968 |
