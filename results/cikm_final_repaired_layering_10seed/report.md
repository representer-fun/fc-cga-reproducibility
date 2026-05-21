# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_repaired_layering_10seed`
Generated: 2026-05-21 03:20:17 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      5 |                1 | 0.951162 |             0.965616 |         0.934097 |
| amlnet    | xgboost    | typology_projected_v2           |      8 |                1 | 0.950942 |             0.962751 |         0.936963 |
| amlnet    | xgboost    | hard_projected_v2               |      8 |                1 | 0.950352 |             0.95702  |         0.936963 |
| amlnet    | xgboost    | curriculum_projected_v2         |      8 |                1 | 0.950017 |             0.95702  |         0.925501 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      3 |                1 | 0.949966 |             0.959885 |         0.928367 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      8 |                1 | 0.949758 |             0.95702  |         0.936963 |
| amlnet    | lightgbm   | typology_projected_v2           |      5 |                1 | 0.949612 |             0.965616 |         0.939828 |
| amlnet    | lightgbm   | typology_projected_v2           |      7 |                1 | 0.949575 |             0.95702  |         0.936963 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      3 |                1 | 0.949307 |             0.954155 |         0.928367 |
| amlnet    | xgboost    | hard_projected_v2               |      4 |                1 | 0.949075 |             0.959885 |         0.936963 |
| amlnet    | lightgbm   | typology_projected_v2           |      2 |                1 | 0.949075 |             0.954155 |         0.934097 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      5 |                1 | 0.949028 |             0.968481 |         0.91404  |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.42866   |                0        |            0         |         1.95762 |          0.945455 |
| feature_noise_repaired_v2       |           0.422319  |                0        |            0         |         2.66744 |          0.945455 |
| feature_noise_v2                |           2.54819   |                0.192121 |            0.0220643 |         2.7287  |          0.753333 |
| hard_projected_v2               |           6.86333   |                0        |            0         |         1.59433 |          0.945455 |
| mixup_repaired_v2               |           3.8164    |                0        |            0         |         2.349   |          0.945455 |
| mixup_v2                        |           2.50704   |                0        |            0         |         2.349   |          0.945455 |
| none                            |         nan         |              nan        |          nan         |       nan       |        nan        |
| plausible_hard_projected_v2     |           4.90286   |                0        |            0         |         1.51722 |          0.945455 |
| plausible_typology_projected_v2 |           5.93076   |                0        |            0         |         1.51904 |          0.945455 |
| random_feasible_v2              |           0.0324612 |                0        |            0         |         2.74822 |          0.945455 |
| smote_repaired_v2               |           0.174858  |                0        |            0         |         2.86344 |          0.945455 |
| smote_v2                        |           0.121275  |                0        |            0         |         2.86344 |          0.945455 |
| typology_projected_v2           |           7.82658   |                0        |            0         |         1.55885 |          0.945455 |
