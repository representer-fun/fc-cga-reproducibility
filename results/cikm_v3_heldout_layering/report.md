# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v3_heldout_layering`
Generated: 2026-05-19 19:28:09 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | typology_projected_v2           |      2 |                1 | 0.949075 |             0.954155 |         0.934097 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      0 |                1 | 0.948659 |             0.95702  |         0.931232 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |                1 | 0.948135 |             0.951289 |         0.931232 |
| amlnet    | xgboost    | curriculum_projected_v2         |      0 |                1 | 0.947975 |             0.95702  |         0.931232 |
| amlnet    | lightgbm   | typology_projected_v2           |      1 |                1 | 0.947048 |             0.951289 |         0.934097 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      2 |                1 | 0.946975 |             0.951289 |         0.922636 |
| amlnet    | lightgbm   | typology_projected_v2           |      0 |                1 | 0.946767 |             0.954155 |         0.934097 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      0 |                1 | 0.946633 |             0.95702  |         0.934097 |
| amlnet    | lightgbm   | hard_projected_v2               |      2 |                1 | 0.946403 |             0.951289 |         0.919771 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      1 |                1 | 0.945981 |             0.954155 |         0.928367 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      2 |                1 | 0.945764 |             0.954155 |         0.931232 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      1 |                1 | 0.945457 |             0.951289 |         0.931232 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.37271   |                       0 |                    0 |         1.96148 |          0.945455 |
| hard_projected_v2               |           6.55429   |                       0 |                    0 |         1.60987 |          0.945455 |
| none                            |         nan         |                     nan |                  nan |       nan       |        nan        |
| plausible_hard_projected_v2     |           4.66082   |                       0 |                    0 |         1.52602 |          0.945455 |
| plausible_typology_projected_v2 |           5.79863   |                       0 |                    0 |         1.5388  |          0.945455 |
| random_feasible_v2              |           0.0164707 |                       0 |                    0 |         2.75894 |          0.945455 |
| typology_projected_v2           |           7.60806   |                       0 |                    0 |         1.57262 |          0.945455 |
