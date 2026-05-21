# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/ablations`
Generated: 2026-05-19 04:39:20 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation         |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:---------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | no_profile           |      2 |                1 | 0.975128 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | no_ledger_projection |      1 |                1 | 0.973656 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | no_ledger_projection |      2 |                1 | 0.973331 |             0.987805 |         0.946341 |
| amlnet    | lightgbm   | full                 |      1 |                1 | 0.97333  |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | amount_only          |      1 |                1 | 0.97333  |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | no_temporal          |      1 |                1 | 0.97333  |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | topology_only        |      1 |                1 | 0.972288 |             0.990244 |         0.95122  |
| amlnet    | lightgbm   | topology_only        |      2 |                1 | 0.971997 |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | no_profile           |      1 |                1 | 0.97182  |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | topology_only        |      0 |                1 | 0.971772 |             0.987805 |         0.94878  |
| amlnet    | lightgbm   | no_temporal          |      0 |                1 | 0.9717   |             0.987805 |         0.95122  |
| amlnet    | lightgbm   | full                 |      0 |                1 | 0.9717   |             0.987805 |         0.95122  |

## Counterfactual Validity

| augmentation             |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:-------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| amount_only              |          0.0181432  |                0        |             0        |         1.30768 |         0.949576  |
| full                     |          0.0181432  |                0        |             0        |         1.30768 |         0.949576  |
| no_adversarial_selection |          0.00521987 |                0        |             0        |         1.30752 |         0.949576  |
| no_ledger_projection     |          0.0181432  |                0.957079 |             0.404706 |         1.37603 |         0.0429207 |
| no_profile               |          0.0181432  |                0        |             0        |         1.36092 |         1         |
| no_temporal              |          0.0181432  |                0        |             0        |         1.30768 |         0.949576  |
| random_feasible          |          0.00521987 |                0        |             0        |         1.30752 |         0.949576  |
| topology_only            |          0.0181432  |                0        |             0        |         1.30472 |         0.949576  |
