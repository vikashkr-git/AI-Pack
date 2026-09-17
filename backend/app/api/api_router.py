"""
PackAI - REST API Endpoints Router
"""

import json
import os
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.database.models import Food, PackagingMaterial, Source, RecommendationLog
from backend.app.schemas.schemas import (
    FoodInputRequest, RecommendationResponse, ValidationRequest, ValidationResponse
)
from backend.app.services.recommendation_service import RecommendationService
from backend.data.scientific_references import FOOD_PROFILES

api_router = APIRouter()

@api_router.get("/foods", response_model=List[Dict[str, Any]])
def get_all_foods(db: Session = Depends(get_db)):
    """Retrieve catalog of all standardized food commodities and proximate profiles."""
    foods = db.query(Food).all()
    results = []
    for f in foods:
        results.append({
            "id": f.id,
            "commodity": f.commodity,
            "category": f.category,
            "moisture_pct": f.moisture_pct,
            "fat_pct": f.fat_pct,
            "protein_pct": f.protein_pct,
            "ph": f.ph,
            "respiration_rate_val": f.respiration_rate_val,
            "respiration_rate_class": f.respiration_rate_class,
            "standard_shelf_life_days": f.standard_shelf_life_days,
            "optimal_storage_type": f.optimal_storage_type,
            "optimal_temp_c": f.optimal_temp_c,
            "optimal_rh_pct": f.optimal_rh_pct,
            "map_suitable": f.map_suitable,
            "optimal_map_gas": f.optimal_map_gas,
            "primary_degradation_modes": f.primary_degradation_modes,
            "critical_barrier_needs": f.critical_barrier_needs
        })
    return results

from backend.data.scientific_references import FOOD_PROFILES, PACKAGING_CATALOG

@api_router.get("/packaging", response_model=List[Dict[str, Any]])
def get_all_packaging(db: Session = Depends(get_db)):
    """Retrieve catalog of empirical packaging structures, barrier specifications, sample photos, and market data."""
    return PACKAGING_CATALOG

@api_router.post("/validate-input", response_model=ValidationResponse)
def validate_food_input(req: ValidationRequest):
    """
    Validates physical consistency of inputs and suggests known USDA defaults.
    """
    warnings = []
    is_valid = True
    suggested = None

    if req.commodity and req.commodity in FOOD_PROFILES:
        profile = FOOD_PROFILES[req.commodity]
        suggested = {
            "commodity": profile["commodity"],
            "category": profile["category"],
            "moisture_pct": profile["moisture_pct"],
            "fat_pct": profile["fat_pct"],
            "protein_pct": profile["protein_pct"],
            "ph": profile["ph"],
            "respiration_rate": profile["respiration_rate_val"],
            "shelf_life_days": profile["standard_shelf_life_days"],
            "storage_temp_c": profile["optimal_temp_c"],
            "relative_humidity_pct": profile["optimal_rh_pct"],
            "storage_type": profile["optimal_storage_type"]
        }

    # Physical checks
    if req.moisture_pct is not None:
        if req.moisture_pct > 100.0:
            is_valid = False
            warnings.append(f"Moisture ({req.moisture_pct}%) cannot exceed 100%. Known biological limit is ~95%.")
        elif req.moisture_pct < 0.0:
            is_valid = False
            warnings.append("Moisture cannot be negative.")

    if req.moisture_pct is not None and req.fat_pct is not None and req.protein_pct is not None:
        total = req.moisture_pct + req.fat_pct + req.protein_pct
        if total > 100.0:
            warnings.append(f"Sum of Moisture ({req.moisture_pct}%) + Fat ({req.fat_pct}%) + Protein ({req.protein_pct}%) = {total:.1f}% exceeds 100%. Please check proximate entries.")

    if req.storage_type and req.storage_temp_c is not None:
        if req.storage_type.lower() == "frozen" and req.storage_temp_c > -5.0:
            warnings.append(f"Storage type is 'Frozen' but temperature is {req.storage_temp_c}°C (typically <= -10°C).")
        elif req.storage_type.lower() == "chilled" and (req.storage_temp_c < -2.0 or req.storage_temp_c > 15.0):
            warnings.append(f"Chilled storage is typically between 0°C and 10°C (current: {req.storage_temp_c}°C).")

    return ValidationResponse(
        is_valid=is_valid,
        warnings=warnings,
        suggested_values=suggested
    )

