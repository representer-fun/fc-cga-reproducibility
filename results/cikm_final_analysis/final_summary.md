# Final CIKM Experiment Summary

- Held-out layering/lightgbm: best=Typology projected AUPRC=0.947.
- Held-out layering/xgboost: best=Curriculum projected AUPRC=0.946.
- Alert budget/lightgbm: best Recall@1% FPR=Mixup (0.962).
- Alert budget/xgboost: best Recall@1% FPR=Plausible typology (0.956).
- Few-shot 0: best=Plausible hard AUPRC=0.946.
- Few-shot 1: best=Hard projected AUPRC=0.946.
- Few-shot 5: best=Hard projected AUPRC=0.947.
- Few-shot 10: best=Hard projected AUPRC=0.949.
- Cold-start low_history_entity: best=Curriculum projected AUPRC=0.934.
- Cold-start new_pair: best=Plausible hard AUPRC=0.947.
- Graph pyg_gat: best=No aug. AUPRC=0.705.
- Graph pyg_sage: best=SMOTE + repair AUPRC=0.355.
- Bootstrap checks with nonzero-sign intervals: 21/26 comparisons.
