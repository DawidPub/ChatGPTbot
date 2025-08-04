@echo off
echo 🧪 Testing ChatGPT Bot Docker Setup...
echo.

REM Check if Docker is running
echo ✅ Checking Docker...
docker version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not running! Please start Docker Desktop.
    pause
    exit /b 1
)
echo ✅ Docker is running

REM Check if docker-compose.yml exists
echo ✅ Checking docker-compose.yml...
if not exist docker-compose.yml (
    echo ❌ docker-compose.yml not found!
    pause
    exit /b 1
)
echo ✅ docker-compose.yml found

REM Check if Dockerfile exists
echo ✅ Checking Dockerfile...
if not exist Dockerfile (
    echo ❌ Dockerfile not found!
    pause
    exit /b 1
)
echo ✅ Dockerfile found

REM Test docker-compose configuration
echo ✅ Testing docker-compose configuration...
docker-compose config >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ docker-compose.yml has configuration errors!
    docker-compose config
    pause
    exit /b 1
)
echo ✅ docker-compose.yml is valid

REM Check available ports
echo ✅ Checking port availability...
netstat -ano | findstr :8000 >nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️ Port 8000 is already in use!
    echo You may need to stop other services or change the port.
)

netstat -ano | findstr :5900 >nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️ Port 5900 (VNC) is already in use!
    echo You may need to stop VNC services.
)

echo.
echo 🎉 All checks passed! Your setup looks good.
echo.
echo 🚀 Ready to run ChatGPT Bot Docker!
echo.
echo Next steps:
echo 1. Run: start-docker.bat
echo 2. Wait for startup (may take a few minutes first time)
echo 3. Open: http://localhost:8000
echo 4. VNC: localhost:5900
echo.
pause
