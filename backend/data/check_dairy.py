from backend.app.services.recommendation_service import RecommendationService
import json

with open("backend/data/food_profiles.json") as f:
    foods = json.load(f)

for item in ["Milk Powder", "Cheese", "Butter", "Yogurt"]:
    p = foods[item]
    res = RecommendationService.recommend(
        commodity=p["commodity"],
        category=p["category"],
        moisture_pct=p["moisture_pct"],
        fat_pct=p["fat_pct"],
        protein_pct=p["protein_pct"],
        ph=p["ph"],
        respiration_rate=p.get("respiration_rate_val", 0.0),
        shelf_life_days=p.get("standard_shelf_life_days", 90),
        storage_temp_c=p.get("optimal_temp_c", 4.0),
        relative_humidity_pct=p.get("optimal_rh_pct", 65.0),
        storage_type=p.get("optimal_storage_type", "Ambient"),
        transportation="Normal"
    )
    print("=== " + item + " ===")
    for rec in res["top_recommendations"]:
        print("  Rank #" + str(rec["rank"]) + ": " + rec["name"] + " (" + rec["id"] + ")")
        rec_s = json.dumps(rec)
        if "chip" in rec_s.lower():
            print("    [!] Found chip in rec!")
            for k, v in rec.items():
                if "chip" in json.dumps(v).lower():
                    print("       key: " + k + " -> " + json.dumps(v)[:140])
