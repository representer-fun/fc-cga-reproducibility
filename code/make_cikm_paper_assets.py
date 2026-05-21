#!/usr/bin/env python3
"""Build paper-facing tables and figures from completed CIKM runs."""

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
APPENDIX = PAPER / "appendix_tables"

METHOD_ORDER = [
    "none",
    "feature_noise_v2",
    "feature_noise_repaired_v2",
    "smote_v2",
    "smote_repaired_v2",
    "mixup_v2",
    "mixup_repaired_v2",
    "edge_rewire_v2",
    "adv_no_projection_v2",
    "random_feasible_v2",
    "hard_projected_v2",
    "boundary_projected_v2",
    "plausible_hard_projected_v2",
    "curriculum_projected_v2",
    "typology_projected_v2",
    "plausible_typology_projected_v2",
]

METHOD_LABEL = {
    "none": "No aug.",
    "feature_noise_v2": "Feature noise",
    "feature_noise_repaired_v2": "Feature noise + repair",
    "smote_v2": "SMOTE",
    "smote_repaired_v2": "SMOTE + repair",
    "mixup_v2": "Mixup",
    "mixup_repaired_v2": "Mixup + repair",
    "edge_rewire_v2": "Edge rewire",
    "adv_no_projection_v2": "Adversarial unprojected",
    "random_feasible_v2": "Random feasible",
    "hard_projected_v2": "Hard projected",
    "boundary_projected_v2": "Boundary projected",
    "plausible_hard_projected_v2": "Plausible hard",
    "curriculum_projected_v2": "Curriculum projected",
    "typology_projected_v2": "Typology projected",
    "plausible_typology_projected_v2": "Plausible typology",
}

PLOT_METHODS = [
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
    "typology_projected_v2",
    "plausible_typology_projected_v2",
]

PROJECTED_METHODS = [
    "random_feasible_v2",
    "hard_projected_v2",
    "plausible_hard_projected_v2",
    "curriculum_projected_v2",
    "typology_projected_v2",
    "plausible_typology_projected_v2",
]


def ensure_dirs() -> None:
    for path in [PAPER, TABLES, CSV, FIGURES, APPENDIX]:
        path.mkdir(parents=True, exist_ok=True)


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def read_preferred(*paths: Path) -> pd.DataFrame:
    for path in paths:
        if path.exists():
            return read(path)
    raise FileNotFoundError(paths[0])


def concat_existing(*paths: Path) -> pd.DataFrame:
    frames = [read(path) for path in paths if path.exists()]
    if not frames:
        raise FileNotFoundError(paths[0])
    out = pd.concat(frames, ignore_index=True)
    return out.drop_duplicates()


def preferred_run(results: pd.DataFrame, preferred: str, fallback: str) -> str:
    return preferred if preferred in set(results["run_name"]) else fallback


def label(method: str) -> str:
    return METHOD_LABEL.get(method, method)


def metric_cell(mean: float, std: float | None = None, digits: int = 3) -> str:
    if pd.isna(mean):
        return ""
    if abs(mean) < 0.001 and mean != 0:
        base = f"{mean:.2e}"
    else:
        base = f"{mean:.{digits}f}"
    if std is None or pd.isna(std):
        return base
    if abs(std) < 0.001 and std != 0:
        spread = f"{std:.1e}"
    else:
        spread = f"{std:.{digits}f}"
    return f"{base} ± {spread}"


def pct(x: float, digits: int = 1) -> str:
    if pd.isna(x):
        return ""
    return f"{100 * x:.{digits}f}%"


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).replace("\n", " ").strip() for c in out.columns]
    return out


def save_table(df: pd.DataFrame, stem: str, title: str, note: str = "") -> None:
    df = flatten_columns(df)
    df.to_csv(CSV / f"{stem}.csv", index=False)
    lines = [f"# {title}", ""]
    if note:
        lines += [note, ""]
    lines += [df.to_markdown(index=False), ""]
    (TABLES / f"{stem}.md").write_text("\n".join(lines))


def save_fig(fig, stem: str) -> None:
    fig.tight_layout()
    fig.savefig(FIGURES / f"{stem}.png", dpi=220)
    fig.savefig(FIGURES / f"{stem}.pdf")
    plt.close(fig)


def grouped_stats(df: pd.DataFrame, group_cols: list[str], metric: str = "auprc") -> pd.DataFrame:
    return df.groupby(group_cols)[metric].agg(["mean", "std", "count"]).reset_index()


