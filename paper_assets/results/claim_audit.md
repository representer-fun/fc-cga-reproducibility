# CIKM Claim Audit

## plausible_hard_projected_v2 vs none

Mean delta AUPRC: -0.0217
Median delta AUPRC: 0.0072
Win rate: 0.600 over 280 paired runs

## plausible_hard_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0192
Median delta AUPRC: 0.0024
Win rate: 0.589 over 304 paired runs

## plausible_hard_projected_v2 vs smote_v2

Mean delta AUPRC: 0.0017
Median delta AUPRC: 0.0070
Win rate: 0.591 over 44 paired runs

## plausible_hard_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0029
Median delta AUPRC: 0.0018
Win rate: 0.545 over 44 paired runs

## plausible_hard_projected_v2 vs feature_noise_v2

Mean delta AUPRC: 0.0010
Median delta AUPRC: 0.0092
Win rate: 0.591 over 44 paired runs

## curriculum_projected_v2 vs none

Mean delta AUPRC: -0.0212
Median delta AUPRC: 0.0035
Win rate: 0.598 over 286 paired runs

## curriculum_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0185
Median delta AUPRC: 0.0026
Win rate: 0.584 over 310 paired runs

## curriculum_projected_v2 vs smote_v2

Mean delta AUPRC: 0.0018
Median delta AUPRC: 0.0017
Win rate: 0.591 over 44 paired runs

## curriculum_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0028
Median delta AUPRC: -0.0002
Win rate: 0.455 over 44 paired runs

## curriculum_projected_v2 vs feature_noise_v2

Mean delta AUPRC: 0.0012
Median delta AUPRC: 0.0043
Win rate: 0.591 over 44 paired runs

## typology_projected_v2 vs none

Mean delta AUPRC: -0.0255
Median delta AUPRC: 0.0057
Win rate: 0.573 over 286 paired runs

## typology_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0227
Median delta AUPRC: 0.0025
Win rate: 0.584 over 310 paired runs

## typology_projected_v2 vs smote_v2

Mean delta AUPRC: 0.0012
Median delta AUPRC: 0.0037
Win rate: 0.591 over 44 paired runs

## typology_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0034
Median delta AUPRC: -0.0003
Win rate: 0.477 over 44 paired runs

## typology_projected_v2 vs feature_noise_v2

Mean delta AUPRC: 0.0006
Median delta AUPRC: 0.0064
Win rate: 0.591 over 44 paired runs

## plausible_typology_projected_v2 vs none

Mean delta AUPRC: -0.0235
Median delta AUPRC: 0.0036
Win rate: 0.577 over 286 paired runs

## plausible_typology_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0206
Median delta AUPRC: 0.0037
Win rate: 0.590 over 310 paired runs

## plausible_typology_projected_v2 vs smote_v2

Mean delta AUPRC: 0.0018
Median delta AUPRC: 0.0053
Win rate: 0.591 over 44 paired runs

## plausible_typology_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0028
Median delta AUPRC: 0.0003
Win rate: 0.523 over 44 paired runs

## plausible_typology_projected_v2 vs feature_noise_v2

Mean delta AUPRC: 0.0011
Median delta AUPRC: 0.0069
Win rate: 0.591 over 44 paired runs

## hard_projected_v2 vs none

Mean delta AUPRC: -0.0292
Median delta AUPRC: 0.0002
Win rate: 0.530 over 336 paired runs

## hard_projected_v2 vs random_feasible_v2

Mean delta AUPRC: -0.0244
Median delta AUPRC: 0.0019
Win rate: 0.564 over 321 paired runs

## hard_projected_v2 vs smote_v2

Mean delta AUPRC: 0.0018
Median delta AUPRC: 0.0058
Win rate: 0.591 over 44 paired runs

## hard_projected_v2 vs mixup_v2

Mean delta AUPRC: -0.0028
Median delta AUPRC: 0.0011
Win rate: 0.545 over 44 paired runs

## hard_projected_v2 vs feature_noise_v2

