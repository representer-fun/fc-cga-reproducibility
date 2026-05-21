# Graph-Model Confirmation On Held-Out Layering

Small CPU PyG confirmation for the main positive typology-shift setting.

| Graph detector   | Method               | AUPRC         | Recall@1% FPR   | Precision@K   |   Seeds |
|:-----------------|:---------------------|:--------------|:----------------|:--------------|--------:|
| pyg_gat          | Curriculum projected | 0.666 ± 0.096 | 0.894 ± 0.037   | 0.587 ± 0.097 |       3 |
| pyg_gat          | No aug.              | 0.705 ± 0.089 | 0.900 ± 0.035   | 0.633 ± 0.099 |       3 |
| pyg_gat          | Plausible typology   | 0.612 ± 0.127 | 0.897 ± 0.026   | 0.567 ± 0.078 |       3 |
| pyg_gat          | Random feasible      | 0.693 ± 0.101 | 0.898 ± 0.036   | 0.625 ± 0.110 |       3 |
| pyg_gat          | SMOTE + repair       | 0.699 ± 0.114 | 0.898 ± 0.041   | 0.632 ± 0.115 |       3 |
| pyg_gat          | Typology projected   | 0.629 ± 0.084 | 0.886 ± 0.051   | 0.555 ± 0.067 |       3 |
| pyg_sage         | Curriculum projected | 0.339 ± 0.268 | 0.598 ± 0.223   | 0.332 ± 0.203 |       3 |
| pyg_sage         | No aug.              | 0.355 ± 0.275 | 0.617 ± 0.237   | 0.362 ± 0.199 |       3 |
| pyg_sage         | Plausible typology   | 0.292 ± 0.219 | 0.638 ± 0.235   | 0.352 ± 0.194 |       3 |
| pyg_sage         | Random feasible      | 0.353 ± 0.279 | 0.626 ± 0.242   | 0.343 ± 0.218 |       3 |
| pyg_sage         | SMOTE + repair       | 0.355 ± 0.278 | 0.625 ± 0.236   | 0.345 ± 0.210 |       3 |
| pyg_sage         | Typology projected   | 0.305 ± 0.239 | 0.614 ± 0.229   | 0.342 ± 0.214 |       3 |
