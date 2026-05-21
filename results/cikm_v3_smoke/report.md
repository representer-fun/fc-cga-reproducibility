# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v3_smoke`
Generated: 2026-05-19 16:17:39 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | smote_v2                    |      0 |                1 | 0.972915 |             0.987805 |         0.946341 |
| amlnet    | lightgbm   | feature_noise_v2            |      0 |                1 | 0.972418 |             0.992683 |         0.941463 |
| amlnet    | lightgbm   | plausible_hard_projected_v2 |      0 |                1 | 0.970733 |             0.992683 |         0.941463 |
| amlnet    | lightgbm   | typology_projected_v2       |      0 |                1 | 0.969907 |             0.995122 |         0.943902 |

## Counterfactual Validity

| augmentation                |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| feature_noise_v2            |         0.0923693   |                0.680851 |             0.174201 |        1.10284  |          0.297872 |
| plausible_hard_projected_v2 |         0.658181    |                0        |             0        |        0.45418  |          0.946809 |
| smote_v2                    |         1.76611e-05 |                0        |             0        |        0.932161 |          0.946809 |
| typology_projected_v2       |         2.5334      |                0        |             0        |        0.807998 |          0.946809 |
