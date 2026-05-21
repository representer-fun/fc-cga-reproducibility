# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/smoke_amlnet`
Generated: 2026-05-18 17:29:50 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation   |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:---------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | topology_only  |      0 |                1 | 0.934449 |             0.95702  |         0.902579 |
| amlnet    | lightgbm   | no_profile     |      0 |                1 | 0.929392 |             0.954155 |         0.896848 |
| amlnet    | lightgbm   | full           |      0 |                1 | 0.928246 |             0.954155 |         0.899713 |
| amlnet    | lightgbm   | no_temporal    |      0 |                1 | 0.928246 |             0.954155 |         0.899713 |
| amlnet    | lightgbm   | amount_only    |      0 |                1 | 0.928246 |             0.954155 |         0.899713 |

## Counterfactual Validity

| augmentation   |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:---------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| amount_only    |          1.3588e-07 |                       0 |                    0 |         1.88916 |          0.945455 |
| full           |          1.3588e-07 |                       0 |                    0 |         1.88916 |          0.945455 |
| no_profile     |          1.3588e-07 |                       0 |                    0 |         1.89482 |          1        |
| no_temporal    |          1.3588e-07 |                       0 |                    0 |         1.88916 |          0.945455 |
| topology_only  |          1.3588e-07 |                       0 |                    0 |         1.89683 |          0.945455 |
