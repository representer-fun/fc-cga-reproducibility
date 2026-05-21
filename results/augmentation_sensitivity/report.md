# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/augmentation_sensitivity`
Generated: 2026-05-19 06:34:19 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation      |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | adv_no_projection |      1 |                1 | 0.973656 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | adv_no_projection |      2 |                1 | 0.973331 |             0.987805 |         0.946341 |
| amlnet    | lightgbm   | ours              |      1 |                1 | 0.97333  |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | ours              |      0 |                1 | 0.9717   |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | random_feasible   |      0 |                1 | 0.971505 |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | random_feasible   |      1 |                1 | 0.970814 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | adv_no_projection |      0 |                1 | 0.970743 |             0.985366 |         0.95122  |
| amlnet    | lightgbm   | random_graph      |      1 |                1 | 0.970604 |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | random_graph      |      0 |                1 | 0.970366 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | random_feasible   |      2 |                1 | 0.970084 |             0.985366 |         0.95122  |
| amlnet    | lightgbm   | ours              |      2 |                1 | 0.969865 |             0.985366 |         0.94878  |
| amlnet    | lightgbm   | random_graph      |      2 |                1 | 0.968898 |             0.982927 |         0.95122  |

## Counterfactual Validity

| augmentation      |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection |          0.0181432  |                0.957079 |             0.404706 |         1.37603 |         0.0429207 |
| ours              |          0.0181432  |                0        |             0        |         1.30768 |         0.949576  |
| random_feasible   |          0.00521987 |                0        |             0        |         1.30752 |         0.949576  |
| random_graph      |          0.00521987 |                0.926662 |             0.236513 |         1.33234 |         0.0733375 |
