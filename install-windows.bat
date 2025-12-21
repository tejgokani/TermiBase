@echo off
REM TermiBase Windows Installation Helper (Batch version)
REM This script helps set up TermiBase on Windows

echo.
echo 🚀 TermiBase Windows Setup
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo 📦 Installing TermiBase...
python -m pip install --upgrade termibase

if errorlevel 1 (
    echo ❌ Installation failed
    pause
    exit /b 1
)

echo.
echo ✓ TermiBase installed successfully!
echo.
echo 💡 You can now use: python -m termibase
echo.
echo To use 'termibase' command directly, run install-windows.ps1 as Administrator
echo or manually add Python Scripts directory to your PATH.
echo.
pause

