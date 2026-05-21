#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p runs/logs

echo "[cikm-final] started at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

WORKERS="${FLOW_FRAUD_WORKERS:-4}"
THREADS="${FLOW_FRAUD_THREADS:-3}"
GRAPH_WORKERS="${FLOW_FRAUD_GRAPH_WORKERS:-2}"
GRAPH_THREADS="${FLOW_FRAUD_GRAPH_THREADS:-3}"

REPAIRED_LAYERING_AUGS=(
  none
  feature_noise_v2
  feature_noise_repaired_v2
  smote_v2
  smote_repaired_v2
  mixup_v2
  mixup_repaired_v2
  random_feasible_v2
  hard_projected_v2
  plausible_hard_projected_v2
  curriculum_projected_v2
  typology_projected_v2
  plausible_typology_projected_v2
)

FEWSHOT_AUGS=(
  none
  smote_repaired_v2
  random_feasible_v2
  hard_projected_v2
  plausible_hard_projected_v2
  curriculum_projected_v2
  typology_projected_v2
  plausible_typology_projected_v2
)

COLDSTART_AUGS=(
  none
  smote_repaired_v2
  random_feasible_v2
  plausible_hard_projected_v2
  curriculum_projected_v2
  typology_projected_v2
  plausible_typology_projected_v2
)

GRAPH_AUGS=(
  none
  smote_repaired_v2
  random_feasible_v2
  curriculum_projected_v2
  typology_projected_v2
  plausible_typology_projected_v2
)

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_final_preflight_fewshot \
  --datasets amlnet \
  --detectors lightgbm \
  --augmentations none smote_repaired_v2 random_feasible_v2 \
  --seeds 0 \
  --label-fractions 1.0 \
  --rho 0.30 \
  --candidate-multiplier 3 \
  --max-train-rows 60000 \
  --heldout-typology layering \
  --heldout-train-positives 5 \
  --workers 2 \
  --threads "$THREADS"

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_final_preflight_coldstart \
  --datasets amlnet \
  --detectors lightgbm \
  --augmentations none random_feasible_v2 \
  --seeds 0 \
  --label-fractions 1.0 \
  --rho 0.30 \
  --candidate-multiplier 3 \
  --max-train-rows 60000 \
  --heldout-typology layering \
  --eval-subset new_pair \
  --workers 2 \
  --threads "$THREADS"

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_final_preflight_low_history \
  --datasets amlnet \
  --detectors lightgbm \
  --augmentations none random_feasible_v2 \
  --seeds 0 \
  --label-fractions 1.0 \
  --rho 0.30 \
  --candidate-multiplier 3 \
  --max-train-rows 60000 \
  --heldout-typology layering \
  --eval-subset low_history_entity \
  --workers 2 \
  --threads "$THREADS"

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_final_preflight_graph \
  --datasets amlnet \
  --detectors pyg_sage pyg_gat \
  --augmentations none random_feasible_v2 \
  --seeds 0 \
  --label-fractions 1.0 \
  --rho 0.20 \
  --candidate-multiplier 2 \
  --max-train-rows 60000 \
  --heldout-typology layering \
  --workers 1 \
  --threads "$GRAPH_THREADS"

for run in cikm_final_preflight_fewshot cikm_final_preflight_coldstart cikm_final_preflight_low_history cikm_final_preflight_graph; do
  if [[ -s "runs/${run}/errors.jsonl" ]]; then
    echo "[cikm-final] preflight failed: ${run}"
    cat "runs/${run}/errors.jsonl"
    exit 1
  fi
done

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_final_repaired_layering_10seed \
  --datasets amlnet \
  --detectors lightgbm xgboost \
  --augmentations "${REPAIRED_LAYERING_AUGS[@]}" \
  --seeds 0 1 2 3 4 5 6 7 8 9 \
  --label-fractions 1.0 \
  --rho 0.75 \
  --candidate-multiplier 8 \
  --heldout-typology layering \
  --save-preds \
  --workers "$WORKERS" \
  --threads "$THREADS"

for shots in 1 5 10; do
  python3 code/cikm_extended_experiment.py run \
    --run-name "cikm_final_fewshot_layering_${shots}" \
    --datasets amlnet \
    --detectors lightgbm xgboost \
    --augmentations "${FEWSHOT_AUGS[@]}" \
    --seeds 0 1 2 3 4 5 6 7 8 9 \
    --label-fractions 1.0 \
    --rho 0.75 \
    --candidate-multiplier 8 \
    --heldout-typology layering \
    --heldout-train-positives "$shots" \
    --save-preds \
    --workers "$WORKERS" \
    --threads "$THREADS"
done

for subset in new_pair low_history_entity; do
  python3 code/cikm_extended_experiment.py run \
    --run-name "cikm_final_coldstart_${subset}" \
    --datasets amlnet \
    --detectors lightgbm xgboost \
    --augmentations "${COLDSTART_AUGS[@]}" \
    --seeds 0 1 2 3 4 \
    --label-fractions 1.0 \
    --rho 0.75 \
    --candidate-multiplier 8 \
    --heldout-typology layering \
    --eval-subset "$subset" \
    --save-preds \
    --workers "$WORKERS" \
    --threads "$THREADS"
done

python3 code/cikm_extended_experiment.py run \
  --run-name cikm_final_graph_layering \
  --datasets amlnet \
  --detectors pyg_sage pyg_gat \
  --augmentations "${GRAPH_AUGS[@]}" \
  --seeds 0 1 2 \
  --label-fractions 1.0 \
  --rho 0.75 \
  --candidate-multiplier 8 \
  --heldout-typology layering \
  --save-preds \
  --workers "$GRAPH_WORKERS" \
  --threads "$GRAPH_THREADS"

python3 code/cikm_result_analysis.py \
  --out-name cikm_final_synthesis \
  --runs \
    cikm_v2_main \
    cikm_v2_label_scarcity \
    cikm_v2_heldout_layering \
    cikm_v2_heldout_structuring \
    cikm_v2_heldout_integration \
    cikm_v2_graph \
    cikm_v2_external \
    cikm_v2_ablations \
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
    cikm_v4_rho_1p25 \
    cikm_final_repaired_layering_10seed \
    cikm_final_fewshot_layering_1 \
    cikm_final_fewshot_layering_5 \
    cikm_final_fewshot_layering_10 \
    cikm_final_coldstart_new_pair \
    cikm_final_coldstart_low_history_entity \
    cikm_final_graph_layering

python3 code/make_cikm_paper_assets.py
python3 code/cikm_final_analysis.py --n-boot "${FLOW_FRAUD_FINAL_BOOT:-200}"

echo "[cikm-final] finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
