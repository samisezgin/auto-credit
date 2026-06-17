@echo off
chcp 65001 >nul 2>&1
title Bot Detection Test

echo ==================================================
echo   Bot Detection Test
echo ==================================================
echo.

:: Python kontrolu
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing...
    winget install Python.Python.3.13 --accept-source-agreements --accept-package-agreements
    if %errorlevel% neq 0 (
        echo ERROR: Python installation failed.
        pause
        exit /b 1
    )
    echo Python installed. Close terminal and run again.
    pause
    exit /b 0
)

:: Venv (ana projenin venv'ini kullan)
if not exist "..\\.venv\\Scripts\\python.exe" (
    echo Creating virtual environment...
    python -m venv ..\.venv
)

:: Paketleri kur (selenium dahil)
echo Checking packages...
..\.venv\Scripts\pip install -r requirements.txt --quiet

:: Calistir
echo.
echo DO NOT touch the mouse!
echo.
..\.venv\Scripts\python test_runner.py

pause
