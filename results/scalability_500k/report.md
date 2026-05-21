# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/scalability_500k`
Generated: 2026-05-19 05:20:22 UTC

## Top Predictive Runs

| dataset   | detector       | augmentation   |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:---------------|:---------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm       | ours           |      0 |                1 | 0.973324 |             0.987805 |         0.94878  |
| amlnet    | lightgbm       | none           |      0 |                1 | 0.972968 |             0.987805 |         0.94878  |
| amlnet    | graphsage_lite | none           |      0 |                1 | 0.969425 |             0.990244 |         0.914634 |
| amlnet    | graphsage_lite | ours           |      0 |                1 | 0.96917  |             0.990244 |         0.917073 |
| transxion | lightgbm       | none           |      0 |                1 | 0.258895 |             0.720621 |         0.378049 |
| transxion | lightgbm       | ours           |      0 |                1 | 0.240925 |             0.718404 |         0.353659 |
| transxion | graphsage_lite | ours           |      0 |                1 | 0.112236 |             0.636364 |         0.165188 |
| transxion | graphsage_lite | none           |      0 |                1 | 0.103532 |             0.676275 |         0.128603 |

## Counterfactual Validity

| augmentation   |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:---------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| none           |          nan        |                     nan |                  nan |       nan       |        nan        |
| ours           |            0.017547 |                       0 |                    0 |         1.26647 |          0.949603 |
