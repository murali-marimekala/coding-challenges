@echo off
REM Algorithm Mastery Platform - Single Command Runner (Windows)
REM Usage: run.bat

setlocal enabledelayedexpansion

REM Change to the script directory
cd /d "%~dp0"

echo.
echo 🎯 Algorithm Mastery Platform
echo ================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo ✓ Python found

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required dependencies...
    python -m pip install -q streamlit plotly pandas pyyaml
    echo ✓ Dependencies installed
)

REM Check if we're in the right directory
if not exist "app.py" (
    echo ⚠️  app.py not found in current directory
    echo Please run this script from the AlgorithmMastery directory
    pause
    exit /b 1
)

echo ================================
echo 🚀 Starting application...
echo ================================
echo.
echo Opening at: http://localhost:8501
echo Press Ctrl+C to stop
echo.

REM Run the streamlit app
python -m streamlit run app.py

pause
