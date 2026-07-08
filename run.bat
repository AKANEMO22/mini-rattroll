@echo off
title Adaptive Hybrid Recommender Platform
echo ===================================================
echo Starting Adaptive Hybrid Recommender Platform...
echo ===================================================

echo [1/2] Starting FastAPI Backend (Port 8000)...
start "FastAPI Backend" cmd /k "python -m uvicorn api.server:app --port 8000 --reload --reload-dir api --reload-dir src"

echo [2/2] Starting React Frontend (Vite)...
cd fontend
echo Installing frontend dependencies if needed...
call npm install
start "React Frontend" cmd /k "npm run dev"

echo.
echo All services have been launched in separate windows!
echo - Backend API: http://127.0.0.1:8000
echo - React UI:    http://localhost:5173
echo.
echo You can now close this window. The background services will keep running in their own windows.
pause
