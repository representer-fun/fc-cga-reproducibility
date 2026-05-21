#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p runs/logs

echo "[cikm-v4] started at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

WORKERS="${FLOW_FRAUD_WORKERS:-4}"
THREADS="${FLOW_FRAUD_THREADS:-3}"

REPAIRED_AUDIT_AUGS=(
  none
  feature_noise_v2
  feature_noise_repaired_v2
  smote_v2
  smote_repaired_v2
  mixup_v2
  mixup_repaired_v2
  edge_rewire_v2
  random_feasible_v2
  hard_projected_v2
  plausible_hard_projected_v2
  curriculum_projected_v2
  typology_projected_v2
  plausible_typology_projected_v2
)

FOCUSED_AUGS=(
  none
  random_feasible_v2
  hard_projected_v2
  plausible_hard_projected_v2
  curriculum_projected_v2
  typology_projected_v2
  plausible_typology_projected_v2
)

LOW_LABEL_AUGS=(
  none
  random_feasible_v2
  plausible_hard_projected_v2
  curriculum_projected_v2
  typology_projected_v2
  plausible_typology_projected_v2
)

RHO_AUGS=(
  random_feasible_v2
  plausible_hard_projected_v2
  curriculum_projected_v2
  typology_projected_v2
  plausible_typology_projected_v2
)

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_v4_preflight \
  --datasets amlnet \
  --detectors lightgbm \
  --augmentations feature_noise_repaired_v2 smote_repaired_v2 mixup_repaired_v2 plausible_typology_projected_v2 \
  --seeds 0 \
  --label-fractions 1.0 \
  --rho 0.30 \
  --candidate-multiplier 3 \
  --max-train-rows 50000 \
  --workers 2 \
  --threads "$THREADS"

if [[ -s runs/cikm_v4_preflight/errors.jsonl ]]; then
  echo "[cikm-v4] preflight failed"
  cat runs/cikm_v4_preflight/errors.jsonl
  exit 1
fi

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_v4_repaired_audit \
  --datasets transxion amlnet \
  --detectors lightgbm xgboost \
  --augmentations "${REPAIRED_AUDIT_AUGS[@]}" \
  --seeds 0 1 2 \
  --label-fractions 1.0 \
  --rho 0.75 \
  --candidate-multiplier 6 \
  --workers "$WORKERS" \
  --threads "$THREADS"

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_v4_heldout_layering_10seed \
  --datasets amlnet \
  --detectors lightgbm xgboost \
  --augmentations "${FOCUSED_AUGS[@]}" \
  --seeds 0 1 2 3 4 5 6 7 8 9 \
  --label-fractions 1.0 \
  --rho 0.75 \
  --candidate-multiplier 8 \
  --heldout-typology layering \
  --save-preds \
  --workers "$WORKERS" \
  --threads "$THREADS"

for typology in structuring integration; do
  python3 code/cikm_extended_experiment.py run \
    --run-name "cikm_v4_heldout_${typology}_5seed" \
    --datasets amlnet \
    --detectors lightgbm xgboost \
    --augmentations "${FOCUSED_AUGS[@]}" \
    --seeds 0 1 2 3 4 \
    --label-fractions 1.0 \
    --rho 0.75 \
    --candidate-multiplier 8 \
    --heldout-typology "$typology" \
    --save-preds \
    --workers "$WORKERS" \
    --threads "$THREADS"
done

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_v4_label_scarcity_5seed \
  --datasets transxion amlnet \
  --detectors lightgbm xgboost \
  --augmentations "${LOW_LABEL_AUGS[@]}" \
  --seeds 0 1 2 3 4 \
  --label-fractions 0.01 0.05 0.25 \
  --rho 0.75 \
  --candidate-multiplier 6 \
  --save-preds \
  --workers "$WORKERS" \
  --threads "$THREADS"

for rho in 0.50 1.25; do
  rho_tag="${rho/./p}"
  python3 code/cikm_extended_experiment.py run \
    --run-name "cikm_v4_rho_${rho_tag}" \
    --datasets transxion amlnet \
    --detectors lightgbm \
    --augmentations "${RHO_AUGS[@]}" \
    --seeds 0 1 2 \
    --label-fractions 1.0 \
    --rho "$rho" \
    --candidate-multiplier 6 \
    --workers "$WORKERS" \
    --threads "$THREADS"
done

python3 code/cikm_result_analysis.py \
  --out-name cikm_v4_synthesis \
  --runs \
    cikm_v2_main \
    cikm_v2_label_scarcity \
    cikm_v2_heldout_layering \
    cikm_v2_heldout_structuring \
    cikm_v2_heldout_integration \
    cikm_v2_graph \
    cikm_v2_external \
    cikm_v3_validity_audit \
    cikm_v3_label_scarcity \
    cikm_v3_heldout_layering \
    cikm_v3_heldout_structuring \
    cikm_v3_heldout_integration \
    cikm_v3_rho_plausible \
    cikm_v4_repaired_audit \
    cikm_v4_heldout_layering_10seed \
    cikm_v4_heldout_structuring_5seed \
    cikm_v4_heldout_integration_5seed \
    cikm_v4_label_scarcity_5seed \
    cikm_v4_rho_0p50 \
    cikm_v4_rho_1p25

python3 code/cikm_strengthening_analysis.py
python3 code/cikm_mechanism_analysis.py
python3 code/make_cikm_paper_assets.py

echo "[cikm-v4] finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
