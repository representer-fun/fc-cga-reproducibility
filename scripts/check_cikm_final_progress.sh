#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 - <<'PY'
from pathlib import Path

root = Path("runs")
runs = [
    ("cikm_final_preflight_fewshot", 3),
    ("cikm_final_preflight_coldstart", 2),
    ("cikm_final_preflight_low_history", 2),
    ("cikm_final_preflight_graph", 4),
    ("cikm_final_repaired_layering_10seed", 260),
    ("cikm_final_fewshot_layering_1", 160),
    ("cikm_final_fewshot_layering_5", 160),
    ("cikm_final_fewshot_layering_10", 160),
    ("cikm_final_coldstart_new_pair", 70),
    ("cikm_final_coldstart_low_history_entity", 70),
    ("cikm_final_graph_layering", 36),
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
    print(f"{run:40s} {done:4d}/{planned:<4d} errors={errors}")
print(f"\nCIKM final total: {done_total}/{planned_total} = {done_total/planned_total*100:.1f}% | errors={err_total}")

analysis = Path("results/cikm_final_analysis/final_summary.md")
print(f"final_analysis={'yes' if analysis.exists() else 'no'}")

log = root / "logs" / "cikm_final_active.log"
if log.exists():
    print("\nLast log lines:")
    for line in log.read_text(errors="replace").splitlines()[-16:]:
        print(line)
PY
