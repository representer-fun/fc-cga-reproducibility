# Cold-Start Counterparty Shift

Evaluation restricted to future held-out-layering rows with unseen sender-receiver pairs or sparse-history entities relative to the training graph.

| Subset             | Detector   | Method               | AUPRC           | Recall@1% FPR   | Precision@K     |   Test positives |   Seeds |
|:-------------------|:-----------|:---------------------|:----------------|:----------------|:----------------|-----------------:|--------:|
| low_history_entity | lightgbm   | Curriculum projected | 0.935 ± 0.021   | 0.964 ± 0.050   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | lightgbm   | No aug.              | 0.920 ± 9.6e-04 | 0.909 ± 0.000   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | lightgbm   | Plausible hard       | 0.934 ± 0.013   | 0.964 ± 0.050   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | lightgbm   | Plausible typology   | 0.930 ± 0.012   | 0.982 ± 0.041   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | lightgbm   | Random feasible      | 0.921 ± 0.002   | 0.909 ± 0.000   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | lightgbm   | SMOTE + repair       | 0.926 ± 0.006   | 0.945 ± 0.050   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | lightgbm   | Typology projected   | 0.926 ± 0.012   | 0.945 ± 0.050   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | xgboost    | Curriculum projected | 0.932 ± 0.020   | 0.945 ± 0.050   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | xgboost    | No aug.              | 0.931 ± 0.005   | 1.000 ± 0.000   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | xgboost    | Plausible hard       | 0.930 ± 0.016   | 0.964 ± 0.050   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | xgboost    | Plausible typology   | 0.936 ± 0.012   | 0.982 ± 0.041   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | xgboost    | Random feasible      | 0.928 ± 0.004   | 0.982 ± 0.041   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | xgboost    | SMOTE + repair       | 0.933 ± 0.005   | 1.000 ± 0.000   | 0.909 ± 0.000   |               11 |       5 |
| low_history_entity | xgboost    | Typology projected   | 0.936 ± 0.010   | 0.982 ± 0.041   | 0.909 ± 0.000   |               11 |       5 |
| new_pair           | lightgbm   | Curriculum projected | 0.946 ± 0.005   | 0.951 ± 0.008   | 0.929 ± 1.2e-16 |               70 |       5 |
| new_pair           | lightgbm   | No aug.              | 0.928 ± 0.002   | 0.954 ± 0.006   | 0.909 ± 0.008   |               70 |       5 |
| new_pair           | lightgbm   | Plausible hard       | 0.951 ± 0.005   | 0.954 ± 0.006   | 0.929 ± 1.2e-16 |               70 |       5 |
| new_pair           | lightgbm   | Plausible typology   | 0.945 ± 0.011   | 0.949 ± 0.013   | 0.929 ± 0.010   |               70 |       5 |
| new_pair           | lightgbm   | Random feasible      | 0.930 ± 0.002   | 0.951 ± 0.008   | 0.911 ± 0.006   |               70 |       5 |
| new_pair           | lightgbm   | SMOTE + repair       | 0.926 ± 0.004   | 0.946 ± 0.006   | 0.900 ± 0.000   |               70 |       5 |
| new_pair           | lightgbm   | Typology projected   | 0.949 ± 0.004   | 0.957 ± 1.2e-16 | 0.931 ± 0.006   |               70 |       5 |
| new_pair           | xgboost    | Curriculum projected | 0.940 ± 0.009   | 0.949 ± 0.008   | 0.929 ± 1.2e-16 |               70 |       5 |
| new_pair           | xgboost    | No aug.              | 0.923 ± 0.001   | 0.929 ± 1.2e-16 | 0.897 ± 0.006   |               70 |       5 |
| new_pair           | xgboost    | Plausible hard       | 0.943 ± 0.009   | 0.954 ± 0.006   | 0.931 ± 0.006   |               70 |       5 |
| new_pair           | xgboost    | Plausible typology   | 0.942 ± 0.012   | 0.951 ± 0.016   | 0.929 ± 1.2e-16 |               70 |       5 |
| new_pair           | xgboost    | Random feasible      | 0.928 ± 0.003   | 0.931 ± 0.006   | 0.917 ± 0.006   |               70 |       5 |
| new_pair           | xgboost    | SMOTE + repair       | 0.925 ± 6.7e-04 | 0.929 ± 1.2e-16 | 0.909 ± 0.008   |               70 |       5 |
| new_pair           | xgboost    | Typology projected   | 0.941 ± 0.010   | 0.951 ± 0.008   | 0.929 ± 1.2e-16 |               70 |       5 |
