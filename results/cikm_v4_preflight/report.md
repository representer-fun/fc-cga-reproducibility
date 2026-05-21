# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v4_preflight`
Generated: 2026-05-20 17:01:47 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | feature_noise_repaired_v2       |      0 |                1 | 0.975009 |             0.990244 |         0.946341 |
| amlnet    | lightgbm   | mixup_repaired_v2               |      0 |                1 | 0.972812 |             0.992683 |         0.943902 |
| amlnet    | lightgbm   | smote_repaired_v2               |      0 |                1 | 0.972372 |             0.990244 |         0.946341 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      0 |                1 | 0.96564  |             0.990244 |         0.936585 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| feature_noise_repaired_v2       |          0.117268   |                       0 |                    0 |        1.3347   |          0.947183 |
| mixup_repaired_v2               |          1.51022    |                       0 |                    0 |        0.892859 |          0.947183 |
| plausible_typology_projected_v2 |          1.3615     |                       0 |                    0 |        0.292635 |          0.947183 |
| smote_repaired_v2               |          0.00101758 |                       0 |                    0 |        1.31065  |          0.947183 |
