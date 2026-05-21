# Experiments And Results

## Experiment 1: Validity Audit

Question:

> Do common augmentations create invalid financial examples?

Evidence:

- `tables/table_01_validity_audit.md`
- `tables/table_12_repaired_standard_baselines.md`
- `figures/fig_01_validity_artifact_bars.png`
- `figures/fig_08_repaired_standard_validity.png`

Finding:

Feature noise creates severe artifacts: about `58.2%` ledger violations,
`49.9%` categorical artifacts, and `35.2%` negative-feature artifacts. Repaired
baselines and projected methods remove these audited artifacts.

Paper use:

This motivates why financial augmentation needs a validity audit, not just
predictive metrics.

## Experiment 2: Repaired Baselines On Held-Out Layering

Question:

> If a simple repair step fixes validity, do we still need the proposed method?

Evidence:

- `tables/table_18_repaired_baselines_on_layering.md`

Finding:

Post-hoc repair is not enough on held-out layering.

- LightGBM `SMOTE + repair`: `0.932`.
- LightGBM typology projected: `0.947`.
- XGBoost `SMOTE + repair`: `0.930`.
- XGBoost curriculum projected: `0.946`.

Paper use:

This is one of the strongest tables. It directly addresses a likely reviewer
objection.

## Experiment 3: Alert-Budget Evaluation

Question:

> Do gains appear under realistic AML alert budgets?

Evidence:

- `tables/table_16_alert_budget_layering.md`
- `figures/fig_13_alert_budget_layering.png`

Finding:

Projected methods improve Recall@0.1% FPR and Precision@500/1000 on held-out
layering. This strengthens the practical AML story because analysts operate
under tight alert budgets.

Paper use:

This should be a main result table or figure.

## Experiment 4: Bootstrap Significance

Question:

> Are held-out layering gains robust across seeds and prediction-level
> resampling?

Evidence:

- `tables/table_17_layering_bootstrap_significance.md`

Finding:

Projected methods beat no augmentation and `SMOTE + repair` with positive
bootstrap intervals and 10/10 seed win rates in the main comparisons.

Paper use:

This supports statistical confidence without overclaiming universal performance.

## Experiment 5: Few-Shot Held-Out Typology Adaptation

Question:

> Does augmentation help when only a few examples of an emerging typology are
> observed?

Evidence:

- `tables/table_19_fewshot_layering_adaptation.md`
- `figures/fig_14_fewshot_layering.png`

Finding:

Projected methods continue to help at 1, 5, and 10 held-out layering positives.
With 10 positives, LightGBM projected variants reach about `0.951` AUPRC and
XGBoost projected variants reach about `0.948`.

Paper use:

This gives the paper a strong emerging-typology adaptation angle.

## Experiment 6: Temporal Buckets

Question:

> Do gains persist across future deployment time?

Evidence:

- `tables/table_20_temporal_bucket_layering.md`
- `figures/fig_15_temporal_bucket_layering.png`

Finding:

The strongest gains appear in harder early/mid temporal buckets:

- LightGBM Q1: no augmentation `0.655`, typology projected `0.738`.
- XGBoost Q1: no augmentation `0.651`, curriculum projected `0.731`.
- XGBoost Q3: no augmentation `0.810`, curriculum/typology projected `0.850`.

Paper use:

This supports temporal robustness for the main typology-transfer claim.

## Experiment 7: Counterparty Shift

Question:

> Does augmentation help on new sender-receiver pairs or sparse-history
> counterparties?

Evidence:

- `tables/table_21_coldstart_counterparty_shift.md`
- `figures/fig_16_coldstart_counterparty_shift.png`

Finding:

New-pair shift is strong:

- LightGBM no augmentation `0.928`, plausible hard `0.951`.
- XGBoost no augmentation `0.923`, plausible hard `0.943`.

Sparse-history entity results have only 11 positives, so they should be
appendix evidence.

Paper use:

Use new-pair results in the main story. Keep sparse-history as secondary.

## Experiment 8: Graph-Model Confirmation

Question:

> Do gains transfer to PyG graph neural detectors?

Evidence:

- `tables/table_22_graph_model_layering_confirmation.md`
- `figures/fig_17_graph_model_layering.png`

Finding:

No. PyG GAT no augmentation is best around `0.705`; PyG SAGE is noisy and weak.
Projected methods do not improve graph neural models in this final CPU check.

Paper use:

Use as limitation or appendix. Do not sell this as graph-model generality.

## Experiment 9: Failure Modes

Question:

> Where does the method fail?

Evidence:

- `tables/table_23_failure_modes_structuring_integration.md`

Finding:

Structuring and integration do not support a broad win claim. Hard projected
variants hurt structuring substantially, and integration has tiny absolute
AUPRC values.

Paper use:

Use this as an honest boundary condition: validity is necessary but not
sufficient; augmentation must match typology geometry.
