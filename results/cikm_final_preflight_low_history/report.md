# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_preflight_low_history`
Generated: 2026-05-21 02:50:37 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation       |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:-------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | random_feasible_v2 |      0 |                1 | 0.936841 |             0.948424 |         0.902579 |
| amlnet    | lightgbm   | none               |      0 |                1 | 0.935222 |             0.954155 |         0.899713 |

## Counterfactual Validity

| augmentation       |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:-------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| none               |          nan        |                     nan |                  nan |       nan       |        nan        |
| random_feasible_v2 |            0.156437 |                       0 |                    0 |         2.00882 |          0.939394 |
