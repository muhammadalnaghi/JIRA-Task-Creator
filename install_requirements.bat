@echo off
echo Installing required Python packages...
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Failed to install requirements.
    echo Please check your Python installation and internet connection.
    pause
    exit /b 1
)

echo.
echo Installation complete!
pause

