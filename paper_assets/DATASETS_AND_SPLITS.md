# Datasets And Splits

## TransXion

Role:

- Large AML benchmark.
- Full-data detection.
- Validity/repaired-baseline audits.

Use in paper:

- Supporting dataset.
- Do not make it the central held-out typology evidence unless typology labels
  are sufficiently reliable.

## AMLNet

Role:

- Controlled AML dataset with laundering phase/typology labels.
- Main held-out typology transfer benchmark.

Main split:

- Temporal train/validation/test.
- For held-out typology experiments, positives from the target typology are
  removed from training and retained for validation/test evaluation.

Main target typology:

- Layering.

Why layering is central:

- It is the strongest and most stable positive result.
- It supports AUPRC, low-FPR, bootstrap, few-shot, temporal, and new-pair
  claims.

Other typologies:

- Structuring and integration are failure/boundary analyses.

## Elliptic++

Role:

- External robustness dataset.
- Useful for appendix/background, not central to the final paper story.

## Few-Shot Held-Out Typology

Few-shot settings retain:

- 0 held-out positives.
- 1 held-out positive.
- 5 held-out positives.
- 10 held-out positives.

Use:

- Emerging typology adaptation.

## Counterparty Shift

Subsets:

- `new_pair`: future sender-receiver pairs not observed in training.
- `low_history_entity`: rows where either endpoint has low training history.

Use:

- Main: `new_pair`.
- Appendix: `low_history_entity`, because it has few positives.
