@echo off
echo ============================================================
echo          📦 Installing ChatGPT Bot API Dependencies
echo ============================================================
echo.
echo Installing required packages for FastAPI server and client...
echo.

REM Get Python executable path
call get_python_executable_details.bat > python_path.txt 2>&1
set /p PYTHON_CMD=<python_path.txt
del python_path.txt

if "%PYTHON_CMD%"=="" (
    echo ❌ Could not determine Python executable path
    echo Trying default python command...
    set PYTHON_CMD=python
)

echo 🐍 Using Python: %PYTHON_CMD%
echo.

echo 📦 Installing API packages from requirements.txt...
%PYTHON_CMD% -m pip install --upgrade pip

REM Install specific API packages
%PYTHON_CMD% -m pip install fastapi>=0.100.0 uvicorn>=0.20.0 pydantic>=2.0.0 requests>=2.28.0

echo.
echo ✅ Installation completed!
echo.
echo 📋 Installed packages:
echo   ✅ fastapi - Web framework for building APIs
echo   ✅ uvicorn - ASGI server for running FastAPI
echo   ✅ pydantic - Data validation using Python type hints  
echo   ✅ requests - HTTP library for API client
echo.
echo 🚀 You can now run:
echo   • chatgpt_api_launcher.py - Full launcher with GUI
echo   • chatgpt_api_server.py - API server only
echo   • chatgpt_api_client.py - API client only
echo.
pause
