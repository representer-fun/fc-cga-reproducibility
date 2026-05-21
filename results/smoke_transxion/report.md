# Flow Fraud Experiment Report

Run directory: `flow_fraud/runs/smoke_transxion`
Generated: 2026-05-18 17:22:47 UTC

## Top Predictive Runs

| dataset   | detector    | augmentation      |   seed |   label_fraction |     auprc |   recall_at_1pct_fpr |   precision_at_k |
|:----------|:------------|:------------------|-------:|-----------------:|----------:|---------------------:|-----------------:|
| transxion | lightgbm    | random_graph      |      0 |                1 | 0.266492  |             0.75388  |        0.359202  |
| transxion | lightgbm    | adv_no_projection |      0 |                1 | 0.265309  |             0.752772 |        0.349224  |
| transxion | lightgbm    | ours              |      0 |                1 | 0.260713  |             0.74612  |        0.348115  |
| transxion | lightgbm    | none              |      0 |                1 | 0.260568  |             0.751663 |        0.356984  |
| transxion | lightgbm    | random_feasible   |      0 |                1 | 0.25805   |             0.747228 |        0.348115  |
| transxion | logistic    | random_graph      |      0 |                1 | 0.112647  |             0.505543 |        0.211752  |
| transxion | topology_lr | random_graph      |      0 |                1 | 0.0684614 |             0.437916 |        0.174058  |
| transxion | logistic    | random_feasible   |      0 |                1 | 0.0590646 |             0.461197 |        0.116408  |
| transxion | topology_lr | none              |      0 |                1 | 0.0537417 |             0.480044 |        0.097561  |
| transxion | logistic    | ours              |      0 |                1 | 0.0531512 |             0.429047 |        0.12306   |
| transxion | topology_lr | adv_no_projection |      0 |                1 | 0.0441185 |             0.467849 |        0.059867  |
| transxion | logistic    | adv_no_projection |      0 |                1 | 0.044009  |             0.426829 |        0.0898004 |

## Counterfactual Validity

| augmentation      |   detector_hardness |   ledger_violation_rate |   mean_flow_residual |   profile_drift |   acceptance_rate |
|:------------------|--------------------:|------------------------:|---------------------:|----------------:|------------------:|
| adv_no_projection |          0.0344522  |                0.959459 |             0.401627 |        0.528062 |         0.0405405 |
| none              |        nan          |              nan        |           nan        |      nan        |       nan         |
| ours              |          0.0344522  |                0        |             0        |        0.350754 |         0.95      |
| random_feasible   |          0.00674008 |                0        |             0        |        0.422113 |         0.95      |
| random_graph      |          0.00674008 |                0.935135 |             0.237658 |        0.479447 |         0.0648649 |
