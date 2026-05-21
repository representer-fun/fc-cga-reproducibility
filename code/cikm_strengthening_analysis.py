#!/usr/bin/env python3
"""Paper-facing analysis for the CIKM v4 strengthening suite."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
TABLES = PAPER / "tables"
CSV = TABLES / "csv"
FIGURES = PAPER / "figures"
OUT = RESULTS / "cikm_v4_strengthening"

METHOD_LABEL = {
    "none": "No aug.",
    "feature_noise_v2": "Feature noise",
    "feature_noise_repaired_v2": "Feature noise + repair",
    "smote_v2": "SMOTE",
    "smote_repaired_v2": "SMOTE + repair",
    "mixup_v2": "Mixup",
    "mixup_repaired_v2": "Mixup + repair",
    "edge_rewire_v2": "Edge rewire",
    "random_feasible_v2": "Random feasible",
    "hard_projected_v2": "Hard projected",
    "plausible_hard_projected_v2": "Plausible hard",
    "curriculum_projected_v2": "Curriculum projected",
    "typology_projected_v2": "Typology projected",
    "plausible_typology_projected_v2": "Plausible typology",
}

METHOD_ORDER = [
    "none",
    "feature_noise_v2",
    "feature_noise_repaired_v2",
    "smote_v2",
    "smote_repaired_v2",
    "mixup_v2",
    "mixup_repaired_v2",
    "edge_rewire_v2",
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


def read_run(run: str, kind: str = "all_results.csv") -> pd.DataFrame:
    path = RESULTS / run / kind
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["run_name"] = run
    return df


def label(method: str) -> str:
    return METHOD_LABEL.get(method, method)


def metric_cell(mean: float, std: float | None = None, digits: int = 3) -> str:
    if pd.isna(mean):
        return ""
    base = f"{mean:.{digits}f}"
    if std is None or pd.isna(std):
        return base
    return f"{base} ± {std:.{digits}f}"


def pct(x: float, digits: int = 1) -> str:
    if pd.isna(x):
        return ""
    return f"{100 * x:.{digits}f}%"


def mean_ci(values: pd.Series | np.ndarray) -> tuple[float, float, float, int]:
    arr = np.asarray(values, dtype="float64")
    arr = arr[~np.isnan(arr)]
    n = len(arr)
    if n == 0:
        return np.nan, np.nan, np.nan, 0
    mean = float(arr.mean())
    if n == 1:
        return mean, np.nan, np.nan, n
    half = 1.96 * float(arr.std(ddof=1)) / math.sqrt(n)
    return mean, mean - half, mean + half, n


def paired_deltas(df: pd.DataFrame, baseline: str, metric: str = "auprc") -> pd.DataFrame:
    keys = ["dataset", "detector", "seed", "label_fraction", "heldout_typology"]
    base = df[df["augmentation"].eq(baseline)][keys + [metric]].rename(columns={metric: "baseline_metric"})
    rows = []
    for method, part in df.groupby("augmentation"):
        if method == baseline:
            continue
        merged = part[keys + [metric]].merge(base, on=keys, how="inner")
        if merged.empty:
            continue
        merged["delta"] = merged[metric] - merged["baseline_metric"]
        for group_cols, group in [(("all",), merged), *list(merged.groupby(["dataset", "detector", "heldout_typology"]))]:
            if isinstance(group_cols, tuple) and len(group_cols) == 1 and group_cols[0] == "all":
                dataset, detector, heldout = "all", "all", "all"
                g = group
            else:
                dataset, detector, heldout = group_cols
                g = group
            mean, lo, hi, n = mean_ci(g["delta"])
            rows.append(
                {
                    "baseline": baseline,
                    "augmentation": method,
                    "dataset": dataset,
                    "detector": detector,
                    "heldout_typology": heldout,
                    "mean_delta": mean,
                    "ci_low": lo,
                    "ci_high": hi,
                    "n_pairs": n,
                    "win_rate": float((g["delta"] > 0).mean()) if n else np.nan,
                }
            )
    return pd.DataFrame(rows)


def summarize_heldout() -> pd.DataFrame:
    runs = [
        "cikm_v4_heldout_layering_10seed",
        "cikm_v4_heldout_structuring_5seed",
        "cikm_v4_heldout_integration_5seed",
    ]
    data = pd.concat([read_run(r) for r in runs], ignore_index=True)
    if data.empty:
        return pd.DataFrame()
    stats = (
        data.groupby(["run_name", "heldout_typology", "detector", "augmentation"])[
            ["auprc", "auroc", "recall_at_1pct_fpr", "precision_at_k", "ece"]
        ]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    stats.to_csv(OUT / "heldout_seed_summary.csv", index=False)
    deltas = pd.concat([paired_deltas(data, "none"), paired_deltas(data, "random_feasible_v2")], ignore_index=True)
    deltas.to_csv(OUT / "heldout_paired_seed_deltas.csv", index=False)
    return data


def summarize_repaired() -> tuple[pd.DataFrame, pd.DataFrame]:
    results = read_run("cikm_v4_repaired_audit")
    validity = read_run("cikm_v4_repaired_audit", "all_validity.csv")
    if results.empty:
        return results, validity
    perf = results.groupby(["dataset", "detector", "augmentation"])["auprc"].agg(["mean", "std", "count"]).reset_index()
    perf.to_csv(OUT / "repaired_predictive_summary.csv", index=False)
    if not validity.empty:
        cols = [
            "ledger_violation_rate",
            "mean_flow_residual",
            "categorical_fractionality_rate",
            "negative_feature_rate",
            "profile_drift",
            "detector_hardness",
            "acceptance_rate",
        ]
        v = validity.groupby("augmentation")[[c for c in cols if c in validity.columns]].mean().reset_index()
        v.to_csv(OUT / "repaired_validity_summary.csv", index=False)
    return results, validity


def summarize_label_scarcity() -> pd.DataFrame:
    df = read_run("cikm_v4_label_scarcity_5seed")
    if df.empty:
        return df
    stats = df.groupby(["dataset", "detector", "label_fraction", "augmentation"])["auprc"].agg(["mean", "std", "count"]).reset_index()
    stats.to_csv(OUT / "label_scarcity_5seed_summary.csv", index=False)
    deltas = paired_deltas(df, "none")
    deltas.to_csv(OUT / "label_scarcity_5seed_paired_deltas.csv", index=False)
    return df


def summarize_rho() -> pd.DataFrame:
    runs = ["cikm_v3_rho_plausible", "cikm_v4_rho_0p50", "cikm_v3_validity_audit", "cikm_v4_rho_1p25"]
    parts = [read_run(r) for r in runs]
    df = pd.concat([p for p in parts if not p.empty], ignore_index=True) if any(not p.empty for p in parts) else pd.DataFrame()
    if df.empty:
        return df
    keep = df[df["augmentation"].isin(["random_feasible_v2", "plausible_hard_projected_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"])]
    stats = keep.groupby(["rho", "augmentation"])["auprc"].agg(["mean", "std", "count"]).reset_index()
    stats.to_csv(OUT / "rho_curve_summary.csv", index=False)
    return keep


def save_table(df: pd.DataFrame, stem: str, title: str, note: str = "") -> None:
    df.to_csv(CSV / f"{stem}.csv", index=False)
    lines = [f"# {title}", ""]
    if note:
        lines += [note, ""]
    lines += [df.to_markdown(index=False), ""]
    (TABLES / f"{stem}.md").write_text("\n".join(lines))


def build_paper_tables(heldout: pd.DataFrame, repaired_results: pd.DataFrame, repaired_validity: pd.DataFrame, label_df: pd.DataFrame, rho_df: pd.DataFrame) -> None:
    if not heldout.empty:
        rows = []
        for (typ, det), part in heldout.groupby(["heldout_typology", "detector"]):
            stat = part.groupby("augmentation")["auprc"].agg(["mean", "std", "count"])
            base = float(stat.loc["none", "mean"]) if "none" in stat.index else np.nan
            best_method = stat["mean"].idxmax()
            rows.append(
                {
                    "Held-out typology": typ,
                    "Detector": det,
                    "No aug.": metric_cell(stat.loc["none", "mean"], stat.loc["none", "std"]) if "none" in stat.index else "",
                    "Random feasible": metric_cell(stat.loc["random_feasible_v2", "mean"], stat.loc["random_feasible_v2", "std"]) if "random_feasible_v2" in stat.index else "",
                    "Hard projected": metric_cell(stat.loc["hard_projected_v2", "mean"], stat.loc["hard_projected_v2", "std"]) if "hard_projected_v2" in stat.index else "",
                    "Plausible hard": metric_cell(stat.loc["plausible_hard_projected_v2", "mean"], stat.loc["plausible_hard_projected_v2", "std"]) if "plausible_hard_projected_v2" in stat.index else "",
                    "Curriculum projected": metric_cell(stat.loc["curriculum_projected_v2", "mean"], stat.loc["curriculum_projected_v2", "std"]) if "curriculum_projected_v2" in stat.index else "",
                    "Typology projected": metric_cell(stat.loc["typology_projected_v2", "mean"], stat.loc["typology_projected_v2", "std"]) if "typology_projected_v2" in stat.index else "",
                    "Plausible typology": metric_cell(stat.loc["plausible_typology_projected_v2", "mean"], stat.loc["plausible_typology_projected_v2", "std"]) if "plausible_typology_projected_v2" in stat.index else "",
                    "Best method": label(best_method),
                    "Best Δ vs no aug.": f"{float(stat.loc[best_method, 'mean']) - base:+.3f}" if not pd.isna(base) else "",
                    "Seeds": int(stat["count"].max()),
                }
            )
        save_table(
            pd.DataFrame(rows),
            "table_11_v4_typology_strengthening",
            "V4 Typology Strengthening",
            "AUPRC mean ± std. Layering uses 10 seeds; structuring/integration use 5 seeds.",
        )

    if not repaired_results.empty and not repaired_validity.empty:
        perf = repaired_results.groupby("augmentation")["auprc"].mean()
        valid = repaired_validity.groupby("augmentation")[
            ["ledger_violation_rate", "categorical_fractionality_rate", "negative_feature_rate", "profile_drift", "detector_hardness"]
        ].mean()
        rows = []
        for method in [m for m in METHOD_ORDER if m in perf.index or m in valid.index]:
            rows.append(
                {
                    "Method": label(method),
                    "Mean AUPRC": metric_cell(perf.get(method, np.nan)),
                    "Ledger violation": pct(valid.loc[method, "ledger_violation_rate"]) if method in valid.index else "",
                    "Categorical artifact": pct(valid.loc[method, "categorical_fractionality_rate"]) if method in valid.index else "",
                    "Negative-feature artifact": pct(valid.loc[method, "negative_feature_rate"]) if method in valid.index else "",
                    "Profile drift": metric_cell(valid.loc[method, "profile_drift"], None, 2) if method in valid.index else "",
                    "Detector hardness": metric_cell(valid.loc[method, "detector_hardness"], None, 2) if method in valid.index else "",
                }
            )
        save_table(
            pd.DataFrame(rows),
            "table_12_repaired_standard_baselines",
            "Repaired Standard Baselines",
            "Tests whether simple post-hoc repair is enough to match ledger-conserving counterfactual generation.",
        )

    if not label_df.empty:
        rows = []
        for frac, part in label_df.groupby("label_fraction"):
            stat = part.groupby("augmentation")["auprc"].agg(["mean", "std"])
            base = float(stat.loc["none", "mean"]) if "none" in stat.index else np.nan
            row = {"Label fraction": f"{frac:g}", "No aug.": metric_cell(stat.loc["none", "mean"], stat.loc["none", "std"]) if "none" in stat.index else ""}
            for method in ["random_feasible_v2", "plausible_hard_projected_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]:
                if method in stat.index:
                    row[label(method)] = metric_cell(stat.loc[method, "mean"], stat.loc[method, "std"])
                    row[f"{label(method)} Δ"] = f"{float(stat.loc[method, 'mean']) - base:+.3f}" if not pd.isna(base) else ""
            rows.append(row)
        save_table(
            pd.DataFrame(rows).sort_values("Label fraction"),
            "table_14_label_scarcity_5seed",
            "Five-Seed Label Scarcity",
            "AUPRC aggregated across TransXion/AMLNet and LightGBM/XGBoost.",
        )

    if not rho_df.empty:
        stat = rho_df.groupby(["rho", "augmentation"])["auprc"].agg(["mean", "std", "count"]).reset_index()
        rows = [
            {"rho": r["rho"], "Method": label(r["augmentation"]), "AUPRC": metric_cell(r["mean"], r["std"]), "Runs": int(r["count"])}
            for _, r in stat.sort_values(["rho", "augmentation"]).iterrows()
        ]
        save_table(
            pd.DataFrame(rows),
            "table_15_rho_curve_extended",
            "Extended Augmentation Ratio Curve",
            "Combines v3/v4 rho sweeps to check sensitivity to augmentation ratio.",
        )


def plot_layering_ci(heldout: pd.DataFrame) -> None:
    if heldout.empty:
        return
    data = heldout[heldout["heldout_typology"].eq("layering")]
    if data.empty:
        return
    deltas = paired_deltas(data, "none")
    plot = deltas[(deltas["dataset"].ne("all")) & (deltas["augmentation"].isin(["random_feasible_v2", "hard_projected_v2", "plausible_hard_projected_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]))]
    plot = plot.sort_values(["detector", "mean_delta"])
    fig, ax = plt.subplots(figsize=(11, 5.2))
    x = np.arange(len(plot))
    ax.bar(x, plot["mean_delta"])
    lower = plot["mean_delta"] - plot["ci_low"]
    upper = plot["ci_high"] - plot["mean_delta"]
    ax.errorbar(x, plot["mean_delta"], yerr=[lower.fillna(0), upper.fillna(0)], fmt="none", color="black", capsize=3, linewidth=1)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{r.detector}\n{label(r.augmentation)}" for r in plot.itertuples()], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Delta AUPRC vs no augmentation")
    ax.set_title("Held-out layering: paired seed deltas")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_07_layering_10seed_delta_ci.png", dpi=220)
    fig.savefig(FIGURES / "fig_07_layering_10seed_delta_ci.pdf")
    plt.close(fig)


def plot_repaired_validity(validity: pd.DataFrame) -> None:
    if validity.empty:
        return
    methods = ["feature_noise_v2", "feature_noise_repaired_v2", "smote_v2", "smote_repaired_v2", "mixup_v2", "mixup_repaired_v2", "hard_projected_v2", "plausible_hard_projected_v2"]
    g = validity.groupby("augmentation")[["ledger_violation_rate", "categorical_fractionality_rate", "negative_feature_rate"]].mean().reindex(methods).dropna(how="all")
    if g.empty:
        return
    x = np.arange(len(g))
    w = 0.26
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.bar(x - w, 100 * g["ledger_violation_rate"].fillna(0), w, label="Ledger")
    ax.bar(x, 100 * g["categorical_fractionality_rate"].fillna(0), w, label="Categorical")
    ax.bar(x + w, 100 * g["negative_feature_rate"].fillna(0), w, label="Negative")
    ax.set_xticks(x)
    ax.set_xticklabels([label(m) for m in g.index], rotation=35, ha="right")
    ax.set_ylabel("Artifact rate (%)")
    ax.set_title("Post-hoc repair removes surface artifacts")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_08_repaired_standard_validity.png", dpi=220)
    fig.savefig(FIGURES / "fig_08_repaired_standard_validity.pdf")
    plt.close(fig)


def plot_label_scarcity(label_df: pd.DataFrame) -> None:
    if label_df.empty:
        return
    base = label_df[label_df["augmentation"].eq("none")][["dataset", "detector", "seed", "label_fraction", "auprc"]].rename(columns={"auprc": "none_auprc"})
    merged = label_df.merge(base, on=["dataset", "detector", "seed", "label_fraction"], how="inner")
    merged["delta"] = merged["auprc"] - merged["none_auprc"]
    methods = ["random_feasible_v2", "plausible_hard_projected_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]
    stat = merged[merged["augmentation"].isin(methods)].groupby(["label_fraction", "augmentation"])["delta"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8.7, 4.7))
    for method in methods:
        part = stat[stat["augmentation"].eq(method)].sort_values("label_fraction")
        ax.plot(part["label_fraction"], part["delta"], marker="o", label=label(method))
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xscale("log")
    ax.set_xlabel("Label fraction")
    ax.set_ylabel("Delta AUPRC vs no augmentation")
    ax.set_title("Five-seed label-scarcity deltas")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_09_label_scarcity_5seed_delta.png", dpi=220)
    fig.savefig(FIGURES / "fig_09_label_scarcity_5seed_delta.pdf")
    plt.close(fig)


def plot_rho(rho_df: pd.DataFrame) -> None:
    if rho_df.empty:
        return
    stat = rho_df.groupby(["rho", "augmentation"])["auprc"].mean().reset_index()
    methods = ["random_feasible_v2", "plausible_hard_projected_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    for method in methods:
        part = stat[stat["augmentation"].eq(method)].sort_values("rho")
        ax.plot(part["rho"], part["auprc"], marker="o", label=label(method))
    ax.set_xlabel("Augmentation ratio rho")
    ax.set_ylabel("AUPRC")
    ax.set_title("Augmentation-ratio sensitivity")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_10_rho_curve_extended.png", dpi=220)
    fig.savefig(FIGURES / "fig_10_rho_curve_extended.pdf")
    plt.close(fig)


def write_summary(heldout: pd.DataFrame, repaired_results: pd.DataFrame, repaired_validity: pd.DataFrame, label_df: pd.DataFrame, rho_df: pd.DataFrame) -> None:
    lines = ["# CIKM V4 Strengthening Summary", ""]
    if not heldout.empty:
        lines.append("## Held-Out Typology")
        for (typ, det), part in heldout.groupby(["heldout_typology", "detector"]):
            stat = part.groupby("augmentation")["auprc"].mean()
            base = stat.get("none", np.nan)
            best = stat.idxmax()
            delta = stat.loc[best] - base if not pd.isna(base) else np.nan
            lines.append(f"- {typ}/{det}: best={label(best)} AUPRC={stat.loc[best]:.3f}, delta vs no aug.={delta:+.3f}.")
        lines.append("")
    if not repaired_validity.empty:
        lines.append("## Repaired Standard Baselines")
        v = repaired_validity.groupby("augmentation")[["ledger_violation_rate", "categorical_fractionality_rate", "negative_feature_rate"]].mean()
        for method in ["feature_noise_repaired_v2", "smote_repaired_v2", "mixup_repaired_v2"]:
            if method in v.index:
                lines.append(
                    f"- {label(method)}: ledger={100*v.loc[method, 'ledger_violation_rate']:.1f}%, "
                    f"categorical={100*v.loc[method, 'categorical_fractionality_rate']:.1f}%, "
                    f"negative={100*v.loc[method, 'negative_feature_rate']:.1f}%."
                )
        lines.append("")
    if not label_df.empty:
        lines.append("## Label Scarcity")
        stat = label_df.groupby(["label_fraction", "augmentation"])["auprc"].mean()
        for frac in sorted(label_df["label_fraction"].unique()):
            part = stat.loc[frac]
            base = part.get("none", np.nan)
            best = part.idxmax()
            lines.append(f"- {frac:g} labels: best={label(best)} delta vs no aug.={part.loc[best] - base:+.3f}.")
        lines.append("")
    if not rho_df.empty:
        lines.append("## Rho Sensitivity")
        stat = rho_df.groupby(["rho", "augmentation"])["auprc"].mean()
        for rho in sorted(rho_df["rho"].unique()):
            part = stat.loc[rho]
            lines.append(f"- rho={rho:g}: best={label(part.idxmax())} AUPRC={part.max():.3f}.")
    (OUT / "strengthening_summary.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    ensure_dirs()
    heldout = summarize_heldout()
    repaired_results, repaired_validity = summarize_repaired()
    label_df = summarize_label_scarcity()
    rho_df = summarize_rho()
    build_paper_tables(heldout, repaired_results, repaired_validity, label_df, rho_df)
    plot_layering_ci(heldout)
    plot_repaired_validity(repaired_validity)
    plot_label_scarcity(label_df)
    plot_rho(rho_df)
    write_summary(heldout, repaired_results, repaired_validity, label_df, rho_df)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
