# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_heldout_integration`
Generated: 2026-05-19 15:17:45 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation          |   seed |   label_fraction |     auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:----------------------|-------:|-----------------:|----------:|---------------------:|-----------------:|
| amlnet    | pyg_sage   | none                  |      2 |                1 | 0.142841  |                    1 |        0.153846  |
| amlnet    | pyg_sage   | adv_no_projection_v2  |      2 |                1 | 0.0762609 |                    1 |        0.153846  |
| amlnet    | pyg_sage   | boundary_projected_v2 |      2 |                1 | 0.0575637 |                    1 |        0.0769231 |
| amlnet    | pyg_sage   | hard_projected_v2     |      2 |                1 | 0.0540592 |                    1 |        0.0769231 |
| amlnet    | pyg_sage   | none                  |      0 |                1 | 0.0269315 |                    1 |        0.0769231 |
| amlnet    | pyg_sage   | boundary_projected_v2 |      1 |                1 | 0.0224262 |                    1 |        0         |
| amlnet    | pyg_sage   | boundary_projected_v2 |      0 |                1 | 0.0215821 |                    1 |        0         |
| amlnet    | pyg_sage   | hard_projected_v2     |      1 |                1 | 0.0211768 |                    1 |        0         |
| amlnet    | pyg_sage   | adv_no_projection_v2  |      0 |                1 | 0.0209126 |                    1 |        0         |
| amlnet    | pyg_sage   | hard_projected_v2     |      0 |                1 | 0.0190563 |                    1 |        0         |
| amlnet    | pyg_sage   | adv_no_projection_v2  |      1 |                1 | 0.018847  |                    1 |        0         |
| amlnet    | pyg_sage   | none                  |      1 |                1 | 0.0161146 |                    1 |        0         |

## Counterfactual Validity

| augmentation          |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:----------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection_v2  |             3.7133  |                0.970671 |             0.458394 |        0.584546 |         0.0293294 |
| boundary_projected_v2 |             9.77735 |                0        |             0        |        0.522693 |         0.949617  |
| hard_projected_v2     |             9.80306 |                0        |             0        |        0.52485  |         0.949617  |
| none                  |           nan       |              nan        |           nan        |      nan        |       nan         |
