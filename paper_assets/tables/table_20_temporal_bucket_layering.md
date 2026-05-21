# Temporal Drift Buckets For Held-Out Layering

Quartiles are computed on the held-out layering test period; lower rows indicate later deployment time.

| Detector   | Time bucket   | Method               | AUPRC           | Recall@1% FPR   |   Mean positives |
|:-----------|:--------------|:---------------------|:----------------|:----------------|-----------------:|
| lightgbm   | Q1 earliest   | Curriculum projected | 0.731 ± 0.019   | 0.879 ± 0.066   |               19 |
| lightgbm   | Q1 earliest   | No aug.              | 0.655 ± 0.006   | 0.805 ± 0.025   |               19 |
| lightgbm   | Q1 earliest   | Plausible typology   | 0.722 ± 0.028   | 0.868 ± 0.057   |               19 |
| lightgbm   | Q1 earliest   | Random feasible      | 0.667 ± 0.013   | 0.805 ± 0.036   |               19 |
| lightgbm   | Q1 earliest   | SMOTE + repair       | 0.657 ± 0.009   | 0.821 ± 0.057   |               19 |
| lightgbm   | Q1 earliest   | Typology projected   | 0.738 ± 0.014   | 0.874 ± 0.051   |               19 |
| lightgbm   | Q2            | Curriculum projected | 0.991 ± 0.003   | 1.000 ± 0.000   |               53 |
| lightgbm   | Q2            | No aug.              | 0.979 ± 0.001   | 1.000 ± 0.000   |               53 |
| lightgbm   | Q2            | Plausible typology   | 0.994 ± 0.003   | 1.000 ± 0.000   |               53 |
| lightgbm   | Q2            | Random feasible      | 0.983 ± 0.005   | 1.000 ± 0.000   |               53 |
| lightgbm   | Q2            | SMOTE + repair       | 0.978 ± 0.002   | 1.000 ± 0.000   |               53 |
| lightgbm   | Q2            | Typology projected   | 0.996 ± 0.001   | 1.000 ± 0.000   |               53 |
| lightgbm   | Q3            | Curriculum projected | 0.848 ± 0.005   | 0.871 ± 0.017   |               82 |
| lightgbm   | Q3            | No aug.              | 0.818 ± 0.004   | 0.874 ± 0.010   |               82 |
| lightgbm   | Q3            | Plausible typology   | 0.852 ± 0.006   | 0.876 ± 0.025   |               82 |
| lightgbm   | Q3            | Random feasible      | 0.824 ± 0.005   | 0.890 ± 0.021   |               82 |
| lightgbm   | Q3            | SMOTE + repair       | 0.819 ± 0.006   | 0.885 ± 0.028   |               82 |
| lightgbm   | Q3            | Typology projected   | 0.852 ± 0.004   | 0.867 ± 0.018   |               82 |
| lightgbm   | Q4 latest     | Curriculum projected | 0.985 ± 7.8e-04 | 0.986 ± 0.002   |              195 |
| lightgbm   | Q4 latest     | No aug.              | 0.985 ± 6.6e-04 | 0.989 ± 0.002   |              195 |
| lightgbm   | Q4 latest     | Plausible typology   | 0.985 ± 0.001   | 0.985 ± 0.002   |              195 |
| lightgbm   | Q4 latest     | Random feasible      | 0.985 ± 6.5e-04 | 0.986 ± 0.002   |              195 |
| lightgbm   | Q4 latest     | SMOTE + repair       | 0.984 ± 9.0e-04 | 0.987 ± 0.003   |              195 |
| lightgbm   | Q4 latest     | Typology projected   | 0.986 ± 0.001   | 0.986 ± 0.002   |              195 |
| xgboost    | Q1 earliest   | Curriculum projected | 0.731 ± 0.024   | 0.889 ± 0.046   |               19 |
| xgboost    | Q1 earliest   | No aug.              | 0.651 ± 0.002   | 0.753 ± 0.025   |               19 |
| xgboost    | Q1 earliest   | Plausible typology   | 0.708 ± 0.017   | 0.884 ± 0.048   |               19 |
| xgboost    | Q1 earliest   | Random feasible      | 0.669 ± 0.008   | 0.784 ± 0.052   |               19 |
| xgboost    | Q1 earliest   | SMOTE + repair       | 0.655 ± 0.005   | 0.789 ± 0.066   |               19 |
| xgboost    | Q1 earliest   | Typology projected   | 0.707 ± 0.023   | 0.879 ± 0.056   |               19 |
| xgboost    | Q2            | Curriculum projected | 0.992 ± 0.004   | 1.000 ± 0.000   |               53 |
| xgboost    | Q2            | No aug.              | 0.979 ± 0.002   | 1.000 ± 0.000   |               53 |
| xgboost    | Q2            | Plausible typology   | 0.993 ± 0.003   | 1.000 ± 0.000   |               53 |
| xgboost    | Q2            | Random feasible      | 0.984 ± 0.003   | 1.000 ± 0.000   |               53 |
| xgboost    | Q2            | SMOTE + repair       | 0.981 ± 0.002   | 1.000 ± 0.000   |               53 |
| xgboost    | Q2            | Typology projected   | 0.992 ± 0.002   | 1.000 ± 0.000   |               53 |
| xgboost    | Q3            | Curriculum projected | 0.850 ± 0.006   | 0.866 ± 0.015   |               82 |
| xgboost    | Q3            | No aug.              | 0.810 ± 0.003   | 0.855 ± 0.009   |               82 |
| xgboost    | Q3            | Plausible typology   | 0.847 ± 0.009   | 0.873 ± 0.029   |               82 |
| xgboost    | Q3            | Random feasible      | 0.816 ± 0.004   | 0.867 ± 0.012   |               82 |
| xgboost    | Q3            | SMOTE + repair       | 0.813 ± 0.006   | 0.870 ± 0.017   |               82 |
| xgboost    | Q3            | Typology projected   | 0.850 ± 0.009   | 0.870 ± 0.021   |               82 |
| xgboost    | Q4 latest     | Curriculum projected | 0.985 ± 5.0e-04 | 0.985 ± 0.002   |              195 |
| xgboost    | Q4 latest     | No aug.              | 0.982 ± 4.9e-04 | 0.985 ± 0.000   |              195 |
| xgboost    | Q4 latest     | Plausible typology   | 0.984 ± 8.9e-04 | 0.985 ± 0.002   |              195 |
| xgboost    | Q4 latest     | Random feasible      | 0.983 ± 6.1e-04 | 0.985 ± 0.000   |              195 |
| xgboost    | Q4 latest     | SMOTE + repair       | 0.983 ± 4.8e-04 | 0.985 ± 0.000   |              195 |
| xgboost    | Q4 latest     | Typology projected   | 0.984 ± 0.001   | 0.985 ± 0.002   |              195 |
