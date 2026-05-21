#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 - <<'PY'
from pathlib import Path

root = Path("runs")
runs = [
    ("cikm_v4_preflight", 4),
    ("cikm_v4_repaired_audit", 168),
    ("cikm_v4_heldout_layering_10seed", 140),
    ("cikm_v4_heldout_structuring_5seed", 70),
    ("cikm_v4_heldout_integration_5seed", 70),
    ("cikm_v4_label_scarcity_5seed", 360),
    ("cikm_v4_rho_0p50", 30),
    ("cikm_v4_rho_1p25", 30),
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
    print(f"{run:36s} {done:4d}/{planned:<4d} errors={errors}")
print(f"\nCIKM v4 strengthening total: {done_total}/{planned_total} = {done_total/planned_total*100:.1f}% | errors={err_total}")

log = root / "logs" / "cikm_strengthening_active.log"
if log.exists():
    print("\nLast log lines:")
    lines = log.read_text(errors="replace").splitlines()[-12:]
    for line in lines:
        print(line)
PY
