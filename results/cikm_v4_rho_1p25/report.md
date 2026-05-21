# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v4_rho_1p25`
Generated: 2026-05-20 20:47:14 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      1 |                1 | 0.980007 |             0.995122 |         0.956098 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |                1 | 0.979589 |             0.990244 |         0.94878  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      0 |                1 | 0.979151 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      2 |                1 | 0.979084 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | curriculum_projected_v2         |      2 |                1 | 0.978938 |             0.990244 |         0.956098 |
| amlnet    | lightgbm   | typology_projected_v2           |      2 |                1 | 0.978723 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      1 |                1 | 0.978668 |             0.990244 |         0.956098 |
| amlnet    | lightgbm   | typology_projected_v2           |      0 |                1 | 0.978145 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | curriculum_projected_v2         |      1 |                1 | 0.97666  |             0.990244 |         0.953659 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      0 |                1 | 0.976266 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | typology_projected_v2           |      1 |                1 | 0.976037 |             0.992683 |         0.94878  |
| amlnet    | lightgbm   | curriculum_projected_v2         |      0 |                1 | 0.974143 |             0.990244 |         0.94878  |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.67115   |                       0 |                    0 |        0.638691 |          0.950021 |
| plausible_hard_projected_v2     |           5.05176   |                       0 |                    0 |        0.335832 |          0.950021 |
| plausible_typology_projected_v2 |           5.25912   |                       0 |                    0 |        0.346619 |          0.950021 |
| random_feasible_v2              |           0.0316123 |                       0 |                    0 |        1.30088  |          0.950021 |
| typology_projected_v2           |           6.56729   |                       0 |                    0 |        0.602274 |          0.950021 |
