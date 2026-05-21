# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v3_label_scarcity`
Generated: 2026-05-19 19:22:25 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      0 |                1 | 0.980495 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      2 |                1 | 0.979511 |             0.995122 |         0.953659 |
| amlnet    | lightgbm   | hard_projected_v2               |      0 |                1 | 0.979199 |             0.990244 |         0.953659 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      0 |                1 | 0.978852 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | hard_projected_v2               |      2 |                1 | 0.978361 |             0.997561 |         0.95122  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |                1 | 0.97787  |             0.995122 |         0.95122  |
| amlnet    | lightgbm   | typology_projected_v2           |      0 |                1 | 0.977841 |             0.995122 |         0.953659 |
| amlnet    | lightgbm   | typology_projected_v2           |      2 |                1 | 0.977418 |             0.995122 |         0.95122  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      1 |                1 | 0.97709  |             0.992683 |         0.953659 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      0 |                1 | 0.975885 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | hard_projected_v2               |      1 |                1 | 0.975451 |             0.990244 |         0.94878  |
| amlnet    | lightgbm   | typology_projected_v2           |      1 |                1 | 0.974761 |             0.990244 |         0.94878  |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |            4.28333  |                       0 |                    0 |        0.862864 |           0.93162 |
| hard_projected_v2               |            6.98769  |                       0 |                    0 |        0.851742 |           0.93162 |
| none                            |          nan        |                     nan |                  nan |      nan        |         nan       |
| plausible_hard_projected_v2     |            5.69109  |                       0 |                    0 |        0.586155 |           0.93162 |
| plausible_typology_projected_v2 |            5.96032  |                       0 |                    0 |        0.577998 |           0.93162 |
| random_feasible_v2              |            0.106467 |                       0 |                    0 |        1.26367  |           0.93162 |
| typology_projected_v2           |            7.31582  |                       0 |                    0 |        0.855934 |           0.93162 |