def method_stats(df: pd.DataFrame, run: str, dataset: str, detector: str, heldout: str = "") -> dict[str, tuple[float, float]]:
    sub = df[
        df["run_name"].eq(run)
        & df["dataset"].eq(dataset)
        & df["detector"].eq(detector)
        & df["heldout_typology"].fillna("").eq(heldout)
    ]
    stats = grouped_stats(sub, ["augmentation"])
    return {r["augmentation"]: (float(r["mean"]), float(r["std"]) if not pd.isna(r["std"]) else np.nan) for _, r in stats.iterrows()}


def make_main_paper_table(results: pd.DataFrame) -> pd.DataFrame:
    full_run = preferred_run(results, "cikm_v4_repaired_audit", "cikm_v3_validity_audit")
    layering_run = preferred_run(results, "cikm_v4_heldout_layering_10seed", "cikm_v3_heldout_layering")
    structuring_run = preferred_run(results, "cikm_v4_heldout_structuring_5seed", "cikm_v3_heldout_structuring")
    integration_run = preferred_run(results, "cikm_v4_heldout_integration_5seed", "cikm_v3_heldout_integration")
    rows_spec = [
        ("Full data", "TransXion", "lightgbm", full_run, "transxion", "lightgbm", ""),
        ("Full data", "TransXion", "xgboost", full_run, "transxion", "xgboost", ""),
        ("Full data", "AMLNet", "lightgbm", full_run, "amlnet", "lightgbm", ""),
        ("Full data", "AMLNet", "xgboost", full_run, "amlnet", "xgboost", ""),
        ("Held-out layering", "AMLNet", "lightgbm", layering_run, "amlnet", "lightgbm", "layering"),
        ("Held-out layering", "AMLNet", "xgboost", layering_run, "amlnet", "xgboost", "layering"),
        ("Held-out structuring", "AMLNet", "lightgbm", structuring_run, "amlnet", "lightgbm", "structuring"),
        ("Held-out structuring", "AMLNet", "xgboost", structuring_run, "amlnet", "xgboost", "structuring"),
        ("Held-out integration", "AMLNet", "lightgbm", integration_run, "amlnet", "lightgbm", "integration"),
        ("Held-out integration", "AMLNet", "xgboost", integration_run, "amlnet", "xgboost", "integration"),
    ]
    cols = [
        "none",
        "feature_noise_v2",
        "smote_v2",
        "mixup_v2",
        "random_feasible_v2",
        "hard_projected_v2",
        "plausible_hard_projected_v2",
        "typology_projected_v2",
        "plausible_typology_projected_v2",
    ]
    rows = []
    for scenario, dataset_label, detector_label, run, ds, det, heldout in rows_spec:
        stats = method_stats(results, run, ds, det, heldout)
        means = {m: stats[m][0] for m in cols if m in stats}
        best = max(means.values()) if means else np.nan
        row = {"Scenario": scenario, "Dataset": dataset_label, "Detector": detector_label}
        for method in cols:
            if method not in stats:
                row[label(method)] = ""
                continue
            mean, std = stats[method]
            cell = metric_cell(mean, std)
            if not pd.isna(best) and abs(mean - best) < 1e-12:
                cell = f"**{cell}**"
            row[label(method)] = cell
        if "none" in stats:
            valid_methods = [m for m in PROJECTED_METHODS if m in stats]
            if valid_methods:
                best_valid = max((stats[m][0], m) for m in valid_methods)
                row["Best valid method"] = label(best_valid[1])
                row["Best valid ΔAUPRC vs no aug."] = f"{best_valid[0] - stats['none'][0]:+.3f}"
        rows.append(row)
    return pd.DataFrame(rows)


def make_full_data_table(results: pd.DataFrame) -> pd.DataFrame:
    run = preferred_run(results, "cikm_v4_repaired_audit", "cikm_v3_validity_audit")
    methods = [m for m in METHOD_ORDER if m in set(results[results["run_name"].eq(run)]["augmentation"])]
    rows = []
    for (dataset, detector), part in results[results["run_name"].eq(run)].groupby(["dataset", "detector"]):
        stats = grouped_stats(part, ["augmentation"])
        stat_map = {r["augmentation"]: (r["mean"], r["std"]) for _, r in stats.iterrows()}
        row = {"Dataset": dataset, "Detector": detector}
        best = max(v[0] for v in stat_map.values())
        for method in methods:
            if method in stat_map:
                cell = metric_cell(stat_map[method][0], stat_map[method][1])
                if abs(stat_map[method][0] - best) < 1e-12:
                    cell = f"**{cell}**"
                row[label(method)] = cell
        rows.append(row)
    return pd.DataFrame(rows)


