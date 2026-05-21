"""Generate paper-facing figures from completed CIKM result tables."""

from __future__ import annotations

from pathlib import Path
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "final_paper_package" / "tables" / "csv"
OUT = Path(__file__).resolve().parent / "figures"

PALETTE = {
    "Random feasible": "#7A869A",
    "Curriculum projected": "#2A9D8F",
    "Hard projected": "#E76F51",
    "Plausible hard": "#F4A261",
    "Typology projected": "#7B2CBF",
    "Plausible typology": "#B5179E",
    "positive": "#2A9D8F",
    "negative": "#C44536",
    "neutral": "#7A869A",
    "target": "#222222",
}


def parse_mean(cell: str) -> float:
    """Parse table cells of the form '0.932 ± 0.001' or '1.74e-04 ± ...'."""
    if pd.isna(cell):
        return np.nan
    match = re.match(r"\s*([+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?)", str(cell))
    if not match:
        return np.nan
    return float(match.group(1))


def save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def style_axes(ax: plt.Axes) -> None:
    ax.grid(axis="y", color="#E7E9EE", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#B8BEC9")
    ax.spines["bottom"].set_color("#B8BEC9")
    ax.tick_params(colors="#30343B", labelsize=8)
    ax.yaxis.label.set_color("#30343B")
    ax.xaxis.label.set_color("#30343B")


def plot_layering_deltas() -> None:
    df = pd.read_csv(CSV / "table_17_layering_bootstrap_significance.csv")
    df = df[df["Baseline"].eq("No aug.")].copy()
    order = [
        ("lightgbm", "Random feasible"),
        ("lightgbm", "Curriculum projected"),
        ("lightgbm", "Hard projected"),
        ("lightgbm", "Plausible typology"),
        ("lightgbm", "Plausible hard"),
        ("lightgbm", "Typology projected"),
        ("xgboost", "Random feasible"),
        ("xgboost", "Plausible typology"),
        ("xgboost", "Typology projected"),
        ("xgboost", "Hard projected"),
        ("xgboost", "Plausible hard"),
        ("xgboost", "Curriculum projected"),
    ]
    rows = []
    for det, method in order:
        row = df[(df["Detector"].eq(det)) & (df["Target"].eq(method))].iloc[0]
        rows.append(row)
    plot = pd.DataFrame(rows)
    x = np.arange(len(plot))
    colors = [PALETTE[m] for m in plot["Target"]]
    lower = plot["Mean ΔAUPRC"].to_numpy() - plot["Mean bootstrap low"].to_numpy()
    upper = plot["Mean bootstrap high"].to_numpy() - plot["Mean ΔAUPRC"].to_numpy()

    fig, ax = plt.subplots(figsize=(8.6, 3.0))
    ax.bar(x, plot["Mean ΔAUPRC"], color=colors, edgecolor="#1F2937", linewidth=0.4)
    ax.errorbar(
        x,
        plot["Mean ΔAUPRC"],
        yerr=np.vstack([lower, upper]),
        fmt="none",
        ecolor="#30343B",
        elinewidth=0.8,
        capsize=2,
        capthick=0.8,
    )
    labels = [
        f"{'LGB' if d == 'lightgbm' else 'XGB'}\n{m.replace(' projected', ' proj.').replace('Plausible ', 'Plaus. ')}"
        for d, m in zip(plot["Detector"], plot["Target"])
    ]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel("AUPRC gain vs no augmentation")
    ax.set_ylim(0, max(plot["Mean bootstrap high"]) + 0.004)
    ax.axhline(0, color="#30343B", linewidth=0.7)
    ax.set_title("Held-out layering: paired gains by detector and augmentation family", fontsize=10, pad=8)
    style_axes(ax)
    save(fig, "fig_07_layering_10seed_delta_ci")


def plot_scope_map() -> None:
    rows = [
        ("Main layering", "LGB", 0.016),
        ("Main layering", "XGB", 0.018),
        ("Few-shot layering", "LGB", 0.013),
        ("Few-shot layering", "XGB", 0.012),
        ("Earliest temporal bucket", "LGB", 0.083),
        ("Earliest temporal bucket", "XGB", 0.080),
        ("New counterparty pairs", "LGB", 0.023),
        ("New counterparty pairs", "XGB", 0.020),
        ("Structuring transfer", "LGB", 0.390 - 0.618),
        ("Structuring transfer", "XGB", 0.387 - 0.625),
        ("Graph layering", "GAT", 0.666 - 0.705),
        ("Graph layering", "SAGE", 0.339 - 0.355),
    ]
    df = pd.DataFrame(rows, columns=["Setting", "Detector", "Delta"])
    labels = [f"{s} ({d})" for s, d in zip(df["Setting"], df["Detector"])]
    colors = [PALETTE["positive"] if v >= 0 else PALETTE["negative"] for v in df["Delta"]]
    y = np.arange(len(df))

    fig, ax = plt.subplots(figsize=(6.7, 4.3))
    ax.barh(y, df["Delta"], color=colors, edgecolor="#1F2937", linewidth=0.35)
    ax.axvline(0, color="#30343B", linewidth=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("AUPRC change of best projected variant vs no augmentation")
    ax.set_title("Where feasibility-projected augmentation helps and where it does not", fontsize=10, pad=8)
    ax.grid(axis="x", color="#E7E9EE", linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#B8BEC9")
    ax.tick_params(colors="#30343B", labelsize=8)
    ax.xaxis.label.set_color("#30343B")
    save(fig, "fig_08_effect_scope_map")


def plot_amount_alignment() -> None:
    raw = pd.read_csv(CSV / "table_13_mechanism_analysis.csv")
    keep_methods = ["Random feasible", "Hard projected", "Typology projected"]
    raw = raw[raw["Method"].isin(keep_methods)].copy()
    raw["generated"] = raw["Synthetic log amount"].map(parse_mean)
    raw["target"] = raw["Held-out log amount"].map(parse_mean)
    typ_order = ["layering", "structuring", "integration"]
    method_offsets = {"Random feasible": -0.22, "Hard projected": 0.0, "Typology projected": 0.22}

    fig, ax = plt.subplots(figsize=(3.55, 2.35))
    base = np.arange(len(typ_order))
    for typ_idx, typ in enumerate(typ_order):
        part = raw[raw["Held-out typology"].eq(typ)]
        target = part["target"].iloc[0]
        ax.hlines(target, typ_idx - 0.34, typ_idx + 0.34, color=PALETTE["target"], linewidth=2.0)
        for _, row in part.iterrows():
            x = typ_idx + method_offsets[row["Method"]]
            ax.scatter(
                x,
                row["generated"],
                s=36,
                color=PALETTE[row["Method"]],
                edgecolor="#1F2937",
                linewidth=0.45,
                zorder=3,
            )
            ax.vlines(x, row["generated"], target, color="#CBD0D8", linewidth=0.8, zorder=1)

    ax.set_xticks(base)
    ax.set_xticklabels([t.capitalize() for t in typ_order])
    ax.set_ylabel("Log amount")
    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE[m],
                   markeredgecolor="#1F2937", markersize=4.5, label=m)
        for m in keep_methods
    ]
    handles.append(plt.Line2D([0], [0], color=PALETTE["target"], linewidth=2, label="Held-out target"))
    ax.legend(handles=handles, loc="lower left", ncol=2, fontsize=5.7, frameon=False)
    style_axes(ax)
    save(fig, "fig_09_amount_alignment")


def main() -> None:
    plot_layering_deltas()
    plot_scope_map()
    plot_amount_alignment()


if __name__ == "__main__":
    main()
