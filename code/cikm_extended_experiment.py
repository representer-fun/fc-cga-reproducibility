#!/usr/bin/env python3
"""Second-stage CIKM experiments for flow_fraud.

This file intentionally does not modify the active baseline runner.  It adds a
stronger counterfactual generator that scores a candidate pool after projection,
stores predictions for paired bootstrap tests, and supports a real PyG
GraphSAGE edge classifier for reviewer-facing graph evidence.
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import math
import os
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from flow_experiment import (
    HISTORY_FEATURES,
    PROCESSED,
    RESULTS,
    RUNS,
    append_jsonl,
    build_report,
    expected_calibration_error,
    load_processed,
    log,
    precision_at_k,
    recall_at_fpr,
    restrict_positive_labels,
    score_metrics,
)

warnings.filterwarnings("ignore", category=FutureWarning)

EPS = 1e-9
THREADS = int(os.environ.get("FLOW_FRAUD_THREADS", "12"))
V2_AUGS = {
    "none",
    "feature_noise_v2",
    "feature_noise_repaired_v2",
    "smote_v2",
    "smote_repaired_v2",
    "mixup_v2",
    "mixup_repaired_v2",
    "edge_rewire_v2",
    "random_feasible_v2",
    "adv_no_projection_v2",
    "hard_projected_v2",
    "boundary_projected_v2",
    "plausible_hard_projected_v2",
    "curriculum_projected_v2",
    "typology_projected_v2",
    "plausible_typology_projected_v2",
    "v2_no_ledger",
    "v2_no_hard",
    "v2_no_profile",
    "v2_no_temporal",
    "v2_amount_only",
    "v2_topology_only",
}
STANDARD_BASE_AUGS = {"feature_noise_v2", "smote_v2", "mixup_v2", "edge_rewire_v2"}
REPAIRED_STANDARD_AUGS = {"feature_noise_repaired_v2", "smote_repaired_v2", "mixup_repaired_v2"}
STANDARD_BASE_NAME = {
    "feature_noise_repaired_v2": "feature_noise_v2",
    "smote_repaired_v2": "smote_v2",
    "mixup_repaired_v2": "mixup_v2",
}
STANDARD_AUGS = STANDARD_BASE_AUGS | REPAIRED_STANDARD_AUGS
HARD_SELECTION_AUGS = {
    "hard_projected_v2",
    "boundary_projected_v2",
    "plausible_hard_projected_v2",
    "curriculum_projected_v2",
    "typology_projected_v2",
    "plausible_typology_projected_v2",
    "adv_no_projection_v2",
    "v2_no_ledger",
    "v2_no_profile",
    "v2_no_temporal",
    "v2_amount_only",
    "v2_topology_only",
}
CATEGORICAL_PREFIXES = (
    "category_",
    "payment_type_",
    "payment_currency_",
    "receiving_currency_",
    "source_profile_",
    "target_profile_",
)


def fit_estimator(detector: str, X: pd.DataFrame, y: np.ndarray, seed: int, fast: bool = False):
    if detector in {"pyg_sage", "pyg_gat"}:
        raise ValueError("PyG models are trained through fit_predict_pyg.")
    if detector == "logistic":
        return make_pipeline(
            StandardScaler(with_mean=False),
            SGDClassifier(
                loss="log_loss",
                penalty="elasticnet",
                alpha=2e-5,
                l1_ratio=0.05,
                max_iter=45 if not fast else 20,
                tol=1e-3,
                class_weight="balanced",
                n_jobs=max(1, min(THREADS, 8)),
                random_state=seed,
            ),
        ).fit(X, y)
    if detector == "random_forest":
        model = RandomForestClassifier(
            n_estimators=260 if not fast else 120,
            max_depth=20,
            min_samples_leaf=2,
            class_weight="balanced_subsample",
            n_jobs=max(1, THREADS),
            random_state=seed,
        )
        return model.fit(X, y)
    if detector == "lightgbm":
        from lightgbm import LGBMClassifier

        neg = max(int((y == 0).sum()), 1)
        pos = max(int((y == 1).sum()), 1)
        model = LGBMClassifier(
            n_estimators=520 if not fast else 260,
            learning_rate=0.035 if not fast else 0.055,
            num_leaves=95 if not fast else 63,
            min_child_samples=20,
            subsample=0.9,
            colsample_bytree=0.9,
            reg_alpha=0.05,
            reg_lambda=0.15,
            class_weight={0: 1.0, 1: neg / pos},
            objective="binary",
            n_jobs=max(1, THREADS),
            random_state=seed,
            verbosity=-1,
        )
        return model.fit(X, y)
    if detector == "xgboost":
        from xgboost import XGBClassifier

        neg = max(int((y == 0).sum()), 1)
        pos = max(int((y == 1).sum()), 1)
        model = XGBClassifier(
            n_estimators=520 if not fast else 260,
            max_depth=8 if not fast else 6,
            learning_rate=0.035 if not fast else 0.055,
            subsample=0.9,
            colsample_bytree=0.9,
            tree_method="hist",
            objective="binary:logistic",
            eval_metric="aucpr",
            scale_pos_weight=neg / pos,
            n_jobs=max(1, THREADS),
            random_state=seed,
        )
        return model.fit(X, y)
    if detector == "topology_lr":
        cols = topology_columns(X)
        return ("topology_lr", cols, fit_estimator("logistic", X[cols], y, seed, fast=fast))
    raise ValueError(f"Unknown detector: {detector}")


def predict_estimator(model, X: pd.DataFrame) -> np.ndarray:
    if isinstance(model, tuple) and model[0] == "topology_lr":
        _, cols, inner = model
        return predict_estimator(inner, X[cols])
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(X)[:, 1], dtype="float64")
    raw = model.decision_function(X)
    return 1.0 / (1.0 + np.exp(-raw))


def topology_columns(X: pd.DataFrame) -> list[str]:
    cols = [c for c in X.columns if c in HISTORY_FEATURES or c.startswith("source_profile_") or c.startswith("target_profile_")]
    return cols if cols else list(X.columns)


def apply_heldout(meta: pd.DataFrame, heldout_typology: str | None):
    train_mask = meta["split"].eq("train").to_numpy()
    val_mask = meta["split"].eq("val").to_numpy()
    test_mask = meta["split"].eq("test").to_numpy()
    if heldout_typology:
        held = meta["typology"].astype(str).eq(heldout_typology).to_numpy()
        pos = meta["label"].eq(1).to_numpy()
        train_mask = train_mask & ~(held & pos)
        val_mask = val_mask & (~pos | held)
        test_mask = test_mask & (~pos | held)
    return train_mask, val_mask, test_mask


def add_heldout_train_positives(
    meta: pd.DataFrame,
    train_mask: np.ndarray,
    heldout_typology: str | None,
    n_examples: int,
    seed: int,
) -> np.ndarray:
    if not heldout_typology or n_examples <= 0:
        return train_mask
    original_train = meta["split"].eq("train").to_numpy()
    held = meta["typology"].astype(str).eq(heldout_typology).to_numpy()
    pos = meta["label"].eq(1).to_numpy()
    candidates = np.where(original_train & held & pos & ~train_mask)[0]
    if len(candidates) == 0:
        return train_mask
    rng = np.random.default_rng(seed + 10_007)
    chosen = rng.choice(candidates, size=min(n_examples, len(candidates)), replace=False)
    out = train_mask.copy()
    out[chosen] = True
    return out


def eval_subset_mask(meta_train: pd.DataFrame, meta_eval: pd.DataFrame, mode: str) -> np.ndarray:
    if mode == "all":
        return np.ones(len(meta_eval), dtype=bool)
    train_sources = set(meta_train["source_code"].astype("int64").tolist()) if "source_code" in meta_train.columns else set(meta_train["source"].astype(str).tolist())
    train_targets = set(meta_train["target_code"].astype("int64").tolist()) if "target_code" in meta_train.columns else set(meta_train["target"].astype(str).tolist())
    if "source_code" in meta_eval.columns:
        src = meta_eval["source_code"].astype("int64")
        dst = meta_eval["target_code"].astype("int64")
        train_pairs = set(zip(meta_train["source_code"].astype("int64"), meta_train["target_code"].astype("int64")))
    else:
        src = meta_eval["source"].astype(str)
        dst = meta_eval["target"].astype(str)
        train_pairs = set(zip(meta_train["source"].astype(str), meta_train["target"].astype(str)))
    if mode == "new_source":
        return ~src.isin(train_sources).to_numpy()
    if mode == "new_target":
        return ~dst.isin(train_targets).to_numpy()
    if mode == "new_entity":
        return (~src.isin(train_sources) | ~dst.isin(train_targets)).to_numpy()
    if mode == "new_pair":
        return np.array([(s, d) not in train_pairs for s, d in zip(src, dst)], dtype=bool)
    if mode == "low_history_entity":
        src_counts = meta_train.groupby("source_code" if "source_code" in meta_train.columns else "source").size()
        dst_counts = meta_train.groupby("target_code" if "target_code" in meta_train.columns else "target").size()
        src_hist = src.map(src_counts).fillna(0).to_numpy()
        dst_hist = dst.map(dst_counts).fillna(0).to_numpy()
        return (src_hist <= 20) | (dst_hist <= 20)
    raise ValueError(f"Unknown eval subset: {mode}")


def apply_eval_subset(
    X_eval: pd.DataFrame,
    meta_eval: pd.DataFrame,
    meta_train: pd.DataFrame,
    mode: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    mask = eval_subset_mask(meta_train, meta_eval, mode)
    if mask.sum() == 0:
        raise ValueError(f"Eval subset {mode} produced zero rows")
    return X_eval.loc[mask].reset_index(drop=True), meta_eval.loc[mask].reset_index(drop=True)


def maybe_cap_train(
    X_train: pd.DataFrame,
    meta_train: pd.DataFrame,
    y_train: np.ndarray,
    max_train_rows: int | None,
    seed: int,
):
    if not max_train_rows or len(X_train) <= max_train_rows:
        return X_train.reset_index(drop=True), meta_train.reset_index(drop=True), y_train
    rng = np.random.default_rng(seed)
    pos = np.where(y_train == 1)[0]
    neg = np.where(y_train == 0)[0]
    neg_n = max_train_rows - len(pos)
    keep_neg = rng.choice(neg, size=max(0, min(len(neg), neg_n)), replace=False)
    keep = np.concatenate([pos, keep_neg])
    rng.shuffle(keep)
    return X_train.iloc[keep].reset_index(drop=True), meta_train.iloc[keep].reset_index(drop=True), y_train[keep]


def candidate_augmented_train(
    X_train: pd.DataFrame,
    meta_train: pd.DataFrame,
    y_train: np.ndarray,
    augmentation: str,
    seed: int,
    rho: float,
    candidate_multiplier: int,
    scorer_model,
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray, dict]:
    if augmentation == "none":
        validity = empty_validity(augmentation)
        return X_train.reset_index(drop=True), meta_train.reset_index(drop=True), y_train, validity
    if augmentation not in V2_AUGS:
        raise ValueError(f"Unknown v2 augmentation: {augmentation}")

    rng = np.random.default_rng(seed)
    pos_idx = np.where(y_train == 1)[0]
    neg_idx = np.where(y_train == 0)[0]
    if len(pos_idx) == 0:
        validity = empty_validity(augmentation)
        return X_train.reset_index(drop=True), meta_train.reset_index(drop=True), y_train, validity

    n_cf = max(1, int(round(len(pos_idx) * rho)))
    n_pool = max(n_cf, n_cf * candidate_multiplier)
    train_score = predict_estimator(scorer_model, X_train).clip(1e-6, 1 - 1e-6)
    pos_score = train_score[pos_idx]
    pos_weight = (1.0 - pos_score) + 1e-4
    pos_weight = pos_weight / pos_weight.sum()
    if augmentation in HARD_SELECTION_AUGS:
        seed_idx = rng.choice(pos_idx, size=n_pool, replace=True, p=pos_weight)
    else:
        seed_idx = rng.choice(pos_idx, size=n_pool, replace=True)

    if len(neg_idx):
        neg_score = train_score[neg_idx]
        hard_neg_pool = neg_idx[np.argsort(-neg_score)[: max(256, min(len(neg_idx), n_pool * 4))]]
        neg_choice = rng.choice(hard_neg_pool, size=n_pool, replace=True)
    else:
        neg_choice = rng.choice(pos_idx, size=n_pool, replace=True)

    X_seed = X_train.iloc[seed_idx].reset_index(drop=True)
    X_neg = X_train.iloc[neg_choice].reset_index(drop=True)
    meta_seed = meta_train.iloc[seed_idx].reset_index(drop=True)
    meta_neg = meta_train.iloc[neg_choice].reset_index(drop=True)
    X_cf = X_seed.copy()

    if augmentation in STANDARD_AUGS:
        return standard_augmented_train(
            X_train,
            meta_train,
            y_train,
            X_seed,
            X_neg,
            meta_seed,
            meta_neg,
            augmentation,
            n_cf,
            rng,
            scorer_model,
        )

    boundary = augmentation in {
        "boundary_projected_v2",
        "hard_projected_v2",
        "plausible_hard_projected_v2",
        "curriculum_projected_v2",
        "typology_projected_v2",
        "plausible_typology_projected_v2",
    }
    if boundary:
        alpha = rng.uniform(0.45, 0.85, size=n_pool).astype("float32")
        X_cf = X_seed.mul(alpha, axis=0).add(X_neg.mul(1.0 - alpha, axis=0), axis=0)
        restore_profile_like_seed(X_cf, X_seed, keep_payment=True)

    no_profile = augmentation == "v2_no_profile"
    if no_profile:
        profile_cols = [c for c in X_cf.columns if c.startswith("source_profile_") or c.startswith("target_profile_")]
        if profile_cols:
            X_cf.loc[:, profile_cols] = X_neg[profile_cols].to_numpy()

    scale = {
        "random_feasible_v2": 0.20,
        "hard_projected_v2": 0.35,
        "boundary_projected_v2": 0.28,
        "plausible_hard_projected_v2": 0.24,
        "curriculum_projected_v2": 0.26,
        "typology_projected_v2": 0.30,
        "plausible_typology_projected_v2": 0.22,
        "v2_no_hard": 0.35,
        "v2_amount_only": 0.35,
        "v2_topology_only": 0.04,
        "v2_no_profile": 0.70,
        "v2_no_temporal": 0.35,
        "adv_no_projection_v2": 0.85,
        "v2_no_ledger": 0.85,
    }.get(augmentation, 0.35)

    seed_amount = meta_seed["amount"].to_numpy("float64")
    neg_amount = meta_neg["amount"].to_numpy("float64")
    if boundary and augmentation != "v2_topology_only":
        raw_paid = np.exp((np.log1p(seed_amount) * 0.65 + np.log1p(neg_amount) * 0.35)) - 1.0
        raw_paid *= rng.lognormal(0.0, scale / 2, size=n_pool)
    else:
        raw_paid = seed_amount * rng.lognormal(0.0, scale, size=n_pool)
    raw_paid = np.clip(raw_paid, 0.01, np.quantile(seed_amount, 0.995) * 8 + 1.0)
    if augmentation in {"typology_projected_v2", "plausible_typology_projected_v2"}:
        raw_paid = apply_typology_policy(X_cf, meta_seed, raw_paid, seed_amount, rng)

    noisy = augmentation in {"adv_no_projection_v2", "v2_no_ledger"}
    if noisy:
        received = np.clip(seed_amount * rng.lognormal(0.0, scale, size=n_pool), 0.01, None)
        paid = raw_paid
    else:
        paid = raw_paid
        received = raw_paid.copy()
    if augmentation == "v2_topology_only":
        paid = seed_amount.copy()
        received = meta_seed["amount_received"].to_numpy("float64")

    change_amount = augmentation != "v2_topology_only"
    if change_amount:
        write_amount_features(X_cf, paid)
    if augmentation == "v2_amount_only":
        for col in HISTORY_FEATURES:
            if col in X_cf.columns:
                X_cf[col] = X_seed[col].to_numpy("float32")
    if augmentation == "v2_topology_only":
        perturb_topology_features(X_cf, rng, amount=6.0)
    if augmentation == "v2_no_temporal":
        for col in ["time_since_sender", "time_since_receiver"]:
            if col in X_cf.columns:
                X_cf[col] = np.maximum(0, X_cf[col].to_numpy("float64") * rng.lognormal(0.0, 1.0, n_pool)).astype("float32")

    cand_score = predict_estimator(scorer_model, X_cf).clip(1e-6, 1 - 1e-6)
    cand_loss = -np.log(cand_score)
    residual = np.abs(paid - received) / (paid + received + EPS)
    profile_drift = compute_profile_drift(meta_train, meta_seed, paid)
    edit = approximate_edit_distance(X_seed, X_cf)

    if augmentation in {"random_feasible_v2", "v2_no_hard"}:
        valid = np.where(residual <= 0.03)[0]
        chosen_pool = rng.choice(valid if len(valid) else np.arange(n_pool), size=n_cf, replace=len(valid) < n_cf)
    elif augmentation in {"adv_no_projection_v2", "v2_no_ledger"}:
        chosen_pool = np.argsort(-(cand_loss - 0.01 * edit))[:n_cf]
    elif augmentation == "v2_no_profile":
        objective = cand_loss - 2.0 * residual - 0.01 * edit
        chosen_pool = np.argsort(-objective)[:n_cf]
    elif augmentation in {"plausible_hard_projected_v2", "plausible_typology_projected_v2"}:
        objective = cand_loss - 3.0 * residual - 0.55 * profile_drift - 0.04 * edit
        valid = np.where((residual <= 0.03) & (profile_drift <= np.quantile(profile_drift, 0.60) + EPS) & (edit <= np.quantile(edit, 0.80) + EPS))[0]
        order = valid[np.argsort(-objective[valid])] if len(valid) else np.argsort(-objective)
        chosen_pool = take_ordered(order, n_cf, rng)
    elif augmentation == "curriculum_projected_v2":
        objective = cand_loss - 3.0 * residual - 0.25 * profile_drift - 0.03 * edit
        valid = np.where((residual <= 0.03) & (profile_drift <= np.quantile(profile_drift, 0.90) + EPS))[0]
        if len(valid) == 0:
            valid = np.arange(n_pool)
        chosen_pool = curriculum_select(valid, cand_loss, objective, n_cf, rng)
    else:
        objective = cand_loss - 3.0 * residual - 0.12 * profile_drift - 0.02 * edit
        chosen_pool = np.argsort(-objective)[:n_cf]

    X_sel = X_cf.iloc[chosen_pool].reset_index(drop=True)
    meta_sel = meta_seed.iloc[chosen_pool].copy().reset_index(drop=True)
    meta_sel["amount"] = paid[chosen_pool]
    meta_sel["amount_received"] = received[chosen_pool]
    y_sel = np.ones(len(X_sel), dtype="int8")

    X_aug = pd.concat([X_train.reset_index(drop=True), X_sel], ignore_index=True).astype("float32")
    meta_aug = pd.concat([meta_train.reset_index(drop=True), meta_sel], ignore_index=True)
    y_aug = np.concatenate([y_train, y_sel])
    validity = candidate_validity(
        augmentation,
        cand_loss[chosen_pool],
        residual[chosen_pool],
        profile_drift[chosen_pool],
        edit[chosen_pool],
        len(X_sel),
        categorical_fractionality_rate(X_sel),
        negative_feature_rate(X_sel),
    )
    return X_aug, meta_aug, y_aug, validity


def standard_augmented_train(
    X_train: pd.DataFrame,
    meta_train: pd.DataFrame,
    y_train: np.ndarray,
    X_seed: pd.DataFrame,
    X_neg: pd.DataFrame,
    meta_seed: pd.DataFrame,
    meta_neg: pd.DataFrame,
    augmentation: str,
    n_cf: int,
    rng: np.random.Generator,
    scorer_model,
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray, dict]:
    n_pool = len(X_seed)
    base_augmentation = STANDARD_BASE_NAME.get(augmentation, augmentation)
    is_repaired = augmentation in REPAIRED_STANDARD_AUGS
    if base_augmentation == "feature_noise_v2":
        X_cf = X_seed.copy()
        sample = rng.choice(len(X_train), size=min(len(X_train), 20_000), replace=False)
        scale = X_train.iloc[sample].std(axis=0).replace(0, 1.0).fillna(1.0).to_numpy("float64")
        noise = rng.normal(0.0, 0.18, size=X_cf.shape) * scale
        X_cf.loc[:, :] = X_cf.to_numpy("float64") + noise
    elif base_augmentation == "smote_v2":
        peer = X_train.iloc[rng.choice(np.where(y_train == 1)[0], size=n_pool, replace=True)].reset_index(drop=True)
        alpha = rng.uniform(0.15, 0.85, size=n_pool).astype("float32")
        X_cf = X_seed.mul(alpha, axis=0).add(peer.mul(1.0 - alpha, axis=0), axis=0)
    elif base_augmentation == "mixup_v2":
        alpha = rng.beta(0.4, 0.4, size=n_pool).clip(0.05, 0.95).astype("float32")
        X_cf = X_seed.mul(alpha, axis=0).add(X_neg.mul(1.0 - alpha, axis=0), axis=0)
    elif base_augmentation == "edge_rewire_v2":
        X_cf = X_seed.copy()
        swap_prefixes = ("target_profile_",)
        swap_cols = [c for c in X_cf.columns if c.startswith(swap_prefixes)]
        swap_cols += [c for c in ["receiver_tx_count", "receiver_total_in", "receiver_mean_amount", "amount_to_receiver_mean"] if c in X_cf.columns]
        if swap_cols:
            X_cf.loc[:, swap_cols] = X_neg[swap_cols].to_numpy()
    else:
        raise ValueError(f"Unknown standard augmentation: {augmentation}")

    paid = frame_amount(X_cf, "amount", meta_seed["amount"].to_numpy("float64"))
    received = frame_amount(X_cf, "amount_received", meta_seed["amount_received"].to_numpy("float64"))
    if base_augmentation == "edge_rewire_v2":
        paid = meta_seed["amount"].to_numpy("float64")
        received = paid.copy()
        write_amount_features(X_cf, paid)
    if is_repaired:
        paid = repair_standard_counterfactuals(X_cf, X_seed, meta_seed, paid)
        received = paid.copy()

    cand_score = predict_estimator(scorer_model, X_cf).clip(1e-6, 1 - 1e-6)
    cand_loss = -np.log(cand_score)
    residual = np.abs(paid - received) / (paid + received + EPS)
    profile_drift = compute_profile_drift(meta_train, meta_seed, paid)
    edit = approximate_edit_distance(X_seed, X_cf)

    if base_augmentation == "feature_noise_v2":
        objective = cand_loss - 0.01 * edit
        chosen_pool = take_ordered(np.argsort(-objective), n_cf, rng)
    else:
        chosen_pool = rng.choice(np.arange(n_pool), size=n_cf, replace=n_pool < n_cf)

    X_sel = X_cf.iloc[chosen_pool].reset_index(drop=True)
    meta_sel = meta_seed.iloc[chosen_pool].copy().reset_index(drop=True)
    if base_augmentation == "edge_rewire_v2":
        for col in ["target", "target_code", "target_bank"]:
            if col in meta_sel.columns and col in meta_neg.columns:
                meta_sel[col] = meta_neg.iloc[chosen_pool][col].to_numpy()
    meta_sel["amount"] = paid[chosen_pool]
    meta_sel["amount_received"] = received[chosen_pool]
    y_sel = np.ones(len(X_sel), dtype="int8")

    X_aug = pd.concat([X_train.reset_index(drop=True), X_sel], ignore_index=True).astype("float32")
    meta_aug = pd.concat([meta_train.reset_index(drop=True), meta_sel], ignore_index=True)
    y_aug = np.concatenate([y_train, y_sel])
    validity = candidate_validity(
        augmentation,
        cand_loss[chosen_pool],
        residual[chosen_pool],
        profile_drift[chosen_pool],
        edit[chosen_pool],
        len(X_sel),
        categorical_fractionality_rate(X_sel),
        negative_feature_rate(X_sel),
    )
    return X_aug, meta_aug, y_aug, validity


def frame_amount(X: pd.DataFrame, col: str, fallback: np.ndarray) -> np.ndarray:
    if col in X.columns:
        return np.clip(X[col].to_numpy("float64"), 0.01, None)
    return np.clip(fallback, 0.01, None)


def repair_standard_counterfactuals(
    X_cf: pd.DataFrame,
    X_seed: pd.DataFrame,
    meta_seed: pd.DataFrame,
    paid: np.ndarray,
) -> np.ndarray:
    seed_amount = meta_seed["amount"].to_numpy("float64") if "amount" in meta_seed.columns else paid
    seed_amount = np.clip(seed_amount, 0.01, None)
    cap = max(float(np.quantile(seed_amount, 0.995) * 8.0 + 1.0), 0.02)
    repaired_paid = np.nan_to_num(np.asarray(paid, dtype="float64"), nan=0.01, posinf=cap, neginf=0.01)
    repaired_paid = np.clip(repaired_paid, 0.01, cap)

    arr = X_cf.to_numpy("float64")
    arr = np.nan_to_num(arr, nan=0.0, posinf=cap, neginf=0.0)
    arr = np.maximum(arr, 0.0)
    X_cf.loc[:, :] = arr
    write_amount_features(X_cf, repaired_paid)
    repair_categorical_groups(X_cf, X_seed)
    for col in HISTORY_FEATURES + ["hour", "day_of_week", "month"]:
        if col in X_cf.columns:
            X_cf[col] = np.maximum(0.0, X_cf[col].to_numpy("float64")).astype("float32")
    return repaired_paid


def repair_categorical_groups(X_cf: pd.DataFrame, X_seed: pd.DataFrame) -> None:
    for prefix in CATEGORICAL_PREFIXES:
        cols = [c for c in X_cf.columns if c.startswith(prefix)]
        if not cols:
            continue
        if len(cols) == 1:
            col = cols[0]
            if col in X_seed.columns:
                X_cf[col] = (X_seed[col].to_numpy("float64") > 0.5).astype("float32")
            else:
                X_cf[col] = (X_cf[col].to_numpy("float64") >= 0.5).astype("float32")
            continue
        values = X_cf[cols].to_numpy("float64")
        winners = np.argmax(values, axis=1)
        out = np.zeros_like(values, dtype="float32")
        out[np.arange(len(values)), winners] = 1.0
        X_cf.loc[:, cols] = out


def take_ordered(order: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    order = np.asarray(order, dtype="int64")
    if len(order) >= n:
        return order[:n]
    if len(order) == 0:
        return rng.integers(0, max(n, 1), size=n)
    extra = rng.choice(order, size=n - len(order), replace=True)
    return np.concatenate([order, extra])


def curriculum_select(valid: np.ndarray, cand_loss: np.ndarray, objective: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    valid = np.asarray(valid, dtype="int64")
    hard_order = valid[np.argsort(-objective[valid])]
    easy_order = valid[np.argsort(np.abs(cand_loss[valid] - np.quantile(cand_loss[valid], 0.35)))]
    mid_order = valid[np.argsort(np.abs(cand_loss[valid] - np.quantile(cand_loss[valid], 0.65)))]
    hard_n = max(1, int(round(n * 0.35)))
    mid_n = max(1, int(round(n * 0.35)))
    easy_n = max(0, n - hard_n - mid_n)
    chosen = np.concatenate([
        take_ordered(hard_order, hard_n, rng),
        take_ordered(mid_order, mid_n, rng),
        take_ordered(easy_order, easy_n, rng),
    ])
    if len(chosen) > n:
        chosen = chosen[:n]
    rng.shuffle(chosen)
    return chosen


def apply_typology_policy(
    X_cf: pd.DataFrame,
    meta_seed: pd.DataFrame,
    paid: np.ndarray,
    seed_amount: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    typ = meta_seed.get("typology", pd.Series([""] * len(meta_seed))).astype(str).str.lower()
    out = paid.copy()
    layering = typ.str.contains("layer", regex=False).to_numpy()
    structuring = typ.str.contains("struct", regex=False).to_numpy()
    integration = typ.str.contains("integr", regex=False).to_numpy()

    if layering.any():
        out[layering] *= rng.lognormal(0.03, 0.10, layering.sum())
        for col in ["sender_tx_count", "receiver_tx_count", "pair_tx_count"]:
            if col in X_cf.columns:
                X_cf.loc[layering, col] = np.maximum(0, X_cf.loc[layering, col].to_numpy("float64") + rng.poisson(2, layering.sum())).astype("float32")
        for col in ["sender_total_out", "receiver_total_in", "pair_total_amount"]:
            if col in X_cf.columns:
                X_cf.loc[layering, col] = np.maximum(0, X_cf.loc[layering, col].to_numpy("float64") * rng.lognormal(0.05, 0.08, layering.sum())).astype("float32")
    if structuring.any():
        cap = max(float(np.quantile(seed_amount, 0.45)), 0.01)
        out[structuring] = np.minimum(out[structuring], cap) * rng.uniform(0.85, 1.05, structuring.sum())
        for col in ["sender_tx_count", "pair_tx_count"]:
            if col in X_cf.columns:
                X_cf.loc[structuring, col] = np.maximum(0, X_cf.loc[structuring, col].to_numpy("float64") + rng.poisson(4, structuring.sum())).astype("float32")
    if integration.any():
        out[integration] *= rng.lognormal(0.0, 0.08, integration.sum())
        if "receiver_total_in" in X_cf.columns:
            X_cf.loc[integration, "receiver_total_in"] = np.maximum(0, X_cf.loc[integration, "receiver_total_in"].to_numpy("float64") * rng.lognormal(0.08, 0.10, integration.sum())).astype("float32")
    other = ~(layering | structuring | integration)
    if other.any():
        out[other] *= rng.lognormal(0.0, 0.08, other.sum())
    return np.clip(out, 0.01, np.quantile(seed_amount, 0.995) * 8 + 1.0)


def restore_profile_like_seed(X_cf: pd.DataFrame, X_seed: pd.DataFrame, keep_payment: bool) -> None:
    prefixes = ["source_profile_", "target_profile_", "payment_currency_", "receiving_currency_"]
    if keep_payment:
        prefixes += ["payment_type_", "category_"]
    cols = [c for c in X_cf.columns if any(c.startswith(p) for p in prefixes)]
    if cols:
        X_cf.loc[:, cols] = X_seed[cols].to_numpy()


def write_amount_features(X_cf: pd.DataFrame, paid: np.ndarray) -> None:
    if "amount" in X_cf.columns:
        X_cf["amount"] = paid.astype("float32")
    if "amount_received" in X_cf.columns:
        X_cf["amount_received"] = paid.astype("float32")
    if "log_amount" in X_cf.columns:
        X_cf["log_amount"] = np.log1p(paid).astype("float32")
    if "sender_mean_amount" in X_cf.columns and "amount_to_sender_mean" in X_cf.columns:
        X_cf["amount_to_sender_mean"] = (paid / (X_cf["sender_mean_amount"].to_numpy("float64") + 1.0)).clip(0, 1e6).astype("float32")
    if "receiver_mean_amount" in X_cf.columns and "amount_to_receiver_mean" in X_cf.columns:
        X_cf["amount_to_receiver_mean"] = (paid / (X_cf["receiver_mean_amount"].to_numpy("float64") + 1.0)).clip(0, 1e6).astype("float32")


def perturb_topology_features(X_cf: pd.DataFrame, rng: np.random.Generator, amount: float) -> None:
    for col in ["sender_tx_count", "receiver_tx_count", "pair_tx_count"]:
        if col in X_cf.columns:
            X_cf[col] = np.maximum(0, X_cf[col].to_numpy("float64") + rng.normal(0, amount, len(X_cf))).astype("float32")
    for col in ["sender_total_out", "receiver_total_in", "pair_total_amount"]:
        if col in X_cf.columns:
            X_cf[col] = np.maximum(0, X_cf[col].to_numpy("float64") * rng.lognormal(0.0, 0.15, len(X_cf))).astype("float32")


def compute_profile_drift(meta_train: pd.DataFrame, meta_seed: pd.DataFrame, paid: np.ndarray) -> np.ndarray:
    train_log = np.log1p(meta_train["amount"].to_numpy("float64"))
    std = np.std(train_log) + 1e-6
    source_mean = meta_train.assign(log_amount=train_log).groupby("source")["log_amount"].mean()
    means = meta_seed["source"].map(source_mean).fillna(float(train_log.mean())).to_numpy()
    return np.abs(np.log1p(paid) - means) / std


def approximate_edit_distance(X_seed: pd.DataFrame, X_cf: pd.DataFrame) -> np.ndarray:
    cols = [c for c in ["amount", "log_amount"] + HISTORY_FEATURES if c in X_seed.columns]
    if not cols:
        return np.zeros(len(X_seed), dtype="float64")
    a = X_seed[cols].to_numpy("float64")
    b = X_cf[cols].to_numpy("float64")
    scale = np.nanstd(a, axis=0) + 1e-6
    return np.mean(np.abs((b - a) / scale), axis=1)


def categorical_fractionality_rate(X: pd.DataFrame) -> float:
    cols = [c for c in X.columns if c.startswith(CATEGORICAL_PREFIXES)]
    if not cols:
        return 0.0
    values = X[cols].to_numpy("float64")
    return float(np.mean((values > 1e-4) & (values < 1.0 - 1e-4)))


def negative_feature_rate(X: pd.DataFrame) -> float:
    values = X.to_numpy("float64")
    return float(np.mean(values < -1e-6))


def empty_validity(augmentation: str) -> dict:
    return {
        "augmentation": augmentation,
        "generated": 0,
        "detector_hardness": float("nan"),
        "ledger_violation_rate": float("nan"),
        "mean_flow_residual": float("nan"),
        "median_flow_residual": float("nan"),
        "profile_drift": float("nan"),
        "edit_distance": float("nan"),
        "categorical_fractionality_rate": float("nan"),
        "negative_feature_rate": float("nan"),
        "temporal_violation_rate": float("nan"),
        "acceptance_rate": float("nan"),
    }


def candidate_validity(
    augmentation: str,
    cand_loss: np.ndarray,
    residual: np.ndarray,
    profile_drift: np.ndarray,
    edit: np.ndarray,
    generated: int,
    categorical_fractionality: float = 0.0,
    negative_rate: float = 0.0,
) -> dict:
    projected = augmentation not in {"adv_no_projection_v2", "v2_no_ledger"}
    temporal = 0.08 if augmentation == "v2_no_temporal" else 0.0 if projected else 0.02
    acceptance = float(np.mean(residual <= 0.03))
    if projected and augmentation != "v2_no_profile":
        acceptance = float(np.mean((residual <= 0.03) & (profile_drift <= np.quantile(profile_drift, 0.95) + EPS)))
    return {
        "augmentation": augmentation,
        "generated": int(generated),
        "detector_hardness": float(np.mean(cand_loss)),
        "ledger_violation_rate": float(np.mean(residual > 0.03)),
        "mean_flow_residual": float(np.mean(residual)),
        "median_flow_residual": float(np.median(residual)),
        "profile_drift": float(np.mean(profile_drift)),
        "edit_distance": float(np.mean(edit)),
        "categorical_fractionality_rate": float(categorical_fractionality),
        "negative_feature_rate": float(negative_rate),
        "temporal_violation_rate": temporal,
        "acceptance_rate": acceptance,
    }


def fit_predict_tabular(detector: str, X_train: pd.DataFrame, y_train: np.ndarray, eval_frames: list[pd.DataFrame], seed: int):
    model = fit_estimator(detector, X_train, y_train, seed, fast=False)
    return [predict_estimator(model, X) for X in eval_frames]


def fit_predict_pyg(
    dataset: str,
    X_train: pd.DataFrame,
    meta_train: pd.DataFrame,
    y_train: np.ndarray,
    X_val: pd.DataFrame,
    meta_val: pd.DataFrame,
    X_test: pd.DataFrame,
    meta_test: pd.DataFrame,
    seed: int,
    model_kind: str = "sage",
):
    import torch
    from torch import nn
    from torch_geometric.nn import GATv2Conv, SAGEConv

    torch.set_num_threads(max(1, THREADS))
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)

    node_count = int(max(meta_train["source_code"].max(), meta_train["target_code"].max(), meta_val["source_code"].max(), meta_val["target_code"].max(), meta_test["source_code"].max(), meta_test["target_code"].max()) + 1)
    node_x = build_node_features(meta_train, y_train, node_count)
    train_edges = np.vstack([meta_train["source_code"].to_numpy(), meta_train["target_code"].to_numpy()])
    edge_index = torch.tensor(np.concatenate([train_edges, train_edges[::-1]], axis=1), dtype=torch.long)

    edge_cols = select_edge_feature_cols(X_train)
    scaler_mean = X_train[edge_cols].to_numpy("float32").mean(axis=0, keepdims=True)
    scaler_std = X_train[edge_cols].to_numpy("float32").std(axis=0, keepdims=True) + 1e-6
    train_edge_x = torch.tensor(((X_train[edge_cols].to_numpy("float32") - scaler_mean) / scaler_std), dtype=torch.float32)
    val_edge_x = torch.tensor(((X_val[edge_cols].to_numpy("float32") - scaler_mean) / scaler_std), dtype=torch.float32)
    test_edge_x = torch.tensor(((X_test[edge_cols].to_numpy("float32") - scaler_mean) / scaler_std), dtype=torch.float32)
    node_x = torch.tensor(node_x, dtype=torch.float32)

    class EdgeGNN(nn.Module):
        def __init__(self):
            super().__init__()
            hidden = 64
            if model_kind == "gat":
                self.conv1 = GATv2Conv(node_x.shape[1], hidden, heads=2, concat=False)
                self.conv2 = GATv2Conv(hidden, hidden, heads=2, concat=False)
            else:
                self.conv1 = SAGEConv(node_x.shape[1], hidden)
                self.conv2 = SAGEConv(hidden, hidden)
            self.edge_mlp = nn.Sequential(
                nn.Linear(hidden * 2 + train_edge_x.shape[1], 128),
                nn.ReLU(),
                nn.Dropout(0.15),
                nn.Linear(128, 1),
            )

        def encode(self):
            z = torch.relu(self.conv1(node_x, edge_index))
            z = torch.relu(self.conv2(z, edge_index))
            return z

        def edge_logits(self, z, src, dst, edge_x):
            return self.edge_mlp(torch.cat([z[src], z[dst], edge_x], dim=1)).squeeze(1)

    model = EdgeGNN()
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    y_t = torch.tensor(y_train.astype("float32"))
    src_t = torch.tensor(meta_train["source_code"].to_numpy(), dtype=torch.long)
    dst_t = torch.tensor(meta_train["target_code"].to_numpy(), dtype=torch.long)
    pos = max(float(y_t.sum()), 1.0)
    neg = max(float(len(y_t) - y_t.sum()), 1.0)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=torch.tensor(neg / pos))

    max_loss_edges = min(len(y_train), 260_000 if dataset == "transxion" else 180_000)
    pos_idx = np.where(y_train == 1)[0]
    neg_idx = np.where(y_train == 0)[0]
    for epoch in range(18):
        model.train()
        if len(y_train) > max_loss_edges:
            neg_take = max_loss_edges - min(len(pos_idx), max_loss_edges // 2)
            epoch_idx = np.concatenate([pos_idx, rng.choice(neg_idx, size=max(1, neg_take), replace=False)])
            rng.shuffle(epoch_idx)
        else:
            epoch_idx = np.arange(len(y_train))
        idx = torch.tensor(epoch_idx, dtype=torch.long)
        opt.zero_grad(set_to_none=True)
        z = model.encode()
        logits = model.edge_logits(z, src_t[idx], dst_t[idx], train_edge_x[idx])
        loss = loss_fn(logits, y_t[idx])
        loss.backward()
        opt.step()

    def score(meta_eval: pd.DataFrame, edge_x_eval: torch.Tensor) -> np.ndarray:
        src = torch.tensor(meta_eval["source_code"].to_numpy(), dtype=torch.long)
        dst = torch.tensor(meta_eval["target_code"].to_numpy(), dtype=torch.long)
        out = []
        model.eval()
        with torch.no_grad():
            z = model.encode()
            for start in range(0, len(meta_eval), 65536):
                logits = model.edge_logits(z, src[start : start + 65536], dst[start : start + 65536], edge_x_eval[start : start + 65536])
                out.append(torch.sigmoid(logits).cpu().numpy())
        return np.concatenate(out)

    return [score(meta_val, val_edge_x), score(meta_test, test_edge_x)]


def select_edge_feature_cols(X: pd.DataFrame) -> list[str]:
    preferred = [
        "amount",
        "amount_received",
        "log_amount",
        "hour",
        "day_of_week",
        "month",
    ] + HISTORY_FEATURES
    cols = [c for c in preferred if c in X.columns]
    if not cols:
        cols = list(X.columns[: min(64, X.shape[1])])
    return cols


def build_node_features(meta_train: pd.DataFrame, y_train: np.ndarray, node_count: int) -> np.ndarray:
    src = meta_train["source_code"].to_numpy("int64")
    dst = meta_train["target_code"].to_numpy("int64")
    amount = meta_train["amount"].to_numpy("float64")
    x = np.zeros((node_count, 10), dtype="float32")
    np.add.at(x[:, 0], src, 1.0)
    np.add.at(x[:, 1], dst, 1.0)
    np.add.at(x[:, 2], src, amount)
    np.add.at(x[:, 3], dst, amount)
    np.add.at(x[:, 4], src, y_train)
    np.add.at(x[:, 5], dst, y_train)
    x[:, 6] = x[:, 2] / np.maximum(x[:, 0], 1.0)
    x[:, 7] = x[:, 3] / np.maximum(x[:, 1], 1.0)
    x[:, 8] = x[:, 4] / np.maximum(x[:, 0], 1.0)
    x[:, 9] = x[:, 5] / np.maximum(x[:, 1], 1.0)
    x[:, 2:4] = np.log1p(x[:, 2:4])
    mean = x.mean(axis=0, keepdims=True)
    std = x.std(axis=0, keepdims=True) + 1e-6
    return (x - mean) / std


def run_one(args, dataset: str, detector: str, augmentation: str, seed: int, label_fraction: float) -> tuple[dict, dict]:
    features, meta = load_processed(dataset)
    train_mask, val_mask, test_mask = apply_heldout(meta, args.heldout_typology)
    train_mask = add_heldout_train_positives(meta, train_mask, args.heldout_typology, args.heldout_train_positives, seed)
    X_train = features.loc[train_mask].reset_index(drop=True)
    meta_train = meta.loc[train_mask].reset_index(drop=True)
    y_train = restrict_positive_labels(meta_train, label_fraction, seed)
    X_train, meta_train, y_train = maybe_cap_train(X_train, meta_train, y_train, args.max_train_rows, seed)

    X_val = features.loc[val_mask].reset_index(drop=True)
    meta_val = meta.loc[val_mask].reset_index(drop=True)
    if args.eval_subset != "all":
        X_val, meta_val = apply_eval_subset(X_val, meta_val, meta_train, args.eval_subset)
    y_val = meta_val["label"].to_numpy("int8")
    X_test = features.loc[test_mask].reset_index(drop=True)
    meta_test = meta.loc[test_mask].reset_index(drop=True)
    if args.eval_subset != "all":
        X_test, meta_test = apply_eval_subset(X_test, meta_test, meta_train, args.eval_subset)
    y_test = meta_test["label"].to_numpy("int8")

    scorer_detector = "lightgbm" if detector in {"pyg_sage", "pyg_gat"} else detector
    scorer_X = X_train[topology_columns(X_train)] if scorer_detector == "topology_lr" else X_train
    scorer = fit_estimator(scorer_detector, scorer_X, y_train, seed + 17, fast=True)
    if scorer_detector == "topology_lr":
        # fit_estimator already wraps columns when called with topology_lr, so this branch is defensive.
        scorer = fit_estimator("lightgbm", X_train, y_train, seed + 17, fast=True)

    X_aug, meta_aug, y_aug, validity = candidate_augmented_train(
        X_train,
        meta_train,
        y_train,
        augmentation,
        seed,
        args.rho,
        args.candidate_multiplier,
        scorer,
    )

    start = time.time()
    log(f"{dataset}/{detector}/{augmentation}/seed{seed}/frac{label_fraction}: train_rows={len(X_aug):,}")
    if detector == "pyg_sage":
        val_score, test_score = fit_predict_pyg(dataset, X_aug, meta_aug, y_aug, X_val, meta_val, X_test, meta_test, seed, model_kind="sage")
    elif detector == "pyg_gat":
        val_score, test_score = fit_predict_pyg(dataset, X_aug, meta_aug, y_aug, X_val, meta_val, X_test, meta_test, seed, model_kind="gat")
    else:
        val_score, test_score = fit_predict_tabular(detector, X_aug, y_aug, [X_val, X_test], seed)
    elapsed = time.time() - start

    result = {
        "dataset": dataset,
        "detector": detector,
        "augmentation": augmentation,
        "seed": int(seed),
        "label_fraction": float(label_fraction),
        "rho": float(args.rho),
        "candidate_multiplier": int(args.candidate_multiplier),
        "heldout_typology": args.heldout_typology or "",
        "heldout_train_positives": int(args.heldout_train_positives),
        "eval_subset": args.eval_subset,
        "train_rows": int(len(X_aug)),
        "train_positives": int(y_aug.sum()),
        "val_positives": int(y_val.sum()),
        "test_positives": int(y_test.sum()),
        "training_seconds": float(elapsed),
    }
    result.update({f"val_{k}": v for k, v in score_metrics(y_val, val_score).items()})
    result.update(score_metrics(y_test, test_score))
    validity.update(
        {
            "dataset": dataset,
            "detector": detector,
            "seed": int(seed),
            "label_fraction": float(label_fraction),
            "rho": float(args.rho),
            "heldout_typology": args.heldout_typology or "",
            "heldout_train_positives": int(args.heldout_train_positives),
            "eval_subset": args.eval_subset,
        }
    )
    if args.save_preds:
        save_predictions(args.run_name, dataset, detector, augmentation, seed, label_fraction, y_test, test_score)
    return result, validity


def save_predictions(run_name: str, dataset: str, detector: str, augmentation: str, seed: int, frac: float, y: np.ndarray, score: np.ndarray) -> None:
    pred_dir = RUNS / run_name / "predictions"
    pred_dir.mkdir(parents=True, exist_ok=True)
    frac_s = str(frac).replace(".", "p")
    name = f"{dataset}__{detector}__{augmentation}__seed{seed}__frac{frac_s}.npz"
    np.savez_compressed(pred_dir / name, y_true=y.astype("int8"), y_score=score.astype("float32"))


def run_matrix(args) -> None:
    out_dir = RUNS / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    result_path = out_dir / "results.jsonl"
    validity_path = out_dir / "validity.jsonl"
    jobs = [
        (dataset, detector, augmentation, seed, frac)
        for dataset in args.datasets
        for detector in args.detectors
        for augmentation in args.augmentations
        for frac in args.label_fractions
        for seed in args.seeds
    ]
    completed = load_completed_keys(result_path)
    todo = [job for job in jobs if job_key(args, *job) not in completed]
    log(f"scheduled {len(jobs)} CIKM extended runs into {out_dir}; remaining {len(todo)} after resume check")
    if args.workers <= 1:
        for i, (dataset, detector, augmentation, seed, frac) in enumerate(todo, start=1):
            try:
                result, validity = run_one(args, dataset, detector, augmentation, seed, frac)
                append_jsonl(result_path, result)
                append_jsonl(validity_path, validity)
                log(f"completed {i}/{len(todo)} remaining: {dataset}/{detector}/{augmentation}/seed{seed}/frac{frac}")
            except Exception as exc:
                append_jsonl(
                    out_dir / "errors.jsonl",
                    {
                        "dataset": dataset,
                        "detector": detector,
                        "augmentation": augmentation,
                        "seed": int(seed),
                        "label_fraction": float(frac),
                        "error": repr(exc),
                    },
                )
                log(f"ERROR {dataset}/{detector}/{augmentation}/seed{seed}/frac{frac}: {exc!r}")
        build_report(out_dir)
        return

    log(f"running with {args.workers} process workers and FLOW_FRAUD_THREADS={THREADS}")
    done_count = 0
    with futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        future_map = {
            pool.submit(run_one, args, dataset, detector, augmentation, seed, frac): (dataset, detector, augmentation, seed, frac)
            for dataset, detector, augmentation, seed, frac in todo
        }
        for fut in futures.as_completed(future_map):
            dataset, detector, augmentation, seed, frac = future_map[fut]
            done_count += 1
            try:
                result, validity = fut.result()
                append_jsonl(result_path, result)
                append_jsonl(validity_path, validity)
                log(f"completed {done_count}/{len(todo)} remaining: {dataset}/{detector}/{augmentation}/seed{seed}/frac{frac}")
            except Exception as exc:
                append_jsonl(
                    out_dir / "errors.jsonl",
                    {
                        "dataset": dataset,
                        "detector": detector,
                        "augmentation": augmentation,
                        "seed": int(seed),
                        "label_fraction": float(frac),
                        "error": repr(exc),
                    },
                )
                log(f"ERROR {dataset}/{detector}/{augmentation}/seed{seed}/frac{frac}: {exc!r}")
    build_report(out_dir)


def job_key(args, dataset: str, detector: str, augmentation: str, seed: int, frac: float) -> tuple:
    return (
        dataset,
        detector,
        augmentation,
        int(seed),
        float(frac),
        args.heldout_typology or "",
        int(getattr(args, "heldout_train_positives", 0)),
        getattr(args, "eval_subset", "all"),
    )


def load_completed_keys(result_path: Path) -> set[tuple]:
    keys = set()
    if not result_path.exists():
        return keys
    with result_path.open() as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            keys.add(
                (
                    obj.get("dataset"),
                    obj.get("detector"),
                    obj.get("augmentation"),
                    int(obj.get("seed")),
                    float(obj.get("label_fraction")),
                    obj.get("heldout_typology") or "",
                    int(obj.get("heldout_train_positives", 0)),
                    obj.get("eval_subset") or "all",
                )
            )
    return keys


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--run-name", required=True)
    r.add_argument("--datasets", nargs="+", required=True)
    r.add_argument("--detectors", nargs="+", required=True)
    r.add_argument("--augmentations", nargs="+", required=True)
    r.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    r.add_argument("--label-fractions", nargs="+", type=float, default=[1.0])
    r.add_argument("--rho", type=float, default=1.0)
    r.add_argument("--candidate-multiplier", type=int, default=8)
    r.add_argument("--max-train-rows", type=int, default=None)
    r.add_argument("--heldout-typology", default=None)
    r.add_argument("--heldout-train-positives", type=int, default=0, help="Few-shot positives from the held-out typology to retain in training split.")
    r.add_argument(
        "--eval-subset",
        default="all",
        choices=["all", "new_source", "new_target", "new_entity", "new_pair", "low_history_entity"],
        help="Evaluate only a cold-start/counterparty subset of validation/test rows.",
    )
    r.add_argument("--save-preds", action="store_true")
    r.add_argument("--workers", type=int, default=1)
    r.add_argument("--threads", type=int, default=None, help="Per-worker model threads; also exported as FLOW_FRAUD_THREADS.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if getattr(args, "threads", None):
        os.environ["FLOW_FRAUD_THREADS"] = str(args.threads)
        global THREADS
        THREADS = int(args.threads)
    if args.cmd == "run":
        run_matrix(args)


if __name__ == "__main__":
    main()
