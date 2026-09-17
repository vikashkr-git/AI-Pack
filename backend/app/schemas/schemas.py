"""
PackAI - Pydantic Request & Response Validation Schemas
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, field_validator

class FoodInputRequest(BaseModel):
    commodity: str = Field(..., example="Potato Chips")
    category: str = Field(..., example="Snacks")
    moisture_pct: float = Field(..., ge=0.0, le=100.0, example=2.0)
    fat_pct: float = Field(..., ge=0.0, le=100.0, example=34.5)
    protein_pct: float = Field(..., ge=0.0, le=100.0, example=6.5)
    ph: float = Field(..., ge=1.0, le=14.0, example=6.2)
    respiration_rate: float = Field(0.0, ge=0.0, example=0.0)
    shelf_life_days: int = Field(..., ge=1, le=1500, example=180)
    storage_temp_c: float = Field(..., ge=-40.0, le=60.0, example=22.0)
    relative_humidity_pct: float = Field(..., ge=5.0, le=100.0, example=50.0)
    storage_type: str = Field("Ambient", example="Ambient") # Ambient, Chilled, Frozen
    transportation: str = Field("Normal", example="Long_Distance") # Normal, Refrigerated, Long_Distance
    optimization_goal: str = Field("Balanced", example="Balanced") # Performance, Balanced, Sustainability, Cost_Optimized
    advanced_notes: Optional[Dict[str, Any]] = None

    @field_validator("storage_type")
    @classmethod
    def validate_storage_type(cls, v: str) -> str:
        valid = ["Ambient", "Chilled", "Frozen"]
        match = next((item for item in valid if item.lower() == v.lower()), None)
        if not match:
            raise ValueError(f"storage_type must be one of: {valid}")
        return match

    @field_validator("transportation")
    @classmethod
    def validate_transport(cls, v: str) -> str:
        valid = ["Normal", "Refrigerated", "Long_Distance"]
        match = next((item for item in valid if item.lower() == v.lower()), None)
        if not match:
            raise ValueError(f"transportation must be one of: {valid}")
        return match

class ValidationRequest(BaseModel):
    commodity: Optional[str] = None
    moisture_pct: Optional[float] = None
    fat_pct: Optional[float] = None
    protein_pct: Optional[float] = None
    storage_temp_c: Optional[float] = None
    storage_type: Optional[str] = None

class ValidationResponse(BaseModel):
    is_valid: bool
    warnings: List[str]
    suggested_values: Optional[Dict[str, Any]] = None

class TechnicalSpecs(BaseModel):
    thickness_um: float
    otr_value: float
    otr_unit: str
    otr_class: str
    wvtr_value: float
    wvtr_unit: str
    wvtr_class: str
    co2_permeability: Optional[float] = None
    puncture_resistance_n: Optional[float] = None
    tensile_strength_mpa: Optional[float] = None
    sealing_temp_range_c: Optional[str] = None
    seal_strength_n_15mm: Optional[float] = None
    min_temperature_c: Optional[float] = None
    breathable: Optional[bool] = False
    micro_perforated: Optional[bool] = False
    map_suitable: Optional[bool] = False
    light_barrier: Optional[str] = None

class SustainabilityProfile(BaseModel):
    recyclability_class: Optional[str] = None
    recyclability_stream: Optional[str] = None
    recycled_content_pct: Optional[float] = 0.0
    biodegradable: Optional[bool] = False
    compostable: Optional[bool] = False
    bio_based_pct: Optional[float] = 0.0
    relative_cost_index: Optional[float] = 1.0

class MaterialLayer(BaseModel):
    layer_no: int
    position: Optional[str] = None
    name: str
    thickness_um: Optional[float] = None
    function: Optional[str] = None
    work: Optional[str] = None

class MaterialComposition(BaseModel):
    layers: List[MaterialLayer] = []
    why_this_material_short: str

class ProcurementMarket(BaseModel):
    estimated_cost_per_kg_inr: Optional[str] = None
    estimated_cost_per_pouch_inr: Optional[str] = None
    approx_cost_usd: Optional[str] = None
    moq: Optional[str] = None
    lead_time: Optional[str] = None
    sourcing_channels: List[str] = []

class QualityInspectionPoint(BaseModel):
    check_item: str
    standard: Optional[str] = None
    acceptance_criteria: str
    how_to_test: str
    criticality: str = "Critical"

class MaterialDurability(BaseModel):
    virgin_material_shelf_life: str
    packaged_product_protection_duration: str
    unfilled_storage_conditions: Optional[str] = None
    aging_failure_modes: Optional[str] = None

class RecommendationItem(BaseModel):
    rank: int
    id: str
    short_name: str
    name: str
    structure: str
    category: str
    suitability_score: float
    sample_photo_url: Optional[str] = None
    technical_specifications: TechnicalSpecs
    sustainability_profile: SustainabilityProfile
    scientific_provenance: Dict[str, Any]
    material_composition: Optional[MaterialComposition] = None
    procurement_market: Optional[ProcurementMarket] = None
    quality_inspection_checklist: Optional[List[QualityInspectionPoint]] = None
    material_durability: Optional[MaterialDurability] = None
    explanation: Dict[str, Any]

class RecommendationResponse(BaseModel):
    query_summary: Dict[str, Any]
    scientific_requirements: Dict[str, Any]
    top_recommendations: List[RecommendationItem]
    sustainable_alternative: Optional[Dict[str, Any]] = None
    disqualified_candidates: Optional[List[Dict[str, Any]]] = None
    confidence_assessment: Dict[str, Any]
    disclaimer: str
