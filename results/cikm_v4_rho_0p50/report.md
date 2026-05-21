# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v4_rho_0p50`
Generated: 2026-05-20 20:36:34 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | curriculum_projected_v2         |      1 |                1 | 0.980195 |             0.992683 |         0.953659 |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      0 |                1 | 0.979149 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      2 |                1 | 0.978879 |             0.995122 |         0.95122  |
| amlnet    | lightgbm   | curriculum_projected_v2         |      0 |                1 | 0.978754 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |                1 | 0.978471 |             0.992683 |         0.953659 |
| amlnet    | lightgbm   | typology_projected_v2           |      0 |                1 | 0.978248 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      0 |                1 | 0.97823  |             0.987805 |         0.953659 |
| amlnet    | lightgbm   | typology_projected_v2           |      2 |                1 | 0.977295 |             0.992683 |         0.953659 |
| amlnet    | lightgbm   | typology_projected_v2           |      1 |                1 | 0.976765 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      1 |                1 | 0.975256 |             0.992683 |         0.95122  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      1 |                1 | 0.974938 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | curriculum_projected_v2         |      2 |                1 | 0.973802 |             0.985366 |         0.94878  |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.42655   |                       0 |                    0 |        0.643439 |          0.949576 |
| plausible_hard_projected_v2     |           4.64498   |                       0 |                    0 |        0.330171 |          0.949576 |
| plausible_typology_projected_v2 |           4.86579   |                       0 |                    0 |        0.337361 |          0.949576 |
| random_feasible_v2              |           0.0269835 |                       0 |                    0 |        1.31353  |          0.949576 |
| typology_projected_v2           |           6.20923   |                       0 |                    0 |        0.605979 |          0.949576 |
