@echo off
echo ==============================================================================
echo   PackAI - Intelligent Food Packaging Material Recommendation System
echo   Smart India Hackathon (SIH) 2026 Prototype
echo ==============================================================================
echo.

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8001 ...
start "PackAI Backend Server" cmd /k "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001"

echo [2/2] Starting React + Vite Frontend on http://localhost:5173 ...
cd frontend
start "PackAI Frontend Server" cmd /k "npm run dev"
cd ..

echo.
echo ==============================================================================
echo   Application successfully launched!
echo   - Frontend: http://localhost:5173
echo   - Backend API Docs: http://127.0.0.1:8001/docs
echo ==============================================================================
echo.
pause
