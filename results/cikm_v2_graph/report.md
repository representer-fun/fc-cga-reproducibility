# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_graph`
Generated: 2026-05-19 15:31:07 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation          |   seed |   label_fraction |     auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------|-------:|-----------------:|----------:|---------------------:|-----------------:|
| amlnet    | pyg_sage   | adv_no_projection_v2  |      2 |                1 | 0.464296  |             0.797561 |        0.395122  |
| amlnet    | pyg_sage   | boundary_projected_v2 |      2 |                1 | 0.458967  |             0.768293 |        0.392683  |
| amlnet    | pyg_sage   | hard_projected_v2     |      2 |                1 | 0.458525  |             0.768293 |        0.392683  |
| amlnet    | pyg_sage   | none                  |      2 |                1 | 0.457597  |             0.787805 |        0.385366  |
| amlnet    | pyg_sage   | none                  |      0 |                1 | 0.453618  |             0.8      |        0.387805  |
| amlnet    | pyg_sage   | random_feasible_v2    |      2 |                1 | 0.448988  |             0.753659 |        0.373171  |
| amlnet    | pyg_sage   | random_feasible_v2    |      0 |                1 | 0.440075  |             0.743902 |        0.365854  |
| amlnet    | pyg_sage   | adv_no_projection_v2  |      0 |                1 | 0.412508  |             0.758537 |        0.373171  |
| amlnet    | pyg_sage   | boundary_projected_v2 |      0 |                1 | 0.399009  |             0.702439 |        0.373171  |
| amlnet    | pyg_sage   | hard_projected_v2     |      0 |                1 | 0.398323  |             0.7      |        0.373171  |
| amlnet    | pyg_sage   | none                  |      1 |                1 | 0.03541   |             0.402439 |        0.0341463 |
| amlnet    | pyg_sage   | hard_projected_v2     |      1 |                1 | 0.0326585 |             0.326829 |        0.0414634 |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection_v2  |           1.767     |                0.972242 |             0.458243 |        0.709639 |         0.0277578 |
| boundary_projected_v2 |           7.30189   |                0        |             0        |        0.572595 |         0.949603  |
| hard_projected_v2     |           7.33741   |                0        |             0        |        0.570082 |         0.949603  |
| none                  |         nan         |              nan        |           nan        |      nan        |       nan         |
| random_feasible_v2    |           0.0242939 |                0        |             0        |        1.31484  |         0.949603  |
