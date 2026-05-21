# CIKM V4 Strengthening Summary

## Held-Out Typology
- integration/lightgbm: best=No aug. AUPRC=0.000, delta vs no aug.=+0.000.
- integration/xgboost: best=Plausible hard AUPRC=0.001, delta vs no aug.=+0.000.
- layering/lightgbm: best=Typology projected AUPRC=0.947, delta vs no aug.=+0.016.
- layering/xgboost: best=Curriculum projected AUPRC=0.946, delta vs no aug.=+0.018.
- structuring/lightgbm: best=No aug. AUPRC=0.618, delta vs no aug.=+0.000.
- structuring/xgboost: best=Random feasible AUPRC=0.709, delta vs no aug.=+0.084.

## Repaired Standard Baselines
- Feature noise + repair: ledger=0.0%, categorical=0.0%, negative=0.0%.
- SMOTE + repair: ledger=0.0%, categorical=0.0%, negative=0.0%.
- Mixup + repair: ledger=0.0%, categorical=0.0%, negative=0.0%.

## Label Scarcity
- 0.01 labels: best=Random feasible delta vs no aug.=+0.008.
- 0.05 labels: best=No aug. delta vs no aug.=+0.000.
- 0.25 labels: best=No aug. delta vs no aug.=+0.000.

## Rho Sensitivity
- rho=0.25: best=Plausible typology AUPRC=0.615.
- rho=0.5: best=Curriculum projected AUPRC=0.622.
- rho=0.75: best=Plausible typology AUPRC=0.612.
- rho=1.25: best=Random feasible AUPRC=0.621.
