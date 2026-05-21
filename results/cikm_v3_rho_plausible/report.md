# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v3_rho_plausible`
Generated: 2026-05-19 20:10:06 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |                1 | 0.9783   |             0.992683 |         0.953659 |
| amlnet    | xgboost    | curriculum_projected_v2         |      2 |                1 | 0.977013 |             0.987805 |         0.953659 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      0 |                1 | 0.976946 |             0.992683 |         0.953659 |
| amlnet    | lightgbm   | typology_projected_v2           |      0 |                1 | 0.976753 |             0.992683 |         0.953659 |
| amlnet    | xgboost    | curriculum_projected_v2         |      1 |                1 | 0.976299 |             0.990244 |         0.953659 |
| amlnet    | lightgbm   | curriculum_projected_v2         |      0 |                1 | 0.975762 |             0.990244 |         0.94878  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      2 |                1 | 0.975567 |             0.990244 |         0.953659 |
| amlnet    | lightgbm   | typology_projected_v2           |      2 |                1 | 0.975488 |             0.992683 |         0.953659 |
| amlnet    | xgboost    | curriculum_projected_v2         |      0 |                1 | 0.975343 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | curriculum_projected_v2         |      1 |                1 | 0.975064 |             0.987805 |         0.94878  |
| amlnet    | xgboost    | plausible_typology_projected_v2 |      1 |                1 | 0.9749   |             0.987805 |         0.95122  |
| amlnet    | xgboost    | plausible_hard_projected_v2     |      2 |                1 | 0.974872 |             0.992683 |         0.95122  |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.29177   |                       0 |                    0 |        0.571073 |          0.949576 |
| plausible_hard_projected_v2     |           4.78849   |                       0 |                    0 |        0.310579 |          0.949576 |
| plausible_typology_projected_v2 |           5.25183   |                       0 |                    0 |        0.297607 |          0.949576 |
| random_feasible_v2              |           0.0261774 |                       0 |                    0 |        1.36568  |          0.949576 |
| typology_projected_v2           |           6.69424   |                       0 |                    0 |        0.533319 |          0.949576 |
