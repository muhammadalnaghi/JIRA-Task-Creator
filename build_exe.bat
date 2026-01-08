@echo off
REM Build standalone EXE from Python script using PyInstaller

echo ============================================================
echo Building Jira Task Creator EXE
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller.
        echo Please run: pip install pyinstaller
        pause
        exit /b 1
    )
)

REM Check if requests is installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing requests module...
    python -m pip install requests
)

echo.
echo Building EXE file...
echo This may take a few minutes...
echo.

REM Build the EXE
REM --onefile: Create a single executable file
REM --windowed: No console window (GUI only)
REM --name: Name of the output EXE
REM --clean: Clean PyInstaller cache before building
REM --hidden-import: Include these modules explicitly

pyinstaller --onefile --windowed --name "JiraTaskCreator" --clean ^
    --hidden-import=tkinter ^
    --hidden-import=requests ^
    --hidden-import=json ^
    --hidden-import=base64 ^
    --hidden-import=threading ^
    --hidden-import=importlib ^
    --noconfirm ^
    jira_task_gui.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Build failed!
    echo ============================================================
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Build Complete!
echo ============================================================
echo.
echo EXE file location: dist\JiraTaskCreator.exe
echo.
echo The EXE file is ready for distribution!
echo You can now upload it to GitHub Releases.
echo.
pause