def make_validity_table(validity: pd.DataFrame) -> pd.DataFrame:
    run = preferred_run(validity, "cikm_v4_repaired_audit", "cikm_v3_validity_audit")
    v3 = validity[validity["run_name"].eq(run)].copy()
    v2_extra = validity[
        validity["run_name"].eq("cikm_v2_main")
        & validity["augmentation"].isin(["adv_no_projection_v2", "boundary_projected_v2"])
    ].copy()
    keep = pd.concat([v3, v2_extra], ignore_index=True)
    cols = [
        "ledger_violation_rate",
        "mean_flow_residual",
        "detector_hardness",
        "acceptance_rate",
        "profile_drift",
        "categorical_fractionality_rate",
        "negative_feature_rate",
    ]
    g = keep.groupby("augmentation")[cols].mean().reset_index()
    g["order"] = g["augmentation"].map({m: i for i, m in enumerate(METHOD_ORDER)}).fillna(999)
    g = g.sort_values("order")
    rows = []
    for _, r in g.iterrows():
        rows.append(
            {
                "Method": label(r["augmentation"]),
                "Ledger violation": pct(r["ledger_violation_rate"]),
                "Mean flow residual": metric_cell(r["mean_flow_residual"], None, 3),
                "Categorical artifact": pct(r["categorical_fractionality_rate"]),
                "Negative-feature artifact": pct(r["negative_feature_rate"]),
                "Detector hardness": metric_cell(r["detector_hardness"], None, 2),
                "Profile drift": metric_cell(r["profile_drift"], None, 2),
                "Acceptance": pct(r["acceptance_rate"]),
            }
        )
    return pd.DataFrame(rows)


def make_standard_artifact_table(results: pd.DataFrame, validity: pd.DataFrame) -> pd.DataFrame:
    run = preferred_run(results, "cikm_v4_repaired_audit", "cikm_v3_validity_audit")
    perf = results[results["run_name"].eq(run)].groupby("augmentation")["auprc"].mean()
    valid = validity[validity["run_name"].eq(run)].groupby("augmentation")[
        ["ledger_violation_rate", "categorical_fractionality_rate", "negative_feature_rate", "profile_drift", "detector_hardness"]
    ].mean()
    methods = [
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
    ]
    rows = []
    for m in methods:
        rows.append(
            {
                "Method": label(m),
                "Mean AUPRC": metric_cell(perf.get(m, np.nan), None, 3),
                "Ledger violation": pct(valid.loc[m, "ledger_violation_rate"]) if m in valid.index else "",
                "Categorical artifact": pct(valid.loc[m, "categorical_fractionality_rate"]) if m in valid.index else "",
                "Negative-feature artifact": pct(valid.loc[m, "negative_feature_rate"]) if m in valid.index else "",
                "Profile drift": metric_cell(valid.loc[m, "profile_drift"], None, 2) if m in valid.index else "",
                "Detector hardness": metric_cell(valid.loc[m, "detector_hardness"], None, 2) if m in valid.index else "",
            }
        )
    return pd.DataFrame(rows)


