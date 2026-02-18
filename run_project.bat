@echo off
TITLE FraudGuard - Unified Server
:: Ensure we are in the script's directory
cd /d "%~dp0"

echo ==========================================
echo   Starting FraudGuard Detection System
echo ==========================================

echo 1. Opening Browser...
:: Opens the frontend immediately (it might take a few seconds to load)
start http://127.0.0.1:5000

echo 2. Starting Backend Server...
echo    (DO NOT CLOSE THIS WINDOW)
echo.

:: Navigate to the functions directory where main.py and models are located
cd firebase_app\functions

:: Run Python using the virtual environment directly
"..\..\venv\Scripts\python.exe" main.py

:: If python crashes, pause so user can read the error
pause
