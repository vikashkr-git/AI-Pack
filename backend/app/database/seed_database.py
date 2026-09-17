"""
PackAI - Database Seeding Pipeline
Populates the relational database with authoritative scientific data,
USDA foods, and empirical packaging structures.
"""

from backend.app.database.database import engine, Base, SessionLocal
from backend.app.database.models import Source, Food, PackagingMaterial
from backend.data.scientific_references import SCIENTIFIC_SOURCES, FOOD_PROFILES, PACKAGING_CATALOG

def seed():
    print("[*] Initializing Database Schema...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Seed Sources
        print(f"[*] Seeding {len(SCIENTIFIC_SOURCES)} Scientific Sources...")
        for src in SCIENTIFIC_SOURCES:
            existing = db.query(Source).filter(Source.id == src["id"]).first()
            if not existing:
                db_source = Source(
                    id=src["id"],
                    source_name=src["source_name"],
                    title=src["title"],
                    authors=src.get("authors"),
                    year=src.get("year"),
                    publisher_or_journal=src.get("publisher") or src.get("journal"),
                    url=src.get("url"),
                    doi=src.get("doi"),
                    scope=src.get("scope"),
                    confidence_score=src.get("confidence_score", 0.95)
                )
                db.add(db_source)
        db.commit()

        # 2. Seed Foods
        print(f"[*] Seeding {len(FOOD_PROFILES)} Commodity Profiles...")
        for name, p in FOOD_PROFILES.items():
            existing = db.query(Food).filter(Food.commodity == p["commodity"]).first()
            if not existing:
                db_food = Food(
                    commodity=p["commodity"],
                    category=p["category"],
                    moisture_pct=p["moisture_pct"],
                    fat_pct=p["fat_pct"],
                    protein_pct=p["protein_pct"],
                    ph=p["ph"],
                    water_activity_aw=p.get("water_activity_aw"),
                    respiration_rate_class=p.get("respiration_rate_class", "None"),
                    respiration_rate_val=p.get("respiration_rate_val", 0.0),
                    standard_shelf_life_days=p.get("standard_shelf_life_days", 30),
                    primary_degradation_modes=p.get("primary_degradation_modes"),
                    critical_barrier_needs=p.get("critical_barrier_needs"),
                    optimal_storage_type=p.get("optimal_storage_type", "Ambient"),
                    optimal_temp_c=p.get("optimal_temp_c", 20.0),
                    optimal_rh_pct=p.get("optimal_rh_pct", 65.0),
                    map_suitable=p.get("map_suitable", False),
                    optimal_map_gas=p.get("optimal_map_gas"),
                    source_id=p.get("source_ref")
                )
                db.add(db_food)
        db.commit()

        # 3. Seed Packaging Materials
        print(f"[*] Seeding {len(PACKAGING_CATALOG)} Packaging Structures...")
        for pkg in PACKAGING_CATALOG:
            existing = db.query(PackagingMaterial).filter(PackagingMaterial.id == pkg["id"]).first()
            if not existing:
                db_pkg = PackagingMaterial(
                    id=pkg["id"],
                    name=pkg["name"],
                    short_name=pkg["short_name"],
                    structure=pkg["structure"],
                    total_thickness_um=pkg["total_thickness_um"],
                    category=pkg["category"],
                    otr_value=pkg["otr_value"],
                    otr_class=pkg["otr_class"],
                    wvtr_value=pkg["wvtr_value"],
                    wvtr_class=pkg["wvtr_class"],
                    co2_permeability=pkg.get("co2_permeability"),
                    tensile_strength_mpa=pkg.get("tensile_strength_mpa"),
                    puncture_resistance_n=pkg.get("puncture_resistance_n"),
                    heat_seal_temp_c_min=pkg.get("heat_seal_temp_c_min"),
                    heat_seal_temp_c_max=pkg.get("heat_seal_temp_c_max"),
                    seal_strength_n_15mm=pkg.get("seal_strength_n_15mm"),
                    min_temperature_c=pkg.get("min_temperature_c", -10.0),
                    max_temperature_c=pkg.get("max_temperature_c", 70.0),
                    breathable=pkg.get("breathable", False),
                    micro_perforated=pkg.get("micro_perforated", False),
                    map_suitable=pkg.get("map_suitable", False),
                    light_barrier=pkg.get("light_barrier", "Moderate"),
                    recyclability_class=pkg.get("recyclability_class"),
                    recyclability_stream=pkg.get("recyclability_stream"),
                    recycled_content_pct=pkg.get("recycled_content_pct", 0.0),
                    biodegradable=pkg.get("biodegradable", False),
                    compostable=pkg.get("compostable", False),
                    bio_based_pct=pkg.get("bio_based_pct", 0.0),
                    cost_index_relative=pkg.get("cost_index_relative", 1.0),
                    primary_applications=pkg.get("primary_applications"),
                    astm_standard=pkg.get("astm_standard"),
                    doi=pkg.get("doi"),
                    source_id=pkg.get("source_ref")
                )
                db.add(db_pkg)
        db.commit()

        print("[+] Database initialized and seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"[!] Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