def make_heldout_table(results: pd.DataFrame) -> pd.DataFrame:
    run_names = [
        preferred_run(results, "cikm_v4_heldout_layering_10seed", "cikm_v3_heldout_layering"),
        preferred_run(results, "cikm_v4_heldout_structuring_5seed", "cikm_v3_heldout_structuring"),
        preferred_run(results, "cikm_v4_heldout_integration_5seed", "cikm_v3_heldout_integration"),
    ]
    held = results[results["run_name"].isin(run_names)]
    methods = ["none", "random_feasible_v2", "hard_projected_v2", "plausible_hard_projected_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]
    rows = []
    for (typology, detector), part in held.groupby(["heldout_typology", "detector"]):
        stats = grouped_stats(part, ["augmentation"])
        stat_map = {r["augmentation"]: (r["mean"], r["std"]) for _, r in stats.iterrows()}
        row = {"Held-out typology": typology, "Detector": detector}
        for method in methods:
            row[label(method)] = metric_cell(*stat_map[method]) if method in stat_map else ""
        if "none" in stat_map:
            valid = [m for m in methods if m != "none" and m in stat_map]
            best_valid = max((stat_map[m][0], m) for m in valid)
            row["Best valid method"] = label(best_valid[1])
            row["Best valid ΔAUPRC"] = f"{best_valid[0] - stat_map['none'][0]:+.3f}"
        rows.append(row)
    return pd.DataFrame(rows)


def make_label_scarcity_table(results: pd.DataFrame) -> pd.DataFrame:
    run = preferred_run(results, "cikm_v4_label_scarcity_5seed", "cikm_v3_label_scarcity")
    ls = results[results["run_name"].eq(run)]
    methods = ["none", "random_feasible_v2", "hard_projected_v2", "plausible_hard_projected_v2", "curriculum_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]
    rows = []
    for frac, part in ls.groupby("label_fraction"):
        stats = grouped_stats(part, ["augmentation"])
        stat_map = {r["augmentation"]: (r["mean"], r["std"]) for _, r in stats.iterrows()}
        row = {"Label fraction": f"{frac:g}"}
        for method in methods:
            row[label(method)] = metric_cell(*stat_map[method]) if method in stat_map else ""
        if "none" in stat_map:
            valid = [m for m in methods if m != "none" and m in stat_map]
            best_valid = max((stat_map[m][0], m) for m in valid)
            row["Best valid method"] = label(best_valid[1])
            row["Best valid ΔAUPRC"] = f"{best_valid[0] - stat_map['none'][0]:+.3f}"
        rows.append(row)
    return pd.DataFrame(rows).sort_values("Label fraction")


def make_external_table(all_results: pd.DataFrame) -> pd.DataFrame:
    ext = all_results[all_results["run_name"].eq("cikm_v2_external")]
    methods = ["none", "random_feasible_v2", "hard_projected_v2", "boundary_projected_v2"]
    rows = []
    for detector, part in ext.groupby("detector"):
        stats = grouped_stats(part, ["augmentation"])
        stat_map = {r["augmentation"]: (r["mean"], r["std"]) for _, r in stats.iterrows()}
        row = {"Dataset": "Elliptic++", "Detector": detector}
        for method in methods:
            row[label(method)] = metric_cell(*stat_map[method]) if method in stat_map else ""
        rows.append(row)
    return pd.DataFrame(rows)


def make_graph_table(all_results: pd.DataFrame) -> pd.DataFrame:
    graph = all_results[all_results["run_name"].eq("cikm_v2_graph")]
    methods = ["none", "random_feasible_v2", "adv_no_projection_v2", "hard_projected_v2", "boundary_projected_v2"]
    rows = []
    for dataset, part in graph.groupby("dataset"):
        stats = grouped_stats(part, ["augmentation"])
        stat_map = {r["augmentation"]: (r["mean"], r["std"]) for _, r in stats.iterrows()}
        row = {"Dataset": dataset, "Detector": "pyg_sage"}
        for method in methods:
            row[label(method)] = metric_cell(*stat_map[method]) if method in stat_map else ""
        rows.append(row)
    return pd.DataFrame(rows)


def make_ablation_table(all_results: pd.DataFrame) -> pd.DataFrame:
    ab = all_results[all_results["run_name"].eq("cikm_v2_ablations")]
    stats = grouped_stats(ab, ["dataset", "detector", "augmentation"])
    rows = []
    for (dataset, detector), part in stats.groupby(["dataset", "detector"]):
        row = {"Dataset": dataset, "Detector": detector}
        best = part["mean"].max()
        for _, r in part.sort_values("augmentation").iterrows():
            cell = metric_cell(r["mean"], r["std"])
            if abs(r["mean"] - best) < 1e-12:
                cell = f"**{cell}**"
            row[label(r["augmentation"])] = cell
        rows.append(row)
    return pd.DataFrame(rows)


def make_rho_table(results: pd.DataFrame, all_results: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    pieces.append(all_results[all_results["run_name"].isin(["cikm_v2_rho", "cikm_v2_rho2"])])
    pieces.append(all_results[all_results["run_name"].eq("cikm_v2_main") & all_results["augmentation"].isin(["random_feasible_v2", "hard_projected_v2", "boundary_projected_v2"])])
    pieces.append(results[results["run_name"].eq("cikm_v3_rho_plausible")])
    pieces.append(results[results["run_name"].isin(["cikm_v4_rho_0p50", "cikm_v4_rho_1p25"])])
    rho = pd.concat(pieces, ignore_index=True)
    stats = grouped_stats(rho, ["rho", "augmentation"])
    rows = []
    for _, r in stats.sort_values(["rho", "augmentation"]).iterrows():
        rows.append({"rho": r["rho"], "Method": label(r["augmentation"]), "AUPRC": metric_cell(r["mean"], r["std"]), "Runs": int(r["count"])})
    return pd.DataFrame(rows)


def make_claims_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Claim": "Unconstrained/adversarial counterfactuals are financially invalid.",
                "Evidence table": "table_01_validity_audit",
                "Key result": "Adversarial unprojected has about 97% ledger violation; feature noise has 58% ledger violation plus categorical/negative-feature artifacts.",
                "Paper role": "Motivation and validity audit.",
            },
            {
                "Claim": "Projection enforces ledger conservation.",
                "Evidence table": "table_01_validity_audit",
                "Key result": "Projected variants have 0% ledger violation and zero flow residual.",
                "Paper role": "Method validity.",
            },
            {
                "Claim": "Plausibility gating reduces behavioral drift.",
                "Evidence table": "table_01_validity_audit",
                "Key result": "Plausible variants reduce profile drift relative to hard projected variants while keeping ledger validity.",
                "Paper role": "Novel v3 method contribution.",
            },
            {
                "Claim": "Valid hard examples help under layering typology shift.",
                "Evidence table": "table_03_heldout_typology",
                "Key result": "Held-out layering improves from about 0.927-0.931 AUPRC to about 0.944-0.948 across LightGBM/XGBoost.",
                "Paper role": "Main positive predictive result.",
            },
            {
                "Claim": "Validity alone does not guarantee better prediction.",
                "Evidence table": "table_03_heldout_typology",
                "Key result": "Structuring favors no augmentation or random feasible; projected hard variants hurt.",
                "Paper role": "Honest limitation and tradeoff framing.",
            },
        ]
    )


