# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_coldstart_low_history_entity`
Generated: 2026-05-21 04:30:32 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | xgboost    | curriculum_projected_v2         |      4 |                1 | 0.964646 |                    1 |         0.909091 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      0 |                1 | 0.964646 |                    1 |         0.909091 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      4 |                1 | 0.95671  |                    1 |         0.909091 |
| amlnet    | xgboost    | plausible_typology_projected_v2 |      0 |                1 | 0.950758 |                    1 |         0.909091 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      3 |                1 | 0.947552 |                    1 |         0.909091 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      3 |                1 | 0.947552 |                    1 |         0.909091 |
| amlnet    | xgboost    | typology_projected_v2           |      0 |                1 | 0.946128 |                    1 |         0.909091 |
| amlnet    | xgboost    | typology_projected_v2           |      2 |                1 | 0.946128 |                    1 |         0.909091 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      0 |                1 | 0.944805 |                    1 |         0.909091 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      3 |                1 | 0.944805 |                    1 |         0.909091 |
| amlnet    | lightgbm   | typology_projected_v2           |      3 |                1 | 0.942424 |                    1 |         0.909091 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      4 |                1 | 0.940341 |                    1 |         0.909091 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.40857   |                       0 |                    0 |         1.95979 |          0.945455 |
| none                            |         nan         |                     nan |                  nan |       nan       |        nan        |
| plausible_hard_projected_v2     |           4.91519   |                       0 |                    0 |         1.51466 |          0.945455 |
| plausible_typology_projected_v2 |           5.96481   |                       0 |                    0 |         1.516   |          0.945455 |
| random_feasible_v2              |           0.0269261 |                       0 |                    0 |         2.75618 |          0.945455 |
| smote_repaired_v2               |           0.174783  |                       0 |                    0 |         2.87697 |          0.945455 |
| typology_projected_v2           |           7.79675   |                       0 |                    0 |         1.56388 |          0.945455 |
