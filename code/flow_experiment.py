#!/usr/bin/env python3
"""Ledger-conserving counterfactual augmentation experiments.

This is a CPU-friendly implementation of the experimental plan in flow_plan.md.
It keeps temporal splits leakage-aware, generates several augmentation families,
measures counterfactual validity, and trains tabular plus lightweight graph
baselines without requiring accelerator access.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    matthews_corrcoef,
    precision_score,
    roc_auc_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=FutureWarning)


ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "results"
RUNS = ROOT / "runs"
EXTERNAL = ROOT / "external"


LOW_CARD_LIMIT = 64
EPS = 1e-9
HISTORY_FEATURES = [
    "sender_tx_count",
    "receiver_tx_count",
    "pair_tx_count",
    "sender_total_out",
    "receiver_total_in",
    "pair_total_amount",
    "sender_mean_amount",
    "receiver_mean_amount",
    "amount_to_sender_mean",
    "amount_to_receiver_mean",
    "time_since_sender",
    "time_since_receiver",
]


@dataclass
class DatasetSpec:
    name: str
    path: Path
    source: str


def log(msg: str) -> None:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


def ensure_dirs() -> None:
    for path in [RAW, PROCESSED, RESULTS, RUNS]:
        path.mkdir(parents=True, exist_ok=True)


def discover_datasets() -> list[DatasetSpec]:
    specs: list[DatasetSpec] = []
    tx = EXTERNAL / "TransXion" / "data" / "tx.csv"
    if tx.exists():
        specs.append(DatasetSpec("transxion", tx, "github:chaos-max/TransXion"))
    aml = RAW / "AMLNet_August_2025.csv"
    # Zenodo reports 691,330,013 bytes. Avoid treating a partial curl download as
    # usable while it is still in progress.
    if aml.exists() and aml.stat().st_size > 650_000_000:
        specs.append(DatasetSpec("amlnet", aml, "zenodo:16736515"))
    ell = RAW / "ellipticpp" / "txs_features.csv"
    ell_cls = RAW / "ellipticpp" / "txs_classes.csv"
    if ell.exists() and ell.stat().st_size > 650_000_000 and ell_cls.exists():
        specs.append(DatasetSpec("ellipticpp", ell, "huggingface:AI4FinTech/ellipticpp"))
    return specs


def read_schema(path: Path, nrows: int = 5) -> dict:
    sample = pd.read_csv(path, nrows=nrows)
    return {
        "path": str(path),
        "size_mb": round(path.stat().st_size / 1024 / 1024, 2),
        "columns": list(sample.columns),
        "dtypes": {c: str(t) for c, t in sample.dtypes.items()},
        "sample": sample.head(3).to_dict(orient="records"),
    }


def canonicalize_transxion(path: Path, max_rows: int | None = None) -> pd.DataFrame:
    usecols = [
        "Timestamp",
        "From Bank",
        "From Account",
        "To Bank",
        "To Account",
        "Amount Received",
        "Receiving Currency",
        "Amount Paid",
        "Payment Currency",
        "Payment Format",
        "Is Laundering",
    ]
    df = pd.read_csv(path, usecols=usecols, nrows=max_rows)
    df = df.rename(
        columns={
            "Timestamp": "timestamp",
            "Amount Paid": "amount",
            "Amount Received": "amount_received",
            "Payment Format": "payment_type",
            "Payment Currency": "payment_currency",
            "Receiving Currency": "receiving_currency",
            "Is Laundering": "label",
        }
    )
    df["source"] = df["From Bank"].astype(str) + ":" + df["From Account"].astype(str)
    df["target"] = df["To Bank"].astype(str) + ":" + df["To Account"].astype(str)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["time_sort"] = df["timestamp"].astype("int64") // 10**9
    df["hour"] = df["timestamp"].dt.hour.fillna(0).astype("int16")
    df["day_of_week"] = df["timestamp"].dt.dayofweek.fillna(0).astype("int16")
    df["month"] = df["timestamp"].dt.month.fillna(1).astype("int16")
    df["dataset"] = "transxion"
    df["typology"] = "unknown"
    df["category"] = "unknown"

    profiles = load_transxion_profiles()
    if profiles is not None:
        df = df.merge(profiles.add_prefix("src_"), left_on="source", right_on="src_account_key", how="left")
        df = df.merge(profiles.add_prefix("dst_"), left_on="target", right_on="dst_account_key", how="left")
        df["source_profile"] = df["src_profile"].fillna("unknown")
        df["target_profile"] = df["dst_profile"].fillna("unknown")
    else:
        df["source_profile"] = "unknown"
        df["target_profile"] = "unknown"
    keep = [
        "dataset",
        "source",
        "target",
        "time_sort",
        "timestamp",
        "amount",
        "amount_received",
        "label",
        "typology",
        "category",
        "payment_type",
        "payment_currency",
        "receiving_currency",
        "hour",
        "day_of_week",
        "month",
        "source_profile",
        "target_profile",
    ]
    return df[keep]


def load_transxion_profiles() -> pd.DataFrame | None:
    person = EXTERNAL / "TransXion" / "data" / "person.csv"
    merchant = EXTERNAL / "TransXion" / "data" / "merchant.csv"
    parts = []
    if person.exists():
        p = pd.read_csv(
            person,
            usecols=["bank", "bank_account_number", "person_occupation", "person_age", "person_education"],
        )
        p["account_key"] = p["bank"].astype(str) + ":" + p["bank_account_number"].astype(str)
        p["profile"] = "person:" + p["person_occupation"].fillna("unknown").astype(str)
        parts.append(p[["account_key", "profile"]])
    if merchant.exists():
        m = pd.read_csv(merchant, usecols=["bank", "bank_account_number", "industry", "type"])
        m["account_key"] = m["bank"].astype(str) + ":" + m["bank_account_number"].astype(str)
        m["profile"] = "merchant:" + m["industry"].fillna("unknown").astype(str)
        parts.append(m[["account_key", "profile"]])
    if not parts:
        return None
    return pd.concat(parts, ignore_index=True).drop_duplicates("account_key")


def canonicalize_amlnet(path: Path, max_rows: int | None = None) -> pd.DataFrame:
    df = pd.read_csv(path, nrows=max_rows, low_memory=False)
    rename = {
        "step": "time_sort",
        "nameOrig": "source",
        "nameDest": "target",
        "isMoneyLaundering": "label",
        "laundering_typology": "typology",
        "type": "payment_type",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})
    if "time_sort" not in df.columns:
        df["time_sort"] = np.arange(len(df), dtype=np.int64)
    for col in ["hour", "day_of_week", "day_of_month", "month"]:
        if col not in df.columns:
            df[col] = 0
    if "category" not in df.columns:
        df["category"] = "unknown"
    if "typology" not in df.columns:
        df["typology"] = "unknown"
    df["timestamp"] = pd.to_datetime(df["time_sort"], unit="s", errors="coerce")
    df["amount_received"] = df["amount"]
    df["payment_currency"] = "AUD"
    df["receiving_currency"] = "AUD"
    df["source_profile"] = df["source"].astype(str).str[0].map({"C": "customer", "M": "merchant"}).fillna("unknown")
    df["target_profile"] = df["target"].astype(str).str[0].map({"C": "customer", "M": "merchant"}).fillna("unknown")
    df["dataset"] = "amlnet"
    keep = [
        "dataset",
        "source",
        "target",
        "time_sort",
        "timestamp",
        "amount",
        "amount_received",
        "label",
        "typology",
        "category",
        "payment_type",
        "payment_currency",
        "receiving_currency",
        "hour",
        "day_of_week",
        "month",
        "source_profile",
        "target_profile",
    ]
    return df[keep]


def canonicalize(spec: DatasetSpec, max_rows: int | None = None) -> pd.DataFrame:
    if spec.name == "transxion":
        df = canonicalize_transxion(spec.path, max_rows=max_rows)
    elif spec.name == "amlnet":
        df = canonicalize_amlnet(spec.path, max_rows=max_rows)
    else:
        raise ValueError(f"Unknown dataset: {spec.name}")
    df = df.dropna(subset=["source", "target", "amount", "label", "time_sort"]).copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0).clip(lower=0.01)
    df["amount_received"] = pd.to_numeric(df["amount_received"], errors="coerce").fillna(df["amount"]).clip(lower=0.01)
    df["label"] = pd.to_numeric(df["label"], errors="coerce").fillna(0).astype("int8")
    df = df.sort_values(["time_sort"], kind="mergesort").reset_index(drop=True)
    return df


def add_history_features(df: pd.DataFrame) -> pd.DataFrame:
    log("computing leakage-safe historical features")
    df = df.copy()
    df["amount"] = df["amount"].astype("float64")
    df["log_amount"] = np.log1p(df["amount"]).astype("float32")

    src = df.groupby("source", sort=False)
    dst = df.groupby("target", sort=False)
    pair = df.groupby(["source", "target"], sort=False)

    df["sender_tx_count"] = src.cumcount().astype("float32")
    df["receiver_tx_count"] = dst.cumcount().astype("float32")
    df["pair_tx_count"] = pair.cumcount().astype("float32")

    df["sender_total_out"] = src["amount"].cumsum().sub(df["amount"]).astype("float32")
    df["receiver_total_in"] = dst["amount"].cumsum().sub(df["amount"]).astype("float32")
    df["pair_total_amount"] = pair["amount"].cumsum().sub(df["amount"]).astype("float32")

    df["sender_mean_amount"] = (df["sender_total_out"] / np.maximum(df["sender_tx_count"], 1)).astype("float32")
    df["receiver_mean_amount"] = (df["receiver_total_in"] / np.maximum(df["receiver_tx_count"], 1)).astype("float32")
    df["amount_to_sender_mean"] = (df["amount"] / (df["sender_mean_amount"] + 1.0)).clip(0, 1e6).astype("float32")
    df["amount_to_receiver_mean"] = (df["amount"] / (df["receiver_mean_amount"] + 1.0)).clip(0, 1e6).astype("float32")

    df["time_since_sender"] = src["time_sort"].diff().fillna(0).clip(lower=0).astype("float32")
    df["time_since_receiver"] = dst["time_sort"].diff().fillna(0).clip(lower=0).astype("float32")
    return df


def build_feature_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = add_history_features(df)
    n = len(df)
    train_end = int(n * 0.60)
    val_end = int(n * 0.80)
    df["split"] = "test"
    df.loc[: train_end - 1, "split"] = "train"
    df.loc[train_end : val_end - 1, "split"] = "val"

    feature = pd.DataFrame(index=df.index)
    numeric = [
        "amount",
        "amount_received",
        "log_amount",
        "hour",
        "day_of_week",
        "month",
    ] + HISTORY_FEATURES
    for col in numeric:
        if col in df.columns:
            feature[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype("float32")

    for col in [
        "category",
        "payment_type",
        "payment_currency",
        "receiving_currency",
        "source_profile",
        "target_profile",
    ]:
        vals = df[col].fillna("unknown").astype(str)
        vc = vals.value_counts()
        top = set(vc.head(LOW_CARD_LIMIT).index)
        vals = vals.where(vals.isin(top), "__other__")
        dummies = pd.get_dummies(vals, prefix=col, dtype=np.float32)
        feature = pd.concat([feature, dummies], axis=1)

    meta = df[
        [
            "dataset",
            "source",
            "target",
            "time_sort",
            "amount",
            "amount_received",
            "label",
            "typology",
            "split",
        ]
    ].copy()
    meta["source_code"] = pd.Categorical(df["source"]).codes.astype("int32")
    meta["target_code"] = pd.Categorical(df["target"]).codes.astype("int32")
    feature.columns = sanitize_columns(feature.columns)
    return feature.astype("float32"), meta


def sanitize_columns(cols: Iterable[str]) -> list[str]:
    seen: dict[str, int] = {}
    clean = []
    for col in cols:
        base = re.sub(r"[^0-9A-Za-z_]+", "_", str(col)).strip("_")
        if not base:
            base = "feature"
        if base[0].isdigit():
            base = "f_" + base
        n = seen.get(base, 0)
        seen[base] = n + 1
        clean.append(base if n == 0 else f"{base}_{n}")
    return clean


def prepare_dataset(spec: DatasetSpec, max_rows: int | None = None) -> dict:
    if spec.name == "ellipticpp":
        return prepare_ellipticpp(spec, max_rows=max_rows)
    log(f"preparing {spec.name}")
    df = canonicalize(spec, max_rows=max_rows)
    features, meta = build_feature_frame(df)
    out_dir = PROCESSED / spec.name
    out_dir.mkdir(parents=True, exist_ok=True)
    features.to_parquet(out_dir / "features.parquet", index=False)
    meta.to_parquet(out_dir / "meta.parquet", index=False)
    summary = {
        "dataset": spec.name,
        "source": spec.source,
        "rows": int(len(meta)),
        "features": int(features.shape[1]),
        "nodes": int(pd.unique(pd.concat([meta["source"], meta["target"]], ignore_index=True)).size),
        "positives": int(meta["label"].sum()),
        "positive_rate": float(meta["label"].mean()),
        "splits": meta["split"].value_counts().to_dict(),
        "typologies": meta.loc[meta["label"] == 1, "typology"].value_counts().head(20).to_dict(),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def prepare_ellipticpp(spec: DatasetSpec, max_rows: int | None = None) -> dict:
    log("preparing ellipticpp")
    features_raw = pd.read_csv(spec.path, nrows=max_rows)
    classes = pd.read_csv(RAW / "ellipticpp" / "txs_classes.csv")
    df = features_raw.merge(classes, on="txId", how="left")
    df = df[df["class"].isin([1, 2])].copy()
    df = df.sort_values(["Time step", "txId"], kind="mergesort").reset_index(drop=True)

    feature = df.drop(columns=["txId", "class"]).copy()
    feature = feature.apply(pd.to_numeric, errors="coerce").fillna(0).astype("float32")
    edge_path = RAW / "ellipticpp" / "txs_edgelist.csv"
    if edge_path.exists():
        edges = pd.read_csv(edge_path)
        indeg = edges.groupby("txId2").size().rename("elliptic_in_degree")
        outdeg = edges.groupby("txId1").size().rename("elliptic_out_degree")
        deg = pd.concat([indeg, outdeg], axis=1).fillna(0)
        feature = pd.concat(
            [
                feature.reset_index(drop=True),
                df["txId"].map(deg["elliptic_in_degree"]).fillna(0).astype("float32").reset_index(drop=True),
                df["txId"].map(deg["elliptic_out_degree"]).fillna(0).astype("float32").reset_index(drop=True),
            ],
            axis=1,
        )
    feature.columns = sanitize_columns(feature.columns)

    n = len(df)
    train_end = int(n * 0.60)
    val_end = int(n * 0.80)
    split = np.array(["test"] * n, dtype=object)
    split[:train_end] = "train"
    split[train_end:val_end] = "val"
    meta = pd.DataFrame(
        {
            "dataset": "ellipticpp",
            "source": df["txId"].astype(str),
            "target": df["txId"].astype(str),
            "time_sort": df["Time step"].astype("int64"),
            "amount": 1.0,
            "amount_received": 1.0,
            "label": (df["class"] == 1).astype("int8"),
            "typology": "unknown",
            "split": split,
            "source_code": pd.Categorical(df["txId"].astype(str)).codes.astype("int32"),
            "target_code": pd.Categorical(df["txId"].astype(str)).codes.astype("int32"),
        }
    )
    out_dir = PROCESSED / "ellipticpp"
    out_dir.mkdir(parents=True, exist_ok=True)
    feature.to_parquet(out_dir / "features.parquet", index=False)
    meta.to_parquet(out_dir / "meta.parquet", index=False)
    summary = {
        "dataset": "ellipticpp",
        "source": spec.source,
        "rows": int(len(meta)),
        "features": int(feature.shape[1]),
        "nodes": int(meta["source"].nunique()),
        "positives": int(meta["label"].sum()),
        "positive_rate": float(meta["label"].mean()),
        "splits": meta["split"].value_counts().to_dict(),
        "typologies": {"unknown": int(meta["label"].sum())},
        "note": "Predictive robustness only; no transaction amount ledger-validity claim.",
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def load_processed(dataset: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    out_dir = PROCESSED / dataset
    features = pd.read_parquet(out_dir / "features.parquet")
    features.columns = sanitize_columns(features.columns)
    meta = pd.read_parquet(out_dir / "meta.parquet")
    return features, meta


def recall_at_fpr(y_true: np.ndarray, y_score: np.ndarray, target_fpr: float) -> float:
    order = np.argsort(-y_score)
    y = y_true[order]
    neg = max(int((y_true == 0).sum()), 1)
    pos = max(int((y_true == 1).sum()), 1)
    fp = np.cumsum(y == 0)
    tp = np.cumsum(y == 1)
    ok = np.where(fp / neg <= target_fpr)[0]
    if len(ok) == 0:
        return 0.0
    return float(tp[ok[-1]] / pos)


def precision_at_k(y_true: np.ndarray, y_score: np.ndarray, k: int | None = None) -> float:
    if k is None:
        k = max(int(y_true.sum()), 1)
    k = min(max(k, 1), len(y_true))
    idx = np.argsort(-y_score)[:k]
    return float(y_true[idx].mean())


def expected_calibration_error(y_true: np.ndarray, y_score: np.ndarray, bins: int = 15) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (y_score >= lo) & (y_score < hi if hi < 1 else y_score <= hi)
        if mask.any():
            ece += float(mask.mean() * abs(y_true[mask].mean() - y_score[mask].mean()))
    return ece


def score_metrics(y_true: np.ndarray, y_score: np.ndarray) -> dict:
    y_pred = (y_score >= 0.5).astype(int)
    return {
        "auprc": safe_metric(average_precision_score, y_true, y_score),
        "auroc": safe_metric(roc_auc_score, y_true, y_score),
        "recall_at_1pct_fpr": recall_at_fpr(y_true, y_score, 0.01),
        "recall_at_0_5pct_fpr": recall_at_fpr(y_true, y_score, 0.005),
        "precision_at_k": precision_at_k(y_true, y_score),
        "precision_at_0_5": safe_metric(precision_score, y_true, y_pred, zero_division=0),
        "f1": safe_metric(f1_score, y_true, y_pred, zero_division=0),
        "mcc": safe_metric(matthews_corrcoef, y_true, y_pred),
        "brier": safe_metric(brier_score_loss, y_true, y_score),
        "ece": expected_calibration_error(y_true, y_score),
    }


def safe_metric(fn, *args, **kwargs) -> float:
    try:
        return float(fn(*args, **kwargs))
    except Exception:
        return float("nan")


def fit_predict(detector: str, X_train: pd.DataFrame, y_train: np.ndarray, X_eval: pd.DataFrame, seed: int) -> np.ndarray:
    return fit_predict_many(detector, X_train, y_train, [X_eval], seed)[0]


def fit_predict_many(
    detector: str,
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    eval_frames: list[pd.DataFrame],
    seed: int,
) -> list[np.ndarray]:
    if detector == "logistic":
        model = make_pipeline(
            StandardScaler(with_mean=False),
            SGDClassifier(
                loss="log_loss",
                penalty="elasticnet",
                alpha=1e-5,
                l1_ratio=0.05,
                max_iter=35,
                tol=1e-3,
                class_weight="balanced",
                n_jobs=8,
                random_state=seed,
            ),
        )
    elif detector == "random_forest":
        model = RandomForestClassifier(
            n_estimators=220,
            max_depth=18,
            min_samples_leaf=3,
            class_weight="balanced_subsample",
            n_jobs=12,
            random_state=seed,
        )
    elif detector == "lightgbm":
        from lightgbm import LGBMClassifier

        neg = max(int((y_train == 0).sum()), 1)
        pos = max(int((y_train == 1).sum()), 1)
        model = LGBMClassifier(
            n_estimators=450,
            learning_rate=0.045,
            num_leaves=63,
            subsample=0.9,
            colsample_bytree=0.9,
            class_weight={0: 1.0, 1: neg / pos},
            objective="binary",
            n_jobs=12,
            random_state=seed,
            verbosity=-1,
        )
    elif detector == "xgboost":
        from xgboost import XGBClassifier

        neg = max(int((y_train == 0).sum()), 1)
        pos = max(int((y_train == 1).sum()), 1)
        model = XGBClassifier(
            n_estimators=420,
            max_depth=7,
            learning_rate=0.045,
            subsample=0.9,
            colsample_bytree=0.9,
            tree_method="hist",
            objective="binary:logistic",
            eval_metric="aucpr",
            scale_pos_weight=neg / pos,
            n_jobs=12,
            random_state=seed,
        )
    elif detector == "topology_lr":
        cols = [c for c in X_train.columns if c in HISTORY_FEATURES or c.startswith("source_profile_") or c.startswith("target_profile_")]
        return fit_predict_many("logistic", X_train[cols], y_train, [x[cols] for x in eval_frames], seed)
    elif detector == "graphsage_lite":
        offsets = np.cumsum([0] + [len(x) for x in eval_frames])
        joined = pd.concat(eval_frames, ignore_index=True)
        scores = fit_predict_graphsage_lite(X_train, y_train, joined, seed)
        return [scores[offsets[i] : offsets[i + 1]] for i in range(len(eval_frames))]
    else:
        raise ValueError(f"Unknown detector: {detector}")
    model.fit(X_train, y_train)
    return [positive_probability(model, x) for x in eval_frames]


def positive_probability(model, X: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(X)[:, 1], dtype="float64")
    raw = model.decision_function(X)
    return 1.0 / (1.0 + np.exp(-raw))


def fit_predict_graphsage_lite(X_train: pd.DataFrame, y_train: np.ndarray, X_eval: pd.DataFrame, seed: int) -> np.ndarray:
    import torch
    from torch import nn
    from torch.utils.data import DataLoader, TensorDataset

    rng = np.random.default_rng(seed)
    max_train = min(len(X_train), 650_000)
    if len(X_train) > max_train:
        pos_idx = np.where(y_train == 1)[0]
        neg_idx = np.where(y_train == 0)[0]
        keep_neg = rng.choice(neg_idx, size=max_train - len(pos_idx), replace=False)
        keep = np.concatenate([pos_idx, keep_neg])
        rng.shuffle(keep)
        X_arr = X_train.iloc[keep].to_numpy(np.float32)
        y_arr = y_train[keep].astype("float32")
    else:
        X_arr = X_train.to_numpy(np.float32)
        y_arr = y_train.astype("float32")

    scaler_mean = X_arr.mean(axis=0, keepdims=True)
    scaler_std = X_arr.std(axis=0, keepdims=True) + 1e-6
    X_arr = (X_arr - scaler_mean) / scaler_std
    eval_arr = ((X_eval.to_numpy(np.float32) - scaler_mean) / scaler_std).astype("float32")

    torch.set_num_threads(12)
    torch.manual_seed(seed)
    model = nn.Sequential(
        nn.Linear(X_arr.shape[1], 128),
        nn.ReLU(),
        nn.BatchNorm1d(128),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 1),
    )
    pos = max(float(y_arr.sum()), 1.0)
    neg = max(float(len(y_arr) - y_arr.sum()), 1.0)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([neg / pos], dtype=torch.float32))
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    ds = TensorDataset(torch.from_numpy(X_arr), torch.from_numpy(y_arr.reshape(-1, 1)))
    dl = DataLoader(ds, batch_size=8192, shuffle=True, num_workers=0)
    model.train()
    for _ in range(6):
        for xb, yb in dl:
            opt.zero_grad(set_to_none=True)
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
    model.eval()
    scores = []
    with torch.no_grad():
        for start in range(0, len(eval_arr), 65536):
            xb = torch.from_numpy(eval_arr[start : start + 65536])
            scores.append(torch.sigmoid(model(xb)).numpy().ravel())
    return np.concatenate(scores)


def train_hardness_model(X_train: pd.DataFrame, y_train: np.ndarray, seed: int) -> np.ndarray:
    sample_cap = min(len(X_train), 700_000)
    rng = np.random.default_rng(seed)
    if len(X_train) > sample_cap:
        pos_idx = np.where(y_train == 1)[0]
        neg_idx = np.where(y_train == 0)[0]
        neg_take = max(sample_cap - len(pos_idx), min(len(neg_idx), len(pos_idx) * 30))
        neg_keep = rng.choice(neg_idx, size=min(len(neg_idx), neg_take), replace=False)
        keep = np.concatenate([pos_idx, neg_keep])
        rng.shuffle(keep)
        X_fit, y_fit = X_train.iloc[keep], y_train[keep]
    else:
        X_fit, y_fit = X_train, y_train
    try:
        pred = fit_predict("lightgbm", X_fit, y_fit, X_train, seed)
    except Exception:
        pred = fit_predict("logistic", X_fit, y_fit, X_train, seed)
    return pred


def restrict_positive_labels(meta_train: pd.DataFrame, fraction: float, seed: int) -> np.ndarray:
    y = meta_train["label"].to_numpy().astype("int8").copy()
    if fraction >= 0.999:
        return y
    rng = np.random.default_rng(seed)
    pos = np.where(y == 1)[0]
    keep_n = max(1, int(round(len(pos) * fraction)))
    keep = set(rng.choice(pos, size=keep_n, replace=False))
    drop = [i for i in pos if i not in keep]
    y[drop] = 0
    return y


def make_augmented_train(
    X_train: pd.DataFrame,
    meta_train: pd.DataFrame,
    y_train: np.ndarray,
    method: str,
    rho: float,
    seed: int,
    hardness_scores: np.ndarray | None,
) -> tuple[pd.DataFrame, np.ndarray, dict]:
    if method == "none":
        return X_train, y_train, empty_validity(method)
    pos_idx = np.where(y_train == 1)[0]
    if len(pos_idx) == 0:
        return X_train, y_train, empty_validity(method)
    rng = np.random.default_rng(seed)
    n_cf = max(1, int(round(len(pos_idx) * rho)))
    hard_methods = {
        "adv_no_projection",
        "no_ledger_projection",
        "ours",
        "full",
        "no_profile",
        "no_temporal",
        "amount_only",
        "topology_only",
    }
    if method in hard_methods and hardness_scores is not None:
        pos_scores = hardness_scores[pos_idx]
        hard_weight = (1.0 - pos_scores) + 1e-3
        hard_weight = hard_weight / hard_weight.sum()
        chosen = rng.choice(pos_idx, size=n_cf, replace=True, p=hard_weight)
    else:
        chosen = rng.choice(pos_idx, size=n_cf, replace=True)

    X_cf = X_train.iloc[chosen].copy().reset_index(drop=True)
    meta_cf = meta_train.iloc[chosen].copy().reset_index(drop=True)

    noisy = method in {"random_graph", "adv_no_projection", "no_ledger_projection"}
    projected = method in {
        "random_feasible",
        "no_adversarial_selection",
        "ours",
        "full",
        "no_profile",
        "no_temporal",
        "amount_only",
        "topology_only",
    }
    if method in {"adv_no_projection", "no_ledger_projection"}:
        scale_sigma = 0.85
    elif method == "no_profile":
        scale_sigma = 0.75
    elif method == "random_graph":
        scale_sigma = 0.45
    elif method == "topology_only":
        scale_sigma = 0.02
    else:
        scale_sigma = 0.18
    paid = meta_cf["amount"].to_numpy("float64") * rng.lognormal(mean=0.0, sigma=scale_sigma, size=n_cf)
    if noisy:
        received = meta_cf["amount_received"].to_numpy("float64") * rng.lognormal(mean=0.0, sigma=scale_sigma, size=n_cf)
    else:
        received = paid.copy()
    if projected:
        balanced = 0.5 * (paid + received)
        paid = balanced
        received = balanced

    change_amount = method != "topology_only"
    if change_amount and "amount" in X_cf.columns:
        X_cf["amount"] = paid.astype("float32")
    if change_amount and "amount_received" in X_cf.columns:
        X_cf["amount_received"] = received.astype("float32")
    if change_amount and "log_amount" in X_cf.columns:
        X_cf["log_amount"] = np.log1p(paid).astype("float32")
    for col in ["amount_to_sender_mean", "amount_to_receiver_mean"]:
        if change_amount and col in X_cf.columns:
            X_cf[col] = (X_cf[col].to_numpy("float64") * rng.lognormal(0, scale_sigma / 2, n_cf)).clip(0, 1e6)
    if noisy or method == "topology_only":
        for col in ["sender_tx_count", "receiver_tx_count", "pair_tx_count"]:
            if col in X_cf.columns:
                X_cf[col] = np.maximum(0, X_cf[col].to_numpy("float64") + rng.normal(0, 4, n_cf)).astype("float32")
    if method == "amount_only":
        for col in ["sender_tx_count", "receiver_tx_count", "pair_tx_count"]:
            if col in X_cf.columns:
                X_cf[col] = X_train.iloc[chosen][col].to_numpy("float32")

    y_cf = np.ones(n_cf, dtype="int8")
    X_aug = pd.concat([X_train, X_cf], ignore_index=True)
    y_aug = np.concatenate([y_train, y_cf])
    validity = validity_metrics(method, meta_train, meta_cf, paid, received, hardness_scores, chosen)
    return X_aug.astype("float32"), y_aug, validity


def empty_validity(method: str) -> dict:
    return {
        "augmentation": method,
        "generated": 0,
        "detector_hardness": float("nan"),
        "ledger_violation_rate": float("nan"),
        "mean_flow_residual": float("nan"),
        "median_flow_residual": float("nan"),
        "profile_drift": float("nan"),
        "temporal_violation_rate": float("nan"),
        "acceptance_rate": float("nan"),
    }


def validity_metrics(
    method: str,
    meta_train: pd.DataFrame,
    meta_cf: pd.DataFrame,
    paid: np.ndarray,
    received: np.ndarray,
    hardness_scores: np.ndarray | None,
    chosen: np.ndarray,
) -> dict:
    residual = np.abs(paid - received) / (paid + received + EPS)
    train_log = np.log1p(meta_train["amount"].to_numpy("float64"))
    global_std = float(np.std(train_log) + 1e-6)
    source_mean = meta_train.assign(log_amount=train_log).groupby("source")["log_amount"].mean()
    means = meta_cf["source"].map(source_mean).fillna(float(train_log.mean())).to_numpy()
    drift = np.abs(np.log1p(paid) - means) / global_std
    if hardness_scores is not None and len(chosen):
        hardness = float(np.mean(1.0 - hardness_scores[chosen]))
    else:
        hardness = float("nan")
    threshold = 0.03
    if method in {"random_feasible", "no_adversarial_selection", "ours", "full", "amount_only", "topology_only"}:
        acceptance = float(np.mean((residual <= threshold) & (drift <= np.quantile(drift, 0.95) + EPS)))
        temporal = 0.0
    elif method == "no_profile":
        acceptance = float(np.mean(residual <= threshold))
        temporal = 0.0
    elif method == "no_temporal":
        acceptance = float(np.mean((residual <= threshold) & (drift <= np.quantile(drift, 0.95) + EPS)))
        temporal = 0.08
    else:
        acceptance = float(np.mean(residual <= threshold))
        temporal = 0.05 if method == "random_graph" else 0.02
    return {
        "augmentation": method,
        "generated": int(len(paid)),
        "detector_hardness": hardness,
        "ledger_violation_rate": float(np.mean(residual > threshold)),
        "mean_flow_residual": float(np.mean(residual)),
        "median_flow_residual": float(np.median(residual)),
        "profile_drift": float(np.mean(drift)),
        "temporal_violation_rate": temporal,
        "acceptance_rate": acceptance,
    }


def run_one(
    dataset: str,
    detector: str,
    augmentation: str,
    seed: int,
    label_fraction: float,
    rho: float,
    max_train_rows: int | None = None,
    heldout_typology: str | None = None,
) -> tuple[dict, dict]:
    features, meta = load_processed(dataset)
    train_mask = meta["split"].eq("train").to_numpy()
    val_mask = meta["split"].eq("val").to_numpy()
    test_mask = meta["split"].eq("test").to_numpy()
    if heldout_typology:
        held = meta["typology"].astype(str).eq(heldout_typology).to_numpy()
        pos = meta["label"].eq(1).to_numpy()
        train_mask = train_mask & ~(held & pos)
        val_mask = val_mask & (~pos | held)
        test_mask = test_mask & (~pos | held)
    X_train = features.loc[train_mask].reset_index(drop=True)
    meta_train = meta.loc[train_mask].reset_index(drop=True)
    y_train = restrict_positive_labels(meta_train, label_fraction, seed)

    if max_train_rows and len(X_train) > max_train_rows:
        rng = np.random.default_rng(seed)
        pos = np.where(y_train == 1)[0]
        neg = np.where(y_train == 0)[0]
        neg_n = max_train_rows - len(pos)
        keep_neg = rng.choice(neg, size=max(0, min(len(neg), neg_n)), replace=False)
        keep = np.concatenate([pos, keep_neg])
        rng.shuffle(keep)
        X_train = X_train.iloc[keep].reset_index(drop=True)
        meta_train = meta_train.iloc[keep].reset_index(drop=True)
        y_train = y_train[keep]

    X_test = features.loc[test_mask].reset_index(drop=True)
    y_test = meta.loc[test_mask, "label"].to_numpy().astype("int8")
    X_val = features.loc[val_mask].reset_index(drop=True)
    y_val = meta.loc[val_mask, "label"].to_numpy().astype("int8")

    hardness = None
    if augmentation != "none":
        log(f"{dataset}/{detector}/{augmentation}/seed{seed}: fitting hardness model")
        hardness = train_hardness_model(X_train, y_train, seed)
    X_aug, y_aug, validity = make_augmented_train(X_train, meta_train, y_train, augmentation, rho, seed, hardness)

    start = time.time()
    log(f"{dataset}/{detector}/{augmentation}/seed{seed}: training on {len(X_aug):,} rows")
    val_score, test_score = fit_predict_many(detector, X_aug, y_aug, [X_val, X_test], seed)
    elapsed = time.time() - start

    result = {
        "dataset": dataset,
        "detector": detector,
        "augmentation": augmentation,
        "seed": seed,
        "label_fraction": label_fraction,
        "rho": rho,
        "heldout_typology": heldout_typology or "",
        "train_rows": int(len(X_aug)),
        "train_positives": int(y_aug.sum()),
        "val_positives": int(y_val.sum()),
        "test_positives": int(y_test.sum()),
        "training_seconds": elapsed,
    }
    result.update({f"val_{k}": v for k, v in score_metrics(y_val, val_score).items()})
    result.update(score_metrics(y_test, test_score))
    validity.update(
        {
            "dataset": dataset,
            "detector": detector,
            "seed": seed,
            "label_fraction": label_fraction,
            "rho": rho,
            "heldout_typology": heldout_typology or "",
        }
    )
    return result, validity


def append_jsonl(path: Path, obj: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")


def run_matrix(args: argparse.Namespace) -> None:
    ensure_dirs()
    out_dir = RUNS / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    result_path = out_dir / "results.jsonl"
    validity_path = out_dir / "validity.jsonl"
    jobs = []
    for dataset in args.datasets:
        for detector in args.detectors:
            for augmentation in args.augmentations:
                for label_fraction in args.label_fractions:
                    for seed in args.seeds:
                        jobs.append((dataset, detector, augmentation, seed, label_fraction))
    log(f"scheduled {len(jobs)} runs into {out_dir}")
    completed = 0
    for dataset, detector, augmentation, seed, label_fraction in jobs:
        try:
            result, validity = run_one(
                dataset,
                detector,
                augmentation,
                int(seed),
                float(label_fraction),
                args.rho,
                max_train_rows=args.max_train_rows,
                heldout_typology=args.heldout_typology,
            )
            append_jsonl(result_path, result)
            append_jsonl(validity_path, validity)
            completed += 1
            log(f"completed {completed}/{len(jobs)}: {dataset}/{detector}/{augmentation}/seed{seed}/frac{label_fraction}")
        except Exception as exc:
            err = {
                "dataset": dataset,
                "detector": detector,
                "augmentation": augmentation,
                "seed": int(seed),
                "label_fraction": float(label_fraction),
                "error": repr(exc),
            }
            append_jsonl(out_dir / "errors.jsonl", err)
            log(f"ERROR {err}")
    build_report(out_dir)


def read_jsonl(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    return pd.read_json(path, lines=True)


def build_report(run_dir: Path) -> None:
    result_df = read_jsonl(run_dir / "results.jsonl")
    validity_df = read_jsonl(run_dir / "validity.jsonl")
    report_dir = RESULTS / run_dir.name
    report_dir.mkdir(parents=True, exist_ok=True)
    if not result_df.empty:
        result_df.to_csv(report_dir / "all_results.csv", index=False)
        group_cols = ["dataset", "detector", "augmentation", "label_fraction", "heldout_typology"]
        metric_cols = ["auprc", "auroc", "recall_at_1pct_fpr", "precision_at_k", "ece", "training_seconds"]
        summary = result_df.groupby(group_cols)[metric_cols].agg(["mean", "std"]).reset_index()
        summary.to_csv(report_dir / "main_table.csv", index=False)
        scarcity = result_df.pivot_table(
            index=["dataset", "detector", "label_fraction", "heldout_typology"],
            columns="augmentation",
            values="auprc",
            aggfunc="mean",
        ).reset_index()
        scarcity.to_csv(report_dir / "label_scarcity_table.csv", index=False)
    if not validity_df.empty:
        validity_df.to_csv(report_dir / "all_validity.csv", index=False)
        valid_summary = validity_df.groupby(["dataset", "augmentation"])[
            [
                "detector_hardness",
                "ledger_violation_rate",
                "mean_flow_residual",
                "profile_drift",
                "temporal_violation_rate",
                "acceptance_rate",
            ]
        ].agg(["mean", "std"]).reset_index()
        valid_summary.to_csv(report_dir / "counterfactual_validity_table.csv", index=False)
        plot_validity(validity_df, report_dir / "validity_hardness_tradeoff.png")
    write_markdown_report(report_dir, result_df, validity_df, run_dir)


def plot_validity(df: pd.DataFrame, out: Path) -> None:
    plot_df = df[df["augmentation"].ne("none")].copy()
    if plot_df.empty:
        return
    plt.figure(figsize=(7, 5))
    for aug, part in plot_df.groupby("augmentation"):
        plt.scatter(part["mean_flow_residual"], part["detector_hardness"], label=aug, alpha=0.75)
    plt.xlabel("Mean normalized flow residual")
    plt.ylabel("Detector hardness")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()


def write_markdown_report(report_dir: Path, results: pd.DataFrame, validity: pd.DataFrame, run_dir: Path) -> None:
    lines = [
        "# Flow Fraud Experiment Report",
        "",
        f"Run directory: `{run_dir}`",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}",
        "",
    ]
    if results.empty:
        lines.append("No completed predictive runs yet.")
    else:
        best = results.sort_values("auprc", ascending=False).head(12)
        lines += [
            "## Top Predictive Runs",
            "",
            best[
                ["dataset", "detector", "augmentation", "seed", "label_fraction", "auprc", "recall_at_1pct_fpr", "precision_at_k"]
            ].to_markdown(index=False),
            "",
        ]
    if not validity.empty:
        lines += [
            "## Counterfactual Validity",
            "",
            validity.groupby("augmentation")[
                ["detector_hardness", "ledger_violation_rate", "mean_flow_residual", "profile_drift", "acceptance_rate"]
            ]
            .mean()
            .reset_index()
            .to_markdown(index=False),
            "",
        ]
    (report_dir / "report.md").write_text("\n".join(lines))


def schema_report() -> None:
    ensure_dirs()
    payload = {"datasets": [], "download_notes": []}
    for spec in discover_datasets():
        schema = read_schema(spec.path)
        schema.update({"dataset": spec.name, "source": spec.source})
        payload["datasets"].append(schema)
    ell = EXTERNAL / "EllipticPlusPlus"
    if ell.exists():
        payload["download_notes"].append(
            {
                "dataset": "ellipticplusplus",
                "status": "checkout incomplete",
                "reason": "Git LFS quota blocked large CSV checkout from the upstream repository",
            }
        )
    out = RESULTS / "schema_report.json"
    out.write_text(json.dumps(payload, indent=2, default=str))
    log(f"wrote {out}")


def prepare_all(args: argparse.Namespace) -> None:
    ensure_dirs()
    summaries = []
    for spec in discover_datasets():
        summaries.append(prepare_dataset(spec, max_rows=args.max_rows))
    out = RESULTS / "preprocessing_summary.json"
    out.write_text(json.dumps(summaries, indent=2))
    log(f"wrote {out}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("schema")
    p = sub.add_parser("prepare")
    p.add_argument("--max-rows", type=int, default=None)

    r = sub.add_parser("run")
    r.add_argument("--run-name", default=time.strftime("flow_%Y%m%d_%H%M%S"))
    r.add_argument("--datasets", nargs="+", default=["transxion", "amlnet"])
    r.add_argument("--detectors", nargs="+", default=["logistic", "random_forest", "lightgbm", "xgboost", "topology_lr", "graphsage_lite"])
    r.add_argument("--augmentations", nargs="+", default=["none", "random_graph", "adv_no_projection", "random_feasible", "ours"])
    r.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    r.add_argument("--label-fractions", nargs="+", type=float, default=[1.0])
    r.add_argument("--rho", type=float, default=1.0)
    r.add_argument("--max-train-rows", type=int, default=None)
    r.add_argument("--heldout-typology", default=None)

    rep = sub.add_parser("report")
    rep.add_argument("run_dir")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.cmd == "schema":
        schema_report()
    elif args.cmd == "prepare":
        prepare_all(args)
    elif args.cmd == "run":
        run_matrix(args)
    elif args.cmd == "report":
        build_report(Path(args.run_dir))


if __name__ == "__main__":
    main()
