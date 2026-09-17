"""
PackAI - Scientific Packaging Requirement Engine
Physics-grounded mass transfer, food degradation kinetics, and respiration equilibrium equations.
"""

import math
from typing import Dict, List, Any, Optional

def calculate_saturation_vapor_pressure(temp_c: float) -> float:
    """Tetens formula for saturation vapor pressure of water in kPa."""
    return 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))

class ScientificRequirementEngine:
    """
    Translates food characteristics, storage parameters, and distribution stress
    into quantitative packaging demands: target OTR, target WVTR, gas permeability,
    thermal ductility, and mechanical puncture thresholds.
    """

    @staticmethod
    def analyze_requirements(
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
        oxidation_sensitivity: str = "Auto",
        moisture_sensitivity: str = "Auto"
    ) -> Dict[str, Any]:
        
        is_fresh_produce = (
            category.lower() in ["fresh produce", "vegetable", "fruit"] or 
            respiration_rate > 2.0
        )
        is_frozen = (storage_type.lower() == "frozen" or storage_temp_c <= -8.0)
        is_chilled = (storage_type.lower() == "chilled" or (-2.0 <= storage_temp_c <= 10.0))
        is_long_transit = (transportation.lower() == "long_distance")

        # -------------------------------------------------------------
        # 1. MOISTURE BARRIER DEMAND (WVTR target in g / m2 * day)
        # -------------------------------------------------------------
        # Estimate water activity (aw) if not directly supplied
        if moisture_pct <= 5.0:
            aw = 0.20 + (moisture_pct / 25.0) # very dry (0.20 - 0.40)
        elif moisture_pct <= 20.0:
            aw = 0.45 + (moisture_pct - 5.0) * 0.02
        else:
            aw = min(0.99, 0.75 + (moisture_pct - 20.0) * 0.003)

        p_sat = calculate_saturation_vapor_pressure(storage_temp_c)
        ambient_rh_fraction = relative_humidity_pct / 100.0
        delta_rh = abs(ambient_rh_fraction - aw)
        vapor_pressure_delta_kpa = p_sat * delta_rh

        # Calculate base WVTR tolerance
        if is_fresh_produce:
            # Produce needs controlled breathability: too low WVTR causes condensation/sweat rot
            target_wvtr_min = 8.0
            target_wvtr_max = 25.0
            wvtr_class_demand = "Moderate / Breathable"
            moisture_risk = "Condensation & mold if hermetic; shriveling if too porous"
        elif moisture_pct < 6.0 and shelf_life_days > 90:
            # Highly hygroscopic crisp food / milk powder
            target_wvtr_min = 0.01
            target_wvtr_max = 1.5
            wvtr_class_demand = "Ultra High Barrier (< 1.5 g/m2/day)"
            moisture_risk = "Severe crispness loss and powder caking"
        elif moisture_pct < 15.0:
            target_wvtr_min = 0.1
            target_wvtr_max = 4.0
            wvtr_class_demand = "High Barrier (< 4.0 g/m2/day)"
            moisture_risk = "Moderate moisture pickup / staling"
        elif is_frozen:
            # Frozen products require high moisture retention to prevent freezer burn (ice sublimation)
            target_wvtr_min = 0.1
            target_wvtr_max = 5.0
            wvtr_class_demand = "High Moisture Retention (< 5.0 g/m2/day)"
            moisture_risk = "Freezer burn and surface desiccation"
        else:
            target_wvtr_min = 0.5
            target_wvtr_max = 10.0
            wvtr_class_demand = "Standard Moisture Barrier"
            moisture_risk = "Standard moisture stability"

        # -------------------------------------------------------------
        # 2. OXYGEN BARRIER DEMAND (OTR target in cm3 / m2 * day * atm)
        # -------------------------------------------------------------
        # Lipid oxidation risk index: fat_pct * (shelf_life_days / 30) * temp_factor
        temp_factor = 2.0 ** ((storage_temp_c - 20.0) / 10.0) if storage_temp_c > 0 else 0.2
        oxidation_index = (fat_pct / 100.0) * (shelf_life_days / 30.0) * temp_factor

        if is_fresh_produce:
            # Fresh produce MUST allow O2 ingress to maintain aerobic metabolism (>1-2% O2)
            target_otr_min = 3000.0
            target_otr_max = 15000.0
            otr_class_demand = "High Gas Permeability (Aerobic Maintenance)"
            oxygen_risk = "Anaerobic fermentation and ethanol production if oxygen blocked"
        elif fat_pct > 15.0 and shelf_life_days >= 60:
            # High fat + long ambient storage -> extreme rancidity risk
            target_otr_min = 0.01
            target_otr_max = 2.5
            otr_class_demand = "Ultra High Barrier (< 2.5 cm3/m2/day)"
            oxygen_risk = "Critical lipid auto-oxidation (rancid hexanal formation)"
        elif fat_pct > 5.0 or category.lower() in ["meat", "dairy", "seafood"]:
            target_otr_min = 0.1
            target_otr_max = 35.0
            otr_class_demand = "High Oxygen Barrier (< 35 cm3/m2/day)"
            oxygen_risk = "Lipid oxidation and aerobic microbial growth"
        elif shelf_life_days > 180:
            target_otr_min = 0.1
            target_otr_max = 50.0
            otr_class_demand = "Moderate-to-High Barrier (< 50 cm3/m2/day)"
            oxygen_risk = "Long-term oxidative degradation"
        else:
            target_otr_min = 1.0
            target_otr_max = 2000.0
            otr_class_demand = "Standard Polyolefin Barrier"
            oxygen_risk = "Low-to-moderate oxygen sensitivity"

        # -------------------------------------------------------------
        # 3. FRESH PRODUCE & MAP RESPIRATION ENGINE
        # -------------------------------------------------------------
        map_recommendations = {}
        if is_fresh_produce:
            # Respiration classification
            if respiration_rate > 20.0:
                resp_severity = "High"
            elif respiration_rate > 10.0:
                resp_severity = "Moderate"
            else:
                resp_severity = "Low"

            map_recommendations = {
                "active_mode": True,
                "respiration_severity": resp_severity,
                "respiration_rate_mg_co2_kg_hr": respiration_rate,
                "breathable_packaging_required": True,
                "micro_perforation_recommended": respiration_rate >= 10.0,
                "recommended_headspace_gas": (
                    "3-5% O2, 3-5% CO2, balance N2" if respiration_rate < 25.0
                    else "2-4% O2, 5-8% CO2, balance N2 (High respiration anti-senescence mix)"
                ),
                "anaerobic_compensation_threshold_o2": 1.5, # Percentage below which fermentation occurs
                "co2_injury_threshold_pct": 10.0,
                "scientific_rationale": (
                    f"Living produce continues respiration consuming O2 and releasing CO2 ({respiration_rate:.1f} mg CO2/kg-hr). "
                    "Hermetic barrier films without micro-perforations cause rapid anaerobiosis (<1% O2), triggering ethanol off-flavor and tissue breakdown."
                )
            }
        else:
            # MAP for non-produce (anti-oxidation / antimicrobial)
            if fat_pct > 15.0 and shelf_life_days > 30:
                map_recommendations = {
                    "active_mode": False,
                    "recommended_headspace_gas": "100% N2 flush (Residual O2 < 0.5%) to arrest lipid oxidation",
                    "map_suitable": True,
                    "scientific_rationale": "Inert nitrogen displacement prevents oxidative rancidity and pillow-pack protects brittle snacks."
                }
            elif category.lower() in ["meat", "seafood"]:
                map_recommendations = {
                    "active_mode": False,
                    "recommended_headspace_gas": "70% O2 / 30% CO2 (for retail red meat bloom) or 70% N2 / 30% CO2 (for extended microbial suppression)",
                    "map_suitable": True,
                    "scientific_rationale": "High CO2 inhibits psychrotrophic bacteria while controlled gas extends fresh shelf life."
                }
            else:
                map_recommendations = {
                    "active_mode": False,
                    "recommended_headspace_gas": "Ambient air or light nitrogen pad",
                    "map_suitable": False,
                    "scientific_rationale": "Standard atmosphere adequate under moisture barrier."
                }

        # -------------------------------------------------------------
        # 4. THERMAL & MECHANICAL CONSTRAINTS
        # -------------------------------------------------------------
        required_min_temp_c = storage_temp_c - 5.0 # Safety buffer
        required_tensile_mpa = 35.0 if is_long_transit else 20.0
        required_puncture_n = 25.0 if is_long_transit else 12.0
        
        thermal_risk = "Standard ambient"
        if is_frozen:
            thermal_risk = f"Sub-zero storage ({storage_temp_c}°C) requires high cold-impact ductility (LLDPE/PA) to avoid flex-cracking"
        elif is_chilled:
            thermal_risk = f"Chilled storage ({storage_temp_c}°C) requires moisture-resistant barrier and anti-fog performance"

        # -------------------------------------------------------------
        # 5. HARD DISQUALIFICATION RULES (Scientific Constraint Filter)
        # -------------------------------------------------------------
        disqualification_criteria = {
            "disallow_non_breathable_for_produce": is_fresh_produce,
            "disallow_brittle_films_for_frozen": is_frozen,
            "min_operational_temp_c": required_min_temp_c,
            "min_puncture_n": required_puncture_n,
            "min_tensile_mpa": required_tensile_mpa
        }

        return {
            "commodity": commodity,
            "category": category,
            "is_fresh_produce": is_fresh_produce,
            "is_frozen": is_frozen,
            "is_chilled": is_chilled,
            "is_long_transit": is_long_transit,
            "water_activity_aw_estimated": round(aw, 3),
            "vapor_pressure_delta_kpa": round(vapor_pressure_delta_kpa, 3),
            "oxidation_risk_index": round(oxidation_index, 3),
            "target_wvtr_range": {"min": target_wvtr_min, "max": target_wvtr_max, "unit": "g/(m2*day)"},
            "wvtr_class_demand": wvtr_class_demand,
            "moisture_risk_analysis": moisture_risk,
            "target_otr_range": {"min": target_otr_min, "max": target_otr_max, "unit": "cm3/(m2*day*atm)"},
            "otr_class_demand": otr_class_demand,
            "oxygen_risk_analysis": oxygen_risk,
            "thermal_mechanical_demands": {
                "min_operating_temp_c": required_min_temp_c,
                "required_puncture_n": required_puncture_n,
                "required_tensile_mpa": required_tensile_mpa,
                "thermal_risk": thermal_risk
            },
            "map_recommendations": map_recommendations,
            "disqualification_criteria": disqualification_criteria
        }

    @staticmethod
    def evaluate_candidate_material(
        requirements: Dict[str, Any],
        packaging: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluates a candidate packaging material against the calculated scientific demands.
        Returns hard disqualification status, penalty deductions, and feature compatibility vector.
        """
        disqualified = False
        reasons = []
        
        # Hard Rule 1: Fresh produce MUST NOT be packaged in hermetic non-breathable films
        if requirements["is_fresh_produce"] and not (packaging.get("breathable") or packaging.get("micro_perforated")):
            disqualified = True
            reasons.append("STRICT DISQUALIFICATION: Living produce requires aerobic gas exchange; hermetic barrier causes anaerobic rot.")

        # Hard Rule 2: Non-produce items MUST NOT be placed in micro-perforated produce bags
        if not requirements["is_fresh_produce"] and packaging.get("micro_perforated"):
            disqualified = True
            reasons.append("DISQUALIFICATION: Micro-perforated film allows unrestricted oxygen/moisture ingress, ruining dry/processed foods.")

        # Hard Rule 3: Cold temperature compatibility
        min_temp_limit = packaging.get("min_temperature_c", -10.0)
        req_min_temp = requirements["thermal_mechanical_demands"]["min_operating_temp_c"]
        if min_temp_limit > req_min_temp:
            disqualified = True
            reasons.append(f"TEMPERATURE FAILURE: Material brittle limit ({min_temp_limit}°C) exceeds storage requirement ({req_min_temp}°C).")

        # Hard Rule 4: Critical puncture resistance for long-distance transit
        punc_res = packaging.get("puncture_resistance_n", 15.0)
        req_punc = requirements["thermal_mechanical_demands"]["required_puncture_n"]
        if requirements["is_long_transit"] and punc_res < (req_punc * 0.7):
            reasons.append(f"MECHANICAL RISK: Low puncture resistance ({punc_res}N) vs transit demand ({req_punc}N).")

        # Hard Rule 5: Physical Form & Category Incompatibility (e.g. Dairy / Liquids vs Dry Snack Pouches)
        category = requirements.get("category", "").lower()
        commodity = requirements.get("commodity", "").lower()
        pkg_id = packaging.get("id", "")

        is_dairy = category == "dairy" or any(d in commodity for d in ["milk", "yogurt", "curd", "cheese", "paneer", "butter", "cream"])
        if is_dairy:
            # Semi-solid or liquid dairy (Yogurt, Curd, Cream, Pudding)
            if any(y in commodity for y in ["yogurt", "curd", "cream", "pudding", "sour cream"]):
                if pkg_id in ["PKG_MET_PET_PE", "PKG_BOPP_PE", "PKG_HDPE_WOVEN", "PKG_LDPE_BAG", "PKG_RPET_PE_CIRCULAR"]:
                    disqualified = True
                    reasons.append("PHYSICAL INCOMPATIBILITY: Flexible dry snack/biscuit pouch cannot contain semi-solid/liquid dairy; rigid thermoformed cups with peelable hermetic lids (PP Cup + Foil Lid) required.")
            # Chilled fatty/solid dairy (Cheese, Paneer, Butter)
            elif any(c in commodity for c in ["cheese", "paneer", "butter"]):
                if pkg_id in ["PKG_MET_PET_PE", "PKG_BOPP_PE", "PKG_HDPE_WOVEN"]:
                    disqualified = True
                    reasons.append("PHYSICAL INCOMPATIBILITY: Dry snack laminates are incompatible with greasy/chilled dairy; vacuum barrier pouches (PA/PE) or aluminum foil wraps required.")
            # Milk Powder / Infant Formula (Ultra-hygroscopic)
            elif "powder" in commodity:
                if pkg_id in ["PKG_MET_PET_PE", "PKG_BOPP_PE", "PKG_LDPE_BAG", "PKG_HDPE_WOVEN"]:
                    disqualified = True
                    reasons.append("BARRIER INCOMPATIBILITY: Standard dry snack/bread polyfilm lacks 100% total moisture opacity required to prevent milk powder caking; solid foil laminates required.")

        # Compatibility scoring components (0 to 100)
        otr_val = packaging.get("otr_value", 100.0)
        wvtr_val = packaging.get("wvtr_value", 5.0)
        
        target_otr = requirements["target_otr_range"]
        target_wvtr = requirements["target_wvtr_range"]

        # OTR compatibility
        if requirements["is_fresh_produce"]:
            # Higher OTR is preferred for fresh produce
            if otr_val >= target_otr["min"]:
                otr_score = 100.0
            else:
                otr_score = max(0.0, 100.0 - (target_otr["min"] - otr_val) / 50.0)
        else:
            # Lower OTR is preferred for non-produce sensitive foods
            if otr_val <= target_otr["max"]:
                otr_score = 100.0
            else:
                ratio = otr_val / max(target_otr["max"], 0.1)
                otr_score = max(10.0, 100.0 - math.log10(ratio) * 30.0)

        # WVTR compatibility
        if requirements["is_fresh_produce"]:
            # Need moderate WVTR
            if target_wvtr["min"] <= wvtr_val <= target_wvtr["max"]:
                wvtr_score = 100.0
            else:
                wvtr_score = max(30.0, 100.0 - abs(wvtr_val - 15.0) * 4.0)
        else:
            # Need low WVTR
            if wvtr_val <= target_wvtr["max"]:
                wvtr_score = 100.0
            else:
                ratio = wvtr_val / max(target_wvtr["max"], 0.1)
                wvtr_score = max(10.0, 100.0 - math.log10(ratio) * 35.0)

        # Mechanical score
        mech_score = min(100.0, (punc_res / max(req_punc, 1.0)) * 75.0 + 25.0)

        # Thermal score
        temp_margin = min_temp_limit - req_min_temp
        thermal_score = 100.0 if temp_margin <= 0 else max(0.0, 100.0 - temp_margin * 10.0)

        # Sustainability score
        sustainability_score = 40.0 # baseline
        if packaging.get("biodegradable") or packaging.get("compostable"):
            sustainability_score += 40.0
        if packaging.get("bio_based_pct", 0) > 50:
            sustainability_score += 15.0
        if packaging.get("recycled_content_pct", 0) > 10:
            sustainability_score += 15.0
        if "Code 4" in packaging.get("recyclability_stream", "") or "Code 5" in packaging.get("recyclability_stream", ""):
            sustainability_score += 15.0
        sustainability_score = min(100.0, sustainability_score)

        # Cost efficiency score (higher is more economical, 1.0 = base)
        cost_idx = packaging.get("cost_index_relative", 1.0)
        cost_score = max(20.0, min(100.0, 100.0 - (cost_idx - 1.0) * 50.0))

        # Scientific baseline suitability
        if disqualified:
            base_suitability = 0.0
        else:
            base_suitability = (
                0.35 * otr_score +
                0.30 * wvtr_score +
                0.20 * mech_score +
                0.15 * thermal_score
            )
            base_suitability = max(5.0, min(100.0, base_suitability))

        return {
            "disqualified": disqualified,
            "disqualification_reasons": reasons,
            "otr_compatibility_score": round(otr_score, 1),
            "wvtr_compatibility_score": round(wvtr_score, 1),
            "mechanical_score": round(mech_score, 1),
            "thermal_score": round(thermal_score, 1),
            "sustainability_score": round(sustainability_score, 1),
            "cost_efficiency_score": round(cost_score, 1),
            "scientific_base_suitability": round(base_suitability, 1)
        }
