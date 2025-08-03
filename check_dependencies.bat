@echo off
echo ============================================================
echo        🔍 ChatGPT Bot - Check Installed Packages
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH
    pause
    exit /b 1
)

echo 🐍 Python version:
python --version
echo.

echo 📦 Checking installed packages...
echo ============================================================

REM Create temporary Python script to check packages
echo import sys > check_packages.py
echo packages = [ >> check_packages.py
echo     ('selenium', 'selenium'), >> check_packages.py
echo     ('webdriver-manager', 'webdriver_manager'), >> check_packages.py
echo     ('fastapi', 'fastapi'), >> check_packages.py
echo     ('uvicorn', 'uvicorn'), >> check_packages.py
echo     ('pydantic', 'pydantic'), >> check_packages.py
echo     ('requests', 'requests'), >> check_packages.py
echo     ('pyinstaller', 'PyInstaller'), >> check_packages.py
echo     ('pytest', 'pytest'), >> check_packages.py
echo     ('black', 'black'), >> check_packages.py
echo     ('flake8', 'flake8'), >> check_packages.py
echo     ('python-multipart', 'multipart'), >> check_packages.py
echo     ('aiofiles', 'aiofiles') >> check_packages.py
echo ] >> check_packages.py
echo. >> check_packages.py
echo installed = [] >> check_packages.py
echo missing = [] >> check_packages.py
echo. >> check_packages.py
echo for display_name, import_name in packages: >> check_packages.py
echo     try: >> check_packages.py
echo         module = __import__(import_name) >> check_packages.py
echo         version = getattr(module, '__version__', 'unknown') >> check_packages.py
echo         print(f'✅ {display_name:<20} {version}') >> check_packages.py
echo         installed.append(display_name) >> check_packages.py
echo     except ImportError: >> check_packages.py
echo         print(f'❌ {display_name:<20} NOT INSTALLED') >> check_packages.py
echo         missing.append(display_name) >> check_packages.py
echo. >> check_packages.py
echo print() >> check_packages.py
echo print('============================================================') >> check_packages.py
echo print(f'📊 Summary: {len(installed)} installed, {len(missing)} missing') >> check_packages.py
echo. >> check_packages.py
echo if missing: >> check_packages.py
echo     print('❌ Missing packages:', ', '.join(missing)) >> check_packages.py
echo     print('💡 Run: pip install ' + ' '.join(missing)) >> check_packages.py
echo     print('💡 Or run: install_all_dependencies.bat') >> check_packages.py
echo else: >> check_packages.py
echo     print('🎉 All packages are installed!') >> check_packages.py

REM Run the check
python check_packages.py

REM Clean up
del check_packages.py

echo.
echo ============================================================
echo.
echo 💡 Available installation options:
echo   • install_all_dependencies.bat - Install all packages
echo   • install_api_dependencies.bat - Install API packages only
echo   • pip install -r requirements.txt - Manual installation
echo.
pause
