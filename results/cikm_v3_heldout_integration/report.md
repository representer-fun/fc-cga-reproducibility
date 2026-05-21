# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v3_heldout_integration`
Generated: 2026-05-19 19:45:41 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |       auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|------------:|---------------------:|-----------------:|
| amlnet    | xgboost    | plausible_hard_projected_v2     |      0 |                1 | 0.00073226  |                    0 |                0 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      2 |                1 | 0.000618666 |                    0 |                0 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      1 |                1 | 0.000584478 |                    0 |                0 |
| amlnet    | xgboost    | plausible_typology_projected_v2 |      0 |                1 | 0.000584293 |                    0 |                0 |
| amlnet    | xgboost    | hard_projected_v2               |      2 |                1 | 0.000519423 |                    0 |                0 |
| amlnet    | xgboost    | typology_projected_v2           |      2 |                1 | 0.000444858 |                    0 |                0 |
| amlnet    | xgboost    | plausible_typology_projected_v2 |      2 |                1 | 0.000442361 |                    0 |                0 |
| amlnet    | xgboost    | plausible_typology_projected_v2 |      1 |                1 | 0.000427204 |                    0 |                0 |
| amlnet    | xgboost    | typology_projected_v2           |      0 |                1 | 0.000406404 |                    0 |                0 |
| amlnet    | xgboost    | typology_projected_v2           |      1 |                1 | 0.000388977 |                    0 |                0 |
| amlnet    | xgboost    | curriculum_projected_v2         |      1 |                1 | 0.000384113 |                    0 |                0 |
| amlnet    | xgboost    | hard_projected_v2               |      1 |                1 | 0.000364128 |                    0 |                0 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           4.22891   |                       0 |                    0 |        0.686347 |          0.948905 |
| hard_projected_v2               |           8.54487   |                       0 |                    0 |        0.539267 |          0.948905 |
| none                            |         nan         |                     nan |                  nan |      nan        |        nan        |
| plausible_hard_projected_v2     |           7.88923   |                       0 |                    0 |        0.395999 |          0.948905 |
| plausible_typology_projected_v2 |           8.90965   |                       0 |                    0 |        0.364204 |          0.948905 |
| random_feasible_v2              |           0.0157821 |                       0 |                    0 |        2.05967  |          0.948905 |
| typology_projected_v2           |          10.0512    |                       0 |                    0 |        0.506642 |          0.948905 |
