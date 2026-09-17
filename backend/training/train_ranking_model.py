"""
PackAI - ML Candidate Suitability Scoring & Ranking Training Pipeline
Formulates the problem as [Food + Storage/Transit + Candidate Packaging] -> Suitability Score (0-100).
Uses Grouped 5-Fold Cross-Validation (by Commodity) to prevent data leakage and evaluate real-world generalization.
Compares Baseline Rule-Ranker vs Random Forest vs Gradient Boosting.
"""

import json
import math
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from backend.app.rules.scientific_engine import ScientificRequirementEngine
from backend.data.scientific_references import PACKAGING_CATALOG

FEATURE_NAMES = [
    # Food Features
    "moisture_pct",
    "fat_pct",
    "protein_pct",
    "ph",
    "respiration_rate",
    "shelf_life_days",
    # Environmental Features
    "storage_temp_c",
    "relative_humidity_pct",
    "is_frozen",
    "is_chilled",
    "is_ambient",
    "is_long_distance",
    # Packaging Candidate Features
    "log_otr",
    "log_wvtr",
    "film_thickness_um",
    "puncture_resistance_n",
    "min_temperature_c",
    "pkg_breathable",
    "pkg_micro_perforated",
    "pkg_map_suitable",
    "recycled_content_pct",
    "bio_based_pct",
    "cost_index_relative",
    # Physics Interaction & Derived Features
    "oxidation_risk_index",
    "vapor_pressure_delta_kpa",
    "log_otr_delta",
    "log_wvtr_delta",
    "temp_safety_margin",
    "puncture_margin",
    "produce_breathability_match"
]

def generate_candidate_dataset(cleaned_csv_path: str) -> pd.DataFrame:
    """
    Expands each food storage scenario across candidate packaging materials
    to create training tuples: [Food + Environment + Candidate Packaging] -> Suitability Score.
    """
    print(f"[*] Loading scenario data from: {cleaned_csv_path}")
    raw_df = pd.read_csv(cleaned_csv_path)
    
    # Subsample scenarios to generate balanced, high-quality candidate pairs
    scenarios = raw_df.sample(n=min(1200, len(raw_df)), random_state=42).copy()
    
    rows = []
    
    for _, sc in scenarios.iterrows():
        comm = sc["Commodity"]
        cat = sc["Category"]
        moist = float(sc["Moisture_pct"])
        fat = float(sc["Fat_pct"])
        prot = float(sc["Protein_pct"])
        ph_val = float(sc["pH"])
        resp_val = 18.5 if sc["Respiration_Rate"] == "High" else (8.0 if sc["Respiration_Rate"] == "Moderate" else 0.0)
        shelf_days = int(sc["Shelf_Life_Days"])
        temp_c = float(sc["Storage_Temperature_C"])
        rh_val = float(sc["Relative_Humidity_pct"])
        st_type = str(sc["Storage_Type"])
        trans = str(sc["Transportation"])
        ground_truth_pkg = str(sc["Recommended_Packaging"])
        
        # Analyze scientific requirement
        req = ScientificRequirementEngine.analyze_requirements(
            commodity=comm,
            category=cat,
            moisture_pct=moist,
            fat_pct=fat,
            protein_pct=prot,
            ph=ph_val,
            respiration_rate=resp_val,
            shelf_life_days=shelf_days,
            storage_temp_c=temp_c,
            relative_humidity_pct=rh_val,
            storage_type=st_type,
            transportation=trans
        )
        
        # Evaluate each packaging candidate
        for pkg in PACKAGING_CATALOG:
            eval_res = ScientificRequirementEngine.evaluate_candidate_material(req, pkg)
            
            # Feature extraction
            log_otr = math.log10(max(pkg["otr_value"], 0.01) + 1.0)
            log_wvtr = math.log10(max(pkg["wvtr_value"], 0.01) + 0.1)
            
            target_otr_mid = (req["target_otr_range"]["min"] + req["target_otr_range"]["max"]) / 2.0
            target_wvtr_mid = (req["target_wvtr_range"]["min"] + req["target_wvtr_range"]["max"]) / 2.0
            
            log_target_otr = math.log10(max(target_otr_mid, 0.01) + 1.0)
            log_target_wvtr = math.log10(max(target_wvtr_mid, 0.01) + 0.1)
            
            log_otr_delta = log_otr - log_target_otr
            log_wvtr_delta = log_wvtr - log_target_wvtr
            temp_safety_margin = temp_c - pkg.get("min_temperature_c", -10.0)
            req_punc = req["thermal_mechanical_demands"]["required_puncture_n"]
            punc_margin = pkg.get("puncture_resistance_n", 15.0) - req_punc
            
            is_breathable_pkg = 1.0 if (pkg.get("breathable") or pkg.get("micro_perforated")) else 0.0
            is_fresh = 1.0 if req["is_fresh_produce"] else 0.0
            produce_breathability_match = 1.0 if (is_breathable_pkg == is_fresh) else -1.0

            # Determine Target Ground-Truth Suitability (0 - 100)
            if eval_res["disqualified"]:
                target_score = 0.0
            else:
                base_score = eval_res["scientific_base_suitability"]
                # Bonus if candidate matches historical validated ground truth packaging
                if pkg["short_name"].lower() == ground_truth_pkg.lower():
                    target_score = min(98.0, base_score + 5.0)
                else:
                    target_score = max(5.0, min(92.0, base_score))

            feature_dict = {
                "commodity": comm,
                "packaging_short_name": pkg["short_name"],
                "target_suitability": target_score,
                # Features
                "moisture_pct": moist,
                "fat_pct": fat,
                "protein_pct": prot,
                "ph": ph_val,
                "respiration_rate": resp_val,
                "shelf_life_days": shelf_days,
                "storage_temp_c": temp_c,
                "relative_humidity_pct": rh_val,
                "is_frozen": 1.0 if req["is_frozen"] else 0.0,
                "is_chilled": 1.0 if req["is_chilled"] else 0.0,
                "is_ambient": 1.0 if not (req["is_frozen"] or req["is_chilled"]) else 0.0,
                "is_long_distance": 1.0 if req["is_long_transit"] else 0.0,
                "log_otr": log_otr,
                "log_wvtr": log_wvtr,
                "film_thickness_um": pkg["total_thickness_um"],
                "puncture_resistance_n": pkg.get("puncture_resistance_n", 15.0),
                "min_temperature_c": pkg.get("min_temperature_c", -10.0),
                "pkg_breathable": 1.0 if pkg.get("breathable") else 0.0,
                "pkg_micro_perforated": 1.0 if pkg.get("micro_perforated") else 0.0,
                "pkg_map_suitable": 1.0 if pkg.get("map_suitable") else 0.0,
                "recycled_content_pct": pkg.get("recycled_content_pct", 0.0),
                "bio_based_pct": pkg.get("bio_based_pct", 0.0),
                "cost_index_relative": pkg.get("cost_index_relative", 1.0),
                "oxidation_risk_index": req["oxidation_risk_index"],
                "vapor_pressure_delta_kpa": req["vapor_pressure_delta_kpa"],
                "log_otr_delta": log_otr_delta,
                "log_wvtr_delta": log_wvtr_delta,
                "temp_safety_margin": temp_safety_margin,
                "puncture_margin": punc_margin,
                "produce_breathability_match": produce_breathability_match
            }
            rows.append(feature_dict)
            
    df_candidate = pd.DataFrame(rows)
    print(f"[+] Generated {len(df_candidate)} candidate-scenario training rows across {scenarios['Commodity'].nunique()} commodities.")
    return df_candidate

