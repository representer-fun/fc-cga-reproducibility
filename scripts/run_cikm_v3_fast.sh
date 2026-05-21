#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p runs/logs

echo "[cikm-v3] started at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

WORKERS="${FLOW_FRAUD_WORKERS:-4}"
THREADS="${FLOW_FRAUD_THREADS:-3}"

STANDARD_AUDIT_AUGS=(
  none
  feature_noise_v2
  smote_v2
  mixup_v2
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

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_v3_preflight \
  --datasets amlnet \
  --detectors lightgbm xgboost \
  --augmentations none plausible_hard_projected_v2 curriculum_projected_v2 typology_projected_v2 feature_noise_v2 smote_v2 \
  --seeds 0 \
  --label-fractions 1.0 \
  --rho 0.30 \
  --candidate-multiplier 3 \
  --max-train-rows 60000 \
  --workers 2 \
  --threads "$THREADS"

if [[ -s runs/cikm_v3_preflight/errors.jsonl ]]; then
  echo "[cikm-v3] preflight failed"
  cat runs/cikm_v3_preflight/errors.jsonl
  exit 1
fi

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_v3_validity_audit \
  --datasets transxion amlnet \
  --detectors lightgbm xgboost \
  --augmentations "${STANDARD_AUDIT_AUGS[@]}" \
  --seeds 0 1 2 \
  --label-fractions 1.0 \
  --rho 0.75 \
  --candidate-multiplier 6 \
  --workers "$WORKERS" \
  --threads "$THREADS"

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_v3_label_scarcity \
  --datasets transxion amlnet \
  --detectors lightgbm xgboost \
  --augmentations "${FOCUSED_AUGS[@]}" \
  --seeds 0 1 2 \
  --label-fractions 0.01 0.05 0.25 1.0 \
  --rho 0.75 \
  --candidate-multiplier 6 \
  --workers "$WORKERS" \
  --threads "$THREADS"

for typology in layering structuring integration; do
  python3 code/cikm_extended_experiment.py run \
    --run-name "cikm_v3_heldout_${typology}" \
    --datasets amlnet \
    --detectors lightgbm xgboost \
    --augmentations "${FOCUSED_AUGS[@]}" \
    --seeds 0 1 2 \
    --label-fractions 1.0 \
    --rho 0.75 \
    --candidate-multiplier 8 \
    --heldout-typology "$typology" \
    --workers "$WORKERS" \
    --threads "$THREADS"
done

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_v3_rho_plausible \
  --datasets transxion amlnet \
  --detectors lightgbm xgboost \
  --augmentations random_feasible_v2 plausible_hard_projected_v2 curriculum_projected_v2 typology_projected_v2 plausible_typology_projected_v2 \
  --seeds 0 1 2 \
  --label-fractions 1.0 \
  --rho 0.25 \
  --candidate-multiplier 6 \
  --workers "$WORKERS" \
  --threads "$THREADS"

python3 code/cikm_result_analysis.py \
  --out-name cikm_v3_synthesis \
  --runs \
    cikm_v2_main \
    cikm_v2_label_scarcity \
    cikm_v2_heldout_layering \
    cikm_v2_heldout_structuring \
    cikm_v2_heldout_integration \
    cikm_v3_validity_audit \
    cikm_v3_label_scarcity \
    cikm_v3_heldout_layering \
    cikm_v3_heldout_structuring \
    cikm_v3_heldout_integration \
    cikm_v3_rho_plausible

echo "[cikm-v3] finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
