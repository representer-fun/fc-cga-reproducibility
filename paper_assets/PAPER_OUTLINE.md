# CIKM Paper Outline

## 1. Introduction

Motivate AML detection under emerging typologies, temporal drift, and alert
budget constraints. Explain why naive feature-space augmentation is risky in
financial transaction graphs: generated examples can violate ledger/flow
constraints or categorical representation.

End with contributions:

1. A ledger-conserving counterfactual augmentation framework.
2. A validity audit for transaction-graph augmentation.
3. A repaired-baseline study showing post-hoc repair is not enough for
   typology transfer.
4. Strong held-out layering results under AUPRC, low-FPR recall, top-alert
   precision, few-shot adaptation, temporal buckets, and new-pair shift.
5. Honest limitations on graph models and non-layering typologies.

## 2. Related Work

Cover:

- Fraud and AML transaction graph learning.
- Counterfactual augmentation and adversarial training.
- Graph data augmentation.
- Financial validity, constraints, and simulation.
- Alert-budget evaluation in fraud/AML.

## 3. Problem Setup

Define:

- Temporal directed transaction graph.
- Edge-level suspicious transaction detection.
- Temporal train/validation/test split.
- Held-out typology transfer.
- Financial validity constraints.

Evaluation metrics:

- AUPRC and AUROC.
- Recall@0.1%, 0.5%, and 1% FPR.
- Precision@K / top-alert precision.
- Validity metrics: ledger violation, flow residual, categorical artifacts,
  negative-feature artifacts, profile drift, detector hardness.

## 4. Method

Describe:

- Candidate generation.
- Ledger projection.
- Categorical repair/one-hot consistency.
- Hardness-aware selection.
- Plausibility/profile-drift control.
- Typology-aware policies.
- Repaired standard baselines as a control.

Avoid overselling exact graph edits if the implemented method is primarily
feature/history counterfactual generation over transaction edges.

## 5. Experimental Setup

Datasets:

- TransXion.
- AMLNet.
- Elliptic++ external robustness.

Detectors:

- LightGBM.
- XGBoost.
- PyG SAGE/GAT as a smaller confirmation/limitation.

Splits:

- Temporal splits.
- Held-out layering/structuring/integration.
- Few-shot held-out positives.
- New-pair and sparse-history subset analysis.

Baselines:

- No augmentation.
- Feature noise, SMOTE, mixup.
- Repaired feature noise/SMOTE/mixup.
- Random feasible.
- Hard projected.
- Plausible hard.
- Curriculum projected.
- Typology projected.
- Plausible typology.

## 6. Results

Suggested order:

1. Validity audit.
2. Main held-out layering transfer.
3. Repaired baselines on layering.
4. Alert-budget metrics.
5. Bootstrap significance.
6. Few-shot adaptation.
7. Temporal buckets.
8. New-pair counterparty shift.
9. Mechanism analysis.
10. Failure modes and graph limitations.

## 7. Discussion

Main discussion points:

- Validity is necessary for financial augmentation.
- Repair solves surface validity, not typology-transfer support.
- Hardness helps only when the generated examples align with the target
  typology.
- Structuring/integration show that valid hard examples can be harmful.
- Graph neural detectors need better integration; current CPU PyG check is not
  supportive.

## 8. Conclusion

Conclude with a focused claim:

Ledger-conserving counterfactual augmentation is a useful and valid tool for
emerging AML typology transfer, especially layering, but it should be deployed
with typology-aware diagnostics and validity audits rather than assumed to help
universally.
