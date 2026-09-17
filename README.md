# PackAI — Intelligent Food Packaging Material Recommendation System
### Smart India Hackathon (SIH) 2026 Solution

> **Problem Statement:** "AI-Based Intelligent Food Packaging Material Recommendation System for Food Commodities"  
> **Target Beneficiaries:** Food MSMEs, Startups, Farmers, FPOs, Local Processors, Packaging Converters.

---

## 🌟 Executive Overview

Food packaging is critical to shelf life, safety, and nutritional integrity. Incorrect packaging leads to moisture absorption, lipid rancidity, microbial rotting, and catastrophic food waste. 

**PackAI** replaces trial-and-error guesswork and static lookup tables with a **Hybrid AI Decision-Support Platform**:
1. **Scientific Packaging Requirement Engine**: Computes target Oxygen Transmission Rate ($D_{OTR}$), Water Vapor Transmission Rate ($D_{WVTR}$), and respiration gas equilibrium using mass-transfer physics and Tetens vapor pressure equations.
2. **Master Packaging Knowledge Base**: Empirical catalog of 15+ packaging materials and multilayer structures (monolayer polyolefins, metallized films, aluminum foil laminates, PA/PE vacuum pouches, and certified biopolymers) with empirical permeabilities linked to peer-reviewed literature, DOIs, and ASTM standards (ASTM D3985 Coulometric OTR, ASTM F1249 Infrared WVTR).
3. **Machine Learning Suitability Ranker**: Evaluates multi-dimensional compatibility vectors using a Random Forest model trained with **Grouped 5-Fold Cross-Validation** (grouped by commodity to prevent target leakage and ensure out-of-distribution generalization).
4. **Explainable AI (XAI) & Decision Support**: Explains *why* the top candidate succeeded, *why* alternatives ranked lower, highlights engineering trade-offs, and provides sustainable alternatives with zero fake guarantees.

---

## 🏛️ System Architecture

```
[ User Input: Food Proximate Composition + Storage Climate + Transit Stress + User Focus ]
                                    ↓
          [ 1. Scientific Packaging Requirement Engine ]
            • Moisture Sorption & WVTR Demand (Tetens equation)
            • Oxidation Risk & OTR Demand (Lipid kinetics, Q10)
            • Fresh Produce Respiration & MAP Gas Equilibrium
            • Sub-Zero Thermal Ductility & Transit Puncture Limits
                                    ↓
          [ 2. Master Packaging Knowledge Base (15+ Structures) ]
            • Empirical OTR, WVTR, Thickness, Sealing Range, Puncture
            • ASTM D3985, ASTM F1249, Academic DOIs & Standards
                                    ↓
          [ 3. Hard-Constraint Scientific Filtering ]
            • Disqualifies incompatible materials (e.g. non-breathable on produce)
                                    ↓
          [ 4. ML Candidate Suitability Scorer (Random Forest) ]
            • Multi-dimensional feature compatibility vectors
            • Predicts continuous suitability score (0–100)
            • Dynamic User Weighting (Performance, Balanced, Sustainability, Cost)
                                    ↓
          [ 5. Explainable AI & Decision Support Layer ]
            • Top-3 Ranked Recommendations
            • Feature contribution breakdown ("Why this was selected")
            • Sustainable Alternatives & Trade-off Matrix
            • Fresh Produce Mode & Controlled Atmosphere Guidelines
                                    ↓
          [ FastAPI REST Backend + React/Tailwind Scientific UI ]
```

---

## 🔬 SIH Judging Defense: Why Hybrid AI?

### 1. Why AI?
A static lookup table cannot account for non-linear interactions between storage temperature, relative humidity, fluctuating transportation shock, and variable shelf-life requirements. The AI model evaluates multi-dimensional compatibility vectors across conflicting requirements.

### 2. Why Not Only Rules?
Rules provide hard physical boundaries (e.g., prohibiting hermetic foils for living produce), but fail to prioritize nuanced trade-offs between competing viable structures across varying supply chain conditions.

### 3. Why Not Only ML?
Training a black-box deep learning model directly on food-to-packaging labels leads to severe memorization. In fact, our **Phase 2 Data Audit** proved that in the synthetic 5,000-row dataset, every commodity had a **100% deterministic 1-to-1 mapping** to packaging labels. Pure ML would simply memorize the table without learning any physical science.

