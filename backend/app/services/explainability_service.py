"""
PackAI - Explainable AI (XAI) & Scientific Decision Support Service
Generates physics-backed explanations, barrier radar dimensions, and alternative trade-offs.
"""

from typing import Dict, List, Any

class ExplainabilityService:

    @staticmethod
    def generate_explanation(
        requirements: Dict[str, Any],
        candidate: Dict[str, Any],
        evaluation: Dict[str, Any],
        ml_score: float,
        is_top_choice: bool = True
    ) -> Dict[str, Any]:
        """
        Synthesizes human-readable scientific reasoning and trade-off points.
        """
        reasons_why = []
        cautions_limitations = []

        is_produce = requirements["is_fresh_produce"]
        is_frozen = requirements["is_frozen"]

        # 1. Respiration & Gas Exchange Explanation
        if is_produce:
            if candidate.get("micro_perforated"):
                reasons_why.append("Engineered laser micro-perforations permit controlled O2/CO2 flux, preventing anaerobic fermentation.")
            elif candidate.get("breathable"):
                reasons_why.append("Breathable polymer matrix allows equilibrium headspace gas exchange matching produce respiration rate.")
        else:
            if candidate.get("otr_value", 100.0) <= 2.5:
                reasons_why.append(f"Ultra-high oxygen barrier (OTR: {candidate['otr_value']} cm3/m2/day) suppresses lipid auto-oxidation.")
            elif candidate.get("otr_value", 100.0) <= 35.0:
                reasons_why.append(f"High oxygen barrier (OTR: {candidate['otr_value']} cm3/m2/day) retards aerobic deterioration.")

        # 2. Moisture Barrier Explanation
        wvtr = candidate.get("wvtr_value", 10.0)
        target_wvtr_max = requirements["target_wvtr_range"]["max"]
        if not is_produce:
            if wvtr <= 1.0:
                reasons_why.append(f"Hermetic moisture barrier (WVTR: {wvtr} g/m2/day) prevents moisture sorption and texture softening.")
            elif wvtr <= target_wvtr_max:
                reasons_why.append(f"WVTR ({wvtr} g/m2/day) satisfies the target threshold ({target_wvtr_max} g/m2/day).")
        else:
            reasons_why.append(f"Moisture transmission rate ({wvtr} g/m2/day) mitigates internal condensation droplets without excessive moisture loss.")

        # 3. Thermal & Mechanical Explanation
        if is_frozen:
            reasons_why.append(f"Sub-zero ductile flexibility down to {candidate.get('min_temperature_c', -10)}°C prevents flex-cracking and freezer burn.")
        
        if requirements["is_long_transit"]:
            punc = candidate.get("puncture_resistance_n", 15.0)
            if punc >= 25.0:
                reasons_why.append(f"High puncture resistance ({punc} N) withstands severe vibration and abrasion during long-distance transit.")

        # 4. Sustainability & Circularity Notes
        if candidate.get("biodegradable") or candidate.get("compostable"):
            reasons_why.append("Certified biodegradable/compostable structure minimizes persistent microplastic pollution.")
        elif candidate.get("recycled_content_pct", 0) > 0:
            reasons_why.append(f"Contains {candidate['recycled_content_pct']}% post-consumer recycled (PCR) content.")
        elif "Code 4" in candidate.get("recyclability_stream", "") or "Code 5" in candidate.get("recyclability_stream", ""):
            reasons_why.append(f"Compatible with municipal mono-material recycling ({candidate.get('recyclability_stream')}).")

        # 5. Limitations & Trade-offs
        if candidate.get("cost_index_relative", 1.0) >= 1.6:
            cautions_limitations.append("Higher unit material cost relative to standard commodity packaging.")
        if candidate.get("biodegradable") and not is_produce:
            cautions_limitations.append("Compostable biopolymers exhibit higher moisture transmission compared to multi-layer barrier foil.")
        if "Code 7" in candidate.get("recyclability_stream", ""):
            cautions_limitations.append("Multi-material composite structure requires specialized mechanical delamination or chemical recycling.")

        # Radar chart metrics (0 - 100 scale)
        radar_metrics = {
            "oxygen_barrier": evaluation.get("otr_compatibility_score", 70.0),
            "moisture_barrier": evaluation.get("wvtr_compatibility_score", 70.0),
            "mechanical_strength": evaluation.get("mechanical_score", 70.0),
            "thermal_stability": evaluation.get("thermal_score", 80.0),
            "sustainability": evaluation.get("sustainability_score", 50.0),
            "cost_efficiency": evaluation.get("cost_efficiency_score", 60.0)
        }

        return {
            "reasons_why": reasons_why,
            "cautions_limitations": cautions_limitations,
            "radar_metrics": radar_metrics,
            "suitability_score": round(ml_score, 1),
            "is_top_choice": is_top_choice
        }
