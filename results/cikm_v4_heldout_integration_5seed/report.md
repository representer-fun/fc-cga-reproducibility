# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v4_heldout_integration_5seed`
Generated: 2026-05-20 18:33:59 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |       auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|------------:|---------------------:|-----------------:|
| amlnet    | xgboost    | plausible_typology_projected_v2 |      4 |                1 | 0.000860665 |                    0 |                0 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      0 |                1 | 0.00073226  |                    0 |                0 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      3 |                1 | 0.000714107 |                    0 |                0 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      4 |                1 | 0.000637801 |                    0 |                0 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      2 |                1 | 0.000618666 |                    0 |                0 |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      1 |                1 | 0.000584478 |                    0 |                0 |
| amlnet    | xgboost    | plausible_typology_projected_v2 |      0 |                1 | 0.000584293 |                    0 |                0 |
| amlnet    | xgboost    | hard_projected_v2               |      2 |                1 | 0.000519423 |                    0 |                0 |
| amlnet    | xgboost    | typology_projected_v2           |      4 |                1 | 0.000512771 |                    0 |                0 |
| amlnet    | xgboost    | hard_projected_v2               |      4 |                1 | 0.000459993 |                    0 |                0 |
| amlnet    | xgboost    | typology_projected_v2           |      2 |                1 | 0.000444858 |                    0 |                0 |
| amlnet    | xgboost    | plausible_typology_projected_v2 |      2 |                1 | 0.000442361 |                    0 |                0 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           4.25736   |                       0 |                    0 |        0.689514 |          0.948905 |
| hard_projected_v2               |           8.59077   |                       0 |                    0 |        0.532853 |          0.948905 |
| none                            |         nan         |                     nan |                  nan |      nan        |        nan        |
| plausible_hard_projected_v2     |           7.95658   |                       0 |                    0 |        0.395781 |          0.948905 |
| plausible_typology_projected_v2 |           8.9737    |                       0 |                    0 |        0.366691 |          0.948905 |
| random_feasible_v2              |           0.0115497 |                       0 |                    0 |        2.05594  |          0.948905 |
| typology_projected_v2           |          10.0497    |                       0 |                    0 |        0.500758 |          0.948905 |
