@echo off
REM Build script for Windows

echo ========================================
echo   Building Tetris for Windows
echo ========================================
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install -q -r requirements-dev.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

REM Run build script
echo.
echo Building executable...
python build.py

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo The executable is in the "dist" folder
echo File: Tetris_Launcher.exe
echo.
echo You can now share this file with your friends!
echo No Python installation needed to run it.
echo.
pause

