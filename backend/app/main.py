"""
PackAI - Intelligent Food Packaging Material Recommendation System
FastAPI Application Entrypoint
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.api.api_router import api_router

app = FastAPI(
    title="PackAI - Intelligent Food Packaging Material Recommendation API",
    description=(
        "Production-grade Decision-Support Engine for Food Packaging Materials & Structures. "
        "Grounded in physical mass-transfer equations, ASTM empirical permeabilities, and explainable ML scoring."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for local development and SIH demonstrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    """System health check and operational status."""
    return {
        "status": "healthy",
        "service": "PackAI Recommendation Backend",
        "version": "1.0.0",
        "framework": "FastAPI",
        "engine": "Hybrid AI (Domain Physics + Random Forest Suitability Scorer)"
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "name": "PackAI API",
        "docs": "/docs",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "foods": "/api/v1/foods",
            "packaging": "/api/v1/packaging",
            "recommend": "/api/v1/recommend",
            "validate_input": "/api/v1/validate-input",
            "sources": "/api/v1/sources",
            "model_info": "/api/v1/model-info",
            "history": "/api/v1/history"
        }
    }

# Mount v1 API
app.include_router(api_router, prefix="/api/v1", tags=["Packaging Recommendation"])
