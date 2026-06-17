@echo off
chcp 65001 >nul 2>&1
title Student Grade Automation

echo ==================================================
echo   Student Grade Entry Automation
echo ==================================================
echo.

:: Python kontrolu
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing...
    echo.
    winget install Python.Python.3.13 --accept-source-agreements --accept-package-agreements
    if %errorlevel% neq 0 (
        echo ERROR: Python installation failed.
        echo Install manually: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    echo.
    echo Python installed. Close terminal and run again.
    pause
    exit /b 0
)

:: Venv kontrolu ve olusturma
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Paketleri kur
echo Checking packages...
.venv\Scripts\pip install -r requirements.txt --quiet

:: Calistir
echo.
.venv\Scripts\python automation.py

pause
