# Flow Fraud Experiment Report

Run directory: `/home/ubuntu/flow_fraud/runs/cikm_v4_label_scarcity_5seed`
Generated: 2026-05-20 20:25:38 UTC

## Top Predictive Runs

| dataset   | detector   | augmentation                    |   seed |   label_fraction |    auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:-----------|:--------------------------------|-------:|-----------------:|---------:|---------------------:|-----------------:|
| amlnet    | lightgbm   | none                            |      2 |             0.25 | 0.923991 |             0.978049 |         0.9      |
| amlnet    | lightgbm   | curriculum_projected_v2         |      2 |             0.25 | 0.917916 |             0.982927 |         0.878049 |
| amlnet    | lightgbm   | random_feasible_v2              |      3 |             0.25 | 0.917879 |             0.985366 |         0.873171 |
| amlnet    | lightgbm   | random_feasible_v2              |      2 |             0.25 | 0.914373 |             0.978049 |         0.882927 |
| amlnet    | lightgbm   | none                            |      3 |             0.25 | 0.912564 |             0.982927 |         0.87561  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      0 |             0.25 | 0.909182 |             0.97561  |         0.890244 |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      2 |             0.25 | 0.90852  |             0.990244 |         0.865854 |
| amlnet    | lightgbm   | none                            |      4 |             0.25 | 0.907122 |             0.987805 |         0.87561  |
| amlnet    | lightgbm   | plausible_typology_projected_v2 |      3 |             0.05 | 0.904314 |             0.953659 |         0.878049 |
| amlnet    | lightgbm   | typology_projected_v2           |      3 |             0.05 | 0.903265 |             0.956098 |         0.84878  |
| amlnet    | lightgbm   | plausible_hard_projected_v2     |      2 |             0.25 | 0.902486 |             0.992683 |         0.853659 |
| amlnet    | lightgbm   | none                            |      2 |             0.05 | 0.901161 |             0.960976 |         0.841463 |

## Counterfactual Validity

| augmentation                    |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:--------------------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| curriculum_projected_v2         |           4.61412   |                       0 |                    0 |        0.990569 |          0.925623 |
| none                            |         nan         |                     nan |                  nan |      nan        |        nan        |
| plausible_hard_projected_v2     |           5.91128   |                       0 |                    0 |        0.681396 |          0.925623 |
| plausible_typology_projected_v2 |           6.11355   |                       0 |                    0 |        0.688582 |          0.925623 |
| random_feasible_v2              |           0.0974616 |                       0 |                    0 |        1.30383  |          0.925623 |
| typology_projected_v2           |           7.50622   |                       0 |                    0 |        0.971712 |          0.925623 |
