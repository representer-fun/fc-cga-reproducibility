# CIKM Claim Audit

## plausible_hard_projected_v2 vs none

Mean delta AUPRC: -0.0374
Median delta AUPRC: -0.0064
Win rate: 0.372 over 78 paired runs

## plausible_hard_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0280
Median delta AUPRC: -0.0036
Win rate: 0.378 over 90 paired runs

## plausible_hard_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0105
Median delta AUPRC: -0.0089
Win rate: 0.250 over 12 paired runs

## plausible_hard_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0085
Median delta AUPRC: -0.0090
Win rate: 0.250 over 12 paired runs

## plausible_hard_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0107
Median delta AUPRC: -0.0133
Win rate: 0.250 over 12 paired runs

## curriculum_projected_v2 vs none

Mean delta AUPRC: -0.0363
Median delta AUPRC: -0.0023
Win rate: 0.397 over 78 paired runs

## curriculum_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0269
Median delta AUPRC: -0.0004
Win rate: 0.422 over 90 paired runs

## curriculum_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0097
Median delta AUPRC: -0.0056
Win rate: 0.250 over 12 paired runs

## curriculum_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0078
Median delta AUPRC: -0.0047
Win rate: 0.167 over 12 paired runs

## curriculum_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0100
Median delta AUPRC: -0.0071
Win rate: 0.250 over 12 paired runs

## typology_projected_v2 vs none

Mean delta AUPRC: -0.0423
Median delta AUPRC: -0.0065
Win rate: 0.333 over 78 paired runs

## typology_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0324
Median delta AUPRC: -0.0039
Win rate: 0.400 over 90 paired runs

## typology_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0102
Median delta AUPRC: -0.0078
Win rate: 0.250 over 12 paired runs

## typology_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0082
Median delta AUPRC: -0.0062
Win rate: 0.250 over 12 paired runs

## typology_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0105
Median delta AUPRC: -0.0117
Win rate: 0.250 over 12 paired runs

## plausible_typology_projected_v2 vs none

Mean delta AUPRC: -0.0340
Median delta AUPRC: -0.0064
Win rate: 0.359 over 78 paired runs

## plausible_typology_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0249
Median delta AUPRC: -0.0019
Win rate: 0.422 over 90 paired runs

## plausible_typology_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0082
Median delta AUPRC: -0.0088
Win rate: 0.250 over 12 paired runs

## plausible_typology_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0062
Median delta AUPRC: -0.0070
Win rate: 0.417 over 12 paired runs

## plausible_typology_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0085
Median delta AUPRC: -0.0118
Win rate: 0.250 over 12 paired runs

## hard_projected_v2 vs none

Mean delta AUPRC: -0.0468
Median delta AUPRC: -0.0065
Win rate: 0.317 over 189 paired runs

## hard_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0394
Median delta AUPRC: -0.0066
Win rate: 0.346 over 162 paired runs

## hard_projected_v2 vs smote_v2

Mean delta AUPRC: -0.0098
Median delta AUPRC: -0.0107
Win rate: 0.250 over 12 paired runs

## hard_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0078
Median delta AUPRC: -0.0058
Win rate: 0.250 over 12 paired runs

## hard_projected_v2 vs feature_noise_v2

Mean delta AUPRC: -0.0100
Median delta AUPRC: -0.0123
Win rate: 0.250 over 12 paired runs

## hard_projected_v2 vs adv_no_projection_v2

Mean delta AUPRC: -0.0086
Median delta AUPRC: -0.0001
Win rate: 0.495 over 111 paired runs

## Validity

| augmentation                    |   ledger_violation_rate |   mean_flow_residual |   detector_hardness |   acceptance_rate |   profile_drift |   categorical_fractionality_rate |   negative_feature_rate |
|:--------------------------------|------------------------:|---------------------:|--------------------:|------------------:|----------------:|---------------------------------:|------------------------:|
| adv_no_projection_v2            |             0.971431    |           0.475069   |           3.28387   |          0.028569 |        0.733564 |                      nan         |              nan        |
| boundary_projected_v2           |             0           |           0          |           8.70273   |          0.944398 |        0.674329 |                      nan         |              nan        |
| curriculum_projected_v2         |             0           |           0          |           4.00908   |          0.939643 |        0.828253 |                        0         |                0        |
| edge_rewire_v2                  |             0           |           0          |           0.178286  |          0.949612 |        1.30039  |                        0         |                0        |
| feature_noise_v2                |             0.582297    |           0.347162   |           2.43057   |          0.39137  |        2.08256  |                        0.49861   |                0.351548 |
| hard_projected_v2               |             0           |           0          |           8.06153   |          0.941805 |        0.730404 |                        0         |                0        |
| mixup_v2                        |             0.000225225 |           0.00023189 |           1.28777   |          0.949387 |        1.0822   |                        0.0614203 |                0        |
| none                            |           nan           |         nan          |         nan         |        nan        |      nan        |                      nan         |              nan        |
| plausible_hard_projected_v2     |             0           |           0          |           5.75256   |          0.939643 |        0.544745 |                        0         |                0        |
| plausible_typology_projected_v2 |             0           |           0          |           6.18864   |          0.939643 |        0.536059 |                        0         |                0        |
| random_feasible_v2              |             0           |           0          |           0.0653504 |          0.9411   |        1.41214  |                        0         |                0        |
| smote_v2                        |             0           |           0          |           0.277121  |          0.949612 |        1.46006  |                        0.0543776 |                0        |
| typology_projected_v2           |             0           |           0          |           7.52175   |          0.939643 |        0.766421 |                        0         |                0        |

## Reviewer-Risk Notes

- CIKM-ready only if projected hard counterfactuals beat both no augmentation and random feasible projection on the main graph/table detectors.
- Validity alone supports a method paper only if predictive gains are strongest under drift, held-out typology, or label scarcity.
- If no-ledger variants dominate AUPRC, frame projection as preserving deployable validity under small performance tradeoff, or improve selection.