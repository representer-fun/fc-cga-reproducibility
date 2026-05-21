# Limitations And Reviewer Risks

## Risk 1: The method does not win everywhere.

Answer:

Do not claim universal wins. Frame the contribution around valid augmentation
and targeted held-out layering transfer.

## Risk 2: Repaired standard baselines are competitive.

Answer:

This is why `table_18_repaired_baselines_on_layering.md` matters. Repaired
SMOTE and mixup are useful controls, but projected methods still outperform them
on held-out layering and under bootstrap tests.

## Risk 3: Graph neural model confirmation is weak.

Answer:

Put graph results in limitations or appendix. The main result is robust across
LightGBM and XGBoost, not across graph neural models.

## Risk 4: Structuring and integration are negative.

Answer:

Use this as an honest scientific point: validity is necessary but not
sufficient. Hard counterfactuals help when typology geometry is compatible.

## Risk 5: AMLNet is synthetic.

Answer:

Use TransXion and Elliptic++ as supporting datasets, but keep the strongest
typology-transfer results on AMLNet because it has usable laundering phase
labels. Be explicit about dataset roles.

## Risk 6: Mechanism may look feature-based rather than graph-native.

Answer:

Describe the method as transaction-edge counterfactual augmentation with graph
history and profile features. Do not overclaim subgraph generation if the
implementation is feature/history level.

## Risk 7: Low-history subset has few positives.

Answer:

Use new-pair shift in the main paper. Keep sparse-history entity analysis in
appendix.

## Risk 8: Very high baseline performance in some buckets.

Answer:

Focus on hard buckets, low-FPR metrics, and emerging typology conditions, not
only aggregate full-data AUPRC.
