# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_preflight_graph`
Generated: 2026-05-21 02:51:30 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation       |   seed |   label_fraction |     auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:-------------------|-------:|-----------------:|----------:|---------------------:|-----------------:|
| amlnet    | pyg_gat    | none               |      0 |                1 | 0.105492  |             0.418338 |       0.17192    |
| amlnet    | pyg_gat    | random_feasible_v2 |      0 |                1 | 0.0917892 |             0.398281 |       0.151862   |
| amlnet    | pyg_sage   | none               |      0 |                1 | 0.0143716 |             0.249284 |       0.00859599 |
| amlnet    | pyg_sage   | random_feasible_v2 |      0 |                1 | 0.0137102 |             0.246418 |       0.00573066 |

## Counterfactual Validity

| augmentation       |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:-------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| none               |       nan           |                     nan |                  nan |       nan       |        nan        |
| random_feasible_v2 |         0.000422746 |                       0 |                    0 |         2.08175 |          0.931818 |