### 4. Data Provenance & Anomaly Audit
- **Synthetic Data**: Acknowledged and documented as synthetic Gemini prototype data.
- **Audit Findings**: Flagged row `F00003` (Tomato Moisture = 101.08%) and 434 records with proximate sums $> 100\%$. Normalized with documented rationale and preserved in `raw_moisture_pct`.
- **Scientific Literature**: Integrated USDA FoodData Central constants and Kader (2002) postharvest respiration rates with academic DOIs and ASTM standards.

---

## 🚀 Quick Start (Running Locally)

### Prerequisites
- Python 3.10+ (Tested on Python 3.13.7)
- Node.js 18+ & npm (Tested on Node v24.16.0)

### 1-Click Launch (Windows)
Double-click `start_app.bat` or run:
```powershell
.\start_app.bat
```

### Manual Launch

#### Terminal 1: Backend
```powershell
# From the project root (SIH/)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001
```
- API Swagger Documentation: `http://127.0.0.1:8001/docs`
- Health Check: `http://127.0.0.1:8001/health`

#### Terminal 2: Frontend
```powershell
cd frontend
npm install
npm run dev
```
- Open your browser at: `http://localhost:5173`

---

## 🧪 Automated Testing

Run the full automated test suite covering rules, ML inference, and REST APIs:
```powershell
python -m pytest backend/tests/ -v
```
All 12 unit and integration tests validate:
- Tomato Fresh Produce Mode & Respiration Permeability
- Potato Chip High-Lipid Oxidation & Moisture Barrier
- Milk Powder Total Hermetic Barrier
- Frozen Peas Sub-Zero Cold-Crack Resistance (-18°C)
- REST API contract validation & autocompletion

---

## 📦 Project Directory Structure

```
SIH/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── api_router.py         # REST Endpoints (foods, packaging, recommend, sources)
│   │   ├── database/
│   │   │   ├── database.py           # SQLAlchemy Engine & Session
│   │   │   ├── models.py             # Relational Schema (Foods, Packaging, Sources, Logs)
│   │   │   └── seed_database.py      # Database Seeding Script
│   │   ├── rules/
│   │   │   └── scientific_engine.py  # Physics & Mass-Transfer Equations
│   │   ├── schemas/
│   │   │   └── schemas.py            # Pydantic v2 Request/Response Models
│   │   ├── services/
│   │   │   ├── recommendation_service.py # Master Recommendation Service
│   │   │   └── explainability_service.py # XAI Rationale & Radar Metrics
│   │   └── main.py                   # FastAPI Application Entrypoint
│   ├── data/
│   │   ├── audit_report.json         # Anomaly Detection & Leakage Audit
│   │   ├── cleaned_prototype_data.csv# Cleaned & Normalized Dataset
│   │   ├── packai.db                 # Seeded SQLite Database
│   │   ├── packaging_catalog.json    # Empirical Packaging Materials
│   │   └── scientific_references.py  # USDA & Literature References
│   ├── models/
│   │   ├── model_metrics.json        # 5-Fold GroupKFold CV Metrics & Feature Weights
│   │   └── packaging_ranker_v1.joblib# Trained ML Model Pipeline
│   ├── tests/
│   │   ├── test_scientific_engine.py # Physics & Constraint Tests
│   │   └── test_recommendation_api.py# API Integration Tests
│   ├── training/
│   │   ├── data_audit.py             # Data Audit & Anomaly Detection Pipeline
│   │   └── train_ranking_model.py    # GroupKFold ML Training Pipeline
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx            # Navigation & Live Status
│   │   │   ├── HeroSection.tsx       # SIH Headline & 1-Click Jury Presets
│   │   │   ├── RecommendationWizard.tsx # 4-Step Input Wizard
│   │   │   ├── ResultsView.tsx       # Top-3 Cards & Radar Chart
│   │   │   ├── ComparisonView.tsx    # 3-Way Side-by-Side Matrix
│   │   │   ├── SustainabilityView.tsx# Eco-Alternatives & Trade-offs
│   │   │   ├── SourcesView.tsx       # Scientific Literature & DOIs
│   │   │   ├── ModelDashboard.tsx    # ML Diagnostics & Audit Report
│   │   │   └── ExportDossierModal.tsx# Printable Technical Dossier
│   │   ├── services/
│   │   │   └── api.ts                # Typed API Client
│   │   ├── types/
│   │   │   └── index.ts              # TypeScript Data Contracts
│   │   ├── App.tsx                   # Main Coordinator Component
│   │   └── index.css                 # Custom Styling & Glassmorphism
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── start_app.bat                     # 1-Click Windows Launcher
└── README.md                         # Technical Documentation
```