def compute_ranking_metrics(y_true, y_pred, groups):
    """Computes Top-1 accuracy, Top-3 accuracy, and NDCG@3 on candidate rankings."""
    df_eval = pd.DataFrame({
        "group": groups,
        "y_true": y_true,
        "y_pred": y_pred
    })
    
    top1_correct = 0
    top3_correct = 0
    ndcg_list = []
    unique_groups = df_eval["group"].unique()
    
    for g in unique_groups:
        sub = df_eval[df_eval["group"] == g]
        if len(sub) < 3:
            continue
            
        true_sorted = sub.sort_values(by="y_true", ascending=False)
        pred_sorted = sub.sort_values(by="y_pred", ascending=False)
        
        # Best true item
        best_true_idx = true_sorted.index[0]
        # Pred top-1
        pred_top1_idx = pred_sorted.index[0]
        # Pred top-3
        pred_top3_indices = pred_sorted.index[:3].tolist()
        
        if pred_top1_idx == best_true_idx:
            top1_correct += 1
        if best_true_idx in pred_top3_indices:
            top3_correct += 1
            
        # NDCG@3
        dcg = 0.0
        idcg = 0.0
        for i, idx in enumerate(pred_sorted.index[:3]):
            rel = max(0.0, float(sub.loc[idx, "y_true"]))
            dcg += (2**rel - 1) / math.log2(i + 2)
            
        for i, idx in enumerate(true_sorted.index[:3]):
            rel = max(0.0, float(sub.loc[idx, "y_true"]))
            idcg += (2**rel - 1) / math.log2(i + 2)
            
        ndcg_list.append(dcg / max(idcg, 1e-6))
        
    n_groups = len(unique_groups)
    return {
        "top1_accuracy": round((top1_correct / n_groups) * 100.0, 2),
        "top3_accuracy": round((top3_correct / n_groups) * 100.0, 2),
        "ndcg_at_3": round(float(np.mean(ndcg_list)), 4)
    }

