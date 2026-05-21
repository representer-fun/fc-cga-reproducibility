#!/usr/bin/env python3
"""Mechanism audit for ledger-conserving counterfactual augmentation.

The predictive tables answer whether augmentation helps.  This audit asks what
the generated examples look like: do they remain ledger-valid, do they stay
near held-out positive typologies, and how much hardness/profile drift do we
buy for each method?
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from cikm_extended_experiment import (
    apply_heldout,
    candidate_augmented_train,
    fit_estimator,
)
from flow_experiment import HISTORY_FEATURES, load_processed, restrict_positive_labels


ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
TABLES = PAPER / "tables"
CSV = TABLES / "csv"
FIGURES = PAPER / "figures"
OUT = RESULTS / "cikm_v4_mechanism"

METHODS = [
    "random_feasible_v2",
    "hard_projected_v2",
    "plausible_hard_projected_v2",
    "curriculum_projected_v2",
    "typology_projected_v2",
    "plausible_typology_projected_v2",
]

METHOD_LABEL = {
    "random_feasible_v2": "Random feasible",
    "hard_projected_v2": "Hard projected",
    "plausible_hard_projected_v2": "Plausible hard",
    "curriculum_projected_v2": "Curriculum projected",
    "typology_projected_v2": "Typology projected",
    "plausible_typology_projected_v2": "Plausible typology",
}


def ensure_dirs() -> None:
    for path in [OUT, PAPER, TABLES, CSV, FIGURES]:
        path.mkdir(parents=True, exist_ok=True)


def label(method: str) -> str:
    return METHOD_LABEL.get(method, method)


def metric_cell(mean: float, std: float | None = None, digits: int = 3) -> str:
    if pd.isna(mean):
        return ""
    base = f"{mean:.{digits}f}"
    if std is None or pd.isna(std):
        return base
    return f"{base} ± {std:.{digits}f}"


def maybe_cap(
    X_train: pd.DataFrame,
    meta_train: pd.DataFrame,
    y_train: np.ndarray,
    max_train_rows: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    if max_train_rows <= 0 or len(X_train) <= max_train_rows:
        return X_train.reset_index(drop=True), meta_train.reset_index(drop=True), y_train
    rng = np.random.default_rng(seed)
    pos = np.where(y_train == 1)[0]
    neg = np.where(y_train == 0)[0]
    neg_n = max_train_rows - len(pos)
    keep_neg = rng.choice(neg, size=max(0, min(len(neg), neg_n)), replace=False)
    keep = np.concatenate([pos, keep_neg])
    rng.shuffle(keep)
    return X_train.iloc[keep].reset_index(drop=True), meta_train.iloc[keep].reset_index(drop=True), y_train[keep]


def selected_feature_cols(X: pd.DataFrame) -> list[str]:
    preferred = [
        "amount",
        "amount_received",
        "log_amount",
        "hour",
        "day_of_week",
        "month",
    ] + HISTORY_FEATURES
    cols = [c for c in preferred if c in X.columns]
    if len(cols) < 4:
        cols = list(X.columns[: min(48, X.shape[1])])
    return cols


def mean_min_distance(
    A: pd.DataFrame,
    B: pd.DataFrame,
    ref: pd.DataFrame,
    cols: list[str],
    rng: np.random.Generator,
    sample: int = 1200,
    batch: int = 200,
) -> float:
    if A.empty or B.empty:
        return np.nan
    a = A[cols]
    b = B[cols]
    if len(a) > sample:
        a = a.iloc[rng.choice(len(a), size=sample, replace=False)]
    if len(b) > sample:
        b = b.iloc[rng.choice(len(b), size=sample, replace=False)]
    mean = ref[cols].to_numpy("float64").mean(axis=0, keepdims=True)
    std = ref[cols].to_numpy("float64").std(axis=0, keepdims=True) + 1e-6
    av = (a.to_numpy("float64") - mean) / std
    bv = (b.to_numpy("float64") - mean) / std
    mins = []
    for start in range(0, len(av), batch):
        block = av[start : start + batch]
        dist2 = ((block[:, None, :] - bv[None, :, :]) ** 2).mean(axis=2)
        mins.append(np.sqrt(dist2.min(axis=1)))
    return float(np.concatenate(mins).mean())


def frame_stats(prefix: str, X: pd.DataFrame, meta: pd.DataFrame) -> dict[str, float]:
    out: dict[str, float] = {}
    amount = meta["amount"].to_numpy("float64") if "amount" in meta.columns else X.get("amount", pd.Series(dtype=float)).to_numpy("float64")
    if len(amount):
        out[f"{prefix}_log_amount_mean"] = float(np.log1p(np.clip(amount, 0, None)).mean())
        out[f"{prefix}_log_amount_std"] = float(np.log1p(np.clip(amount, 0, None)).std())
    for col in ["sender_tx_count", "receiver_tx_count", "pair_tx_count", "sender_total_out", "receiver_total_in", "pair_total_amount"]:
        if col in X.columns and len(X):
            out[f"{prefix}_{col}_mean"] = float(X[col].mean())
    return out


def run_mechanism(args) -> pd.DataFrame:
    features, meta = load_processed("amlnet")
    rows = []
    for typology in args.typologies:
        train_mask, val_mask, test_mask = apply_heldout(meta, typology)
        X_train_full = features.loc[train_mask].reset_index(drop=True)
        meta_train_full = meta.loc[train_mask].reset_index(drop=True)
        X_eval = features.loc[val_mask | test_mask].reset_index(drop=True)
        meta_eval = meta.loc[val_mask | test_mask].reset_index(drop=True)
        held_pos_mask = meta_eval["label"].eq(1) & meta_eval["typology"].astype(str).eq(typology)
        X_held_pos = X_eval.loc[held_pos_mask].reset_index(drop=True)
        meta_held_pos = meta_eval.loc[held_pos_mask].reset_index(drop=True)

        for seed in args.seeds:
            rng = np.random.default_rng(seed + 9001)
            y_train_full = restrict_positive_labels(meta_train_full, 1.0, seed)
            X_train, meta_train, y_train = maybe_cap(X_train_full, meta_train_full, y_train_full, args.max_train_rows, seed)
            X_train_pos = X_train.loc[y_train == 1].reset_index(drop=True)
            meta_train_pos = meta_train.loc[y_train == 1].reset_index(drop=True)
            scorer = fit_estimator("lightgbm", X_train, y_train, seed + 17, fast=True)
            cols = selected_feature_cols(X_train)

            for method in METHODS:
                X_aug, meta_aug, y_aug, validity = candidate_augmented_train(
                    X_train,
                    meta_train,
                    y_train,
                    method,
                    seed,
                    args.rho,
                    args.candidate_multiplier,
                    scorer,
                )
                X_syn = X_aug.iloc[len(X_train) :].reset_index(drop=True)
                meta_syn = meta_aug.iloc[len(meta_train) :].reset_index(drop=True)
                row = {
                    "dataset": "amlnet",
                    "heldout_typology": typology,
                    "seed": int(seed),
                    "augmentation": method,
                    "generated": int(len(X_syn)),
                    "nn_distance_to_heldout_positive": mean_min_distance(X_syn, X_held_pos, X_train, cols, rng),
                    "nn_distance_to_train_positive": mean_min_distance(X_syn, X_train_pos, X_train, cols, rng),
                    "heldout_positive_count": int(len(X_held_pos)),
                    "train_positive_count": int(len(X_train_pos)),
                }
                row.update(frame_stats("synthetic", X_syn, meta_syn))
                row.update(frame_stats("heldout_positive", X_held_pos, meta_held_pos))
                row.update(frame_stats("train_positive", X_train_pos, meta_train_pos))
                for key, value in validity.items():
                    if isinstance(value, (int, float, np.floating)) and key not in row:
                        row[key] = float(value)
                rows.append(row)
                print(f"[mechanism] {typology}/seed{seed}/{method}: generated={len(X_syn)}", flush=True)
    return pd.DataFrame(rows)


def save_table(df: pd.DataFrame) -> None:
    if df.empty:
        return
    stat_cols = [
        "nn_distance_to_heldout_positive",
        "nn_distance_to_train_positive",
        "detector_hardness",
        "profile_drift",
        "edit_distance",
        "synthetic_log_amount_mean",
        "heldout_positive_log_amount_mean",
    ]
    stats = df.groupby(["heldout_typology", "augmentation"])[stat_cols].agg(["mean", "std", "count"]).reset_index()
    stats.to_csv(OUT / "mechanism_grouped_summary.csv", index=False)
    rows = []
    for (typology, method), part in df.groupby(["heldout_typology", "augmentation"]):
        rows.append(
            {
                "Held-out typology": typology,
                "Method": label(method),
                "Generated": int(part["generated"].mean()),
                "NN dist. to held-out positives": metric_cell(part["nn_distance_to_heldout_positive"].mean(), part["nn_distance_to_heldout_positive"].std()),
                "NN dist. to train positives": metric_cell(part["nn_distance_to_train_positive"].mean(), part["nn_distance_to_train_positive"].std()),
                "Detector hardness": metric_cell(part["detector_hardness"].mean(), part["detector_hardness"].std(), 2),
                "Profile drift": metric_cell(part["profile_drift"].mean(), part["profile_drift"].std(), 2),
                "Synthetic log amount": metric_cell(part["synthetic_log_amount_mean"].mean(), part["synthetic_log_amount_mean"].std(), 2),
                "Held-out log amount": metric_cell(part["heldout_positive_log_amount_mean"].mean(), part["heldout_positive_log_amount_mean"].std(), 2),
            }
        )
    table = pd.DataFrame(rows)
    table.to_csv(CSV / "table_13_mechanism_analysis.csv", index=False)
    lines = [
        "# Mechanism Analysis",
        "",
        "Generated-example diagnostics on AMLNet. Distances are nearest-neighbor distances in standardized transaction/history feature space; lower distance to held-out positives indicates closer support coverage.",
        "",
        table.to_markdown(index=False),
        "",
    ]
    (TABLES / "table_13_mechanism_analysis.md").write_text("\n".join(lines))


def make_plots(df: pd.DataFrame) -> None:
    if df.empty:
        return
    stats = df.groupby(["heldout_typology", "augmentation"])[
        ["nn_distance_to_heldout_positive", "nn_distance_to_train_positive", "detector_hardness", "profile_drift"]
    ].mean().reset_index()

    for typology in sorted(stats["heldout_typology"].unique()):
        part = stats[stats["heldout_typology"].eq(typology)]
        x = np.arange(len(part))
        width = 0.36
        fig, ax = plt.subplots(figsize=(9.5, 4.6))
        ax.bar(x - width / 2, part["nn_distance_to_heldout_positive"], width, label="Held-out positives")
        ax.bar(x + width / 2, part["nn_distance_to_train_positive"], width, label="Train positives")
        ax.set_xticks(x)
        ax.set_xticklabels([label(m) for m in part["augmentation"]], rotation=35, ha="right")
        ax.set_ylabel("Nearest-neighbor distance")
        ax.set_title(f"Mechanism audit: {typology} support coverage")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(FIGURES / f"fig_11_mechanism_distance_{typology}.png", dpi=220)
        fig.savefig(FIGURES / f"fig_11_mechanism_distance_{typology}.pdf")
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for typology, part in stats.groupby("heldout_typology"):
        ax.scatter(part["profile_drift"], part["detector_hardness"], label=typology, s=70, alpha=0.85)
        for _, r in part.iterrows():
            ax.annotate(label(r["augmentation"]), (r["profile_drift"], r["detector_hardness"]), fontsize=7, xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("Profile drift")
    ax.set_ylabel("Detector hardness")
    ax.set_title("Mechanism audit: hardness vs profile drift")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_12_mechanism_hardness_profile.png", dpi=220)
    fig.savefig(FIGURES / "fig_12_mechanism_hardness_profile.pdf")
    plt.close(fig)


def write_summary(df: pd.DataFrame) -> None:
    lines = ["# CIKM Mechanism Analysis", ""]
    if df.empty:
        lines.append("No mechanism rows available.")
    else:
        for typology, part in df.groupby("heldout_typology"):
            mean = part.groupby("augmentation")["nn_distance_to_heldout_positive"].mean()
            best = mean.idxmin()
            hardness = part.groupby("augmentation")["detector_hardness"].mean().idxmax()
            lines.append(f"- {typology}: closest held-out support coverage is {label(best)}; hardest generated examples are {label(hardness)}.")
        lines.append("")
        lines.append("Interpretation: a CIKM story is stronger when projected/typology-aware variants are both ledger-valid and closer to held-out positives than generic feasible samples, while avoiding the largest profile drift.")
    (OUT / "mechanism_summary.md").write_text("\n".join(lines) + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--typologies", nargs="+", default=["layering", "structuring", "integration"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    parser.add_argument("--rho", type=float, default=0.75)
    parser.add_argument("--candidate-multiplier", type=int, default=8)
    parser.add_argument("--max-train-rows", type=int, default=250000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_dirs()
    df = run_mechanism(args)
    df.to_csv(OUT / "mechanism_summary.csv", index=False)
    save_table(df)
    make_plots(df)
    write_summary(df)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
