# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/full_matrix`
Generated: 2026-05-18 20:28:31 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation      |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | xgboost    | adv_no_projection |      2 |                1 | 0.976751 |             0.990244 |         0.95122  |
| amlnet    | xgboost    | random_graph      |      1 |                1 | 0.975819 |             0.990244 |         0.95122  |
| amlnet    | xgboost    | none              |      2 |                1 | 0.974894 |             0.987805 |         0.95122  |
| amlnet    | xgboost    | random_feasible   |      0 |                1 | 0.974802 |             0.987805 |         0.95122  |
| amlnet    | xgboost    | ours              |      2 |                1 | 0.974799 |             0.987805 |         0.953659 |
| amlnet    | lightgbm   | adv_no_projection |      2 |                1 | 0.974686 |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | random_feasible   |      0 |                1 | 0.974371 |             0.985366 |         0.95122  |
| amlnet    | xgboost    | adv_no_projection |      1 |                1 | 0.974337 |             0.992683 |         0.95122  |
| amlnet    | xgboost    | none              |      1 |                1 | 0.974201 |             0.987805 |         0.94878  |
| amlnet    | xgboost    | none              |      0 |                1 | 0.974055 |             0.990244 |         0.95122  |
| amlnet    | xgboost    | random_feasible   |      1 |                1 | 0.974043 |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | random_graph      |      2 |                1 | 0.973919 |             0.987805 |         0.95122  |

## Counterfactual Validity

| augmentation      |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection |          0.018563   |                0.960006 |             0.401408 |         1.39359 |         0.0399936 |
| none              |        nan          |              nan        |           nan        |       nan       |       nan         |
| ours              |          0.018563   |                0        |             0        |         1.31328 |         0.949603  |
| random_feasible   |          0.00517075 |                0        |             0        |         1.30348 |         0.949603  |
| random_graph      |          0.00517075 |                0.924495 |             0.239236 |         1.32745 |         0.075505  |
