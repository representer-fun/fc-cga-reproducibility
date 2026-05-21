# Claims To Evidence

## Claim 1: Standard augmentation can be invalid for financial transactions.

Use:

- `tables/table_01_validity_audit.md`
- `tables/table_12_repaired_standard_baselines.md`
- `figures/fig_01_validity_artifact_bars.png`

Key sentence:

Feature noise produces large ledger, categorical, and negative-feature artifact
rates, showing that predictive gains from unconstrained augmentation can be
financially invalid.

## Claim 2: Post-hoc repair is useful but not sufficient.

Use:

- `tables/table_12_repaired_standard_baselines.md`
- `tables/table_18_repaired_baselines_on_layering.md`

Key sentence:

Repair removes audited artifacts, but repaired SMOTE/mixup remain below
typology-aware projected counterfactuals on the main held-out layering task.

## Claim 3: Projected counterfactuals improve held-out layering transfer.

Use:

- `tables/table_18_repaired_baselines_on_layering.md`
- `tables/table_17_layering_bootstrap_significance.md`
- `figures/fig_07_layering_10seed_delta_ci.png`

Key sentence:

On held-out layering, projected variants improve AUPRC by about `+0.014` to
`+0.018` over no augmentation across LightGBM/XGBoost and win across all 10
seeds in the main comparisons.

## Claim 4: Gains matter at realistic alert budgets.

Use:

- `tables/table_16_alert_budget_layering.md`
- `figures/fig_13_alert_budget_layering.png`

Key sentence:

The method improves low-FPR recall and top-alert precision, which are more
deployment-relevant than AUPRC alone.

## Claim 5: Benefits persist in emerging-typology few-shot settings.

Use:

- `tables/table_19_fewshot_layering_adaptation.md`
- `figures/fig_14_fewshot_layering.png`

Key sentence:

Projected variants continue to outperform no augmentation when 1, 5, or 10
held-out layering positives are allowed into the training split.

## Claim 6: Benefits are visible under temporal and counterparty shift.

Use:

- `tables/table_20_temporal_bucket_layering.md`
- `tables/table_21_coldstart_counterparty_shift.md`
- `figures/fig_15_temporal_bucket_layering.png`
- `figures/fig_16_coldstart_counterparty_shift.png`

Key sentence:

Projected variants improve the hard early/mid temporal buckets and future
new-pair detection.

## Claim 7: The method is not universally beneficial.

Use:

- `tables/table_22_graph_model_layering_confirmation.md`
- `tables/table_23_failure_modes_structuring_integration.md`

Key sentence:

Graph neural detectors and non-layering typologies expose limitations,
supporting a nuanced claim: validity-aware augmentation is strongest when the
generated support matches the target typology geometry.
