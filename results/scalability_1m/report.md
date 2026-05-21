# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/scalability_1m`
Generated: 2026-05-19 05:26:58 UTC

## Top Predictive Runs

| dataset   | detector       | augmentation   |   seed |   label_fraction |     auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:---------------|:---------------|-------:|-----------------:|----------:|---------------------:|-----------------:|
| amlnet    | graphsage_lite | ours           |      0 |                1 | 0.973544  |             0.992683 |         0.931707 |
| amlnet    | lightgbm       | ours           |      0 |                1 | 0.972819  |             0.987805 |         0.95122  |
| amlnet    | lightgbm       | none           |      0 |                1 | 0.970295  |             0.987805 |         0.95122  |
| amlnet    | graphsage_lite | none           |      0 |                1 | 0.960654  |             0.97561  |         0.919512 |
| transxion | lightgbm       | none           |      0 |                1 | 0.263051  |             0.722838 |         0.379157 |
| transxion | lightgbm       | ours           |      0 |                1 | 0.251956  |             0.726164 |         0.359202 |
| transxion | graphsage_lite | none           |      0 |                1 | 0.113698  |             0.669623 |         0.138581 |
| transxion | graphsage_lite | ours           |      0 |                1 | 0.0899036 |             0.662971 |         0.118625 |

## Counterfactual Validity

| augmentation   |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:---------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| none           |         nan         |                     nan |                  nan |       nan       |        nan        |
| ours           |           0.0180507 |                       0 |                    0 |         1.33963 |          0.949603 |
