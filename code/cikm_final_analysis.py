#!/usr/bin/env python3
"""Final CIKM experiment synthesis.

This script turns the last experiment suite into reviewer-facing tables:
alert-budget metrics, bootstrap CIs, repaired-baseline transfer, few-shot
typology adaptation, temporal drift buckets, cold-start slices, graph-model
confirmation, and failure-mode diagnostics.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

from cikm_extended_experiment import apply_heldout
from flow_experiment import load_processed, precision_at_k, recall_at_fpr


ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RUNS = ROOT / "runs"
PAPER = ROOT / "paper"
TABLES = PAPER / "tables"
CSV = TABLES / "csv"
FIGURES = PAPER / "figures"
OUT = RESULTS / "cikm_final_analysis"

FINAL_LAYERING = "cikm_final_repaired_layering_10seed"
GRAPH_LAYERING = "cikm_final_graph_layering"
FEWSHOT_RUNS = {
    0: "cikm_v4_heldout_layering_10seed",
    1: "cikm_final_fewshot_layering_1",
    5: "cikm_final_fewshot_layering_5",
    10: "cikm_final_fewshot_layering_10",
}
COLDSTART_RUNS = {
    "new_pair": "cikm_final_coldstart_new_pair",
    "low_history_entity": "cikm_final_coldstart_low_history_entity",
}

METHOD_LABEL = {
    "none": "No aug.",
    "feature_noise_v2": "Feature noise",
    "feature_noise_repaired_v2": "Feature noise + repair",
    "smote_v2": "SMOTE",
    "smote_repaired_v2": "SMOTE + repair",
    "mixup_v2": "Mixup",
    "mixup_repaired_v2": "Mixup + repair",
    "random_feasible_v2": "Random feasible",
    "hard_projected_v2": "Hard projected",
    "plausible_hard_projected_v2": "Plausible hard",
    "curriculum_projected_v2": "Curriculum projected",
    "typology_projected_v2": "Typology projected",
    "plausible_typology_projected_v2": "Plausible typology",
}

PAPER_METHODS = [
    "none",
    "smote_repaired_v2",
    "mixup_repaired_v2",
    "random_feasible_v2",
    "hard_projected_v2",
    "plausible_hard_projected_v2",
    "curriculum_projected_v2",
    "typology_projected_v2",
    "plausible_typology_projected_v2",
]


def ensure_dirs() -> None:
    for path in [OUT, PAPER, TABLES, CSV, FIGURES]:
        path.mkdir(parents=True, exist_ok=True)


def label(method: str) -> str:
    return METHOD_LABEL.get(method, method)


def metric_cell(mean: float, std: float | None = None, digits: int = 3) -> str:
    if pd.isna(mean):
        return ""
    base = f"{mean:.{digits}f}" if abs(mean) >= 0.001 or mean == 0 else f"{mean:.2e}"
    if std is None or pd.isna(std):
        return base
    spread = f"{std:.{digits}f}" if abs(std) >= 0.001 or std == 0 else f"{std:.1e}"
    return f"{base} ± {spread}"


def save_table(df: pd.DataFrame, stem: str, title: str, note: str = "") -> None:
    df.to_csv(CSV / f"{stem}.csv", index=False)
    lines = [f"# {title}", ""]
    if note:
        lines += [note, ""]
    lines += [df.to_markdown(index=False), ""]
    (TABLES / f"{stem}.md").write_text("\n".join(lines))


def read_results(run: str) -> pd.DataFrame:
    path = RESULTS / run / "all_results.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["run_name"] = run
    return df


def parse_pred_file(path: Path) -> dict | None:
    parts = path.stem.split("__")
    if len(parts) != 5:
        return None
    dataset, detector, augmentation, seed_s, frac_s = parts
    data = np.load(path)
    return {
        "dataset": dataset,
        "detector": detector,
        "augmentation": augmentation,
        "seed": int(seed_s.replace("seed", "")),
        "label_fraction": float(frac_s.replace("frac", "").replace("p", ".")),
        "y_true": data["y_true"].astype("int8"),
        "y_score": data["y_score"].astype("float64"),
        "path": path,
    }


def load_predictions(run: str) -> list[dict]:
    pred_dir = RUNS / run / "predictions"
    if not pred_dir.exists():
        return []
    rows = []
    for path in sorted(pred_dir.glob("*.npz")):
        item = parse_pred_file(path)
        if item:
            item["run_name"] = run
            rows.append(item)
    return rows


def prediction_metrics(preds: list[dict]) -> pd.DataFrame:
    rows = []
    for p in preds:
        y = p["y_true"]
        s = p["y_score"]
        row = {k: p[k] for k in ["run_name", "dataset", "detector", "augmentation", "seed", "label_fraction"]}
        row.update(
            {
                "auprc": average_precision_score(y, s) if y.sum() else np.nan,
                "recall_at_0_1pct_fpr": recall_at_fpr(y, s, 0.001),
                "recall_at_0_5pct_fpr": recall_at_fpr(y, s, 0.005),
                "recall_at_1pct_fpr": recall_at_fpr(y, s, 0.01),
                "precision_top_100": precision_at_k(y, s, 100),
                "precision_top_500": precision_at_k(y, s, 500),
                "precision_top_1000": precision_at_k(y, s, 1000),
                "positives": int(y.sum()),
                "rows": int(len(y)),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def make_alert_budget_table() -> pd.DataFrame:
    df = prediction_metrics(load_predictions(FINAL_LAYERING))
    if df.empty:
        return pd.DataFrame()
    df.to_csv(OUT / "alert_budget_prediction_metrics.csv", index=False)
    methods = [m for m in PAPER_METHODS if m in set(df["augmentation"])]
    rows = []
    for (detector, method), part in df[df["augmentation"].isin(methods)].groupby(["detector", "augmentation"]):
        rows.append(
            {
                "Detector": detector,
                "Method": label(method),
                "AUPRC": metric_cell(part["auprc"].mean(), part["auprc"].std()),
                "Recall@0.1% FPR": metric_cell(part["recall_at_0_1pct_fpr"].mean(), part["recall_at_0_1pct_fpr"].std()),
                "Recall@0.5% FPR": metric_cell(part["recall_at_0_5pct_fpr"].mean(), part["recall_at_0_5pct_fpr"].std()),
                "Recall@1% FPR": metric_cell(part["recall_at_1pct_fpr"].mean(), part["recall_at_1pct_fpr"].std()),
                "Prec@100": metric_cell(part["precision_top_100"].mean(), part["precision_top_100"].std()),
                "Prec@500": metric_cell(part["precision_top_500"].mean(), part["precision_top_500"].std()),
                "Prec@1000": metric_cell(part["precision_top_1000"].mean(), part["precision_top_1000"].std()),
            }
        )
    table = pd.DataFrame(rows)
    table["order"] = table["Method"].map({label(m): i for i, m in enumerate(methods)}).fillna(999)
    table = table.sort_values(["Detector", "order"]).drop(columns=["order"])
    save_table(
        table,
        "table_16_alert_budget_layering",
        "Alert-Budget Evaluation On Held-Out Layering",
        "Mean ± std across 10 seeds. This is the deployment-facing low-FPR/top-alert view.",
    )
    return df


def bootstrap_delta(y: np.ndarray, s_t: np.ndarray, s_b: np.ndarray, rng: np.random.Generator, n_boot: int) -> tuple[float, float, float]:
    base = average_precision_score(y, s_t) - average_precision_score(y, s_b)
    vals = []
    n = len(y)
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        if y[idx].sum() == 0:
            continue
        vals.append(average_precision_score(y[idx], s_t[idx]) - average_precision_score(y[idx], s_b[idx]))
    if not vals:
        return float(base), np.nan, np.nan
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return float(base), float(lo), float(hi)


def make_bootstrap_table(n_boot: int) -> pd.DataFrame:
    preds = load_predictions(FINAL_LAYERING)
    if not preds:
        return pd.DataFrame()
    keyed = {(p["detector"], p["augmentation"], p["seed"]): p for p in preds}
    targets = [
        "random_feasible_v2",
        "smote_repaired_v2",
        "hard_projected_v2",
        "plausible_hard_projected_v2",
        "curriculum_projected_v2",
        "typology_projected_v2",
        "plausible_typology_projected_v2",
    ]
    baselines = ["none", "smote_repaired_v2"]
    rng = np.random.default_rng(20260521)
    rows = []
    for detector in sorted({p["detector"] for p in preds}):
        for target in targets:
            for baseline in baselines:
                if target == baseline:
                    continue
                deltas = []
                lows = []
                highs = []
                wins = 0
                n = 0
                for seed in sorted({p["seed"] for p in preds}):
                    tp = keyed.get((detector, target, seed))
                    bp = keyed.get((detector, baseline, seed))
                    if not tp or not bp:
                        continue
                    y = tp["y_true"]
                    d, lo, hi = bootstrap_delta(y, tp["y_score"], bp["y_score"], rng, n_boot)
                    deltas.append(d)
                    lows.append(lo)
                    highs.append(hi)
                    wins += int(d > 0)
                    n += 1
                if n:
                    rows.append(
                        {
                            "Detector": detector,
                            "Target": label(target),
                            "Baseline": label(baseline),
                            "Mean ΔAUPRC": float(np.mean(deltas)),
                            "Mean bootstrap low": float(np.nanmean(lows)),
                            "Mean bootstrap high": float(np.nanmean(highs)),
                            "Seed win rate": wins / n,
                            "Seeds": n,
                        }
                    )
    raw = pd.DataFrame(rows)
    raw.to_csv(OUT / "layering_prediction_bootstrap.csv", index=False)
    table = raw.copy()
    for col in ["Mean ΔAUPRC", "Mean bootstrap low", "Mean bootstrap high", "Seed win rate"]:
        table[col] = table[col].map(lambda x: f"{x:.3f}")
    save_table(
        table,
        "table_17_layering_bootstrap_significance",
        "Paired Bootstrap Significance On Held-Out Layering",
        f"Prediction-level bootstrap with {n_boot} resamples per seed, summarized across seeds.",
    )
    return raw


def make_repaired_transfer_table() -> pd.DataFrame:
    df = read_results(FINAL_LAYERING)
    if df.empty:
        return df
    methods = [
        "none",
        "feature_noise_v2",
        "feature_noise_repaired_v2",
        "smote_v2",
        "smote_repaired_v2",
        "mixup_v2",
        "mixup_repaired_v2",
        "random_feasible_v2",
        "hard_projected_v2",
        "plausible_hard_projected_v2",
        "curriculum_projected_v2",
        "typology_projected_v2",
        "plausible_typology_projected_v2",
    ]
    rows = []
    for detector, part in df.groupby("detector"):
        stat = part.groupby("augmentation")["auprc"].agg(["mean", "std", "count"])
        base = stat.loc["none", "mean"] if "none" in stat.index else np.nan
        for method in methods:
            if method not in stat.index:
                continue
            rows.append(
                {
                    "Detector": detector,
                    "Method": label(method),
                    "AUPRC": metric_cell(stat.loc[method, "mean"], stat.loc[method, "std"]),
                    "Δ vs no aug.": f"{stat.loc[method, 'mean'] - base:+.3f}" if not pd.isna(base) else "",
                    "Seeds": int(stat.loc[method, "count"]),
                }
            )
    table = pd.DataFrame(rows)
    save_table(
        table,
        "table_18_repaired_baselines_on_layering",
        "Repaired Baselines On Held-Out Layering",
        "Tests whether post-hoc repair is enough to match typology-aware projected counterfactuals under the main positive shift.",
    )
    return df


def make_fewshot_table() -> pd.DataFrame:
    pieces = []
    for shots, run in FEWSHOT_RUNS.items():
        df = read_results(run)
        if df.empty:
            continue
        df["shots"] = shots
        pieces.append(df)
    if not pieces:
        return pd.DataFrame()
    data = pd.concat(pieces, ignore_index=True)
    methods = [m for m in PAPER_METHODS if m in set(data["augmentation"])]
    rows = []
    for (shots, detector), part in data.groupby(["shots", "detector"]):
        stat = part.groupby("augmentation")["auprc"].agg(["mean", "std"])
        base = stat.loc["none", "mean"] if "none" in stat.index else np.nan
        row = {"Held-out positives in train": int(shots), "Detector": detector}
        for method in methods:
            if method in stat.index:
                row[label(method)] = metric_cell(stat.loc[method, "mean"], stat.loc[method, "std"])
                row[f"{label(method)} Δ"] = f"{stat.loc[method, 'mean'] - base:+.3f}" if method != "none" and not pd.isna(base) else ""
        rows.append(row)
    table = pd.DataFrame(rows).sort_values(["Detector", "Held-out positives in train"])
    save_table(
        table,
        "table_19_fewshot_layering_adaptation",
        "Few-Shot Held-Out Layering Adaptation",
        "Adds 0, 1, 5, or 10 held-out layering positives from the training split, then evaluates on future held-out layering.",
    )
    data.to_csv(OUT / "fewshot_layering_results.csv", index=False)
    return data


def make_temporal_bucket_table() -> pd.DataFrame:
    preds = [p for p in load_predictions(FINAL_LAYERING) if p["dataset"] == "amlnet"]
    if not preds:
        return pd.DataFrame()
    _, meta = load_processed("amlnet")
    _, _, test_mask = apply_heldout(meta, "layering")
    meta_test = meta.loc[test_mask].reset_index(drop=True)
    if "time_sort" in meta_test.columns:
        time_values = meta_test["time_sort"].to_numpy()
    else:
        time_values = np.arange(len(meta_test))
    bucket = pd.qcut(pd.Series(time_values).rank(method="first"), 4, labels=["Q1 earliest", "Q2", "Q3", "Q4 latest"]).astype(str).to_numpy()
    rows = []
    for p in preds:
        if len(p["y_true"]) != len(meta_test):
            continue
        for b in ["Q1 earliest", "Q2", "Q3", "Q4 latest"]:
            mask = bucket == b
            y = p["y_true"][mask]
            s = p["y_score"][mask]
            rows.append(
                {
                    "detector": p["detector"],
                    "augmentation": p["augmentation"],
                    "seed": p["seed"],
                    "time_bucket": b,
                    "auprc": average_precision_score(y, s) if y.sum() else np.nan,
                    "recall_at_1pct_fpr": recall_at_fpr(y, s, 0.01),
                    "positives": int(y.sum()),
                    "rows": int(len(y)),
                }
            )
    data = pd.DataFrame(rows)
    data.to_csv(OUT / "temporal_bucket_metrics.csv", index=False)
    methods = [m for m in ["none", "smote_repaired_v2", "random_feasible_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"] if m in set(data["augmentation"])]
    table_rows = []
    for (detector, bucket_name, method), part in data[data["augmentation"].isin(methods)].groupby(["detector", "time_bucket", "augmentation"]):
        table_rows.append(
            {
                "Detector": detector,
                "Time bucket": bucket_name,
                "Method": label(method),
                "AUPRC": metric_cell(part["auprc"].mean(), part["auprc"].std()),
                "Recall@1% FPR": metric_cell(part["recall_at_1pct_fpr"].mean(), part["recall_at_1pct_fpr"].std()),
                "Mean positives": int(round(part["positives"].mean())),
            }
        )
    table = pd.DataFrame(table_rows)
    save_table(
        table,
        "table_20_temporal_bucket_layering",
        "Temporal Drift Buckets For Held-Out Layering",
        "Quartiles are computed on the held-out layering test period; lower rows indicate later deployment time.",
    )
    return data


def make_coldstart_table() -> pd.DataFrame:
    pieces = []
    for subset, run in COLDSTART_RUNS.items():
        df = read_results(run)
        if df.empty:
            continue
        df["coldstart_subset"] = subset
        pieces.append(df)
    if not pieces:
        return pd.DataFrame()
    data = pd.concat(pieces, ignore_index=True)
    methods = [m for m in PAPER_METHODS if m in set(data["augmentation"])]
    rows = []
    for (subset, detector, method), part in data[data["augmentation"].isin(methods)].groupby(["coldstart_subset", "detector", "augmentation"]):
        rows.append(
            {
                "Subset": subset,
                "Detector": detector,
                "Method": label(method),
                "AUPRC": metric_cell(part["auprc"].mean(), part["auprc"].std()),
                "Recall@1% FPR": metric_cell(part["recall_at_1pct_fpr"].mean(), part["recall_at_1pct_fpr"].std()),
                "Precision@K": metric_cell(part["precision_at_k"].mean(), part["precision_at_k"].std()),
                "Test positives": int(round(part["test_positives"].mean())),
                "Seeds": int(part["seed"].nunique()),
            }
        )
    table = pd.DataFrame(rows)
    save_table(
        table,
        "table_21_coldstart_counterparty_shift",
        "Cold-Start Counterparty Shift",
        "Evaluation restricted to future held-out-layering rows with unseen sender-receiver pairs or sparse-history entities relative to the training graph.",
    )
    return data


def make_graph_table() -> pd.DataFrame:
    df = read_results(GRAPH_LAYERING)
    if df.empty:
        return df
    rows = []
    for (detector, method), part in df.groupby(["detector", "augmentation"]):
        rows.append(
            {
                "Graph detector": detector,
                "Method": label(method),
                "AUPRC": metric_cell(part["auprc"].mean(), part["auprc"].std()),
                "Recall@1% FPR": metric_cell(part["recall_at_1pct_fpr"].mean(), part["recall_at_1pct_fpr"].std()),
                "Precision@K": metric_cell(part["precision_at_k"].mean(), part["precision_at_k"].std()),
                "Seeds": int(part["seed"].nunique()),
            }
        )
    table = pd.DataFrame(rows)
    save_table(
        table,
        "table_22_graph_model_layering_confirmation",
        "Graph-Model Confirmation On Held-Out Layering",
        "Small CPU PyG confirmation for the main positive typology-shift setting.",
    )
    return df


def make_failure_table() -> pd.DataFrame:
    pieces = [read_results("cikm_v4_heldout_structuring_5seed"), read_results("cikm_v4_heldout_integration_5seed")]
    data = pd.concat([p for p in pieces if not p.empty], ignore_index=True) if any(not p.empty for p in pieces) else pd.DataFrame()
    if data.empty:
        return data
    rows = []
    for (typology, detector), part in data.groupby(["heldout_typology", "detector"]):
        stat = part.groupby("augmentation")["auprc"].agg(["mean", "std"])
        base = stat.loc["none", "mean"] if "none" in stat.index else np.nan
        for method in [m for m in PAPER_METHODS if m in stat.index]:
            rows.append(
                {
                    "Held-out typology": typology,
                    "Detector": detector,
                    "Method": label(method),
                    "AUPRC": metric_cell(stat.loc[method, "mean"], stat.loc[method, "std"]),
                    "Δ vs no aug.": f"{stat.loc[method, 'mean'] - base:+.3f}" if method != "none" and not pd.isna(base) else "",
                }
            )
    table = pd.DataFrame(rows)
    save_table(
        table,
        "table_23_failure_modes_structuring_integration",
        "Failure Modes: Structuring And Integration",
        "These results should be used as an honest boundary condition: hard valid counterfactuals do not help every AML typology.",
    )
    return data


def save_fig(fig, stem: str) -> None:
    fig.tight_layout()
    fig.savefig(FIGURES / f"{stem}.png", dpi=220)
    fig.savefig(FIGURES / f"{stem}.pdf")
    plt.close(fig)


def make_plots(alert: pd.DataFrame, fewshot: pd.DataFrame, temporal: pd.DataFrame, cold: pd.DataFrame, graph: pd.DataFrame) -> None:
    if not alert.empty:
        methods = ["none", "smote_repaired_v2", "random_feasible_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]
        part = alert[alert["augmentation"].isin(methods)].groupby(["detector", "augmentation"])["recall_at_1pct_fpr"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 4.8))
        labels = [f"{r.detector}\n{label(r.augmentation)}" for r in part.itertuples()]
        ax.bar(np.arange(len(part)), part["recall_at_1pct_fpr"])
        ax.set_xticks(np.arange(len(part)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Recall@1% FPR")
        ax.set_title("Held-out layering alert-budget recall")
        save_fig(fig, "fig_13_alert_budget_layering")

    if not fewshot.empty:
        methods = ["none", "random_feasible_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]
        stat = fewshot[fewshot["augmentation"].isin(methods)].groupby(["shots", "augmentation"])["auprc"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(8.5, 4.7))
        for method in methods:
            p = stat[stat["augmentation"].eq(method)].sort_values("shots")
            ax.plot(p["shots"], p["auprc"], marker="o", label=label(method))
        ax.set_xlabel("Held-out layering positives retained in training")
        ax.set_ylabel("AUPRC")
        ax.set_title("Few-shot held-out typology adaptation")
        ax.legend(frameon=False, fontsize=8)
        save_fig(fig, "fig_14_fewshot_layering")

    if not temporal.empty:
        methods = ["none", "smote_repaired_v2", "curriculum_projected_v2", "typology_projected_v2"]
        stat = temporal[temporal["augmentation"].isin(methods)].groupby(["time_bucket", "augmentation"])["auprc"].mean().reset_index()
        order = ["Q1 earliest", "Q2", "Q3", "Q4 latest"]
        fig, ax = plt.subplots(figsize=(8.8, 4.7))
        for method in methods:
            p = stat[stat["augmentation"].eq(method)].copy()
            p["order"] = p["time_bucket"].map({b: i for i, b in enumerate(order)})
            p = p.sort_values("order")
            ax.plot(p["time_bucket"], p["auprc"], marker="o", label=label(method))
        ax.set_ylabel("AUPRC")
        ax.set_title("Held-out layering over future temporal buckets")
        ax.legend(frameon=False, fontsize=8)
        save_fig(fig, "fig_15_temporal_bucket_layering")

    if not cold.empty:
        methods = ["none", "smote_repaired_v2", "random_feasible_v2", "curriculum_projected_v2", "typology_projected_v2"]
        stat = cold[cold["augmentation"].isin(methods)].groupby(["coldstart_subset", "augmentation"])["auprc"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(9.5, 4.8))
        labels = [f"{r.coldstart_subset}\n{label(r.augmentation)}" for r in stat.itertuples()]
        ax.bar(np.arange(len(stat)), stat["auprc"])
        ax.set_xticks(np.arange(len(stat)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("AUPRC")
        ax.set_title("Cold-start counterparty shift")
        save_fig(fig, "fig_16_coldstart_counterparty_shift")

    if not graph.empty:
        stat = graph.groupby(["detector", "augmentation"])["auprc"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(8.5, 4.7))
        labels = [f"{r.detector}\n{label(r.augmentation)}" for r in stat.itertuples()]
        ax.bar(np.arange(len(stat)), stat["auprc"])
        ax.set_xticks(np.arange(len(stat)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("AUPRC")
        ax.set_title("Graph-model confirmation on held-out layering")
        save_fig(fig, "fig_17_graph_model_layering")


def write_summary(alert: pd.DataFrame, boot: pd.DataFrame, repaired: pd.DataFrame, fewshot: pd.DataFrame, cold: pd.DataFrame, graph: pd.DataFrame) -> None:
    lines = ["# Final CIKM Experiment Summary", ""]
    if not repaired.empty:
        stat = repaired.groupby(["detector", "augmentation"])["auprc"].mean()
        for detector in sorted(repaired["detector"].unique()):
            part = stat.loc[detector]
            best = part.idxmax()
            lines.append(f"- Held-out layering/{detector}: best={label(best)} AUPRC={part.loc[best]:.3f}.")
    if not alert.empty:
        stat = alert.groupby(["detector", "augmentation"])["recall_at_1pct_fpr"].mean()
        for detector in sorted(alert["detector"].unique()):
            part = stat.loc[detector]
            best = part.idxmax()
            lines.append(f"- Alert budget/{detector}: best Recall@1% FPR={label(best)} ({part.loc[best]:.3f}).")
    if not fewshot.empty:
        stat = fewshot.groupby(["shots", "augmentation"])["auprc"].mean()
        for shots in sorted(fewshot["shots"].unique()):
            part = stat.loc[shots]
            lines.append(f"- Few-shot {shots}: best={label(part.idxmax())} AUPRC={part.max():.3f}.")
    if not cold.empty:
        stat = cold.groupby(["coldstart_subset", "augmentation"])["auprc"].mean()
        for subset in sorted(cold["coldstart_subset"].unique()):
            part = stat.loc[subset]
            lines.append(f"- Cold-start {subset}: best={label(part.idxmax())} AUPRC={part.max():.3f}.")
    if not graph.empty:
        stat = graph.groupby(["detector", "augmentation"])["auprc"].mean()
        for detector in sorted(graph["detector"].unique()):
            part = stat.loc[detector]
            lines.append(f"- Graph {detector}: best={label(part.idxmax())} AUPRC={part.max():.3f}.")
    if not boot.empty:
        sig = boot[(boot["Mean bootstrap low"] > 0) | (boot["Mean bootstrap high"] < 0)]
        lines.append(f"- Bootstrap checks with nonzero-sign intervals: {len(sig)}/{len(boot)} comparisons.")
    (OUT / "final_summary.md").write_text("\n".join(lines) + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-boot", type=int, default=200)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_dirs()
    alert = make_alert_budget_table()
    boot = make_bootstrap_table(args.n_boot)
    repaired = make_repaired_transfer_table()
    fewshot = make_fewshot_table()
    temporal = make_temporal_bucket_table()
    cold = make_coldstart_table()
    graph = make_graph_table()
    make_failure_table()
    make_plots(alert, fewshot, temporal, cold, graph)
    write_summary(alert, boot, repaired, fewshot, cold, graph)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
