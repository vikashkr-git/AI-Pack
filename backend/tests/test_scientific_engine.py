"""
PackAI - Test Suite for Scientific Requirement Engine
Validates physics calculations, barrier demands, and candidate material evaluations.
"""

import pytest
from backend.app.rules.scientific_engine import ScientificRequirementEngine
from backend.data.scientific_references import PACKAGING_CATALOG

def test_tomato_produce_respiration():
    """Tomato requires breathable / micro-perforated film and disallows hermetic foils."""
    req = ScientificRequirementEngine.analyze_requirements(
        commodity="Tomato",
        category="Fresh Produce",
        moisture_pct=94.5,
        fat_pct=0.2,
        protein_pct=0.9,
        ph=4.3,
        respiration_rate=18.5,
        shelf_life_days=14,
        storage_temp_c=12.0,
        relative_humidity_pct=90.0,
        storage_type="Chilled",
        transportation="Refrigerated"
    )
    
    assert req["is_fresh_produce"] is True
    assert req["map_recommendations"]["active_mode"] is True
    assert req["map_recommendations"]["micro_perforation_recommended"] is True
    assert req["target_otr_range"]["min"] >= 3000.0

    # Evaluate Micro-Perforated PE
    micro_perf = next(p for p in PACKAGING_CATALOG if p["short_name"] == "Micro_Perforated_PE")
    res_micro = ScientificRequirementEngine.evaluate_candidate_material(req, micro_perf)
    assert res_micro["disqualified"] is False
    assert res_micro["scientific_base_suitability"] >= 80.0

    # Evaluate Aluminum Foil Laminate (should be disqualified for produce)
    foil = next(p for p in PACKAGING_CATALOG if p["short_name"] == "Aluminum_Foil_Laminate")
    res_foil = ScientificRequirementEngine.evaluate_candidate_material(req, foil)
    assert res_foil["disqualified"] is True
    assert "STRICT DISQUALIFICATION" in res_foil["disqualification_reasons"][0]

def test_potato_chips_oxidation_barrier():
    """Potato chips demand high oxygen and ultra-high moisture barrier."""
    req = ScientificRequirementEngine.analyze_requirements(
        commodity="Potato Chips",
        category="Snacks",
        moisture_pct=2.0,
        fat_pct=34.5,
        protein_pct=6.5,
        ph=6.2,
        respiration_rate=0.0,
        shelf_life_days=180,
        storage_temp_c=22.0,
        relative_humidity_pct=50.0,
        storage_type="Ambient",
        transportation="Long_Distance"
    )
    
    assert req["is_fresh_produce"] is False
    assert req["target_otr_range"]["max"] <= 5.0
    assert req["target_wvtr_range"]["max"] <= 1.5

    # Metallized PET/PE should score very high
    met_pet = next(p for p in PACKAGING_CATALOG if p["short_name"] == "Metallized_PET_PE")
    res_met = ScientificRequirementEngine.evaluate_candidate_material(req, met_pet)
    assert res_met["disqualified"] is False
    assert res_met["scientific_base_suitability"] >= 85.0

    # Micro perforated PE must be disqualified for chips
    micro_perf = next(p for p in PACKAGING_CATALOG if p["short_name"] == "Micro_Perforated_PE")
    res_micro = ScientificRequirementEngine.evaluate_candidate_material(req, micro_perf)
    assert res_micro["disqualified"] is True

def test_milk_powder_barrier():
    """Milk powder requires ultra-high moisture and oxygen barrier (Foil / High Barrier Laminate)."""
    req = ScientificRequirementEngine.analyze_requirements(
        commodity="Milk Powder",
        category="Dairy",
        moisture_pct=3.5,
        fat_pct=26.5,
        protein_pct=26.0,
        ph=6.6,
        respiration_rate=0.0,
        shelf_life_days=365,
        storage_temp_c=22.0,
        relative_humidity_pct=60.0,
        storage_type="Ambient",
        transportation="Long_Distance"
    )
    
    foil = next(p for p in PACKAGING_CATALOG if p["short_name"] == "Aluminum_Foil_Laminate")
    res_foil = ScientificRequirementEngine.evaluate_candidate_material(req, foil)
    assert res_foil["disqualified"] is False
    assert res_foil["scientific_base_suitability"] >= 90.0

def test_frozen_peas_subzero_compatibility():
    """Frozen peas (-18°C) mandate cold-crack resistant flexible film."""
    req = ScientificRequirementEngine.analyze_requirements(
        commodity="Frozen Peas",
        category="Frozen Vegetable",
        moisture_pct=79.0,
        fat_pct=0.5,
        protein_pct=5.4,
        ph=6.5,
        respiration_rate=0.0,
        shelf_life_days=365,
        storage_temp_c=-18.0,
        relative_humidity_pct=90.0,
        storage_type="Frozen",
        transportation="Refrigerated"
    )
    
    assert req["is_frozen"] is True
    # PE film should succeed
    pe_film = next(p for p in PACKAGING_CATALOG if p["short_name"] == "PE_Film")
    res_pe = ScientificRequirementEngine.evaluate_candidate_material(req, pe_film)
    assert res_pe["disqualified"] is False
    assert res_pe["scientific_base_suitability"] >= 75.0

    # Breathable PP with min_temp = 5°C must be disqualified
    pp = next(p for p in PACKAGING_CATALOG if p["short_name"] == "Breathable_PP")
    res_pp = ScientificRequirementEngine.evaluate_candidate_material(req, pp)
    assert res_pp["disqualified"] is True
    assert any("TEMPERATURE FAILURE" in r for r in res_pp["disqualification_reasons"])

if __name__ == "__main__":
    pytest.main(["-v", "backend/tests/test_scientific_engine.py"])
