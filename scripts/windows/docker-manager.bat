@echo off
setlocal EnableDelayedExpansion

REM ChatGPT Bot - Docker Management Script for Windows
title ChatGPT Bot - Docker Management

set COMPOSE_FILE=docker-compose.yml
set PROJECT_NAME=chatgpt-bot

:header
cls
echo ============================================================
echo             🐳 ChatGPT Bot - Docker Management
echo ============================================================
echo.

:menu
echo Choose your option:
echo.
echo 📦 Basic Operations:
echo   1. 🚀 Start Production (API + GUI access)
echo   2. 🛠️ Start Development (with hot reload)
echo   3. ⏹️ Stop All Services
echo   4. 🔄 Restart Services
echo   5. 📋 Show Status
echo.
echo 🏗️ Advanced Operations:
echo   6. 🏭 Start Full Stack (API + Redis + Nginx)
echo   7. 📊 Start with Monitoring (+ Prometheus + Grafana)
echo   8. 🗄️ Start with Database (+ PostgreSQL)
echo   9. 🔧 Development Mode (all services)
echo.
echo 🛠️ Maintenance:
echo   10. 🏗️ Build Images
echo   11. 🧹 Clean Up (remove containers, volumes)
echo   12. 📊 View Logs
echo   13. 🔍 Execute Shell in Container
echo   14. 📈 Show Resource Usage
echo.
echo 🌐 Access URLs:
echo   15. 🌍 Show All Access URLs
echo   16. 🖥️ VNC Connection Instructions
echo.
echo   17. ❌ Exit
echo.
set /p choice="Enter your choice (1-17): "

if "%choice%"=="1" goto start_production
if "%choice%"=="2" goto start_development
if "%choice%"=="3" goto stop_all
if "%choice%"=="4" goto restart_services
if "%choice%"=="5" goto show_status
if "%choice%"=="6" goto start_full_stack
if "%choice%"=="7" goto start_monitoring
if "%choice%"=="8" goto start_database
if "%choice%"=="9" goto start_dev_full
if "%choice%"=="10" goto build_images
if "%choice%"=="11" goto cleanup
if "%choice%"=="12" goto view_logs
if "%choice%"=="13" goto exec_shell
if "%choice%"=="14" goto show_resources
if "%choice%"=="15" goto show_all_urls
if "%choice%"=="16" goto connect_vnc
if "%choice%"=="17" goto exit_script
goto invalid_choice

:start_production
echo.
echo 🚀 Starting Production environment...
docker-compose -p %PROJECT_NAME% up -d chatgpt-api
call :show_access_info
echo ✅ Production environment started!
echo 🔗 API available at: http://localhost:8008
echo 🖥️ VNC available at: localhost:5900
goto return_to_menu

:start_development
echo.
echo 🛠️ Starting Development environment...
docker-compose -p %PROJECT_NAME% --profile dev up -d chatgpt-api-dev
echo ✅ Development environment started!
echo 🔗 API available at: http://localhost:8001
echo 🖥️ VNC available at: localhost:5901
echo 📓 Jupyter available at: http://localhost:8888
goto return_to_menu

:stop_all
echo.
echo ⏹️ Stopping all services...
docker-compose -p %PROJECT_NAME% down
echo ✅ All services stopped!
goto return_to_menu

:restart_services
echo.
echo 🔄 Restarting services...
docker-compose -p %PROJECT_NAME% restart
echo ✅ Services restarted!
goto return_to_menu

:show_status
echo.
echo 📋 Current Status:
echo.
docker-compose -p %PROJECT_NAME% ps
echo.
echo 🐳 Docker Images:
docker images | findstr chatgpt
echo.
echo 💾 Volumes:
docker volume ls | findstr chatgpt
goto return_to_menu

:start_full_stack
echo.
echo 🏭 Starting Full Stack (API + Redis + Nginx)...
docker-compose -p %PROJECT_NAME% --profile redis --profile nginx up -d
call :show_access_info
echo ✅ Full stack started!
echo 🔗 Nginx proxy: http://localhost:80
echo 🔗 Direct API: http://localhost:8008
echo 🔗 Redis: localhost:6379
goto return_to_menu