@api_router.post("/recommend", response_model=RecommendationResponse)
def generate_recommendation(payload: FoodInputRequest, db: Session = Depends(get_db)):
    """
    Main Hybrid AI Recommendation Engine:
    Physics constraints -> Candidate filtering -> ML scoring -> Top 3 -> Explainability -> Provenance
    """
    try:
        result = RecommendationService.recommend(
            commodity=payload.commodity,
            category=payload.category,
            moisture_pct=payload.moisture_pct,
            fat_pct=payload.fat_pct,
            protein_pct=payload.protein_pct,
            ph=payload.ph,
            respiration_rate=payload.respiration_rate,
            shelf_life_days=payload.shelf_life_days,
            storage_temp_c=payload.storage_temp_c,
            relative_humidity_pct=payload.relative_humidity_pct,
            storage_type=payload.storage_type,
            transportation=payload.transportation,
            optimization_goal=payload.optimization_goal,
            advanced_notes=payload.advanced_notes
        )

        # Log recommendation to DB asynchronously / safely
        try:
            top_rec = result["top_recommendations"][0]
            log_entry = RecommendationLog(
                commodity=payload.commodity,
                category=payload.category,
                moisture_pct=payload.moisture_pct,
                fat_pct=payload.fat_pct,
                protein_pct=payload.protein_pct,
                ph=payload.ph,
                respiration_rate=payload.respiration_rate,
                shelf_life_days=payload.shelf_life_days,
                storage_temp_c=payload.storage_temp_c,
                relative_humidity_pct=payload.relative_humidity_pct,
                storage_type=payload.storage_type,
                transportation=payload.transportation,
                optimization_goal=payload.optimization_goal,
                top_recommendation_name=top_rec["name"],
                top_suitability_score=top_rec["suitability_score"],
                top_technical_summary=top_rec["technical_specifications"],
                confidence_level=result["confidence_assessment"]["overall_confidence"],
                explanation_summary=" | ".join(top_rec["explanation"]["reasons_why"])
            )
            db.add(log_entry)
            db.commit()
        except Exception as db_err:
            db.rollback()
            print(f"[!] Non-fatal log failure: {db_err}")

        return result

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Recommendation Engine Error: {str(e)}")

@api_router.get("/sources", response_model=List[Dict[str, Any]])
def get_sources(db: Session = Depends(get_db)):
    """Retrieve all peer-reviewed scientific literature sources, DOIs, and test standards."""
    sources = db.query(Source).all()
    results = []
    for s in sources:
        results.append({
            "id": s.id,
            "source_name": s.source_name,
            "title": s.title,
            "authors": s.authors,
            "year": s.year,
            "publisher_or_journal": s.publisher_or_journal,
            "url": s.url,
            "doi": s.doi,
            "scope": s.scope,
            "confidence_score": s.confidence_score
        })
    return results

@api_router.get("/model-info")
def get_model_diagnostics():
    """Retrieve active ML model metadata, evaluation metrics, feature importances, and audit stats."""
    metrics_path = "backend/models/model_metrics.json"
    audit_path = "backend/data/audit_report.json"
    
    metrics = {}
    audit = {}
    
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)
            
    if os.path.exists(audit_path):
        with open(audit_path, "r", encoding="utf-8") as f:
            audit = json.load(f)

    return {
        "model_status": "Ready / Production",
        "model_version": metrics.get("model_version", "v1.0-rf-grouped"),
        "evaluation_strategy": metrics.get("evaluation_strategy"),
        "model_comparisons": metrics.get("model_comparisons"),
        "final_model_metrics": metrics.get("final_model_metrics"),
        "feature_importances": metrics.get("feature_importances"),
        "total_training_samples": metrics.get("total_training_samples"),
        "dataset_audit_summary": {
            "total_raw_rows": audit.get("dataset_metadata", {}).get("total_rows", 5000),
            "flagged_anomalies_count": audit.get("anomalies_detected", {}).get("total_anomalies_flagged", 435),
            "target_leakage_finding": audit.get("target_leakage_audit", {}).get("finding"),
            "architectural_remedy": audit.get("target_leakage_audit", {}).get("architectural_remedy")
        }
    }

@api_router.get("/history", response_model=List[Dict[str, Any]])
def get_recommendation_history(limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve recent queries and recommendation history logs."""
    logs = db.query(RecommendationLog).order_by(RecommendationLog.timestamp.desc()).limit(limit).all()
    results = []
    for l in logs:
        results.append({
            "id": l.id,
            "timestamp": l.timestamp.isoformat() if l.timestamp else None,
            "commodity": l.commodity,
            "category": l.category,
            "storage_type": l.storage_type,
            "transportation": l.transportation,
            "shelf_life_days": l.shelf_life_days,
            "optimization_goal": l.optimization_goal,
            "top_recommendation_name": l.top_recommendation_name,
            "top_suitability_score": l.top_suitability_score,
            "confidence_level": l.confidence_level,
            "explanation_summary": l.explanation_summary
        })
    return results
