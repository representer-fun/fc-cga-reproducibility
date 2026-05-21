# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_final_graph_layering`
Generated: 2026-05-21 04:53:52 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | pyg_gat    | smote_repaired_v2               |      0 |                1 | 0.775593 |             0.91404  |         0.716332 |
| amlnet    | pyg_gat    | none                            |      0 |                1 | 0.770579 |             0.91404  |         0.707736 |
| amlnet    | pyg_gat    | random_feasible_v2              |      0 |                1 | 0.76621  |             0.91404  |         0.713467 |
| amlnet    | pyg_gat    | smote_repaired_v2               |      1 |                1 | 0.753954 |             0.928367 |         0.679083 |
| amlnet    | pyg_gat    | none                            |      1 |                1 | 0.741054 |             0.925501 |         0.670487 |
| amlnet    | pyg_gat    | curriculum_projected_v2         |      0 |                1 | 0.740789 |             0.916905 |         0.664756 |
| amlnet    | pyg_gat    | random_feasible_v2              |      1 |                1 | 0.736275 |             0.922636 |         0.659026 |
| amlnet    | pyg_gat    | curriculum_projected_v2         |      1 |                1 | 0.697733 |             0.91404  |         0.618911 |
| amlnet    | pyg_gat    | plausible_typology_projected_v2 |      0 |                1 | 0.691335 |             0.919771 |         0.624642 |
| amlnet    | pyg_gat    | typology_projected_v2           |      0 |                1 | 0.68985  |             0.931232 |         0.604585 |
| amlnet    | pyg_gat    | plausible_typology_projected_v2 |      1 |                1 | 0.678941 |             0.902579 |         0.598854 |
| amlnet    | pyg_gat    | typology_projected_v2           |      1 |                1 | 0.664353 |             0.896848 |         0.581662 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           3.79012   |                       0 |                    0 |         1.90515 |          0.945455 |
| none                            |         nan         |                     nan |                  nan |       nan       |        nan        |
| plausible_typology_projected_v2 |           5.69457   |                       0 |                    0 |         1.46139 |          0.945455 |
| random_feasible_v2              |           0.0241664 |                       0 |                    0 |         2.75894 |          0.945455 |
| smote_repaired_v2               |           0.245883  |                       0 |                    0 |         2.88207 |          0.945455 |
| typology_projected_v2           |           8.10301   |                       0 |                    0 |         1.50471 |          0.945455 |
