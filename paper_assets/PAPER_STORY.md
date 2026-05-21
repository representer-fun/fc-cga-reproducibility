# Recommended Paper Story

## Core Thesis

Fraud and AML augmentation should not be evaluated only as feature-space
perturbation. In transaction graphs, generated examples must remain financially
valid. Ledger-conserving counterfactual augmentation offers a way to generate
hard examples without violating basic transaction constraints.

The paper should argue:

1. Standard augmentation can produce invalid or representationally broken
   transaction examples.
2. Post-hoc repair can remove surface artifacts, but it does not fully solve
   typology-transfer.
3. Hard/typology-aware ledger-conserving counterfactuals improve held-out
   layering detection.
4. The improvement appears in AUPRC, low-FPR recall, top-alert precision,
   paired bootstrap tests, few-shot adaptation, temporal buckets, and new-pair
   shift.
5. The method has limits: graph models do not improve in the final check, and
   structuring/integration are failure modes.

## What To Emphasize

Emphasize held-out layering as the central predictive result:

- LightGBM: `0.932` no augmentation to `0.947` typology projected.
- XGBoost: `0.927` no augmentation to `0.946` curriculum projected.
- Projected methods beat no augmentation and `SMOTE + repair` with positive
  bootstrap intervals and 10/10 seed win rates on the main comparisons.

Emphasize alert-budget metrics:

- Recall@0.1% FPR improves for both LightGBM and XGBoost.
- Precision@500/1000 improves modestly but consistently.
- This is more AML-relevant than AUPRC alone.

Emphasize validity:

- Feature noise creates ledger/categorical/negative artifacts.
- Repaired baselines and projected methods have zero audited surface artifacts.
- The contribution is not only performance; it is deployable validity.

## What Not To Claim

Do not claim:

- Universal improvement across all typologies.
- Superiority for graph neural models.
- Broad label-scarcity dominance.
- SOTA across all financial graph benchmarks.

Instead claim:

- Targeted robustness for held-out layering.
- Validity-aware augmentation is necessary for financial graphs.
- The proposed method improves a realistic AML transfer setting where standard
  repaired baselines are insufficient.

## Suggested Abstract Arc

1. AML detectors face emerging typologies and scarce positive labels.
2. Standard augmentation is attractive but can produce invalid financial
   transactions.
3. We propose ledger-conserving counterfactual augmentation with
   hardness/plausibility/typology-aware selection.
4. Across TransXion, AMLNet, and Elliptic++ experiments, validity audits show
   standard/noisy augmentations can violate ledger and representation
   constraints.
5. On held-out AMLNet layering, projected counterfactuals improve AUPRC,
   low-FPR recall, top-alert precision, and new-pair transfer over no
   augmentation and repaired baselines.
6. We also report failures on structuring/integration and graph models, showing
   that validity is necessary but not sufficient for every typology.