def convert_appendix_tables() -> None:
    index_rows = []
    for result_dir in sorted(p for p in RESULTS.iterdir() if p.is_dir()):
        for csv_name in ["main_table.csv", "label_scarcity_table.csv", "counterfactual_validity_table.csv"]:
            path = result_dir / csv_name
            if not path.exists():
                continue
            try:
                df = pd.read_csv(path)
            except Exception:
                continue
            stem = f"{result_dir.name}__{csv_name.replace('.csv', '')}"
            md_path = APPENDIX / f"{stem}.md"
            csv_path = APPENDIX / f"{stem}.csv"
            df = flatten_columns(df)
            df.to_csv(csv_path, index=False)
            md_path.write_text(f"# {result_dir.name}: {csv_name}\n\n{df.to_markdown(index=False)}\n")
            index_rows.append({"Run": result_dir.name, "Table": csv_name, "Markdown": f"{stem}.md", "CSV": f"{stem}.csv"})
    idx = pd.DataFrame(index_rows)
    idx.to_csv(APPENDIX / "index.csv", index=False)
    (APPENDIX / "index.md").write_text("# Appendix Table Index\n\n" + idx.to_markdown(index=False) + "\n")


def plot_validity_bars(validity: pd.DataFrame) -> None:
    run = preferred_run(validity, "cikm_v4_repaired_audit", "cikm_v3_validity_audit")
    v3 = validity[validity["run_name"].eq(run)]
    adv = validity[validity["run_name"].eq("cikm_v2_main") & validity["augmentation"].eq("adv_no_projection_v2")]
    data = pd.concat([v3, adv], ignore_index=True)
    order = [
        m
        for m in [
            "adv_no_projection_v2",
            "feature_noise_v2",
            "feature_noise_repaired_v2",
            "smote_v2",
            "smote_repaired_v2",
            "mixup_v2",
            "mixup_repaired_v2",
            "random_feasible_v2",
            "hard_projected_v2",
            "plausible_hard_projected_v2",
            "typology_projected_v2",
        ]
        if m in set(data["augmentation"])
    ]
    g = data.groupby("augmentation")[["ledger_violation_rate", "categorical_fractionality_rate", "negative_feature_rate"]].mean().reindex(order)
    x = np.arange(len(g))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.bar(x - width, 100 * g["ledger_violation_rate"].fillna(0), width, label="Ledger violation")
    ax.bar(x, 100 * g["categorical_fractionality_rate"].fillna(0), width, label="Categorical artifact")
    ax.bar(x + width, 100 * g["negative_feature_rate"].fillna(0), width, label="Negative feature")
    ax.set_xticks(x)
    ax.set_xticklabels([label(m) for m in g.index], rotation=35, ha="right")
    ax.set_ylabel("Rate (%)")
    ax.set_title("Validity and representation artifacts by augmentation")
    ax.legend(frameon=False)
    save_fig(fig, "fig_01_validity_artifact_bars")


