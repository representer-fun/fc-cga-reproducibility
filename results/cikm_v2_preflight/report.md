# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v2_preflight`
Generated: 2026-05-19 10:16:47 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation      |   seed |   label_fraction |     auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:------------------|-------:|-----------------:|----------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | hard_projected_v2 |      0 |                1 | 0.978488  |             0.997561 |       0.95122    |
| amlnet    | lightgbm   | hard_projected_v2 |      0 |                1 | 0.978488  |             0.997561 |       0.95122    |
| amlnet    | lightgbm   | none              |      0 |                1 | 0.96911   |             0.990244 |       0.939024   |
| amlnet    | lightgbm   | none              |      0 |                1 | 0.96911   |             0.990244 |       0.939024   |
| amlnet    | pyg_sage   | none              |      0 |                1 | 0.0165699 |             0.136585 |       0.00731707 |
| amlnet    | pyg_sage   | none              |      0 |                1 | 0.0165699 |             0.136585 |       0.00731707 |
| amlnet    | pyg_sage   | hard_projected_v2 |      0 |                1 | 0.0158685 |             0.12439  |       0.00731707 |
| amlnet    | pyg_sage   | hard_projected_v2 |      0 |                1 | 0.0158685 |             0.12439  |       0.00731707 |

## Counterfactual Validity

| augmentation      |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| hard_projected_v2 |             3.35804 |                       0 |                    0 |        0.814365 |           0.94709 |
| none              |           nan       |                     nan |                  nan |      nan        |         nan       |
