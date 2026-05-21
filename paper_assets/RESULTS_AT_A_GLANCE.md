# Results At A Glance

This is the quick numerical spine for the CIKM paper. Use it when writing the
abstract, introduction, result overview, and conclusion.

## Main Supported Claim

Ledger-conserving, typology-aware counterfactual augmentation improves held-out
layering detection under realistic AML alert budgets, while preserving audited
financial validity. The claim is intentionally targeted: the method is strongest
for compatible unseen typology shifts, not for every AML typology or every model
family.

## Headline Held-Out Layering Results

| Model | Baseline | Best projected variant | AUPRC gain |
|---|---:|---:|---:|
| LightGBM | `0.932` | `0.947` typology projected | `+0.016` |
| XGBoost | `0.927` | `0.946` curriculum projected | `+0.018` |

Interpretation:

The primary predictive win is held-out layering transfer. This is the result to
anchor the paper around, because it is consistent with the method's design:
valid counterfactuals help when they create hard support near a compatible
future typology.

## Repaired Baselines Are Not Enough

| Model | SMOTE + repair | Mixup + repair | Best projected variant |
|---|---:|---:|---:|
| LightGBM | `0.932` | `0.934` | `0.947` |
| XGBoost | `0.930` | `0.933` | `0.946` |

Interpretation:

Simple repair is important as a control because it removes obvious invalid
artifacts. The key result is that repair alone does not close the held-out
layering gap. Selection and projection strategy still matter.

## Alert-Budget Evidence

Use `tables/table_16_alert_budget_layering.md` and
`figures/fig_13_alert_budget_layering.png`.

Main message:

- Recall@0.1% FPR improves for both LightGBM and XGBoost.
- Precision@500 and Precision@1000 improve modestly but consistently.
- This converts the AUPRC result into a deployment-facing AML result.

## Robustness Evidence

Use `tables/table_17_layering_bootstrap_significance.md`.

Main message:

Projected methods beat no augmentation and `SMOTE + repair` with positive
bootstrap intervals and 10/10 seed win rates on the main held-out layering
comparisons.

## Emerging-Typology Adaptation

Use `tables/table_19_fewshot_layering_adaptation.md` and
`figures/fig_14_fewshot_layering.png`.

Main message:

Projected methods continue to help with 1, 5, and 10 held-out positives. With
10 positives, LightGBM projected variants reach about `0.951` AUPRC and XGBoost
projected variants reach about `0.948`.

## Shift Evidence

Use:

- `tables/table_20_temporal_bucket_layering.md`
- `tables/table_21_coldstart_counterparty_shift.md`
- `figures/fig_15_temporal_bucket_layering.png`
- `figures/fig_16_coldstart_counterparty_shift.png`

Main message:

The gains are strongest in harder early/mid temporal buckets and on new
sender-receiver pairs. This supports the paper's claim that the method helps
future typology transfer, not just random held-out examples.

## Boundary Conditions

Use:

- `tables/table_22_graph_model_layering_confirmation.md`
- `tables/table_23_failure_modes_structuring_integration.md`

Main message:

Graph neural detectors did not improve in the final CPU PyG confirmation, and
structuring/integration are not broad wins. The paper should use this honestly:
validity is necessary, but validity alone is not sufficient when generated
support does not match target typology geometry.
