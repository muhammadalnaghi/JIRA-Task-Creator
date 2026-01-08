@echo off
echo Starting Jira Task Creator GUI...
echo.

REM Check if requests module is installed
python -c "import requests" 2>nul
if errorlevel 1 (
    echo Warning: 'requests' module not found.
    echo.
    echo Installing required dependencies...
    python -m pip install requests
    if errorlevel 1 (
        echo.
        echo Error: Could not install 'requests' module.
        echo Please install it manually by running:
        echo   pip install requests
        echo.
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
    echo.
)

REM Run the GUI
python jira_task_gui.py
if errorlevel 1 (
    echo.
    echo Error: Could not start the application.
    echo Make sure Python is installed and in your PATH.
    pause
)

