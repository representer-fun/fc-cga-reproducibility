# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v4_smoke_repaired`
Generated: 2026-05-20 15:14:44 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation              |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | feature_noise_repaired_v2 |      0 |                1 | 0.972979 |             0.992683 |         0.943902 |
| amlnet    | lightgbm   | smote_repaired_v2         |      0 |                1 | 0.971715 |             0.990244 |         0.943902 |
| amlnet    | lightgbm   | mixup_repaired_v2         |      0 |                1 | 0.963658 |             0.995122 |         0.941463 |

## Counterfactual Validity

| augmentation              |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| feature_noise_repaired_v2 |         0.00845007  |                       0 |                    0 |        0.931922 |          0.946809 |
| mixup_repaired_v2         |         1.35188     |                       0 |                    0 |        0.959357 |          0.946809 |
| smote_repaired_v2         |         1.76599e-05 |                       0 |                    0 |        0.932161 |          0.946809 |
