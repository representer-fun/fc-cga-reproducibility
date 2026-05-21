# Final Paper Package

This folder is the curated source for writing the CIKM paper. It contains the
tables, figures, result summaries, and narrative notes that matter most.

Use this folder instead of browsing every raw run directory.

## Start Here

1. [PAPER_STORY.md](PAPER_STORY.md): recommended paper narrative.
2. [PAPER_OUTLINE.md](PAPER_OUTLINE.md): section-by-section CIKM outline.
3. [CLAIMS_TO_EVIDENCE.md](CLAIMS_TO_EVIDENCE.md): which table supports which
   claim.
4. [RESULTS_AT_A_GLANCE.md](RESULTS_AT_A_GLANCE.md): compact headline numbers
   and safe claim wording.
5. [EXPERIMENTS_AND_RESULTS.md](EXPERIMENTS_AND_RESULTS.md): detailed
   experiment and result explanation.
6. [TABLE_CAPTIONS.md](TABLE_CAPTIONS.md): draft captions for paper tables and
   figures.
7. [LIMITATIONS_AND_REVIEWER_RISKS.md](LIMITATIONS_AND_REVIEWER_RISKS.md):
   risks, negative results, and how to frame them.

## Included Assets

- `tables/`: curated Markdown tables for the main paper and appendix.
- `tables/csv/`: matching CSVs.
- `figures/`: selected PNG figures for the paper.
- `results/`: final text summaries and claim audits copied from `results/`.
- `notes/`: writing support docs.

## Recommended Main-Paper Tables

- `tables/table_01_validity_audit.md`
- `tables/table_12_repaired_standard_baselines.md`
- `tables/table_16_alert_budget_layering.md`
- `tables/table_17_layering_bootstrap_significance.md`
- `tables/table_18_repaired_baselines_on_layering.md`
- `tables/table_19_fewshot_layering_adaptation.md`
- `tables/table_20_temporal_bucket_layering.md`
- `tables/table_21_coldstart_counterparty_shift.md`

## Recommended Main-Paper Figures

- `figures/fig_01_validity_artifact_bars.png`
- `figures/fig_07_layering_10seed_delta_ci.png`
- `figures/fig_08_repaired_standard_validity.png`
- `figures/fig_13_alert_budget_layering.png`
- `figures/fig_14_fewshot_layering.png`
- `figures/fig_15_temporal_bucket_layering.png`
- `figures/fig_16_coldstart_counterparty_shift.png`

## One-Line Paper Positioning

This is a validity-aware augmentation paper for AML transaction graphs, with
the strongest predictive evidence on held-out layering transfer and practical
low-FPR alert-budget metrics.
