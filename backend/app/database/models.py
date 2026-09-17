"""
PackAI - SQLAlchemy Relational Schema
Tables: Sources, Foods, PackagingMaterials, RecommendationLogs, ModelRegistry
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from backend.app.database.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(String(50), primary_key=True, index=True)
    source_name = Column(String(150), nullable=False)
    title = Column(String(255), nullable=False)
    authors = Column(String(255), nullable=True)
    year = Column(Integer, nullable=True)
    publisher_or_journal = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)
    doi = Column(String(100), nullable=True, index=True)
    scope = Column(Text, nullable=True)
    confidence_score = Column(Float, default=0.95)

    foods = relationship("Food", back_populates="source")
    packaging = relationship("PackagingMaterial", back_populates="source")


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    commodity = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    moisture_pct = Column(Float, nullable=False)
    fat_pct = Column(Float, nullable=False)
    protein_pct = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)
    water_activity_aw = Column(Float, nullable=True)
    respiration_rate_class = Column(String(50), default="None")
    respiration_rate_val = Column(Float, default=0.0) # mg CO2 / kg-hr
    standard_shelf_life_days = Column(Integer, default=30)
    primary_degradation_modes = Column(JSON, nullable=True)
    critical_barrier_needs = Column(JSON, nullable=True)
    optimal_storage_type = Column(String(50), default="Ambient")
    optimal_temp_c = Column(Float, default=20.0)
    optimal_rh_pct = Column(Float, default=65.0)
    map_suitable = Column(Boolean, default=False)
    optimal_map_gas = Column(Text, nullable=True)
    
    source_id = Column(String(50), ForeignKey("sources.id"), nullable=True)
    source = relationship("Source", back_populates="foods")


class PackagingMaterial(Base):
    __tablename__ = "packaging_materials"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    short_name = Column(String(100), unique=True, index=True, nullable=False)
    structure = Column(String(255), nullable=False)
    total_thickness_um = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    
    # Barrier Specifications
    otr_value = Column(Float, nullable=False) # cm3 / (m2 * day * atm)
    otr_class = Column(String(50), nullable=False)
    wvtr_value = Column(Float, nullable=False) # g / (m2 * day)
    wvtr_class = Column(String(50), nullable=False)
    co2_permeability = Column(Float, nullable=True)
    
    # Mechanical & Sealing
    tensile_strength_mpa = Column(Float, nullable=True)
    puncture_resistance_n = Column(Float, nullable=True)
    heat_seal_temp_c_min = Column(Float, nullable=True)
    heat_seal_temp_c_max = Column(Float, nullable=True)
    seal_strength_n_15mm = Column(Float, nullable=True)
    
    # Operational Temperature Tolerance
    min_temperature_c = Column(Float, default=-10.0)
    max_temperature_c = Column(Float, default=70.0)
    
    # Produce & Gas Features
    breathable = Column(Boolean, default=False)
    micro_perforated = Column(Boolean, default=False)
    map_suitable = Column(Boolean, default=False)
    light_barrier = Column(String(100), default="Moderate")
    
    # Circular Economy & Sustainability
    recyclability_class = Column(String(100), nullable=True)
    recyclability_stream = Column(String(100), nullable=True)
    recycled_content_pct = Column(Float, default=0.0)
    biodegradable = Column(Boolean, default=False)
    compostable = Column(Boolean, default=False)
    bio_based_pct = Column(Float, default=0.0)
    cost_index_relative = Column(Float, default=1.0) # Relative to standard LDPE = 1.0
    
    primary_applications = Column(JSON, nullable=True)
    astm_standard = Column(String(100), nullable=True)
    doi = Column(String(100), nullable=True)
    
    source_id = Column(String(50), ForeignKey("sources.id"), nullable=True)
    source = relationship("Source", back_populates="packaging")


class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    commodity = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    moisture_pct = Column(Float, nullable=False)
    fat_pct = Column(Float, nullable=False)
    protein_pct = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)
    respiration_rate = Column(Float, default=0.0)
    shelf_life_days = Column(Integer, nullable=False)
    storage_temp_c = Column(Float, nullable=False)
    relative_humidity_pct = Column(Float, nullable=False)
    storage_type = Column(String(50), nullable=False)
    transportation = Column(String(50), nullable=False)
    optimization_goal = Column(String(50), default="Balanced")
    
    # Result Snapshot
    top_recommendation_name = Column(String(100), nullable=False)
    top_suitability_score = Column(Float, nullable=False)
    top_technical_summary = Column(JSON, nullable=True)
    confidence_level = Column(String(50), default="High")
    explanation_summary = Column(Text, nullable=True)


class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_version = Column(String(50), unique=True, nullable=False)
    model_type = Column(String(100), nullable=False)
    trained_timestamp = Column(DateTime, default=datetime.utcnow)
    ndcg_at_3 = Column(Float, nullable=True)
    top1_accuracy = Column(Float, nullable=True)
    top3_accuracy = Column(Float, nullable=True)
    rmse = Column(Float, nullable=True)
    r2_score = Column(Float, nullable=True)
    total_train_samples = Column(Integer, default=0)
    features_list = Column(JSON, nullable=True)
    feature_importances = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
