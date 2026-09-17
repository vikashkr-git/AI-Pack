"""
PackAI - API Integration Tests
Tests all FastAPI endpoints, payload validation, and scientific decision-support outputs.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_foods():
    response = client.get("/api/v1/foods")
    assert response.status_code == 200
    foods = response.json()
    assert len(foods) >= 15
    commodities = [f["commodity"] for f in foods]
    assert "Tomato" in commodities
    assert "Potato Chips" in commodities
    assert "Milk Powder" in commodities
    assert "Frozen Peas" in commodities

def test_get_packaging():
    response = client.get("/api/v1/packaging")
    assert response.status_code == 200
    pkgs = response.json()
    assert len(pkgs) >= 12
    short_names = [p["short_name"] for p in pkgs]
    assert "Metallized_PET_PE" in short_names
    assert "Micro_Perforated_PE" in short_names
    assert "Aluminum_Foil_Laminate" in short_names

def test_validate_input():
    # Test valid commodity autocompletion
    res = client.post("/api/v1/validate-input", json={"commodity": "Tomato"})
    assert res.status_code == 200
    data = res.json()
    assert data["is_valid"] is True
    assert data["suggested_values"]["category"] == "Fresh Produce"
    assert data["suggested_values"]["moisture_pct"] == 94.5

    # Test moisture > 100% warning
    res_bad = client.post("/api/v1/validate-input", json={"moisture_pct": 105.0})
    assert res_bad.status_code == 200
    data_bad = res_bad.json()
    assert data_bad["is_valid"] is False
    assert any("cannot exceed 100%" in w for w in data_bad["warnings"])

def test_recommend_tomato_fresh_produce():
    payload = {
        "commodity": "Tomato",
        "category": "Fresh Produce",
        "moisture_pct": 94.5,
        "fat_pct": 0.2,
        "protein_pct": 0.9,
        "ph": 4.3,
        "respiration_rate": 18.5,
        "shelf_life_days": 14,
        "storage_temp_c": 12.0,
        "relative_humidity_pct": 90.0,
        "storage_type": "Chilled",
        "transportation": "Refrigerated",
        "optimization_goal": "Balanced"
    }
    res = client.post("/api/v1/recommend", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["top_recommendations"]) == 3
    assert data["scientific_requirements"]["is_fresh_produce"] is True
    assert data["scientific_requirements"]["map_recommendations"]["active_mode"] is True
    # Verify breathable / micro-perforated recommendation
    top_rec = data["top_recommendations"][0]
    assert top_rec["technical_specifications"]["breathable"] is True or top_rec["technical_specifications"]["micro_perforated"] is True

def test_recommend_potato_chips_high_barrier():
    payload = {
        "commodity": "Potato Chips",
        "category": "Snacks",
        "moisture_pct": 2.0,
        "fat_pct": 34.5,
        "protein_pct": 6.5,
        "ph": 6.2,
        "respiration_rate": 0.0,
        "shelf_life_days": 180,
        "storage_temp_c": 22.0,
        "relative_humidity_pct": 50.0,
        "storage_type": "Ambient",
        "transportation": "Long_Distance",
        "optimization_goal": "Performance"
    }
    res = client.post("/api/v1/recommend", json=payload)
    assert res.status_code == 200
    data = res.json()
    top_rec = data["top_recommendations"][0]
    assert "Metallized" in top_rec["name"] or "Barrier" in top_rec["name"]
    assert top_rec["technical_specifications"]["wvtr_value"] <= 1.5

def test_recommend_frozen_peas():
    payload = {
        "commodity": "Frozen Peas",
        "category": "Frozen Vegetable",
        "moisture_pct": 79.0,
        "fat_pct": 0.5,
        "protein_pct": 5.4,
        "ph": 6.5,
        "respiration_rate": 0.0,
        "shelf_life_days": 365,
        "storage_temp_c": -18.0,
        "relative_humidity_pct": 90.0,
        "storage_type": "Frozen",
        "transportation": "Refrigerated"
    }
    res = client.post("/api/v1/recommend", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["scientific_requirements"]["is_frozen"] is True
    top_rec = data["top_recommendations"][0]
    assert top_rec["technical_specifications"]["min_temperature_c"] <= -18.0

def test_get_sources_and_model_info():
    res_src = client.get("/api/v1/sources")
    assert res_src.status_code == 200
    sources = res_src.json()
    assert len(sources) >= 5
    assert any("USDA" in s["source_name"] for s in sources)
    assert any("Kader" in str(s.get("authors", "")) or "Kader" in str(s.get("title", "")) for s in sources)

    res_mod = client.get("/api/v1/model-info")
    assert res_mod.status_code == 200
    model_info = res_mod.json()
    assert model_info["model_status"] == "Ready / Production"
    assert "feature_importances" in model_info
    assert "dataset_audit_summary" in model_info