Mean delta AUPRC: 0.0012
Median delta AUPRC: 0.0083
Win rate: 0.591 over 44 paired runs

## hard_projected_v2 vs adv_no_projection_v2

Mean delta AUPRC: -0.0083
Median delta AUPRC: -0.0001
Win rate: 0.479 over 117 paired runs

## Validity

| augmentation                    |   ledger_violation_rate |   mean_flow_residual |   detector_hardness |   acceptance_rate |   profile_drift |   categorical_fractionality_rate |   negative_feature_rate |
|:--------------------------------|------------------------:|---------------------:|--------------------:|------------------:|----------------:|---------------------------------:|------------------------:|
| adv_no_projection_v2            |              0.971473   |          0.474206    |           3.20608   |         0.0285274 |        0.732337 |                      nan         |              nan        |
| boundary_projected_v2           |              0          |          0           |           8.51511   |         0.945044  |      391.319    |                      nan         |              nan        |
| curriculum_projected_v2         |              0          |          0           |           3.91683   |         0.94073   |        1.24411  |                        0         |                0        |
| edge_rewire_v2                  |              0          |          0           |           0.178286  |         0.949612  |        1.30039  |                        0         |                0        |
| feature_noise_repaired_v2       |              0          |          0           |           1.00704   |         0.947211  |        2.4344   |                        0         |                0        |
| feature_noise_v2                |              0.404965   |          0.199428    |           2.48405   |         0.555878  |        2.37627  |                        0.498471  |                0.318521 |
| hard_projected_v2               |              0          |          0           |           7.67821   |         0.944367  |      177.74     |                        0         |                0        |
| mixup_repaired_v2               |              0          |          0           |           2.94016   |         0.947014  |        1.87395  |                        0         |                0        |
| mixup_v2                        |              0.00012285 |          0.000126485 |           1.84198   |         0.947599  |        1.65802  |                        0.114884  |                0        |
| none                            |            nan          |        nan           |         nan         |       nan         |      nan        |                      nan         |              nan        |
| plausible_hard_projected_v2     |              0          |          0           |           5.66648   |         0.940636  |        0.883791 |                        0         |                0        |
| plausible_typology_projected_v2 |              0          |          0           |           6.26997   |         0.94073   |        0.89116  |                        0         |                0        |
| random_feasible_v2              |              0          |          0           |           0.0534505 |         0.941692  |     1695.59     |                        0         |                0        |
| smote_repaired_v2               |              0          |          0           |           0.173327  |         0.946628  |        2.71492  |                        0         |                0        |
| smote_v2                        |              0          |          0           |           0.206282  |         0.947722  |        2.09796  |                        0.0741509 |                0        |
| typology_projected_v2           |              0          |          0           |           7.74131   |         0.94073   |        1.05743  |                        0         |                0        |
| v2_amount_only                  |              0          |          0           |           0.641229  |         0.949603  |        0.386806 |                      nan         |              nan        |
| v2_no_hard                      |              0          |          0           |           0.0434035 |         0.949603  |        1.32503  |                      nan         |              nan        |
| v2_no_ledger                    |              0.968743   |          0.458543    |           2.46542   |         0.0312574 |        0.673569 |                      nan         |              nan        |
| v2_no_profile                   |              0          |          0           |           2.92748   |         1         |        0.657251 |                      nan         |              nan        |
| v2_no_temporal                  |              0          |          0           |           2.01581   |         0.949603  |        0.464932 |                      nan         |              nan        |
| v2_topology_only                |              0          |          0           |           1.27169   |         0.953302  |        0.447996 |                      nan         |              nan        |

## Reviewer-Risk Notes

- CIKM-ready only if projected hard counterfactuals beat both no augmentation and random feasible projection on the main graph/table detectors.
- Validity alone supports a method paper only if predictive gains are strongest under drift, held-out typology, or label scarcity.
- If no-ledger variants dominate AUPRC, frame projection as preserving deployable validity under small performance tradeoff, or improve selection.