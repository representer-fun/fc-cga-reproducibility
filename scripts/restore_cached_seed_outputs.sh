#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p runs
rsync -a cached_seed_outputs/runs/ runs/

echo "Restored cached seed-level JSONL outputs into ./runs"
echo "Use scripts/check_cikm_final_progress.sh to verify the final suite."
