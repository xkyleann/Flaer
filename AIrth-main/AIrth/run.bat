@echo off
REM AIrth Platform Launcher
REM Professional Sustainability Intelligence Platform

echo ========================================================================
echo 🌍 Starting AIrth Platform
echo ========================================================================
echo.
echo 📦 Checking dependencies...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✓ Python found
echo.
echo 🚀 Launching application...
echo.

REM Run the application
cd /d "%~dp0"
python src\app.py

pause

@REM Made with Bob
