# CIKM Claim Audit

## plausible_hard_projected_v2 vs none

Mean delta AUPRC: -0.0390
Median delta AUPRC: -0.0045
Win rate: 0.411 over 190 paired runs

## plausible_hard_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0324
Median delta AUPRC: -0.0022
Win rate: 0.421 over 214 paired runs

## plausible_hard_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0105
Median delta AUPRC: -0.0089
Win rate: 0.250 over 24 paired runs

## plausible_hard_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0085
Median delta AUPRC: -0.0090
Win rate: 0.250 over 24 paired runs

## plausible_hard_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0106
Median delta AUPRC: -0.0133
Win rate: 0.250 over 24 paired runs

## curriculum_projected_v2 vs none

Mean delta AUPRC: -0.0377
Median delta AUPRC: -0.0016
Win rate: 0.432 over 190 paired runs

## curriculum_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0310
Median delta AUPRC: -0.0004
Win rate: 0.435 over 214 paired runs

## curriculum_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0097
Median delta AUPRC: -0.0056
Win rate: 0.250 over 24 paired runs

## curriculum_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0078
Median delta AUPRC: -0.0047
Win rate: 0.167 over 24 paired runs

## curriculum_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0098
Median delta AUPRC: -0.0071
Win rate: 0.250 over 24 paired runs

## typology_projected_v2 vs none

Mean delta AUPRC: -0.0430
Median delta AUPRC: -0.0044
Win rate: 0.389 over 190 paired runs

## typology_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0360
Median delta AUPRC: -0.0033
Win rate: 0.430 over 214 paired runs

## typology_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0102
Median delta AUPRC: -0.0078
Win rate: 0.250 over 24 paired runs

## typology_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0082
Median delta AUPRC: -0.0062
Win rate: 0.250 over 24 paired runs

## typology_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0103
Median delta AUPRC: -0.0117
Win rate: 0.250 over 24 paired runs

## plausible_typology_projected_v2 vs none

Mean delta AUPRC: -0.0391
Median delta AUPRC: -0.0045
Win rate: 0.389 over 190 paired runs

## plausible_typology_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0323
Median delta AUPRC: -0.0017
Win rate: 0.444 over 214 paired runs

## plausible_typology_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0082
Median delta AUPRC: -0.0088
Win rate: 0.250 over 24 paired runs

## plausible_typology_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0062
Median delta AUPRC: -0.0070
Win rate: 0.417 over 24 paired runs

## plausible_typology_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0083
Median delta AUPRC: -0.0097
Win rate: 0.250 over 24 paired runs

## hard_projected_v2 vs none

Mean delta AUPRC: -0.0429
Median delta AUPRC: -0.0041
Win rate: 0.383 over 256 paired runs

## hard_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0384
Median delta AUPRC: -0.0024
Win rate: 0.415 over 229 paired runs

## hard_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0098
Median delta AUPRC: -0.0107
Win rate: 0.250 over 24 paired runs

## hard_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0078
Median delta AUPRC: -0.0058
Win rate: 0.250 over 24 paired runs

## hard_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0099
Median delta AUPRC: -0.0123
Win rate: 0.250 over 24 paired runs

## hard_projected_v2 vs adv_no_projection_v2

Mean delta AUPRC: -0.0083
Median delta AUPRC: -0.0001
Win rate: 0.479 over 117 paired runs

## Validity

| augmentation                    |   ledger_violation_rate |   mean_flow_residual |   detector_hardness |   acceptance_rate |   profile_drift |   categorical_fractionality_rate |   negative_feature_rate |
|:--------------------------------|------------------------:|---------------------:|--------------------:|------------------:|----------------:|---------------------------------:|------------------------:|
| adv_no_projection_v2            |             0.971473    |           0.474206   |           3.20608   |         0.0285274 |        0.732337 |                      nan         |              nan        |
| boundary_projected_v2           |             0           |           0          |           8.51511   |         0.945044  |      391.319    |                      nan         |              nan        |
| curriculum_projected_v2         |             0           |           0          |           4.11337   |         0.938251  |        0.937222 |                        0         |                0        |
| edge_rewire_v2                  |             0           |           0          |           0.178286  |         0.949612  |        1.30039  |                        0         |                0        |
| feature_noise_repaired_v2       |             0           |           0          |           1.98158   |         0.950138  |        2.04599  |                        0         |                0        |
| feature_noise_v2                |             0.582335    |           0.347231   |           2.43061   |         0.391332  |        2.08258  |                        0.498618  |                0.351541 |
| hard_projected_v2               |             0           |           0          |           7.88665   |         0.943482  |      241.104    |                        0         |                0        |
| mixup_repaired_v2               |             0           |           0          |           1.47977   |         0.949612  |        1.0822   |                        0         |                0        |
| mixup_v2                        |             0.000225225 |           0.00023189 |           1.28777   |         0.949387  |        1.0822   |                        0.0614203 |                0        |
| none                            |           nan           |         nan          |         nan         |       nan         |      nan        |                      nan         |              nan        |
| plausible_hard_projected_v2     |             0           |           0          |           5.86306   |         0.938251  |        0.631643 |                        0         |                0        |
| plausible_typology_projected_v2 |             0           |           0          |           6.29742   |         0.938251  |        0.628854 |                        0         |                0        |
| random_feasible_v2              |             0           |           0          |           0.0607974 |         0.939989  |     2279.76     |                        0         |                0        |
| smote_repaired_v2               |             0           |           0          |           0.265202  |         0.949612  |        1.46006  |                        0         |                0        |
| smote_v2                        |             0           |           0          |           0.277121  |         0.949612  |        1.46006  |                        0.0543776 |                0        |
| typology_projected_v2           |             0           |           0          |           7.65393   |         0.938251  |        0.848206 |                        0         |                0        |

## Reviewer-Risk Notes

- CIKM-ready only if projected hard counterfactuals beat both no augmentation and random feasible projection on the main graph/table detectors.
- Validity alone supports a method paper only if predictive gains are strongest under drift, held-out typology, or label scarcity.
- If no-ledger variants dominate AUPRC, frame projection as preserving deployable validity under small performance tradeoff, or improve selection.