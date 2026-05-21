# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/scalability_100k`
Generated: 2026-05-19 05:15:06 UTC

## Top Predictive Runs

| dataset   | detector       | augmentation   |   seed |   label_fraction |     auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:---------------|:---------------|-------:|-----------------:|----------:|---------------------:|-----------------:|
| amlnet    | lightgbm       | ours           |      0 |                1 | 0.974405  |             0.987805 |         0.946341 |
| amlnet    | lightgbm       | none           |      0 |                1 | 0.973828  |             0.990244 |         0.946341 |
| amlnet    | graphsage_lite | ours           |      0 |                1 | 0.96015   |             0.987805 |         0.917073 |
| amlnet    | graphsage_lite | none           |      0 |                1 | 0.959054  |             0.982927 |         0.919512 |
| transxion | lightgbm       | none           |      0 |                1 | 0.254075  |             0.737251 |         0.365854 |
| transxion | lightgbm       | ours           |      0 |                1 | 0.241326  |             0.735033 |         0.351441 |
| transxion | graphsage_lite | none           |      0 |                1 | 0.108471  |             0.646341 |         0.136364 |
| transxion | graphsage_lite | ours           |      0 |                1 | 0.0938078 |             0.608647 |         0.126386 |

## Counterfactual Validity

| augmentation   |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:---------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| none           |         nan         |                     nan |                  nan |      nan        |        nan        |
| ours           |           0.0174687 |                       0 |                    0 |        0.962394 |          0.949603 |