def plot_full_data(results: pd.DataFrame) -> None:
    run_name = preferred_run(results, "cikm_v4_repaired_audit", "cikm_v3_validity_audit")
    run = results[results["run_name"].eq(run_name)]
    methods = ["none", "feature_noise_v2", "feature_noise_repaired_v2", "smote_v2", "smote_repaired_v2", "mixup_v2", "mixup_repaired_v2", "random_feasible_v2", "hard_projected_v2", "plausible_hard_projected_v2", "typology_projected_v2"]
    stats = grouped_stats(run[run["augmentation"].isin(methods)], ["dataset", "detector", "augmentation"])
    facets = list(stats.groupby(["dataset", "detector"]).groups)
    fig, axes = plt.subplots(2, 2, figsize=(13, 7), sharey=False)
    for ax, key in zip(axes.ravel(), facets):
        part = stats[(stats["dataset"].eq(key[0])) & (stats["detector"].eq(key[1]))].set_index("augmentation").reindex(methods)
        ax.bar(np.arange(len(methods)), part["mean"], yerr=part["std"].fillna(0), capsize=2)
        ax.set_title(f"{key[0]} / {key[1]}")
        ax.set_xticks(np.arange(len(methods)))
        ax.set_xticklabels([label(m) for m in methods], rotation=40, ha="right", fontsize=8)
        ax.set_ylabel("AUPRC")
    save_fig(fig, "fig_02_full_data_auprc")


def plot_heldout(results: pd.DataFrame) -> None:
    run_names = [
        preferred_run(results, "cikm_v4_heldout_layering_10seed", "cikm_v3_heldout_layering"),
        preferred_run(results, "cikm_v4_heldout_structuring_5seed", "cikm_v3_heldout_structuring"),
        preferred_run(results, "cikm_v4_heldout_integration_5seed", "cikm_v3_heldout_integration"),
    ]
    held = results[results["run_name"].isin(run_names)]
    methods = ["none", "random_feasible_v2", "hard_projected_v2", "plausible_hard_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]
    stats = grouped_stats(held[held["augmentation"].isin(methods)], ["heldout_typology", "detector", "augmentation"])
    for typ in ["layering", "structuring", "integration"]:
        fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=False)
        for ax, det in zip(axes, ["lightgbm", "xgboost"]):
            part = stats[(stats["heldout_typology"].eq(typ)) & (stats["detector"].eq(det))].set_index("augmentation").reindex(methods)
            ax.bar(np.arange(len(methods)), part["mean"], yerr=part["std"].fillna(0), capsize=2)
            ax.set_title(f"{typ} / {det}")
            ax.set_xticks(np.arange(len(methods)))
            ax.set_xticklabels([label(m) for m in methods], rotation=35, ha="right", fontsize=8)
            ax.set_ylabel("AUPRC")
        save_fig(fig, f"fig_03_heldout_{typ}_auprc")


