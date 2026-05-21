#!/usr/bin/env python3
"""Create paper-facing synthesis tables and claim audits."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RUNS = ROOT / "runs"


def read_csv_if_exists(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def collect_results(run_names: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    vals = []
    for run in run_names:
        r = read_csv_if_exists(RESULTS / run / "all_results.csv")
        if not r.empty:
            r["run_name"] = run
            rows.append(r)
        v = read_csv_if_exists(RESULTS / run / "all_validity.csv")
        if not v.empty:
            v["run_name"] = run
            vals.append(v)
    return (pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(), pd.concat(vals, ignore_index=True) if vals else pd.DataFrame())


def mean_std_table(df: pd.DataFrame, group_cols: list[str], metrics: list[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    metrics = [m for m in metrics if m in df.columns]
    if not metrics:
        return pd.DataFrame()
    out = df.groupby(group_cols)[metrics].agg(["mean", "std", "count"]).reset_index()
    return out


def delta_against(df: pd.DataFrame, target_aug: str, baseline_aug: str, metric: str = "auprc") -> pd.DataFrame:
    keys = ["run_name", "dataset", "detector", "seed", "label_fraction", "heldout_typology"]
    a = df[df["augmentation"].eq(target_aug)][keys + [metric]].rename(columns={metric: f"{target_aug}_{metric}"})
    b = df[df["augmentation"].eq(baseline_aug)][keys + [metric]].rename(columns={metric: f"{baseline_aug}_{metric}"})
    m = a.merge(b, on=keys, how="inner")
    if m.empty:
        return m
    m["delta"] = m[f"{target_aug}_{metric}"] - m[f"{baseline_aug}_{metric}"]
    return m


def bootstrap_prediction_cis(run_names: list[str], target_aug: str = "hard_projected_v2", baseline_aug: str = "none", n_boot: int = 300) -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(123)
    for run in run_names:
        pred_dir = RUNS / run / "predictions"
        if not pred_dir.exists():
            continue
        files = list(pred_dir.glob(f"*__{target_aug}__*.npz"))
        for f in files:
            parts = f.stem.split("__")
            if len(parts) < 5:
                continue
            dataset, detector, _, seed_s, frac_s = parts[:5]
            b = pred_dir / f"{dataset}__{detector}__{baseline_aug}__{seed_s}__{frac_s}.npz"
            if not b.exists():
                continue
            ta = np.load(f)
            ba = np.load(b)
            y = ta["y_true"]
            if len(y) == 0 or y.sum() == 0:
                continue
            s_t = ta["y_score"]
            s_b = ba["y_score"]
            base_delta = average_precision_score(y, s_t) - average_precision_score(y, s_b)
            boots = []
            n = len(y)
            for _ in range(n_boot):
                idx = rng.integers(0, n, size=n)
                if y[idx].sum() == 0:
                    continue
                boots.append(average_precision_score(y[idx], s_t[idx]) - average_precision_score(y[idx], s_b[idx]))
            lo, hi = (np.nan, np.nan) if not boots else np.quantile(boots, [0.025, 0.975])
            rows.append(
                {
                    "run_name": run,
                    "dataset": dataset,
                    "detector": detector,
                    "seed": int(seed_s.replace("seed", "")),
                    "label_fraction": float(frac_s.replace("frac", "").replace("p", ".")),
                    "target": target_aug,
                    "baseline": baseline_aug,
                    "delta_auprc": float(base_delta),
                    "ci_low": float(lo),
                    "ci_high": float(hi),
                }
            )
    return pd.DataFrame(rows)


def write_claim_audit(out_dir: Path, results: pd.DataFrame, validity: pd.DataFrame, cis: pd.DataFrame) -> None:
    lines = ["# CIKM Claim Audit", ""]
    if results.empty:
        lines.append("No results available.")
        (out_dir / "claim_audit.md").write_text("\n".join(lines))
        return

    target_candidates = [
        a
        for a in [
            "plausible_hard_projected_v2",
            "curriculum_projected_v2",
            "typology_projected_v2",
            "plausible_typology_projected_v2",
            "hard_projected_v2",
            "ours",
            "full",
        ]
        if a in set(results["augmentation"])
    ]
    for target in target_candidates:
        for baseline in ["none", "random_feasible_v2", "smote_v2", "mixup_v2", "feature_noise_v2", "adv_no_projection_v2", "random_feasible", "adv_no_projection"]:
            if baseline in set(results["augmentation"]):
                d = delta_against(results, target, baseline)
                if not d.empty:
                    lines.append(f"## {target} vs {baseline}")
                    lines.append("")
                    lines.append(f"Mean delta AUPRC: {d['delta'].mean():.4f}")
                    lines.append(f"Median delta AUPRC: {d['delta'].median():.4f}")
                    lines.append(f"Win rate: {(d['delta'] > 0).mean():.3f} over {len(d)} paired runs")
                    lines.append("")
    if not validity.empty:
        lines.append("## Validity")
        lines.append("")
        valid_cols = [
            c
            for c in [
                "ledger_violation_rate",
                "mean_flow_residual",
                "detector_hardness",
                "acceptance_rate",
                "profile_drift",
                "categorical_fractionality_rate",
                "negative_feature_rate",
            ]
            if c in validity.columns
        ]
        v = validity.groupby("augmentation")[valid_cols].mean().reset_index()
        lines.append(v.to_markdown(index=False))
        lines.append("")
    if not cis.empty:
        lines.append("## Bootstrap Prediction CIs")
        lines.append("")
        sig = cis[(cis["ci_low"] > 0) | (cis["ci_high"] < 0)]
        lines.append(f"Significant paired prediction deltas: {len(sig)} / {len(cis)}")
        lines.append("")
    lines.append("## Reviewer-Risk Notes")
    lines.append("")
    lines.append("- CIKM-ready only if projected hard counterfactuals beat both no augmentation and random feasible projection on the main graph/table detectors.")
    lines.append("- Validity alone supports a method paper only if predictive gains are strongest under drift, held-out typology, or label scarcity.")
    lines.append("- If no-ledger variants dominate AUPRC, frame projection as preserving deployable validity under small performance tradeoff, or improve selection.")
    (out_dir / "claim_audit.md").write_text("\n".join(lines))


def plot_deltas(out_dir: Path, results: pd.DataFrame, target: str = "hard_projected_v2") -> None:
    if results.empty or target not in set(results["augmentation"]) or "none" not in set(results["augmentation"]):
        return
    d = delta_against(results, target, "none")
    if d.empty:
        return
    plt.figure(figsize=(8, 4))
    labels = []
    vals = []
    for key, part in d.groupby(["dataset", "detector"]):
        labels.append(f"{key[0]}\n{key[1]}")
        vals.append(part["delta"].mean())
    order = np.argsort(vals)
    plt.bar(np.arange(len(vals)), np.array(vals)[order])
    plt.axhline(0, color="black", linewidth=1)
    plt.xticks(np.arange(len(vals)), np.array(labels)[order], rotation=45, ha="right")
    plt.ylabel("Delta AUPRC vs none")
    plt.tight_layout()
    plt.savefig(out_dir / "delta_auprc_vs_none.png", dpi=180)
    plt.close()


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runs", nargs="+", default=[
        "full_matrix",
        "label_scarcity",
        "ablations",
        "heldout_layering",
        "heldout_structuring",
        "scalability_100k",
        "scalability_500k",
        "scalability_1m",
        "augmentation_sensitivity",
        "augmentation_sensitivity_rho2",
        "external_robustness",
        "cikm_v2_main",
        "cikm_v2_label_scarcity",
        "cikm_v2_ablations",
        "cikm_v2_heldout_layering",
        "cikm_v2_heldout_structuring",
        "cikm_v2_heldout_integration",
        "cikm_v2_graph",
        "cikm_v2_rho",
        "cikm_v2_rho2",
        "cikm_v2_external",
        "cikm_v3_preflight",
        "cikm_v3_validity_audit",
        "cikm_v3_label_scarcity",
        "cikm_v3_heldout_layering",
        "cikm_v3_heldout_structuring",
        "cikm_v3_heldout_integration",
        "cikm_v3_rho_plausible",
    ])
    p.add_argument("--out-name", default="cikm_synthesis")
    p.add_argument("--bootstrap", action="store_true", help="Run paired prediction bootstrap CIs. This can be slow on million-row predictions.")
    p.add_argument("--n-boot", type=int, default=120)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = RESULTS / args.out_name
    out_dir.mkdir(parents=True, exist_ok=True)
    results, validity = collect_results(args.runs)
    if not results.empty:
        results.to_csv(out_dir / "all_combined_results.csv", index=False)
        mean_std_table(
            results,
            ["run_name", "dataset", "detector", "augmentation", "label_fraction", "heldout_typology"],
            ["auprc", "auroc", "recall_at_1pct_fpr", "precision_at_k", "ece", "training_seconds"],
        ).to_csv(out_dir / "predictive_mean_std.csv", index=False)
        for target in ["hard_projected_v2", "ours", "full"]:
            if target in set(results["augmentation"]):
                plot_deltas(out_dir, results, target=target)
                break
    if not validity.empty:
        validity.to_csv(out_dir / "all_combined_validity.csv", index=False)
        mean_std_table(
            validity,
            ["run_name", "dataset", "detector", "augmentation", "label_fraction", "heldout_typology"],
            [
                "detector_hardness",
                "ledger_violation_rate",
                "mean_flow_residual",
                "profile_drift",
                "acceptance_rate",
                "categorical_fractionality_rate",
                "negative_feature_rate",
            ],
        ).to_csv(out_dir / "validity_mean_std.csv", index=False)
    cis = bootstrap_prediction_cis(args.runs, n_boot=args.n_boot) if args.bootstrap else pd.DataFrame()
    if not cis.empty:
        cis.to_csv(out_dir / "paired_bootstrap_prediction_ci.csv", index=False)
    write_claim_audit(out_dir, results, validity, cis)
    print(f"Wrote {out_dir}")


if __name__ == "__main__":
    main()
