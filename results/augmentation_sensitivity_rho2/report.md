# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/augmentation_sensitivity_rho2`
Generated: 2026-05-19 07:19:03 UTC

## Top Predictive Runs

| dataset   | detector       | augmentation      |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:---------------|:------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm       | ours              |      2 |                1 | 0.973543 |             0.987805 |         0.94878  |
| amlnet    | lightgbm       | random_graph      |      1 |                1 | 0.973209 |             0.985366 |         0.94878  |
| amlnet    | lightgbm       | random_graph      |      0 |                1 | 0.97312  |             0.990244 |         0.94878  |
| amlnet    | lightgbm       | adv_no_projection |      2 |                1 | 0.973044 |             0.985366 |         0.94878  |
| amlnet    | lightgbm       | adv_no_projection |      0 |                1 | 0.9728   |             0.990244 |         0.946341 |
| amlnet    | lightgbm       | ours              |      0 |                1 | 0.972587 |             0.985366 |         0.946341 |
| amlnet    | lightgbm       | random_feasible   |      1 |                1 | 0.972432 |             0.985366 |         0.94878  |
| amlnet    | lightgbm       | random_feasible   |      0 |                1 | 0.972275 |             0.987805 |         0.946341 |
| amlnet    | graphsage_lite | adv_no_projection |      1 |                1 | 0.972151 |             0.990244 |         0.936585 |
| amlnet    | lightgbm       | random_graph      |      2 |                1 | 0.971922 |             0.982927 |         0.94878  |
| amlnet    | lightgbm       | random_feasible   |      2 |                1 | 0.971864 |             0.987805 |         0.95122  |
| amlnet    | graphsage_lite | adv_no_projection |      0 |                1 | 0.97159  |             0.995122 |         0.931707 |

## Counterfactual Validity

| augmentation      |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection |          0.0184821  |                0.960197 |             0.400655 |         1.39802 |         0.0398035 |
| ours              |          0.0184821  |                0        |             0        |         1.31052 |         0.949868  |
| random_feasible   |          0.00512961 |                0        |             0        |         1.30888 |         0.949868  |
| random_graph      |          0.00512961 |                0.928385 |             0.239792 |         1.33586 |         0.0716154 |
