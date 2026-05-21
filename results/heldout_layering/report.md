# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/heldout_layering`
Generated: 2026-05-19 04:52:40 UTC

## Top Predictive Runs

| dataset   | detector       | augmentation      |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:---------------|:------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | xgboost        | adv_no_projection |      1 |                1 | 0.939118 |             0.948424 |         0.919771 |
| amlnet    | lightgbm       | adv_no_projection |      2 |                1 | 0.936425 |             0.951289 |         0.905444 |
| amlnet    | lightgbm       | adv_no_projection |      0 |                1 | 0.936414 |             0.948424 |         0.899713 |
| amlnet    | xgboost        | adv_no_projection |      2 |                1 | 0.935269 |             0.948424 |         0.911175 |
| amlnet    | graphsage_lite | ours              |      2 |                1 | 0.934486 |             0.959885 |         0.885387 |
| amlnet    | lightgbm       | adv_no_projection |      1 |                1 | 0.934102 |             0.951289 |         0.902579 |
| amlnet    | lightgbm       | none              |      2 |                1 | 0.934042 |             0.948424 |         0.899713 |
| amlnet    | lightgbm       | ours              |      2 |                1 | 0.933679 |             0.948424 |         0.902579 |
| amlnet    | xgboost        | adv_no_projection |      0 |                1 | 0.932935 |             0.942693 |         0.899713 |
| amlnet    | xgboost        | ours              |      1 |                1 | 0.932357 |             0.948424 |         0.902579 |
| amlnet    | lightgbm       | none              |      0 |                1 | 0.931741 |             0.948424 |         0.896848 |
| amlnet    | lightgbm       | ours              |      1 |                1 | 0.931559 |             0.948424 |         0.902579 |

## Counterfactual Validity

| augmentation      |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection |         3.19517e-08 |                0.965152 |             0.409366 |         2.72226 |         0.0348485 |
| none              |       nan           |              nan        |           nan        |       nan       |       nan         |
| ours              |         3.19517e-08 |                0        |             0        |         2.75866 |         0.95      |
