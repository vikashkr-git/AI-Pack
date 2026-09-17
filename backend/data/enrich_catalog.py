"""
Script to enrich backend/data/packaging_catalog.json with:
1. Sample packaging photo URLs and visual format specs
2. Pre-receiving quality inspection checklist for MSMEs
3. Marketplace sourcing availability and cost approximations (INR and USD)
4. Material composition layers, functional roles ("works"), and scientific rationale ("why only this material")
5. Material durability and shelf life (unfilled roll lifespan vs packaged food protection duration)
"""

import json
import os

ENRICHMENT_DATA = {
    "PKG_MET_PET_PE": {
        "sample_photo_url": "/packaging/met_pet_pe.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Outer Layer (Print Side)",
                    "name": "Biaxially Oriented Polyethylene Terephthalate (BOPET)",
                    "thickness_um": 12.0,
                    "function": "Mechanical Strength & High-Gloss Printing",
                    "work": "Provides high tensile stiffness, thermal resistance during sealing, and a scratch-resistant glossy surface for rotogravure or flexographic branding."
                },
                {
                    "layer_no": 2,
                    "position": "Core Barrier Coating",
                    "name": "Vacuum Metallized Aluminum Coating (Met)",
                    "thickness_um": 0.03,
                    "function": "Light & Gas Barrier (Specular Opacity)",
                    "work": "Deposition of vaporized aluminum onto PET that cuts oxygen transmission by 98% and reflects 99% of UV/visible light to prevent lipid photo-oxidation and rancidity."
                },
                {
                    "layer_no": 3,
                    "position": "Tie / Interlayer Adhesive",
                    "name": "Polyurethane Laminating Adhesive (PU)",
                    "thickness_um": 2.5,
                    "function": "Permanent Substrate Bonding",
                    "work": "Food-grade thermosetting adhesive bonding polyester to polyethylene, preventing delamination under transit flexing."
                },
                {
                    "layer_no": 4,
                    "position": "Inner Layer (Food Contact & Sealant)",
                    "name": "Low-Density Polyethylene (LDPE / LLDPE)",
                    "thickness_um": 57.5,
                    "function": "Hermetic Fusion Sealing & Moisture Barrier",
                    "work": "Melts at 115–145°C to form an airtight, water-vapor-impermeable fusion seal that prevents moisture ingress and crispness loss."
                }
            ],
            "why_this_material_short": "No single polymer can simultaneously provide optical printability, high gas barrier, low-temperature hermetic heat sealing, and low cost. Combining BOPET (mechanical strength & print), vapor metallization (gas/light shield), and LDPE (sealant & moisture shield) creates a synergistic composite barrier at 40% lower cost and weight than solid aluminum foil."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹270 – ₹350 / kg",
            "estimated_cost_per_pouch_inr": "₹1.60 – ₹2.80 / pouch (200g snack size)",
            "approx_cost_usd": "$3.25 – $4.20 / kg",
            "moq": "1,500 pouches (Plain Stock) | 250 kg (Custom Rotogravure Printed)",
            "lead_time": "3–5 days (Stock) | 12–16 days (Custom Cylinders)",
            "sourcing_channels": [
                "IndiaMART B2B Marketplace (Search: 'Met-PET LDPE snack pouches')",
                "TradeIndia B2B Portal",
                "Western India Packaging Cluster (Vapi, Daman, Silvassa, Ahmedabad)",
                "NCR Packaging Industrial Belt (Faridabad, Noida, Kundli)",
                "South India Packaging Hub (Peenya Bengaluru, Cherlapally Hyderabad)"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Visual Pinhole & Metallization Streak Test",
                "standard": "ASTM F392 / IS 1060",
                "acceptance_criteria": "Zero pinholes or light leakage when checked over 100W back-lit inspection table; uniform metallic specular reflection with zero de-metallized streaks.",
                "how_to_test": "Place pouch flat over a high-intensity illuminated inspection table in a darkened room and check for light dots.",
                "criticality": "Critical"
            },
            {
                "check_item": "Gauge & Thickness Uniformity Check",
                "standard": "IS 2508 / ASTM D6988",
                "acceptance_criteria": "Total thickness: 72µm ± 3µm (measured at 5 distinct positions across pouch width).",
                "how_to_test": "Use a calibrated digital dead-weight micrometer (0.001mm resolution) at top, center, bottom, and side edges.",
                "criticality": "Critical"
            },
            {
                "check_item": "Seal Peel Strength & Hermetic Burst Test",
                "standard": "ASTM F88 / ASTM D3078",
                "acceptance_criteria": "Seal tensile peel strength ≥ 35 N/15mm. Zero bubbles during 30-second underwater vacuum chamber test at -50 kPa.",
                "how_to_test": "Cut 15mm strip across seal and pull on tensiometer, or submerge filled pouch in vacuum desiccator tank.",
                "criticality": "Critical"
            },
            {
                "check_item": "Solvent Odor & Migration Food Safety Check",
                "standard": "IS 9845 / FDA 21 CFR 177.1520",
                "acceptance_criteria": "Zero solvent odor (ethyl acetate / toluene smell) inside the pouch; total residual solvents < 10 mg/m².",
                "how_to_test": "Organoleptic sniff test immediately upon slicing open a sealed pouch bundle, confirmed by supplier GC-MS Certificate of Analysis.",
                "criticality": "Critical"
            },
            {
                "check_item": "Layer Interfacial Adhesion (Tape Peel Test)",
                "standard": "ASTM D3359",
                "acceptance_criteria": "Zero delamination between PET and PE film layers prior to substrate structural tear.",
                "how_to_test": "Apply 3M 610 industrial adhesive tape firmly over cross-hatch cut and peel rapidly at 90 degrees.",
                "criticality": "Major"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "18 – 24 Months (unfilled rollstock/pouches stored in original stretch wrap, 15–28°C, RH < 65%)",
            "packaged_product_protection_duration": "Guarantees 180 – 270 Days ambient shelf life for fried snacks & chips against rancidity and crispness loss",
            "unfilled_storage_conditions": "Store pallets horizontally on wooden runners; avoid contact with damp concrete floors; maintain RH < 65% to avoid moisture condensation on aluminum metal coat.",
            "aging_failure_modes": "Decay of surface corona treatment (<38 dynes/cm causing printing ink flaking), plasticizer migration weakening seal initiation, and embrittlement of sealant PE."
        }
    },
    "PKG_AL_FOIL_LAM": {
        "sample_photo_url": "/packaging/al_foil_lam.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Outer Protective Layer",
                    "name": "Biaxially Oriented PET (12µm)",
                    "thickness_um": 12.0,
                    "function": "Tensile Strength & Puncture Protection",
                    "work": "Protects the soft aluminum foil core from flex-cracking and provides a printable, scuff-resistant exterior."
                },
                {
                    "layer_no": 2,
                    "position": "Impermeable Barrier Core",
                    "name": "Soft-Tempered Aluminum Foil (9µm)",
                    "thickness_um": 9.0,
                    "function": "Absolute Gas, Vapor & UV Barrier",
                    "work": "Provides a continuous metallic barrier delivering near-zero OTR (<0.05) and WVTR (<0.05), completely blocking light, aroma transfer, and oxygen."
                },
                {
                    "layer_no": 3,
                    "position": "Adhesive Tie Layer",
                    "name": "Two-Component Polyurethane Adhesive (3µm)",
                    "thickness_um": 3.0,
                    "function": "High-Bond Foil-to-Polymer Adhesion",
                    "work": "Chemically bonds the metallic foil to polyethylene to eliminate delamination during pouch forming and shipping vibrations."
                },
                {
                    "layer_no": 4,
                    "position": "Inner Sealant & Food Contact",
                    "name": "Linear Low-Density Polyethylene (LLDPE, 67µm)",
                    "thickness_um": 67.0,
                    "function": "Hermetic Fusion Sealing",
                    "work": "Provides high hot-tack seal strength (≥42 N/15mm) across 125–160°C, ensuring a 100% airtight closure around powders and infant formula."
                }
            ],
            "why_this_material_short": "Solid aluminum foil provides an absolute physical barrier against oxygen, moisture, and light with zero gas diffusion. Supported by PET on the outside for mechanical toughness and PE on the inside for airtight fusion sealing, it guarantees maximum shelf-life for ultra-hygroscopic powders and infant nutrition."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹440 – ₹580 / kg",
            "estimated_cost_per_pouch_inr": "₹3.50 – ₹6.20 / pouch (500g stand-up pouch)",
            "approx_cost_usd": "$5.30 – $7.00 / kg",
            "moq": "2,000 pouches (Stock) | 300 kg (Custom Printed)",
            "lead_time": "4–7 days (Stock) | 16–21 days (Custom Printed)",
            "sourcing_channels": [
                "IndiaMART B2B Marketplace (Search: 'Aluminium foil laminate pouches')",
                "TradeIndia Packaging Section",
                "Gujarat Industrial Packaging Belt (Ahmedabad / Surat / Vapi)",
                "Peenya Packaging Hub (Bengaluru)",
                "Cherlapally Industrial Zone (Hyderabad)"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Foil Flex-Crack & Micro-Pinhole Light Table Check",
                "standard": "ASTM F392 / IS 1060",
                "acceptance_criteria": "Zero pinholes or flex-cracks in the aluminum foil barrier; zero light penetration across entire surface area.",
                "how_to_test": "Inspect across 100W light inspection table while flexing folds gently.",
                "criticality": "Critical"
            },
            {
                "check_item": "Foil Layer Thickness Verification",
                "standard": "ASTM B479 / IS 2508",
                "acceptance_criteria": "Total gauge: 91µm ± 4µm (Foil thickness 9µm confirmed by supplier test cert).",
                "how_to_test": "Micrometer cross-point testing at 6 locations.",
                "criticality": "Critical"
            },
            {
                "check_item": "Hermetic Vacuum Chamber Burst Hold Test",
                "standard": "ASTM D3078",
                "acceptance_criteria": "Maintains seal without bubble leakage under -60 kPa underwater vacuum for 45 seconds.",
                "how_to_test": "Submerge sealed sample in methylene blue vacuum inspection chamber.",
                "criticality": "Critical"
            },
            {
                "check_item": "Foil-to-PE Interfacial Bond Strength",
                "standard": "ASTM D903",
                "acceptance_criteria": "Adhesion peel force ≥ 3.0 N/15mm; film must tear before foil separates.",
                "how_to_test": "Tensile testing machine peeling foil from PE at 180 degrees.",
                "criticality": "Major"
            },
            {
                "check_item": "Food Migration & Heavy Metal Compliance",
                "standard": "IS 9845 / FSSAI Packaging Regulations",
                "acceptance_criteria": "Certificate of Analysis verifying zero heavy metal leaching (lead, cadmium < 1 ppm) and overall migration < 10 mg/dm².",
                "how_to_test": "Review batch CoA from certified NABL accredited testing laboratory.",
                "criticality": "Critical"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "24 – 36 Months (in original climate-controlled warehouse packaging, 10–30°C)",
            "packaged_product_protection_duration": "Guarantees 365 – 730 Days (1 to 2 Years) shelf life for milk powder, pharmaceuticals, and sensitive nutritionals",
            "unfilled_storage_conditions": "Dry storage strictly below 60% RH to prevent aluminum foil white-rust oxidation on exposed slit roll edges.",
            "aging_failure_modes": "Edge oxidation of exposed aluminum foil layer, polyurethane adhesive crystallization weakening peel bond."
        }
    },
    "PKG_HIGH_BARRIER_LAM": {
        "sample_photo_url": "/packaging/high_barrier_evoh.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Outer Layer",
                    "name": "Biaxially Oriented PET (12µm)",
                    "thickness_um": 12.0,
                    "function": "Clarity & Printability",
                    "work": "Provides high optical transparency (>92% light transmission) and scratch resistance for premium visual packaging."
                },
                {
                    "layer_no": 2,
                    "position": "Core Barrier",
                    "name": "Ethylene Vinyl Alcohol Copolymer (EVOH, 5µm)",
                    "thickness_um": 5.0,
                    "function": "Ultra-High Gas & Aroma Barrier",
                    "work": "Contains highly polar hydroxyl groups that create a dense polymer matrix blocking oxygen, CO2, and essential oil aromas."
                },
                {
                    "layer_no": 3,
                    "position": "Compatibilizing Tie Layers (x2)",
                    "name": "Maleic Anhydride Grafted Polyethylene (3µm)",
                    "thickness_um": 3.0,
                    "function": "Molecular Tie-Layer",
                    "work": "Chemically bonds the polar EVOH barrier resin to the non-polar polyethylene sealing layer."
                },
                {
                    "layer_no": 4,
                    "position": "Inner Sealant",
                    "name": "Metallocene LLDPE (50µm)",
                    "thickness_um": 50.0,
                    "function": "Hermetic Seal & Moisture Protection",
                    "work": "Provides rapid hermetic heat sealing, high dart impact strength, and moisture barrier, all compatible with Code 4/Code 7 recycling."
                }
            ],
            "why_this_material_short": "EVOH delivers exceptional oxygen barrier comparable to metallized films while preserving 100% optical clarity so consumers can inspect food freshness. Designed with compatible polyolefin layers to enable circular recycling under Code 4/Code 7 streams."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹380 – ₹490 / kg",
            "estimated_cost_per_pouch_inr": "₹2.90 – ₹4.80 / pouch (250g Stand-up with Zipper)",
            "approx_cost_usd": "$4.60 – $5.90 / kg",
            "moq": "2,000 pouches (Clear Stock) | 250 kg (Rolls)",
            "lead_time": "3–5 days (Stock) | 14–18 days (Custom)",
            "sourcing_channels": [
                "IndiaMART B2B Marketplace (Search: 'EVOH high barrier pouches')",
                "Cherlapally Packaging Zone (Hyderabad)",
                "Daman & Silvassa Multilayer Converters",
                "Manesar / Gurugram Industrial Area"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Optical Clarity & Gel Blister Inspection",
                "standard": "ASTM D1003",
                "acceptance_criteria": "Haze < 3.5%; crystal-clear transparency with zero yellow tint, fish-eye gels, or un-melted resin streaks.",
                "how_to_test": "Inspect against high-contrast black/white background in bright daylight.",
                "criticality": "Major"
            },
            {
                "check_item": "Total Thickness & EVOH Layer Verification",
                "standard": "ASTM D6988",
                "acceptance_criteria": "Total gauge: 70µm ± 3µm; EVOH core layer verified at ≥ 4.5µm via supplier micro-section analysis.",
                "how_to_test": "Calibrated micrometer across 5 distinct points on pouch.",
                "criticality": "Critical"
            },
            {
                "check_item": "Oxygen Transmission Rate (OTR) Batch Certification",
                "standard": "ASTM D3985",
                "acceptance_criteria": "OTR ≤ 1.5 cm³/(m²·day·atm) at 23°C and 0% RH.",
                "how_to_test": "Review batch Coulometric test report from supplier CoA.",
                "criticality": "Critical"
            },
            {
                "check_item": "Zipper Reclosure & Seal Integrity",
                "standard": "ASTM F88",
                "acceptance_criteria": "Zipper track snaps firmly with audible tactile click; side seal strength ≥ 30 N/15mm without leaks.",
                "how_to_test": "Manual zipper open/close cycling 10 times and air pressure squeeze test.",
                "criticality": "Critical"
            },
            {
                "check_item": "Organoleptic Odor Purity",
                "standard": "IS 9845",
                "acceptance_criteria": "Neutral odor; completely free of amine, monomer, or plasticizer smell.",
                "how_to_test": "Sensory sniff test on pouch headspace after 2 hours enclosed at 40°C.",
                "criticality": "Critical"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "18 – 24 Months (stored in original moisture-proof pallet wrap)",
            "packaged_product_protection_duration": "Guarantees 180 – 360 Days shelf-life for dried fruits, organic nuts, and gourmet confectionery",
            "unfilled_storage_conditions": "Store in climate-controlled warehouse; EVOH is sensitive to high humidity. Maintain warehouse RH < 65% to prevent moisture plasticization.",
            "aging_failure_modes": "EVOH absorbs atmospheric moisture if stored unwrapped in humid ambient conditions, causing temporary drop in oxygen barrier performance."
        }
    },
    "PKG_BIO_PLA_PBAT": {
        "sample_photo_url": "/packaging/bio_compostable_pla.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Outer Layer",
                    "name": "Polylactic Acid (PLA from Corn Starch, 15µm)",
                    "thickness_um": 15.0,
                    "function": "Renewable Bio-Carbon & Stiffness",
                    "work": "Derived from fermented plant starch; provides tensile rigidity, oil resistance, and a natural tactile premium finish."
                },
                {
                    "layer_no": 2,
                    "position": "Core Blended Matrix",
                    "name": "Polybutylene Adipate Terephthalate (PBAT, 25µm)",
                    "thickness_um": 25.0,
                    "function": "Flexibility & Tear Resistance",
                    "work": "Biodegradable synthetic copolyester that prevents the brittle PLA from cracking, providing high elongation and dart impact resistance."
                },
                {
                    "layer_no": 3,
                    "position": "Inner Sealant Layer",
                    "name": "Bio-Sealant PBAT / PLA Compound (10µm)",
                    "thickness_um": 10.0,
                    "function": "Low-Temp Heat Sealing & Compostability",
                    "work": "Heat seals cleanly at 95–125°C and breaks down into organic humus, CO2, and water within 180 days in commercial compost facilities."
                }
            ],
            "why_this_material_short": "Synthesized from renewable agricultural starches (PLA) compounded with ductile biodegradable polyester (PBAT). It delivers adequate moisture and grease protection for organic dry goods while offering 100% industrial compostability certified under EN 13432 and ASTM D6400 with zero microplastic residue."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹350 – ₹480 / kg",
            "estimated_cost_per_pouch_inr": "₹2.80 – ₹4.50 / pouch",
            "approx_cost_usd": "$4.20 – $5.80 / kg",
            "moq": "1,000 pouches (Stock) | 200 kg (Rolls)",
            "lead_time": "4–8 days (Stock) | 15–20 days (Custom)",
            "sourcing_channels": [
                "IndiaMART Compostable Packaging Sellers",
                "CIPET Certified Bio-Plastics Manufacturers",
                "Green Packaging Hubs in Bengaluru, Pune, and Coimbatore",
                "TradeIndia Eco-Friendly Packaging Category"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Compostability Certification Verification",
                "standard": "IS/ISO 17088 / EN 13432 / ASTM D6400",
                "acceptance_criteria": "Clear CPCB / CIPET certificate number and seedling compostable logo printed on the packaging.",
                "how_to_test": "Cross-check CPCB registration number on the official Central Pollution Control Board portal.",
                "criticality": "Critical"
            },
            {
                "check_item": "Film Elasticity & Dart Impact Test",
                "standard": "ASTM D1709",
                "acceptance_criteria": "Dart impact resistance > 120g; no brittle cracking or pinhole formation when creased sharply 180 degrees.",
                "how_to_test": "Fold film sharply between fingers and apply pressure; check fold line for cracking.",
                "criticality": "Critical"
            },
            {
                "check_item": "Heat Seal Temperature Window",
                "standard": "ASTM F88",
                "acceptance_criteria": "Seals cleanly between 100–120°C with seal strength ≥ 20 N/15mm; no burning, shrinkage, or toxic smoke.",
                "how_to_test": "Test on heat sealer bar at 110°C for 1.0 second dwell time.",
                "criticality": "Major"
            },
            {
                "check_item": "Water Vapor Transmission Check",
                "standard": "ASTM F1249",
                "acceptance_criteria": "WVTR ≤ 18.0 g/(m²·day); confirms biopolymer has not absorbed moisture prior to delivery.",
                "how_to_test": "Review supplier batch CoA for barrier compliance.",
                "criticality": "Critical"
            },
            {
                "check_item": "Thickness & Gauge Consistency",
                "standard": "IS 2508",
                "acceptance_criteria": "Total thickness 50µm ± 3µm.",
                "how_to_test": "Micrometer check at 5 positions.",
                "criticality": "Major"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "9 – 12 Months (strictly avoid high heat and humidity; bio-polymers naturally age faster)",
            "packaged_product_protection_duration": "Guarantees 60 – 120 Days shelf-life for organic grains, pulses, and dry bakery items",
            "unfilled_storage_conditions": "Store in cool, dry warehouse below 25°C and RH < 50%, away from UV rays, direct sunlight, and heat ducts.",
            "aging_failure_modes": "Hydrolytic degradation causing film embrittlement, tensile strength drop, and spontaneous cracking after 12 months."
        }
    },
    "PKG_PA_PE_VACUUM": {
        "sample_photo_url": "/packaging/pa_pe_vacuum.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Outer Layer",
                    "name": "Polyamide 6 / Nylon (PA, 20µm)",
                    "thickness_um": 20.0,
                    "function": "Extreme Puncture Resistance & Aroma Barrier",
                    "work": "High-tenacity polyamide protects against puncture from sharp bones, hard pasta, and crusts, while preventing oxygen penetration."
                },
                {
                    "layer_no": 2,
                    "position": "Interlayer Coextrusion Tie",
                    "name": "Modified Polyolefin Adhesive Resin (5µm)",
                    "thickness_um": 5.0,
                    "function": "Permanent Coextruded Interfacial Bond",
                    "work": "Bonds polar nylon with non-polar polyethylene during blown coextrusion without risk of delamination under deep vacuum."
                },
                {
                    "layer_no": 3,
                    "position": "Inner Sealant",
                    "name": "Metallocene Polyethylene (mPE, 70µm)",
                    "thickness_um": 70.0,
                    "function": "Deep Vacuum Sealing & Oil Resistance",
                    "work": "Heavy-duty sealant layer that fuses hermetically even through grease or moisture contamination on the seal bar."
                }
            ],
            "why_this_material_short": "Biaxially oriented polyamide (Nylon) provides exceptional toughness and puncture resistance to prevent sharp food edges from puncturing the pouch, while the thick inner metallocene PE layer seals tight under vacuum without micro-leakers."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹320 – ₹420 / kg",
            "estimated_cost_per_pouch_inr": "₹2.20 – ₹3.80 / pouch (Sous-vide size)",
            "approx_cost_usd": "$3.90 – $5.10 / kg",
            "moq": "1,000 pouches (Stock) | 200 kg",
            "lead_time": "2–4 days (Stock) | 12–15 days (Custom)",
            "sourcing_channels": [
                "IndiaMART Vacuum Pouches Category",
                "Meat & Seafood Processing Equipment Distributors (Kochi, Mumbai, Chennai, Kolkata)",
                "TradeIndia B2B Food Packaging"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Vacuum Retention & Pouch Deflation Check",
                "standard": "ASTM D3078",
                "acceptance_criteria": "Holds -90 kPa vacuum with zero pouch puffing or loss of contour cling over 48 hours.",
                "how_to_test": "Seal product in chamber sealer and monitor pouch vacuum retention for 48 hours.",
                "criticality": "Critical"
            },
            {
                "check_item": "Sharp Edge Puncture Resistance Test",
                "standard": "ASTM F1306",
                "acceptance_criteria": "Puncture resistance ≥ 45 N; resists penetration by 3.2mm hemispherical probe.",
                "how_to_test": "Slow-speed penetration probe test on universal testing machine.",
                "criticality": "Critical"
            },
            {
                "check_item": "Seal-Through-Contamination Reliability",
                "standard": "ASTM F88",
                "acceptance_criteria": "Forms hermetic seal with strength ≥ 30 N/15mm even when seal area is smeared with vegetable oil.",
                "how_to_test": "Apply light oil film on seal area before sealing on impulse sealer bar.",
                "criticality": "Critical"
            },
            {
                "check_item": "Total Thickness & Nylon Layer Ratio",
                "standard": "IS 2508",
                "acceptance_criteria": "Total gauge: 95µm ± 4µm (Nylon layer ≥ 18µm verified).",
                "how_to_test": "Digital micrometer verification.",
                "criticality": "Major"
            },
            {
                "check_item": "Freezer Ductility Test (-20°C)",
                "standard": "ASTM D1790",
                "acceptance_criteria": "Zero cracking or brittle shattering after 24 hours at -20°C when dropped from 1.2m.",
                "how_to_test": "Drop filled frozen pack onto smooth concrete.",
                "criticality": "Critical"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "24 – 36 Months (high chemical stability in standard dry warehouse)",
            "packaged_product_protection_duration": "Guarantees 90 – 180 Days refrigerated / frozen shelf-life for paneer, meats, and marinated seafood",
            "unfilled_storage_conditions": "Ambient storage 15–30°C; protect from high humidity which can temporarily plasticize nylon outer surface.",
            "aging_failure_modes": "Atmospheric moisture absorption by nylon layer causing roll curling if stored unwrapped."
        }
    },
    "PKG_MICRO_PERF_PE": {
        "sample_photo_url": "/packaging/micro_perf_produce.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Base Film",
                    "name": "Low-Density Polyethylene with Anti-Fog Masterbatch",
                    "thickness_um": 35.0,
                    "function": "Clarity & Condensation Dissipation",
                    "work": "Incorporates food-grade non-ionic surfactants that spread moisture into a continuous invisible water sheet, preventing light-scattering droplet fogging."
                },
                {
                    "layer_no": 2,
                    "position": "Perforation Matrix",
                    "name": "Precision Laser Micro-Perforations (80–120µm)",
                    "thickness_um": 0.0,
                    "function": "Equilibrium Respiration Gas Exchange",
                    "work": "Calculated hole density regulates O2 ingress and CO2 egress to match produce respiration kinetics, maintaining 3–5% O2 to prevent anaerobic fermentation."
                }
            ],
            "why_this_material_short": "Living produce consumes oxygen and exhales carbon dioxide. Solid plastic suffocates fresh produce within 48 hours, causing anaerobic rotting. Laser micro-perforations maintain an optimal equilibrium atmosphere (3-5% O2, 5-8% CO2) while preventing water condensation droplets via anti-fog additives."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹210 – ₹290 / kg",
            "estimated_cost_per_pouch_inr": "₹0.90 – ₹1.80 / bag (Produce zipper bag)",
            "approx_cost_usd": "$2.50 – $3.50 / kg",
            "moq": "2,500 bags (Stock) | 200 kg (Rolls)",
            "lead_time": "2–4 days (Stock) | 10–14 days (Laser Perforation Custom)",
            "sourcing_channels": [
                "IndiaMART Agro-Packaging Wholesalers",
                "FPO & Horticulture Packaging Hubs (Nashik, Pune, Bangalore, Himachal)",
                "TradeIndia Produce Packaging"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Laser Micro-Hole Inspection & Count",
                "standard": "Optical Microscopy 50x",
                "acceptance_criteria": "Laser micro-holes cleanly circular (80–120µm diameter) with zero thermal burn slag, clogging, or tears.",
                "how_to_test": "Examine under 50x portable optical loupe or digital microscope.",
                "criticality": "Critical"
            },
            {
                "check_item": "Anti-Fog Efficacy Hot/Cold Test",
                "standard": "ASTM D1003 modified (Hot Fog)",
                "acceptance_criteria": "Water vapor forms a transparent film within 3 minutes over 60°C water bath with zero droplet beads.",
                "how_to_test": "Place film sheet over a 60°C warm water beaker in a cold room; check for transparency vs fogging.",
                "criticality": "Critical"
            },
            {
                "check_item": "Produce Respiration Breathability (OTR)",
                "standard": "ASTM D3985 / ISO 15105",
                "acceptance_criteria": "Equilibrium OTR > 2,000 cm³/(m²·day·atm) to prevent anaerobic produce souring.",
                "how_to_test": "Review laser perforation specification sheet from converter.",
                "criticality": "Critical"
            },
            {
                "check_item": "Micro-Hole Tear Propagation Resistance",
                "standard": "ASTM D1922",
                "acceptance_criteria": "Perforations must not tear or run when film is pulled diagonally by hand.",
                "how_to_test": "Manual tensile pull across hole line.",
                "criticality": "Critical"
            },
            {
                "check_item": "Direct Food Contact Purity",
                "standard": "IS 9845",
                "acceptance_criteria": "Food-grade certification for anti-fog surfactant masterbatch.",
                "how_to_test": "Supplier certificate of analysis.",
                "criticality": "Major"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "12 – 18 Months (anti-fog additive migrates; use within 12 months for peak anti-fog performance)",
            "packaged_product_protection_duration": "Guarantees 14 – 28 Days cold-chain shelf-life for fresh vegetables, salad greens, and berries",
            "unfilled_storage_conditions": "Cool, dry storage below 30°C; protect from dust and airborne particles that could clog micro-perforations.",
            "aging_failure_modes": "Depletion of anti-fog surfactant bloom leading to condensation fogging inside bags."
        }
    },
    "PKG_PE_FILM_FROZEN": {
        "sample_photo_url": "/packaging/frozen_pe_film.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Outer Layer",
                    "name": "High-Clarity LDPE with Cold-Slip Additives (25µm)",
                    "thickness_um": 25.0,
                    "function": "Machinability & Frost Slip",
                    "work": "Prevents frozen bags from sticking together in freezer bins and ensures smooth passage over high-speed vertical form-fill-seal (VFFS) collars."
                },
                {
                    "layer_no": 2,
                    "position": "Core Impact Resin",
                    "name": "Metallocene LLDPE (mLLDPE, 40µm)",
                    "thickness_um": 40.0,
                    "function": "Sub-Zero Impact Ductility",
                    "work": "High-molecular-weight metallocene polymer structure that prevents embrittlement and flex-cracking down to -30°C."
                },
                {
                    "layer_no": 3,
                    "position": "Inner Sealant",
                    "name": "High-Tack Polyethylene Sealant (25µm)",
                    "thickness_um": 25.0,
                    "function": "Hermetic Freezer Seal & Moisture Shield",
                    "work": "Thick sealant bead that prevents air exchange and eliminates freezer-burn dehydration in frozen peas, corn, and meats."
                }
            ],
            "why_this_material_short": "Standard plastics become glass-brittle at sub-zero temperatures and shatter on conveyor drop. Metallocene-catalyzed PE preserves high ductile impact resistance down to -30°C, and prevents freezer burn dehydration with a thick water vapor barrier."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹220 – ₹310 / kg",
            "estimated_cost_per_pouch_inr": "₹1.40 – ₹2.50 / bag (1kg Frozen Veg pouch)",
            "approx_cost_usd": "$2.65 – $3.75 / kg",
            "moq": "2,000 bags (Stock) | 250 kg",
            "lead_time": "3–5 days (Stock) | 12–15 days (Custom)",
            "sourcing_channels": [
                "IndiaMART Frozen Food Packaging",
                "Gujarat Plastics Belt (Ahmedabad / Anand / Vapi)",
                "NCR Industrial Polyfilm Converters"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Sub-Zero Freezer Drop Impact Test",
                "standard": "ASTM D1709 / ASTM D1790",
                "acceptance_criteria": "Frozen filled pack dropped from 1.5m height at -18°C: zero seam split, puncture, or corner rupture.",
                "how_to_test": "Freeze 5 filled packs overnight at -18°C and drop onto smooth steel plate.",
                "criticality": "Critical"
            },
            {
                "check_item": "Film Thickness & Dart Drop Verification",
                "standard": "IS 2508",
                "acceptance_criteria": "Total thickness: 90µm ± 4µm; Dart drop impact resistance ≥ 280g.",
                "how_to_test": "Micrometer check at 5 positions across film width.",
                "criticality": "Critical"
            },
            {
                "check_item": "Water Vapor Moisture Barrier (Freezer Burn Defense)",
                "standard": "ASTM F1249",
                "acceptance_criteria": "WVTR ≤ 2.2 g/(m²·day) to prevent ice sublimation inside the package.",
                "how_to_test": "Supplier batch test certificate.",
                "criticality": "Critical"
            },
            {
                "check_item": "Seal Tensile Strength",
                "standard": "ASTM F88",
                "acceptance_criteria": "Hermetic seal strength ≥ 32 N/15mm without channel leaks.",
                "how_to_test": "Tensiometer pull across heat seal seam.",
                "criticality": "Major"
            },
            {
                "check_item": "Odor & Taste Transfer Purity",
                "standard": "IS 9845",
                "acceptance_criteria": "Zero plastic odor transfer onto frozen food during prolonged sub-zero storage.",
                "how_to_test": "Headspace sensory evaluation on thawed product.",
                "criticality": "Major"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "24 – 36 Months (inert polyolefin film)",
            "packaged_product_protection_duration": "Guarantees 270 – 365 Days frozen storage at -18°C with zero freezer burn dehydration",
            "unfilled_storage_conditions": "Standard dry warehouse storage; keep pallets out of direct sunlight and away from heat.",
            "aging_failure_modes": "Gradual loss of slip additive coefficient of friction leading to drag on VFFS packaging machines."
        }
    },
    "PKG_BOPP_PE": {
        "sample_photo_url": "/packaging/bopp_pe_flowwrap.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Outer Layer",
                    "name": "Biaxially Oriented Polypropylene (BOPP, 20µm)",
                    "thickness_um": 20.0,
                    "function": "High-Gloss & Rotogravure Printability",
                    "work": "High tensile stiffness, exceptional clarity, and excellent water vapor barrier for biscuit and bakery flow-wrapping."
                },
                {
                    "layer_no": 2,
                    "position": "Tie Layer",
                    "name": "Extrusion Polyethylene or Solventless PU (3µm)",
                    "thickness_um": 3.0,
                    "function": "Lamination Bonding",
                    "work": "High-speed solventless adhesive that cures without residual solvent odor."
                },
                {
                    "layer_no": 3,
                    "position": "Inner Sealant",
                    "name": "Cast Polyethylene (PE, 32µm)",
                    "thickness_um": 32.0,
                    "function": "High-Speed Flow-Wrap Heat Sealing",
                    "work": "Rapid sealing window (110–135°C) enabling high packaging line speeds up to 120 packs per minute."
                }
            ],
            "why_this_material_short": "BOPP film gives exceptional gloss, clarity, and moisture resistance at minimal cost, while LDPE provides high-speed heat sealing. It is the gold standard for bakery, biscuits, and confectionery flow-wrapping."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹220 – ₹295 / kg",
            "estimated_cost_per_pouch_inr": "₹0.80 – ₹1.60 / flow-wrap pack",
            "approx_cost_usd": "$2.65 – $3.55 / kg",
            "moq": "150 kg (Plain/Stock rolls) | 300 kg (Custom Printed)",
            "lead_time": "2–4 days (Stock) | 10–14 days (Printed)",
            "sourcing_channels": [
                "IndiaMART B2B Marketplace (Search: 'BOPP PE laminated rolls')",
                "Local Packaging Converters across all major industrial states",
                "TradeIndia Bakery Packaging"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Dynamic Coefficient of Friction (COF)",
                "standard": "ASTM D1894",
                "acceptance_criteria": "Dynamic COF between 0.20 – 0.28 to guarantee jam-free high-speed packaging machine feeding.",
                "how_to_test": "COF inclined plane or horizontal sled friction tester.",
                "criticality": "Critical"
            },
            {
                "check_item": "Seal Initiation Temperature & Dwell Window",
                "standard": "ASTM F88",
                "acceptance_criteria": "Consistent hermetic seal at 115°C with 0.5 sec dwell; no film burning or seam pinholes.",
                "how_to_test": "Test on flow-wrap sealer jaws at operating line speed.",
                "criticality": "Critical"
            },
            {
                "check_item": "Print Inking Adhesion (Tape Pull Test)",
                "standard": "ASTM D3359",
                "acceptance_criteria": "Zero ink lift-off using 3M 610 adhesive tape across reverse-printed areas.",
                "how_to_test": "Press tape firmly over printed area and peel sharply at 90 degrees.",
                "criticality": "Major"
            },
            {
                "check_item": "Gauge & Thickness Uniformity",
                "standard": "IS 2508",
                "acceptance_criteria": "55µm ± 2.5µm across web width.",
                "how_to_test": "Micrometer check at 5 points.",
                "criticality": "Major"
            },
            {
                "check_item": "Moisture Barrier (WVTR) Compliance",
                "standard": "ASTM F1249",
                "acceptance_criteria": "WVTR ≤ 3.5 g/(m²·day) to preserve biscuit crispness.",
                "how_to_test": "Supplier batch test report.",
                "criticality": "Critical"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "18 – 24 Months",
            "packaged_product_protection_duration": "Guarantees 90 – 180 Days ambient crispness protection for biscuits and confectionery",
            "unfilled_storage_conditions": "Dry storage at 18–28°C; keep rolls wrapped in dust jackets away from humid walls.",
            "aging_failure_modes": "Loss of surface dyne level affecting slip and sealing speed."
        }
    },
    "PKG_PP_CUP_FOIL": {
        "sample_photo_url": "/packaging/pp_cup_foil.jpg",
        "material_composition": {
            "layers": [
                {
                    "layer_no": 1,
                    "position": "Rigid Cup Container",
                    "name": "Thermoformed Polypropylene (PP, 450µm)",
                    "thickness_um": 450.0,
                    "function": "Structural Rigidity & Thermal Resistance",
                    "work": "Provides crush-resistant container integrity and withstands hot-filling or pasteurization up to 90°C."
                },
                {
                    "layer_no": 2,
                    "position": "Die-Cut Closure Lid",
                    "name": "Lacquered Aluminum Foil Lid (38µm)",
                    "thickness_um": 38.0,
                    "function": "Hermetic Peelable Seal & 100% Light Barrier",
                    "work": "Die-cut embossed aluminum lid with PP-compatible heat-seal lacquer that seals airtight yet peels smoothly without shredding."
                }
            ],
            "why_this_material_short": "Rigid PP container provides structural protection against crushing during transit and can withstand hot-fill pasteurization up to 90°C. The peelable aluminum foil lid ensures a 100% airtight seal while allowing easy consumer opening without tearing."
        },
        "procurement_market": {
            "estimated_cost_per_kg_inr": "₹260 – ₹340 / kg (Cups + Lids combo)",
            "estimated_cost_per_pouch_inr": "₹1.75 – ₹3.20 / cup with printed foil lid (100ml – 200ml)",
            "approx_cost_usd": "$3.15 – $4.10 / kg",
            "moq": "5,000 cups with matching die-cut foil lids",
            "lead_time": "3–5 days (Plain Stock) | 14–18 days (Custom IML / Printed Lids)",
            "sourcing_channels": [
                "IndiaMART Dairy Packaging Suppliers",
                "Gujarat & Maharashtra Thermoforming Hubs",
                "TradeIndia Food Containers"
            ]
        },
        "quality_inspection_checklist": [
            {
                "check_item": "Peelability & Seal Integrity",
                "standard": "ASTM F88",
                "acceptance_criteria": "Smooth continuous peel without foil shredding; burst pressure ≥ 30 kPa before peeling.",
                "how_to_test": "Manual tab peel test and air-injection burst test.",
                "criticality": "Critical"
            },
            {
                "check_item": "Rim Flatness & Flange Gauge",
                "standard": "Vernier Caliper Check",
                "acceptance_criteria": "Flange rim flatness tolerance ±0.2mm to ensure airtight lid sealing all around.",
                "how_to_test": "Place cup inverted on surface plate and check for gap with feeler gauge.",
                "criticality": "Critical"
            },
            {
                "check_item": "Top-Load Compression Crush Strength",
                "standard": "ASTM D2659",
                "acceptance_criteria": "Top load crush resistance ≥ 15 kgf to survive 4-layer pallet stacking.",
                "how_to_test": "Universal compression tester top-load test.",
                "criticality": "Critical"
            },
            {
                "check_item": "Food Migration Compliance (Acidic / Dairy)",
                "standard": "IS 9845",
                "acceptance_criteria": "Overall migration < 10 mg/dm² into 3% acetic acid and 50% ethanol.",
                "how_to_test": "Review supplier NABL accredited laboratory test certificate.",
                "criticality": "Critical"
            },
            {
                "check_item": "Foil Lid Pinhole Inspection",
                "standard": "ASTM B479",
                "acceptance_criteria": "Zero pinholes in die-cut aluminum lid.",
                "how_to_test": "Light table inspection of lid samples.",
                "criticality": "Major"
            }
        ],
        "material_durability": {
            "virgin_material_shelf_life": "36 Months (rigid PP containers do not degrade under dry warehouse conditions)",
            "packaged_product_protection_duration": "Guarantees 30 – 90 Days chilled shelf-life for yogurt, curd, dips, and desserts",
            "unfilled_storage_conditions": "Keep nested sleeves in original corrugated cartons; protect from dust and weights.",
            "aging_failure_modes": "Heat-seal lacquer on foil lids can lose activation tack if stored above 40°C."
        }
    }
}

