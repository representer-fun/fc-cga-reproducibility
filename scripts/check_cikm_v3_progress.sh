#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 - <<'PY'
from pathlib import Path

root = Path("runs")
runs = [
    ("cikm_v3_preflight", 12),
    ("cikm_v3_validity_audit", 132),
    ("cikm_v3_label_scarcity", 336),
    ("cikm_v3_heldout_layering", 42),
    ("cikm_v3_heldout_structuring", 42),
    ("cikm_v3_heldout_integration", 42),
    ("cikm_v3_rho_plausible", 60),
]
done_total = 0
planned_total = 0
err_total = 0
for run, planned in runs:
    result_path = root / run / "results.jsonl"
    error_path = root / run / "errors.jsonl"
    done = sum(1 for _ in result_path.open()) if result_path.exists() else 0
    errors = sum(1 for _ in error_path.open()) if error_path.exists() else 0
    done_total += min(done, planned)
    planned_total += planned
    err_total += errors
    print(f"{run:32s} {done:4d}/{planned:<4d} errors={errors}")
print(f"\nCIKM v3 total: {done_total}/{planned_total} = {done_total/planned_total*100:.1f}% | errors={err_total}")
PY