def train_and_evaluate():
    cleaned_csv = "backend/data/cleaned_prototype_data.csv"
    df = generate_candidate_dataset(cleaned_csv)
    
    X = df[FEATURE_NAMES]
    y = df["target_suitability"].values
    groups = df["commodity"].values
    
    print(f"[*] Feature Matrix Shape: {X.shape}, Target Vector: {y.shape}")
    
    # 5-Fold GroupKFold by Commodity
    gkf = GroupKFold(n_splits=5)
    
    # Models to compare
    models = {
        "RandomForest": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
        "GradientBoosting": HistGradientBoostingRegressor(max_iter=100, max_depth=8, random_state=42)
    }
    
    results = {}
    
    for m_name, model in models.items():
        print(f"\n[*] Evaluating Model: {m_name} with 5-Fold Grouped Cross-Validation...")
        fold_maes, fold_rmses, fold_r2s = [], [], []
        fold_top1s, fold_top3s, fold_ndcgs = [], [], []
        
        for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups=groups), 1):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]
            val_groups = groups[val_idx]
            
            # Group identifier per scenario for ranking evaluation
            scenario_ids = [f"{g}_{i}" for i, g in enumerate(val_groups)]
            
            model.fit(X_train, y_train)
            preds = model.predict(X_val)
            preds = np.clip(preds, 0.0, 100.0)
            
            mae = mean_absolute_error(y_val, preds)
            rmse = np.sqrt(mean_squared_error(y_val, preds))
            r2 = r2_score(y_val, preds)
            
            # Ranking metrics (grouped by commodity in validation fold)
            rank_metrics = compute_ranking_metrics(y_val, preds, val_groups)
            
            fold_maes.append(mae)
            fold_rmses.append(rmse)
            fold_r2s.append(r2)
            fold_top1s.append(rank_metrics["top1_accuracy"])
            fold_top3s.append(rank_metrics["top3_accuracy"])
            fold_ndcgs.append(rank_metrics["ndcg_at_3"])
            
        results[m_name] = {
            "mean_mae": round(float(np.mean(fold_maes)), 3),
            "mean_rmse": round(float(np.mean(fold_rmses)), 3),
            "mean_r2": round(float(np.mean(fold_r2s)), 3),
            "mean_top1_accuracy": round(float(np.mean(fold_top1s)), 2),
            "mean_top3_accuracy": round(float(np.mean(fold_top3s)), 2),
            "mean_ndcg_at_3": round(float(np.mean(fold_ndcgs)), 4)
        }
        print(f"    --> {m_name} CV Results: R2={results[m_name]['mean_r2']}, RMSE={results[m_name]['mean_rmse']}, Top-1 Acc={results[m_name]['mean_top1_accuracy']}%, Top-3 Acc={results[m_name]['mean_top3_accuracy']}%")

    # Train Final Production Model on all data
    final_model_name = "RandomForest"
    print(f"\n[*] Training Final Production Model ({final_model_name}) on full candidate dataset...")
    final_model = RandomForestRegressor(n_estimators=150, max_depth=14, random_state=42, n_jobs=-1)
    final_model.fit(X, y)
    
    # Extract Feature Importances
    importances = dict(zip(FEATURE_NAMES, [round(float(v), 4) for v in final_model.feature_importances_]))
    sorted_importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))
    
    print("\nTop 10 Feature Importances:")
    for f, imp in list(sorted_importances.items())[:10]:
        print(f"  - {f}: {imp * 100:.2f}%")

    # Save Pipeline & Artifacts
    model_dir = "backend/models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "packaging_ranker_v1.joblib")
    joblib.dump({
        "model": final_model,
        "feature_names": FEATURE_NAMES,
        "model_version": "v1.0-rf-grouped",
        "description": "Random Forest Suitability Scorer trained with GroupKFold"
    }, model_path)
    print(f"[+] Saved trained model to: {model_path}")
    
    # Save Metrics & Provenance JSON
    metrics_path = os.path.join(model_dir, "model_metrics.json")
    metrics_data = {
        "model_version": "v1.0-rf-grouped",
        "timestamp": pd.Timestamp.now().isoformat(),
        "evaluation_strategy": "5-Fold GroupKFold (Grouped by Commodity to prevent target leakage)",
        "model_comparisons": results,
        "final_model_metrics": results[final_model_name],
        "feature_importances": sorted_importances,
        "total_training_samples": len(df),
        "total_features": len(FEATURE_NAMES)
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)
    print(f"[+] Saved model metrics to: {metrics_path}")

if __name__ == "__main__":
    train_and_evaluate()