def plot_label_scarcity(results: pd.DataFrame) -> None:
    run = preferred_run(results, "cikm_v4_label_scarcity_5seed", "cikm_v3_label_scarcity")
    ls = results[results["run_name"].eq(run)]
    base = ls[ls["augmentation"].eq("none")][["dataset", "detector", "seed", "label_fraction", "auprc"]].rename(columns={"auprc": "none_auprc"})
    merged = ls.merge(base, on=["dataset", "detector", "seed", "label_fraction"])
    merged["delta"] = merged["auprc"] - merged["none_auprc"]
    methods = ["random_feasible_v2", "hard_projected_v2", "plausible_hard_projected_v2", "curriculum_projected_v2", "plausible_typology_projected_v2"]
    stats = merged[merged["augmentation"].isin(methods)].groupby(["label_fraction", "augmentation"])["delta"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    for method in methods:
        part = stats[stats["augmentation"].eq(method)].sort_values("label_fraction")
        ax.plot(part["label_fraction"], part["delta"], marker="o", label=label(method))
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xscale("log")
    ax.set_xlabel("Label fraction")
    ax.set_ylabel("Delta AUPRC vs no augmentation")
    ax.set_title("Label scarcity: augmentation gains are conditional")
    ax.legend(frameon=False, fontsize=8)
    save_fig(fig, "fig_04_label_scarcity_delta")


def plot_tradeoff(results: pd.DataFrame, validity: pd.DataFrame) -> None:
    run = preferred_run(results, "cikm_v4_repaired_audit", "cikm_v3_validity_audit")
    perf = results[results["run_name"].eq(run)].groupby("augmentation")["auprc"].mean()
    valid = validity[validity["run_name"].eq(run)].groupby("augmentation")[["detector_hardness", "profile_drift", "ledger_violation_rate"]].mean()
    df = valid.join(perf.rename("auprc")).dropna(subset=["detector_hardness", "profile_drift"])
    df = df.reindex([m for m in METHOD_ORDER if m in df.index])
    fig, ax = plt.subplots(figsize=(8, 5.5))
    sizes = 80 + 500 * df["ledger_violation_rate"].fillna(0)
    ax.scatter(df["profile_drift"], df["detector_hardness"], s=sizes, alpha=0.8)
    for method, r in df.iterrows():
        ax.annotate(label(method), (r["profile_drift"], r["detector_hardness"]), fontsize=8, xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("Profile drift")
    ax.set_ylabel("Detector hardness")
    ax.set_title("Hardness-plausibility-validity tradeoff")
    save_fig(fig, "fig_05_hardness_profile_tradeoff")


def plot_layering_delta(results: pd.DataFrame) -> None:
    run = preferred_run(results, "cikm_v4_heldout_layering_10seed", "cikm_v3_heldout_layering")
    held = results[results["run_name"].eq(run)]
    base = held[held["augmentation"].eq("none")][["detector", "seed", "auprc"]].rename(columns={"auprc": "none_auprc"})
    merged = held.merge(base, on=["detector", "seed"])
    methods = ["random_feasible_v2", "hard_projected_v2", "plausible_hard_projected_v2", "typology_projected_v2", "plausible_typology_projected_v2"]
    stats = merged[merged["augmentation"].isin(methods)].groupby(["detector", "augmentation"])[["auprc", "none_auprc"]].mean().reset_index()
    stats["delta"] = stats["auprc"] - stats["none_auprc"]
    fig, ax = plt.subplots(figsize=(9, 4.7))
    labels = [f"{d}\n{label(m)}" for d, m in zip(stats["detector"], stats["augmentation"])]
    ax.bar(np.arange(len(stats)), stats["delta"])
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xticks(np.arange(len(stats)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Delta AUPRC vs no augmentation")
    ax.set_title("Held-out layering: valid counterfactuals improve transfer")
    save_fig(fig, "fig_06_layering_delta_vs_none")


def make_figures(results: pd.DataFrame, validity: pd.DataFrame) -> None:
    plot_validity_bars(validity)
    plot_full_data(results)
    plot_heldout(results)
    plot_label_scarcity(results)
    plot_tradeoff(results, validity)
    plot_layering_delta(results)


def write_readme() -> None:
    lines = [
        "# CIKM Paper Assets",
        "",
        "This folder contains paper-facing tables and figures generated from completed `flow_fraud` experiments.",
        "",
        "## Main Tables",
        "",
        "- `tables/main_paper_results_table.md`: primary result table for the paper body.",
        "- `tables/table_01_validity_audit.md`: validity and artifact audit.",
        "- `tables/table_02_standard_augmentation_artifact_audit.md`: standard augmentation artifact comparison.",
        "- `tables/table_03_heldout_typology.md`: typology-transfer table.",
        "- `tables/table_04_label_scarcity.md`: label-scarcity table.",
        "- `tables/table_05_full_data_detection.md`: full-data detection table.",
        "- `tables/table_06_external_ellipticpp.md`: external Elliptic++ robustness.",
        "- `tables/table_07_graph_models.md`: PyG GraphSAGE evidence.",
        "- `tables/table_08_ablation_results.md`: v2 ablation summary.",
        "- `tables/table_09_rho_sensitivity.md`: augmentation-ratio sensitivity.",
        "- `tables/table_10_claims_to_evidence.md`: how to map claims to tables.",
        "- `tables/table_11_v4_typology_strengthening.md`: extended seed typology-transfer strengthening when v4 is complete.",
        "- `tables/table_12_repaired_standard_baselines.md`: repaired standard-baseline audit when v4 is complete.",
        "- `tables/table_13_mechanism_analysis.md`: generated-example mechanism diagnostics when v4 is complete.",
        "- `tables/table_14_label_scarcity_5seed.md`: five-seed label-scarcity strengthening when v4 is complete.",
        "- `tables/table_15_rho_curve_extended.md`: extended augmentation-ratio curve when v4 is complete.",
        "",
        "Every curated Markdown table has a matching CSV under `tables/csv/`.",
        "",
        "## Figures",
        "",
        "- `figures/fig_01_validity_artifact_bars.*`: validity/artifact audit.",
        "- `figures/fig_02_full_data_auprc.*`: full-data AUPRC comparison.",
        "- `figures/fig_03_heldout_layering_auprc.*`: held-out layering comparison.",
        "- `figures/fig_03_heldout_structuring_auprc.*`: held-out structuring comparison.",
        "- `figures/fig_03_heldout_integration_auprc.*`: held-out integration comparison.",
        "- `figures/fig_04_label_scarcity_delta.*`: label scarcity deltas.",
        "- `figures/fig_05_hardness_profile_tradeoff.*`: hardness/profile-drift tradeoff.",
        "- `figures/fig_06_layering_delta_vs_none.*`: layering deltas versus no augmentation.",
        "- `figures/fig_07_layering_10seed_delta_ci.*`: paired seed deltas for 10-seed layering when v4 is complete.",
        "- `figures/fig_08_repaired_standard_validity.*`: repair audit artifacts when v4 is complete.",
        "- `figures/fig_09_label_scarcity_5seed_delta.*`: five-seed low-label deltas when v4 is complete.",
        "- `figures/fig_10_rho_curve_extended.*`: extended rho curve when v4 is complete.",
        "- `figures/fig_11_mechanism_distance_*.{png,pdf}`: mechanism support-coverage distances when v4 is complete.",
        "- `figures/fig_12_mechanism_hardness_profile.*`: mechanism hardness/profile tradeoff when v4 is complete.",
        "",
        "## Appendix Tables",
        "",
        "`appendix_tables/` contains Markdown conversions of every run-level `main_table.csv`, `label_scarcity_table.csv`, and `counterfactual_validity_table.csv` found under `results/`.",
        "",
        "## Paper Framing",
        "",
        "The results support a CIKM full-paper framing around financial validity and validity-performance tradeoffs, not a universal SOTA-performance claim.",
        "The strongest positive predictive result is held-out layering; the strongest methodological result is zero ledger violation for projected methods while standard/noisy augmentations show invalid transaction artifacts.",
        "",
    ]
    (PAPER / "README.md").write_text("\n".join(lines))


def main() -> None:
    ensure_dirs()
    v3_results = read_preferred(
        RESULTS / "cikm_v4_synthesis" / "all_combined_results.csv",
        RESULTS / "cikm_v3_synthesis" / "all_combined_results.csv",
    )
    v3_validity = read_preferred(
        RESULTS / "cikm_v4_synthesis" / "all_combined_validity.csv",
        RESULTS / "cikm_v3_synthesis" / "all_combined_validity.csv",
    )
    all_results = concat_existing(
        RESULTS / "cikm_v4_synthesis" / "all_combined_results.csv",
        RESULTS / "cikm_synthesis" / "all_combined_results.csv",
    )

    tables = [
        ("main_paper_results_table", "Main Paper Results Table", make_main_paper_table(v3_results), "AUPRC mean ± std across seeds. Bold indicates best method in each row."),
        ("table_01_validity_audit", "Validity Audit", make_validity_table(v3_validity), "Rates are averaged over the validity-audit grid; adversarial unprojected uses the completed v2 main grid."),
        ("table_02_standard_augmentation_artifact_audit", "Standard Augmentation Artifact Audit", make_standard_artifact_table(v3_results, v3_validity), "Shows why predictive-only evaluation can reward invalid or representationally broken examples."),
        ("table_03_heldout_typology", "Held-Out Typology Transfer", make_heldout_table(v3_results), "AUPRC mean ± std across seeds on AMLNet held-out typologies."),
        ("table_04_label_scarcity", "Label Scarcity", make_label_scarcity_table(v3_results), "AUPRC aggregated across TransXion/AMLNet and LightGBM/XGBoost."),
        ("table_05_full_data_detection", "Full-Data Detection", make_full_data_table(v3_results), "AUPRC mean ± std on full-data TransXion and AMLNet."),
        ("table_06_external_ellipticpp", "External Elliptic++ Robustness", make_external_table(all_results), "External predictive robustness on Elliptic++ from the completed v2 suite."),
        ("table_07_graph_models", "Graph Model Evidence", make_graph_table(all_results), "PyG GraphSAGE evidence from the completed v2 graph suite."),
        ("table_08_ablation_results", "Ablation Results", make_ablation_table(all_results), "AUPRC mean ± std for v2 ablation variants."),
        ("table_09_rho_sensitivity", "Augmentation Ratio Sensitivity", make_rho_table(v3_results, all_results), "AUPRC mean ± std across augmentation ratio sweeps."),
        ("table_10_claims_to_evidence", "Claims To Evidence Map", make_claims_table(), "Use this as the outline bridge from results to paper claims."),
    ]
    for stem, title, df, note in tables:
        save_table(df, stem, title, note)

    make_figures(v3_results, v3_validity)
    convert_appendix_tables()
    write_readme()
    print(f"Wrote paper assets to {PAPER}")


if __name__ == "__main__":
    main()
