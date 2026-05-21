# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v3_preflight`
Generated: 2026-05-19 16:19:23 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | xgboost    | curriculum_projected_v2     |      0 |                1 | 0.974448 |             0.995122 |         0.941463 |
| amlnet    | xgboost    | feature_noise_v2            |      0 |                1 | 0.973687 |             0.990244 |         0.946341 |
| amlnet    | lightgbm   | typology_projected_v2       |      0 |                1 | 0.973578 |             0.995122 |         0.939024 |
| amlnet    | lightgbm   | feature_noise_v2            |      0 |                1 | 0.973157 |             0.992683 |         0.941463 |
| amlnet    | xgboost    | smote_v2                    |      0 |                1 | 0.973013 |             0.990244 |         0.94878  |
| amlnet    | xgboost    | none                        |      0 |                1 | 0.97217  |             0.990244 |         0.946341 |
| amlnet    | lightgbm   | none                        |      0 |                1 | 0.972033 |             0.992683 |         0.939024 |
| amlnet    | lightgbm   | curriculum_projected_v2     |      0 |                1 | 0.972001 |             0.995122 |         0.92439  |
| amlnet    | lightgbm   | smote_v2                    |      0 |                1 | 0.96976  |             0.990244 |         0.941463 |
| amlnet    | lightgbm   | plausible_hard_projected_v2 |      0 |                1 | 0.969676 |             0.995122 |         0.936585 |
| amlnet    | xgboost    | typology_projected_v2       |      0 |                1 | 0.968602 |             0.995122 |         0.943902 |
| amlnet    | xgboost    | plausible_hard_projected_v2 |      0 |                1 | 0.96722  |             0.992683 |         0.941463 |

## Counterfactual Validity

| augmentation                |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2     |           2.90191   |                0        |             0        |        0.818728 |          0.947183 |
| feature_noise_v2            |           0.701553  |                0.554577 |             0.109066 |        1.27422  |          0.403169 |
| none                        |         nan         |              nan        |           nan        |      nan        |        nan        |
| plausible_hard_projected_v2 |           1.94012   |                0        |             0        |        0.411165 |          0.947183 |
| smote_v2                    |           0.0109205 |                0        |             0        |        1.29661  |          0.947183 |
| typology_projected_v2       |           6.07753   |                0        |             0        |        0.78668  |          0.947183 |
