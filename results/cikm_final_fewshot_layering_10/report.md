# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_fewshot_layering_10`
Generated: 2026-05-21 04:15:05 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | hard_projected_v2               |      7 |                1 | 0.959053 |             0.977077 |         0.939828 |
| amlnet    | lightgbm   | typology_projected_v2           |      1 |                1 | 0.958553 |             0.977077 |         0.934097 |
| amlnet    | lightgbm   | hard_projected_v2               |      1 |                1 | 0.958368 |             0.965616 |         0.934097 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      1 |                1 | 0.957619 |             0.974212 |         0.936963 |
| amlnet    | lightgbm   | typology_projected_v2           |      7 |                1 | 0.957397 |             0.977077 |         0.934097 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      7 |                1 | 0.956956 |             0.979943 |         0.934097 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      1 |                1 | 0.955424 |             0.977077 |         0.939828 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      7 |                1 | 0.954987 |             0.974212 |         0.936963 |
| amlnet    | lightgbm   | hard_projected_v2               |      9 |                1 | 0.954422 |             0.968481 |         0.931232 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      1 |                1 | 0.954232 |             0.974212 |         0.908309 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      9 |                1 | 0.953925 |             0.971347 |         0.922636 |
| amlnet    | lightgbm   | typology_projected_v2           |      9 |                1 | 0.953563 |             0.959885 |         0.936963 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.43882   |                       0 |                    0 |         1.88569 |          0.947674 |
| hard_projected_v2               |           7.00173   |                       0 |                    0 |         1.52541 |          0.947674 |
| none                            |         nan         |                     nan |                  nan |       nan       |        nan        |
| plausible_hard_projected_v2     |           5.30203   |                       0 |                    0 |         1.41536 |          0.947674 |
| plausible_typology_projected_v2 |           6.34058   |                       0 |                    0 |         1.4136  |          0.947674 |
| random_feasible_v2              |           0.0311499 |                       0 |                    0 |         2.72833 |          0.947674 |
| smote_repaired_v2               |           0.137359  |                       0 |                    0 |         2.86216 |          0.947674 |
| typology_projected_v2           |           7.82778   |                       0 |                    0 |         1.49076 |          0.947674 |
