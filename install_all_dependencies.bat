@echo off
echo ============================================================
echo        📦 ChatGPT Bot - Complete Dependencies Install
echo ============================================================
echo.
echo Installing ALL required packages from requirements.txt...
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    echo Make sure you're in the correct directory.
    pause
    exit /b 1
)

REM Get Python executable path
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo Trying alternative Python paths...
    
    REM Try common Python installations
    if exist "C:\Program Files\Python312\python.exe" (
        set PYTHON_CMD="C:\Program Files\Python312\python.exe"
        echo 🐍 Found Python: %PYTHON_CMD%
    ) else if exist "C:\Python312\python.exe" (
        set PYTHON_CMD="C:\Python312\python.exe"
        echo 🐍 Found Python: %PYTHON_CMD%
    ) else (
        echo ❌ Could not find Python installation
        echo Please install Python or add it to PATH
        pause
        exit /b 1
    )
) else (
    set PYTHON_CMD=python
    echo 🐍 Using Python from PATH
)

echo.
echo 📋 Current requirements.txt contents:
echo ============================================================
type requirements.txt
echo ============================================================
echo.

echo 🚀 Starting installation...
echo.

REM Upgrade pip first
echo 📦 Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip

REM Install all packages from requirements.txt
echo.
echo 📦 Installing packages from requirements.txt...
%PYTHON_CMD% -m pip install -r requirements.txt

REM Check installation
echo.
echo 🔍 Verifying installation...
%PYTHON_CMD% -c "
import sys
packages = ['selenium', 'webdriver_manager', 'fastapi', 'uvicorn', 'pydantic', 'requests']
failed = []
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg} - OK')
    except ImportError:
        print(f'❌ {pkg} - FAILED')
        failed.append(pkg)

if failed:
    print(f'\n❌ Failed packages: {failed}')
    sys.exit(1)
else:
    print('\n🎉 All core packages installed successfully!')
"

if errorlevel 1 (
    echo.
    echo ❌ Some packages failed to install or import
    echo 💡 Try running: python -m pip install --upgrade --force-reinstall -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ============================================================
echo                    🎉 Installation Complete!
echo ============================================================
echo.
echo ✅ All packages installed successfully!
echo.
echo 🚀 You can now run:
echo   • RUN_ChatGPT_API.bat - Full API system
echo   • RUN_ChatGPT_Bot_WORKING.bat - Original bot
echo   • python chatgpt_api_launcher.py - API launcher GUI
echo.
echo 📖 For more info see:
echo   • README_API.md - API documentation
echo   • INSTALL.md - Detailed installation guide
echo.
pause
