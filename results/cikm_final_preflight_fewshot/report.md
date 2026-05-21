# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_preflight_fewshot`
Generated: 2026-05-21 02:50:22 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation       |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:-------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | smote_repaired_v2  |      0 |                1 | 0.939311 |             0.954155 |         0.919771 |
| amlnet    | lightgbm   | random_feasible_v2 |      0 |                1 | 0.938877 |             0.954155 |         0.919771 |
| amlnet    | lightgbm   | none               |      0 |                1 | 0.938734 |             0.95702  |         0.916905 |

## Counterfactual Validity

| augmentation       |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:-------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| none               |        nan          |                     nan |                  nan |       nan       |        nan        |
| random_feasible_v2 |          0.0275528  |                       0 |                    0 |         1.77497 |          0.941176 |
| smote_repaired_v2  |          0.00826543 |                       0 |                    0 |         1.91948 |          0.941176 |