OTHER_MATERIALS_DATA = {
    "PKG_AL_LAMINATE": {
        "sample_photo_url": "/packaging/al_laminate.jpg",
        "why_this_material_short": "Provides complete light and moisture blockage for spices, rations, and sensitive powders using a tough BOPP outer layer laminated to aluminum foil.",
        "cost_kg": "₹420 – ₹550 / kg",
        "cost_pouch": "₹3.20 – ₹5.50 / pouch",
        "usd": "$5.00 – $6.60 / kg",
        "shelf_life": "24 – 36 Months",
        "food_life": "365 – 730 Days"
    },
    "PKG_BREATHABLE_PE": {
        "sample_photo_url": "/packaging/breathable_pe.jpg",
        "why_this_material_short": "Microporous polyethylene permits controlled oxygen transfer for moderate respiration produce without letting liquid water escape.",
        "cost_kg": "₹230 – ₹310 / kg",
        "cost_pouch": "₹1.10 – ₹2.10 / bag",
        "usd": "$2.75 – $3.70 / kg",
        "shelf_life": "18 Months",
        "food_life": "14 – 25 Days"
    },
    "PKG_BREATHABLE_PP": {
        "sample_photo_url": "/packaging/breathable_pp.jpg",
        "why_this_material_short": "Perforated polypropylene offers sparkling optical clarity for fresh cut salads while allowing respiration gases to diffuse rapidly.",
        "cost_kg": "₹240 – ₹320 / kg",
        "cost_pouch": "₹1.20 – ₹2.20 / bag",
        "usd": "$2.90 – $3.85 / kg",
        "shelf_life": "18 Months",
        "food_life": "10 – 20 Days"
    },
    "PKG_LDPE_BAG": {
        "sample_photo_url": "/packaging/ldpe_bag.jpg",
        "why_this_material_short": "Economic monolayer polyethylene bag providing reliable water vapor barrier and simple heat sealability for short-shelf-life general food items.",
        "cost_kg": "₹160 – ₹220 / kg",
        "cost_pouch": "₹0.50 – ₹1.10 / bag",
        "usd": "$1.90 – $2.65 / kg",
        "shelf_life": "24 Months",
        "food_life": "15 – 45 Days"
    },
    "PKG_HDPE_WOVEN": {
        "sample_photo_url": "/packaging/hdpe_woven.jpg",
        "why_this_material_short": "High-tensile woven HDPE structure designed to bear heavy mechanical stress (25kg–50kg bulk grains and pulses) with an internal barrier liner.",
        "cost_kg": "₹170 – ₹240 / kg",
        "cost_pouch": "₹12.00 – ₹24.00 / sack (25–50kg)",
        "usd": "$2.05 – $2.90 / kg",
        "shelf_life": "24 Months",
        "food_life": "180 – 365 Days"
    },
    "PKG_RPET_PE_CIRCULAR": {
        "sample_photo_url": "/packaging/rpet_pe_circular.jpg",
        "why_this_material_short": "Incorporates 30% post-consumer recycled food-grade rPET to reduce virgin fossil plastic usage while maintaining high structural barrier.",
        "cost_kg": "₹280 – ₹370 / kg",
        "cost_pouch": "₹2.00 – ₹3.40 / pouch",
        "usd": "$3.35 – $4.45 / kg",
        "shelf_life": "18 – 24 Months",
        "food_life": "120 – 240 Days"
    }
}

