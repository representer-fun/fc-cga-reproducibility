# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_fewshot_layering_5`
Generated: 2026-05-21 03:56:43 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      8 |                1 | 0.955366 |             0.974212 |         0.936963 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      8 |                1 | 0.953849 |             0.982808 |         0.939828 |
| amlnet    | lightgbm   | hard_projected_v2               |      7 |                1 | 0.953616 |             0.965616 |         0.936963 |
| amlnet    | lightgbm   | hard_projected_v2               |      8 |                1 | 0.953523 |             0.974212 |         0.925501 |
| amlnet    | xgboost    | curriculum_projected_v2         |      0 |                1 | 0.95215  |             0.95702  |         0.936963 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      8 |                1 | 0.951861 |             0.977077 |         0.931232 |
| amlnet    | lightgbm   | typology_projected_v2           |      8 |                1 | 0.951466 |             0.977077 |         0.934097 |
| amlnet    | lightgbm   | typology_projected_v2           |      7 |                1 | 0.950871 |             0.95702  |         0.936963 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      7 |                1 | 0.950232 |             0.968481 |         0.922636 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |                1 | 0.950231 |             0.962751 |         0.931232 |
| amlnet    | lightgbm   | hard_projected_v2               |      9 |                1 | 0.949468 |             0.951289 |         0.934097 |
| amlnet    | xgboost    | hard_projected_v2               |      6 |                1 | 0.949437 |             0.954155 |         0.936963 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.53874   |                       0 |                    0 |         1.89311 |          0.946746 |
| hard_projected_v2               |           7.35153   |                       0 |                    0 |         1.53566 |          0.946746 |
| none                            |         nan         |                     nan |                  nan |       nan       |        nan        |
| plausible_hard_projected_v2     |           5.63338   |                       0 |                    0 |         1.46361 |          0.946746 |
| plausible_typology_projected_v2 |           6.59201   |                       0 |                    0 |         1.44614 |          0.946746 |
| random_feasible_v2              |           0.0395051 |                       0 |                    0 |         2.69996 |          0.946746 |
| smote_repaired_v2               |           0.157248  |                       0 |                    0 |         2.89503 |          0.946746 |
| typology_projected_v2           |           8.19788   |                       0 |                    0 |         1.48327 |          0.946746 |