:start_monitoring
echo.
echo 📊 Starting with Monitoring...
docker-compose -p %PROJECT_NAME% --profile monitoring up -d
echo ✅ Monitoring started!
echo 📊 Prometheus: http://localhost:9090
echo 📈 Grafana: http://localhost:3000 (admin/admin)
goto return_to_menu

:start_database
echo.
echo 🗄️ Starting with Database...
docker-compose -p %PROJECT_NAME% --profile database up -d
echo ✅ Database started!
echo 🗄️ PostgreSQL: localhost:5432
goto return_to_menu

:start_dev_full
echo.
echo 🔧 Starting Full Development Stack...
docker-compose -p %PROJECT_NAME% --profile dev --profile redis --profile monitoring up -d
call :show_access_info
echo ✅ Full development stack started!
goto return_to_menu

:build_images
echo.
echo 🏗️ Building Docker images...
docker-compose -p %PROJECT_NAME% build --no-cache
echo ✅ Images built successfully!
goto return_to_menu

:cleanup
echo.
echo ⚠️ This will remove all containers, networks, and volumes!
set /p confirm="Are you sure? (y/N): "
if /i "%confirm%"=="y" (
    echo 🧹 Cleaning up...
    docker-compose -p %PROJECT_NAME% down -v --remove-orphans
    docker system prune -f
    docker volume prune -f
    echo ✅ Cleanup completed!
) else (
    echo Cleanup cancelled.
)
goto return_to_menu

:view_logs
echo.
echo 📊 Available services:
docker-compose -p %PROJECT_NAME% ps --services
echo.
set /p service="Enter service name (or 'all' for all services): "
if "%service%"=="all" (
    docker-compose -p %PROJECT_NAME% logs -f
) else (
    docker-compose -p %PROJECT_NAME% logs -f %service%
)
goto return_to_menu

:exec_shell
echo.
echo 🔍 Available containers:
docker-compose -p %PROJECT_NAME% ps
echo.
set /p container="Enter container name: "
echo Connecting to %container%...
docker exec -it %container% /bin/bash
goto return_to_menu

:show_resources
echo.
echo 📈 Resource Usage:
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
goto return_to_menu

:show_access_info
echo.
echo 🌍 Access Information:
echo ┌─────────────────────────────────────────────────────────┐
echo │ 🔗 API Server:      http://localhost:8008              │
echo │ 📖 API Docs:        http://localhost:8008/docs         │
echo │ 🖥️ VNC GUI:         localhost:5900 (password: none)    │
echo │ 🔄 Health Check:    http://localhost:8008/             │
echo └─────────────────────────────────────────────────────────┘
exit /b

:show_all_urls
call :show_access_info
echo.
echo 🌐 All Possible URLs:
echo ┌─────────────────────────────────────────────────────────┐
echo │ 🏭 Production API:   http://localhost:8008              │
echo │ 🛠️ Development API:  http://localhost:8001              │
echo │ 🌐 Nginx Proxy:     http://localhost:80               │
echo │ 🔴 Redis:           localhost:6379                     │
echo │ 🗄️ PostgreSQL:      localhost:5432                     │
echo │ 📊 Prometheus:      http://localhost:9090              │
echo │ 📈 Grafana:         http://localhost:3000              │
echo │ 📓 Jupyter:         http://localhost:8888              │
echo │ 🖥️ VNC (Prod):      localhost:5900                     │
echo │ 🖥️ VNC (Dev):       localhost:5901                     │
echo └─────────────────────────────────────────────────────────┘
goto return_to_menu

:connect_vnc
echo.
echo 🖥️ VNC Connection Instructions:
echo.
echo 1. Install VNC viewer:
echo    • Windows: TightVNC, RealVNC, or UltraVNC
echo    • Download from official websites
echo.
echo 2. Connect to:
echo    • Production: localhost:5900
echo    • Development: localhost:5901
echo.
echo 3. No password required
echo.
echo 4. You should see the Chrome browser in GUI environment
echo.
echo 5. Recommended VNC clients for Windows:
echo    • TightVNC Viewer (free)
echo    • RealVNC Viewer (free for personal use)
echo    • UltraVNC (free, open source)
goto return_to_menu

:invalid_choice
echo.
echo ❌ Invalid choice. Please enter a number between 1-17.
timeout /t 2 /nobreak >nul
goto header

:return_to_menu
echo.
echo ============================================================
pause
goto header

:exit_script
echo.
echo 👋 Goodbye!
exit /b 0
