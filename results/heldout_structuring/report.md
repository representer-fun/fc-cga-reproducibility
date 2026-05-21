# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/heldout_structuring`
Generated: 2026-05-19 05:10:51 UTC

## Top Predictive Runs

| dataset   | detector       | augmentation      |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:---------------|:------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | graphsage_lite | adv_no_projection |      2 |                1 | 0.952483 |             0.958333 |         0.9375   |
| amlnet    | graphsage_lite | none              |      2 |                1 | 0.947284 |             0.958333 |         0.9375   |
| amlnet    | graphsage_lite | ours              |      2 |                1 | 0.945432 |             0.958333 |         0.9375   |
| amlnet    | graphsage_lite | ours              |      0 |                1 | 0.935455 |             0.958333 |         0.916667 |
| amlnet    | graphsage_lite | none              |      0 |                1 | 0.921861 |             0.958333 |         0.895833 |
| amlnet    | graphsage_lite | ours              |      1 |                1 | 0.904324 |             0.9375   |         0.875    |
| amlnet    | graphsage_lite | adv_no_projection |      1 |                1 | 0.745371 |             0.916667 |         0.6875   |
| amlnet    | xgboost        | none              |      0 |                1 | 0.670343 |             1        |         0.458333 |
| amlnet    | xgboost        | none              |      2 |                1 | 0.669949 |             1        |         0.520833 |
| amlnet    | xgboost        | adv_no_projection |      2 |                1 | 0.666229 |             1        |         0.458333 |
| amlnet    | xgboost        | ours              |      2 |                1 | 0.66491  |             1        |         0.5      |
| amlnet    | xgboost        | adv_no_projection |      1 |                1 | 0.663475 |             1        |         0.458333 |

## Counterfactual Validity

| augmentation      |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection |         2.14684e-08 |                 0.96081 |             0.409506 |         2.02413 |         0.0391898 |
| none              |       nan           |               nan       |           nan        |       nan       |       nan         |
| ours              |         2.14684e-08 |                 0       |             0        |         1.97453 |         0.949802  |