def enrich_catalog():
    catalog_path = "backend/data/packaging_catalog.json"
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"Enriching {len(catalog)} materials...")

    for item in catalog:
        m_id = item["id"]
        if m_id in ENRICHMENT_DATA:
            enriched = ENRICHMENT_DATA[m_id]
            item["sample_photo_url"] = enriched["sample_photo_url"]
            item["material_composition"] = enriched["material_composition"]
            item["procurement_market"] = enriched["procurement_market"]
            item["quality_inspection_checklist"] = enriched["quality_inspection_checklist"]
            item["material_durability"] = enriched["material_durability"]
        elif m_id in OTHER_MATERIALS_DATA:
            meta = OTHER_MATERIALS_DATA[m_id]
            item["sample_photo_url"] = meta["sample_photo_url"]
            item["material_composition"] = {
                "layers": [
                    {
                        "layer_no": 1,
                        "position": "Outer Layer",
                        "name": item.get("structure", "").split("/")[0].strip() if "/" in item.get("structure", "") else item["name"],
                        "thickness_um": round(item["total_thickness_um"] * 0.4, 1),
                        "function": "Structural Integrity & Printability",
                        "work": "Provides protective exterior barrier and mechanical stability."
                    },
                    {
                        "layer_no": 2,
                        "position": "Inner Sealant Layer",
                        "name": item.get("structure", "").split("/")[-1].strip() if "/" in item.get("structure", "") else "Polyethylene Sealant",
                        "thickness_um": round(item["total_thickness_um"] * 0.6, 1),
                        "function": "Hermetic Fusion Sealing",
                        "work": "Fuses under heat to seal in food freshness and prevent vapor transmission."
                    }
                ],
                "why_this_material_short": meta["why_this_material_short"]
            }
            item["procurement_market"] = {
                "estimated_cost_per_kg_inr": meta["cost_kg"],
                "estimated_cost_per_pouch_inr": meta["cost_pouch"],
                "approx_cost_usd": meta["usd"],
                "moq": "1,500 units / 200 kg",
                "lead_time": "3–5 days (Stock) | 12–15 days (Custom)",
                "sourcing_channels": [
                    "IndiaMART B2B Marketplace",
                    "TradeIndia B2B Portal",
                    "Local Regional Industrial Packaging Clusters"
                ]
            }
            item["quality_inspection_checklist"] = [
                {
                    "check_item": "Visual Pinhole & Defect Inspection",
                    "standard": "IS 1060 / ASTM F392",
                    "acceptance_criteria": "Zero visible pinholes, cracks, or web wrinkles under bright light inspection.",
                    "how_to_test": "Visual light table check across web width.",
                    "criticality": "Critical"
                },
                {
                    "check_item": "Gauge & Thickness Micrometer Check",
                    "standard": "IS 2508 / ASTM D6988",
                    "acceptance_criteria": f"Total thickness: {item['total_thickness_um']}µm ± 5%.",
                    "how_to_test": "Calibrated digital micrometer at 5 locations.",
                    "criticality": "Critical"
                },
                {
                    "check_item": "Heat Seal Strength Integrity",
                    "standard": "ASTM F88",
                    "acceptance_criteria": f"Seal strength ≥ {item.get('seal_strength_n_15mm', 25.0)} N/15mm without leaks.",
                    "how_to_test": "Tensiometer pull across seal joint.",
                    "criticality": "Critical"
                },
                {
                    "check_item": "Solvent Odor Organoleptic Check",
                    "standard": "IS 9845",
                    "acceptance_criteria": "Zero chemical/solvent odor taint inside packaging.",
                    "how_to_test": "Headspace sniff test upon package opening.",
                    "criticality": "Critical"
                }
            ]
            item["material_durability"] = {
                "virgin_material_shelf_life": meta["shelf_life"] + " in dry warehouse conditions (15–28°C, RH < 65%)",
                "packaged_product_protection_duration": f"Guarantees {meta['food_life']} shelf life protection under recommended storage climate",
                "unfilled_storage_conditions": "Clean, dry warehouse, elevated on wooden pallets away from direct damp walls.",
                "aging_failure_modes": "Surface tension drop affecting seal strength and potential polymer oxidation."
            }

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print(f"[OK] Successfully enriched all {len(catalog)} materials in {catalog_path}!")

if __name__ == "__main__":
    enrich_catalog()
