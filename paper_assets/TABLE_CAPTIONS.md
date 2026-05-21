# Draft Table And Figure Captions

These captions are intentionally paper-ready but should be tightened once the
LaTeX tables are placed.

## Main Table Candidates

### Validity Audit

Suggested caption:

Validity audit for standard and ledger-conserving augmentations. Unconstrained
feature-space perturbation creates ledger, categorical, and negative-feature
artifacts, while repaired and projected variants remove the audited surface
violations.

Use:

- `tables/table_01_validity_audit.md`
- `tables/table_12_repaired_standard_baselines.md`

### Held-Out Layering Versus Repaired Baselines

Suggested caption:

Held-out layering AUPRC after removing layering positives from training.
Post-hoc repair fixes obvious validity artifacts but remains below hard and
typology-aware projected counterfactual augmentation.

Use:

- `tables/table_18_repaired_baselines_on_layering.md`

### Alert-Budget Results

Suggested caption:

Deployment-facing held-out layering metrics under strict alert budgets.
Projected counterfactuals improve low-FPR recall and top-alert precision over
no augmentation and repaired standard baselines.

Use:

- `tables/table_16_alert_budget_layering.md`

### Bootstrap And Seed Robustness

Suggested caption:

Paired bootstrap and seed-win analysis for held-out layering. Projected
counterfactual methods show positive prediction-level intervals and consistent
seed wins over the strongest baseline controls.

Use:

- `tables/table_17_layering_bootstrap_significance.md`

### Few-Shot Emerging Typology

Suggested caption:

Few-shot adaptation to an emerging held-out layering typology. Projected
counterfactual augmentation remains beneficial when 1, 5, or 10 held-out
positives are added to the training split.

Use:

- `tables/table_19_fewshot_layering_adaptation.md`

### Temporal And Counterparty Shift

Suggested caption:

Future temporal and counterparty-shift evaluation for held-out layering.
Projected methods are strongest in harder early/mid temporal buckets and on new
sender-receiver pairs.

Use:

- `tables/table_20_temporal_bucket_layering.md`
- `tables/table_21_coldstart_counterparty_shift.md`

### Boundary Conditions

Suggested caption:

Boundary conditions for validity-aware augmentation. The final graph neural
confirmation and non-layering typology experiments show that valid
counterfactuals help only when generated support is aligned with the target
typology.

Use:

- `tables/table_22_graph_model_layering_confirmation.md`
- `tables/table_23_failure_modes_structuring_integration.md`

## Main Figure Candidates

### Validity Artifacts

Suggested caption:

Artifact rates for standard augmentation. Feature-space perturbation frequently
violates basic transaction validity, motivating ledger-conserving augmentation.

Use:

- `figures/fig_01_validity_artifact_bars.png`
- `figures/fig_08_repaired_standard_validity.png`

### Held-Out Layering Seed Deltas

Suggested caption:

Seed-level held-out layering improvements over no augmentation. Projected
variants produce consistent positive deltas for the main LightGBM and XGBoost
comparisons.

Use:

- `figures/fig_07_layering_10seed_delta_ci.png`

### Alert-Budget Bar Chart

Suggested caption:

Low-FPR recall and top-alert precision for held-out layering. The plot shows
that the main AUPRC improvements translate into practical alert-budget gains.

Use:

- `figures/fig_13_alert_budget_layering.png`

### Few-Shot, Temporal, And Counterparty Curves

Suggested caption:

Projected counterfactual augmentation across emerging-typology adaptation,
future temporal buckets, and counterparty shift. Gains are strongest in settings
closest to plausible future layering drift.

Use:

- `figures/fig_14_fewshot_layering.png`
- `figures/fig_15_temporal_bucket_layering.png`
- `figures/fig_16_coldstart_counterparty_shift.png`
