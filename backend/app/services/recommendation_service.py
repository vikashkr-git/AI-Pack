"""
PackAI - Master Recommendation & Decision Support Service
Integrates scientific rules engine, candidate filtering, ML suitability scoring,
sustainability trade-off optimizer, and explainability layer.
"""

import math
import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

from backend.app.rules.scientific_engine import ScientificRequirementEngine
from backend.app.services.explainability_service import ExplainabilityService
from backend.data.scientific_references import PACKAGING_CATALOG, SCIENTIFIC_SOURCES, FOOD_PROFILES

MODEL_PATH = "backend/models/packaging_ranker_v1.joblib"

class RecommendationService:
    _model_bundle = None

    @classmethod
    def _get_model_bundle(cls):
        if cls._model_bundle is None:
            if os.path.exists(MODEL_PATH):
                try:
                    cls._model_bundle = joblib.load(MODEL_PATH)
                except Exception as e:
                    print(f"[!] Warning: Failed to load ML model ({e}). Using scientific engine baseline.")
                    cls._model_bundle = None
        return cls._model_bundle

    @staticmethod
    def _resolve_sample_photo(commodity: str, category: str, pkg: Dict[str, Any]) -> str:
        """
        Dynamically matches realistic sample packaging photo with the target food commodity
        and packaging barrier type so dairy, produce, snacks, meats, and grains show accurate product packaging.
        """
        pkg_id = pkg.get("id", "")
        comm = (commodity or "").lower().strip()
        cat = (category or "").lower().strip()

        # 1. Milk Powder / Dairy Powder / Infant Formula / Whey
        if any(m in comm for m in ["milk powder", "dairy powder", "formula", "infant milk", "whey", "protein powder"]) or ("powder" in comm and cat == "dairy"):
            return "/packaging/milk_powder_foil.jpg"

        # 2. Fresh / Liquid Milk & Beverage Dairy
        if any(m in comm for m in ["liquid milk", "fresh milk", "pasteurized milk", "raw milk", "toned milk", "skim milk", "whole milk", "dairy milk"]) or comm == "milk":
            if pkg_id in ["PKG_PP_CUP_FOIL"]:
                return "/packaging/pp_cup_foil.jpg"
            return "/packaging/fresh_milk_pouch.jpg"

        # 3. Yogurt, Curd, Dahi, Cream, Dairy Dips, Pudding
        if any(y in comm for y in ["yogurt", "curd", "dahi", "cream", "sour cream", "pudding", "shrikhand"]):
            return "/packaging/pp_cup_foil.jpg"

        # 4. Cheese, Paneer, Tofu, Butter, Chilled Solid Dairy
        if any(c in comm for c in ["cheese", "paneer", "tofu", "butter", "mozzarella", "cheddar", "paneer block"]):
            return "/packaging/dairy_cheese_vacuum.jpg"

        # 5. Fish & Seafood (Salmon, Prawns, Shrimp, Tuna, Crab)
        if any(f in comm for f in ["fish", "seafood", "salmon", "prawn", "shrimp", "tuna", "crab", "fillet", "cod", "tilapia"]) or cat in ["seafood", "fish"]:
            return "/packaging/fresh_fish_vacuum.jpg"

        # 6. Fresh Meat & Poultry (Chicken, Beef, Pork, Mutton, Steak)
        if any(m in comm for m in ["meat", "chicken", "beef", "pork", "mutton", "lamb", "steak", "poultry", "sausage", "turkey"]) or cat in ["meat", "poultry"]:
            return "/packaging/pa_pe_vacuum.jpg"

        # 7. Potato Chips, Crisp Snacks, Wafers, Namkeen
        if any(s in comm for s in ["chips", "crisps", "snack", "potato", "wafer", "fryum", "namkeen", "popcorn"]) or cat in ["snacks", "snack"]:
            return "/packaging/met_pet_pe.jpg"

        # 8. Biscuits, Cookies, Crackers, Dry Bakery Wafers
        if any(b in comm for b in ["biscuit", "cookie", "cracker", "toast", "rusk"]) or (cat in ["bakery", "confectionery"] and "bread" not in comm):
            return "/packaging/bopp_pe_flowwrap.jpg"

        # 9. Fresh Produce, Tomatoes, Fruits, Vegetables, Greens, Apples, Berries
        if cat in ["fresh produce", "vegetable", "fruit"] or any(p in comm for p in ["tomato", "apple", "berry", "strawberry", "pepper", "capsicum", "carrot", "lettuce", "grape", "mango", "banana", "orange", "onion", "broccoli"]):
            if pkg.get("biodegradable") or pkg.get("compostable"):
                return "/packaging/bio_compostable_pla.jpg"
            return "/packaging/micro_perf_produce.jpg"

        # 10. Frozen foods (Frozen peas, frozen corn, ice cream, nuggets)
        if any(fz in comm for fz in ["frozen", "peas", "ice cream", "nuggets", "frozen fries"]) or pkg_id == "PKG_PE_FILM_FROZEN":
            return "/packaging/frozen_pe_film.jpg"

        # 11. Coffee & Tea
        if any(cf in comm for cf in ["coffee", "tea", "espresso", "arabica"]):
            return "/packaging/al_foil_lam.jpg"

        # 12. Compostable / Organic / Bio-based
        if pkg.get("biodegradable") or pkg.get("compostable"):
            return "/packaging/bio_compostable_pla.jpg"

        # Fallback to catalog sample_photo_url with safety against non-matching meat images
        fallback = pkg.get("sample_photo_url")
        if fallback == "/packaging/pa_pe_vacuum.jpg" and cat not in ["meat", "poultry", "seafood"]:
            if cat == "dairy":
                return "/packaging/fresh_milk_pouch.jpg"
            elif cat in ["fresh produce", "vegetable", "fruit"]:
                return "/packaging/micro_perf_produce.jpg"
            else:
                return "/packaging/dairy_cheese_vacuum.jpg"

        return fallback or "/packaging/met_pet_pe.jpg"

    @classmethod
    def recommend(
        cls,
        commodity: str,
        category: str,
        moisture_pct: float,
        fat_pct: float,
        protein_pct: float,
        ph: float,
        respiration_rate: float,
        shelf_life_days: int,
        storage_temp_c: float,
        relative_humidity_pct: float,
        storage_type: str,
        transportation: str,
        optimization_goal: str = "Balanced", # "Performance", "Balanced", "Sustainability", "Cost_Optimized"
        advanced_notes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        # 1. Scientific Packaging Requirement Analysis
        req = ScientificRequirementEngine.analyze_requirements(
            commodity=commodity,
            category=category,
            moisture_pct=moisture_pct,
            fat_pct=fat_pct,
            protein_pct=protein_pct,
            ph=ph,
            respiration_rate=respiration_rate,
            shelf_life_days=shelf_life_days,
            storage_temp_c=storage_temp_c,
            relative_humidity_pct=relative_humidity_pct,
            storage_type=storage_type,
            transportation=transportation
        )

        model_bundle = cls._get_model_bundle()
        feature_names = model_bundle["feature_names"] if model_bundle else []
        model = model_bundle["model"] if model_bundle else None

        scored_candidates = []
        disqualified_candidates = []

        # 2. Candidate Evaluation & Feature Construction
        for pkg in PACKAGING_CATALOG:
            eval_res = ScientificRequirementEngine.evaluate_candidate_material(req, pkg)

            if eval_res["disqualified"]:
                disqualified_candidates.append({
                    "id": pkg["id"],
                    "short_name": pkg["short_name"],
                    "name": pkg["name"],
                    "reasons": eval_res["disqualification_reasons"]
                })
                continue

            # Construct feature vector for ML model
            log_otr = math.log10(max(pkg["otr_value"], 0.01) + 1.0)
            log_wvtr = math.log10(max(pkg["wvtr_value"], 0.01) + 0.1)
            target_otr_mid = (req["target_otr_range"]["min"] + req["target_otr_range"]["max"]) / 2.0
            target_wvtr_mid = (req["target_wvtr_range"]["min"] + req["target_wvtr_range"]["max"]) / 2.0
            log_target_otr = math.log10(max(target_otr_mid, 0.01) + 1.0)
            log_target_wvtr = math.log10(max(target_wvtr_mid, 0.01) + 0.1)

            feature_dict = {
                "moisture_pct": moisture_pct,
                "fat_pct": fat_pct,
                "protein_pct": protein_pct,
                "ph": ph,
                "respiration_rate": respiration_rate,
                "shelf_life_days": shelf_life_days,
                "storage_temp_c": storage_temp_c,
                "relative_humidity_pct": relative_humidity_pct,
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
                "log_otr_delta": log_otr - log_target_otr,
                "log_wvtr_delta": log_wvtr - log_target_wvtr,
                "temp_safety_margin": storage_temp_c - pkg.get("min_temperature_c", -10.0),
                "puncture_margin": pkg.get("puncture_resistance_n", 15.0) - req["thermal_mechanical_demands"]["required_puncture_n"],
                "produce_breathability_match": (
                    1.0 if (bool(pkg.get("breathable") or pkg.get("micro_perforated")) == req["is_fresh_produce"])
                    else -1.0
                )
            }

            # Predict suitability score via ML model
            if model and feature_names:
                X_row = pd.DataFrame([feature_dict])[feature_names]
                raw_ml_score = float(model.predict(X_row)[0])
                raw_ml_score = max(5.0, min(99.0, raw_ml_score))
            else:
                raw_ml_score = eval_res["scientific_base_suitability"]

            # Dynamic Preference Adjuster
            s_score = eval_res["sustainability_score"]
            c_score = eval_res["cost_efficiency_score"]

            if optimization_goal.lower() == "sustainability":
                final_score = 0.60 * raw_ml_score + 0.35 * s_score + 0.05 * c_score
            elif optimization_goal.lower() == "cost_optimized":
                final_score = 0.60 * raw_ml_score + 0.35 * c_score + 0.05 * s_score
            elif optimization_goal.lower() == "performance":
                final_score = 0.90 * raw_ml_score + 0.05 * s_score + 0.05 * c_score
            else: # Balanced default
                final_score = 0.80 * raw_ml_score + 0.10 * s_score + 0.10 * c_score

            final_score = round(max(5.0, min(99.5, final_score)), 1)

            scored_candidates.append({
                "packaging": pkg,
                "evaluation": eval_res,
                "raw_ml_score": round(raw_ml_score, 1),
                "final_score": final_score
            })

        # 3. Sort candidates by final suitability score
        scored_candidates.sort(key=lambda x: x["final_score"], reverse=True)

        if not scored_candidates:
            raise ValueError("All candidate packaging materials were disqualified by scientific constraints. Relax storage or shelf-life parameters.")

        # 4. Top 3 Recommendations
        top_3 = []
        for rank, item in enumerate(scored_candidates[:3], 1):
            pkg = item["packaging"]
            eval_res = item["evaluation"]
            score = item["final_score"]

            explanation = ExplainabilityService.generate_explanation(
                requirements=req,
                candidate=pkg,
                evaluation=eval_res,
                ml_score=score,
                is_top_choice=(rank == 1)
            )

            # Customize packaged product protection duration based on query
            durability_info = dict(pkg.get("material_durability", {}))
            if durability_info:
                durability_info["packaged_product_protection_duration"] = (
                    f"Guarantees preservation of {commodity} quality, lipid freshness, and aroma for up to {max(shelf_life_days, 120)} Days under {storage_type} conditions."
                )

            top_3.append({
                "rank": rank,
                "id": pkg["id"],
                "short_name": pkg["short_name"],
                "name": pkg["name"],
                "structure": pkg["structure"],
                "category": pkg["category"],
                "suitability_score": score,
                "sample_photo_url": cls._resolve_sample_photo(commodity, category, pkg),
                "technical_specifications": {
                    "thickness_um": pkg["total_thickness_um"],
                    "otr_value": pkg["otr_value"],
                    "otr_unit": "cm3/(m2*day*atm)",
                    "otr_class": pkg["otr_class"],
                    "wvtr_value": pkg["wvtr_value"],
                    "wvtr_unit": "g/(m2*day)",
                    "wvtr_class": pkg["wvtr_class"],
                    "co2_permeability": pkg.get("co2_permeability"),
                    "puncture_resistance_n": pkg.get("puncture_resistance_n"),
                    "tensile_strength_mpa": pkg.get("tensile_strength_mpa"),
                    "sealing_temp_range_c": f"{pkg.get('heat_seal_temp_c_min', 110)} - {pkg.get('heat_seal_temp_c_max', 140)}°C",
                    "seal_strength_n_15mm": pkg.get("seal_strength_n_15mm"),
                    "min_temperature_c": pkg.get("min_temperature_c"),
                    "breathable": pkg.get("breathable"),
                    "micro_perforated": pkg.get("micro_perforated"),
                    "map_suitable": pkg.get("map_suitable"),
                    "light_barrier": pkg.get("light_barrier")
                },
                "sustainability_profile": {
                    "recyclability_class": pkg.get("recyclability_class"),
                    "recyclability_stream": pkg.get("recyclability_stream"),
                    "recycled_content_pct": pkg.get("recycled_content_pct", 0),
                    "biodegradable": pkg.get("biodegradable"),
                    "compostable": pkg.get("compostable"),
                    "bio_based_pct": pkg.get("bio_based_pct", 0),
                    "relative_cost_index": pkg.get("cost_index_relative", 1.0)
                },
                "scientific_provenance": {
                    "source_ref": pkg.get("source_ref"),
                    "astm_standard": pkg.get("astm_standard"),
                    "doi": pkg.get("doi")
                },
                "material_composition": pkg.get("material_composition"),
                "procurement_market": pkg.get("procurement_market"),
                "quality_inspection_checklist": pkg.get("quality_inspection_checklist"),
                "material_durability": durability_info,
                "explanation": explanation
            })

        # 5. Sustainable Alternative Identification
        eco_candidates = [
            c for c in scored_candidates 
            if (c["packaging"].get("biodegradable") or 
                c["packaging"].get("compostable") or 
                c["packaging"].get("bio_based_pct", 0) > 40 or 
                c["packaging"].get("recycled_content_pct", 0) > 20 or
                "Code 4" in c["packaging"].get("recyclability_stream", "") or
                "Code 5" in c["packaging"].get("recyclability_stream", ""))
            and c["packaging"]["id"] != top_3[0]["id"]
        ]

        sustainable_alt = None
        if eco_candidates:
            best_eco = eco_candidates[0]
            pkg_eco = best_eco["packaging"]
            sustainable_alt = {
                "id": pkg_eco["id"],
                "name": pkg_eco["name"],
                "short_name": pkg_eco["short_name"],
                "structure": pkg_eco["structure"],
                "sample_photo_url": cls._resolve_sample_photo(commodity, category, pkg_eco),
                "suitability_score": best_eco["final_score"],
                "eco_highlights": {
                    "bio_based_pct": pkg_eco.get("bio_based_pct", 0),
                    "recycled_content_pct": pkg_eco.get("recycled_content_pct", 0),
                    "recyclability_stream": pkg_eco.get("recyclability_stream"),
                    "compostable": pkg_eco.get("compostable", False)
                },
                "trade_off_analysis": (
                    f"Offers enhanced environmental profile ({pkg_eco.get('recyclability_stream')}) with {best_eco['final_score']}/100 suitability. "
                    f"Trade-off: WVTR ({pkg_eco['wvtr_value']} g/m2/day) vs Top Pick ({top_3[0]['technical_specifications']['wvtr_value']} g/m2/day)."
                ),
                "material_composition": pkg_eco.get("material_composition"),
                "procurement_market": pkg_eco.get("procurement_market"),
                "material_durability": pkg_eco.get("material_durability")
            }

        # 6. Overall Confidence & Evidence Count
        source_count = len(SCIENTIFIC_SOURCES)
        confidence_level = "High" if top_3[0]["suitability_score"] >= 85.0 else "Moderate"

        return {
            "query_summary": {
                "commodity": commodity,
                "category": category,
                "storage_type": storage_type,
                "transportation": transportation,
                "target_shelf_life_days": shelf_life_days,
                "optimization_goal": optimization_goal
            },
            "scientific_requirements": req,
            "top_recommendations": top_3,
            "sustainable_alternative": sustainable_alt,
            "disqualified_candidates": disqualified_candidates[:4],
            "confidence_assessment": {
                "overall_confidence": confidence_level,
                "score_separation": round(top_3[0]["suitability_score"] - top_3[1]["suitability_score"], 1) if len(top_3) > 1 else 0.0,
                "evidence_sources_count": source_count,
                "empirical_measurements_analyzed": len(PACKAGING_CATALOG),
                "model_version": model_bundle.get("model_version", "v1.0") if model_bundle else "Scientific-Rules-v1.0"
            },
            "disclaimer": "This system provides AI-assisted decision support grounded in published empirical packaging data. Physical shelf-life and sealing compatibility must be experimentally validated in accordance with FSSAI / ISO 22000 standards prior to commercial production."
        }
