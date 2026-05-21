# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_external`
Generated: 2026-05-19 16:05:17 UTC

## Top Predictive Runs

| dataset    | detector   | augmentation          |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:-----------|:-----------|:----------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| ellipticpp | xgboost    | hard_projected_v2     |      0 |                1 | 0.56401  |             0.486998 |         0.503546 |
| ellipticpp | xgboost    | boundary_projected_v2 |      0 |                1 | 0.561277 |             0.489362 |         0.503546 |
| ellipticpp | lightgbm   | none                  |      0 |                1 | 0.557204 |             0.491726 |         0.503546 |
| ellipticpp | xgboost    | random_feasible_v2    |      2 |                1 | 0.5569   |             0.49409  |         0.501182 |
| ellipticpp | xgboost    | boundary_projected_v2 |      1 |                1 | 0.556635 |             0.48227  |         0.496454 |
| ellipticpp | xgboost    | boundary_projected_v2 |      2 |                1 | 0.556416 |             0.48227  |         0.49409  |
| ellipticpp | xgboost    | hard_projected_v2     |      1 |                1 | 0.555563 |             0.48227  |         0.498818 |
| ellipticpp | xgboost    | hard_projected_v2     |      2 |                1 | 0.555191 |             0.48227  |         0.49409  |
| ellipticpp | lightgbm   | random_feasible_v2    |      0 |                1 | 0.554722 |             0.489362 |         0.508274 |
| ellipticpp | lightgbm   | boundary_projected_v2 |      2 |                1 | 0.554166 |             0.479905 |         0.496454 |
| ellipticpp | lightgbm   | random_feasible_v2    |      2 |                1 | 0.553919 |             0.486998 |         0.498818 |
| ellipticpp | lightgbm   | hard_projected_v2     |      2 |                1 | 0.553701 |             0.477541 |         0.49409  |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| boundary_projected_v2 |          7.00999    |                       0 |                    0 |         5469.77 |          0.949968 |
| hard_projected_v2     |          7.00893    |                       0 |                    0 |         6837    |          0.949968 |
| none                  |        nan          |                     nan |                  nan |          nan    |        nan        |
| random_feasible_v2    |          0.00153999 |                       0 |                    0 |        79233.9  |          0.949968 |
