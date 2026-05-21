# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_fewshot_layering_1`
Generated: 2026-05-21 03:38:23 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      2 |                1 | 0.950192 |             0.968481 |         0.936963 |
| amlnet    | lightgbm   | hard_projected_v2               |      6 |                1 | 0.950009 |             0.954155 |         0.934097 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      8 |                1 | 0.949498 |             0.954155 |         0.936963 |
| amlnet    | xgboost    | curriculum_projected_v2         |      9 |                1 | 0.949252 |             0.954155 |         0.928367 |
| amlnet    | xgboost    | hard_projected_v2               |      8 |                1 | 0.949028 |             0.951289 |         0.936963 |
| amlnet    | xgboost    | curriculum_projected_v2         |      2 |                1 | 0.948859 |             0.95702  |         0.931232 |
| amlnet    | xgboost    | plausible_typology_projected_v2 |      8 |                1 | 0.948492 |             0.95702  |         0.936963 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      6 |                1 | 0.948356 |             0.95702  |         0.934097 |
| amlnet    | xgboost    | hard_projected_v2               |      9 |                1 | 0.94835  |             0.951289 |         0.934097 |
| amlnet    | lightgbm   | typology_projected_v2           |      6 |                1 | 0.947953 |             0.95702  |         0.934097 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |                1 | 0.947914 |             0.95702  |         0.939828 |
| amlnet    | xgboost    | curriculum_projected_v2         |      0 |                1 | 0.947865 |             0.959885 |         0.928367 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |            3.45025  |                       0 |                    0 |         1.96764 |          0.945783 |
| hard_projected_v2               |            7.04832  |                       0 |                    0 |         1.59054 |          0.945783 |
| none                            |          nan        |                     nan |                  nan |       nan       |        nan        |
| plausible_hard_projected_v2     |            5.09985  |                       0 |                    0 |         1.52152 |          0.945783 |
| plausible_typology_projected_v2 |            6.24798  |                       0 |                    0 |         1.50903 |          0.945783 |
| random_feasible_v2              |            0.031195 |                       0 |                    0 |         2.73007 |          0.945783 |
| smote_repaired_v2               |            0.146223 |                       0 |                    0 |         2.86079 |          0.945783 |
| typology_projected_v2           |            7.91171  |                       0 |                    0 |         1.54809 |          0.945783 |
