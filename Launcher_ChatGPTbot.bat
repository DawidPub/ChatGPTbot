@echo off
echo ============================================================
echo              ChatGPT Bot API System Launcher
echo ============================================================
echo.
echo Choose your option:
echo.
echo 1.  Install ALL Dependencies (from requirements.txt)
echo 2.  Install API Dependencies Only (FastAPI, uvicorn, pydantic, requests)
echo 3.  Launch API Launcher (GUI for managing server + client)
echo 4.  Start API Server Only
echo 5.  Start API Client Only  
echo 6.  Start Both Server and Client
echo 7.  Open API Documentation
echo 8.  Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto install_all_deps
if "%choice%"=="2" goto install_api_deps
if "%choice%"=="3" goto launch_gui
if "%choice%"=="4" goto start_server
if "%choice%"=="5" goto start_client
if "%choice%"=="6" goto start_both
if "%choice%"=="7" goto open_docs
if "%choice%"=="8" goto exit
goto invalid_choice

:install_all_deps
echo.
echo  Installing ALL dependencies from requirements.txt...
call install_all_dependencies.bat
goto menu

:install_api_deps
echo.
echo 🔧 Installing API dependencies only...
call install_api_dependencies.bat
goto menu

:launch_gui
echo.
echo  Starting API Launcher GUI...
python chatgpt_api_launcher.py
goto menu

:start_server
echo.
echo  Starting API Server...
echo  API Documentation will be available at: http://localhost:8000/docs
echo  API Root: http://localhost:8000/
echo.
python chatgpt_api_server.py
goto menu

:start_client
echo.
echo  Starting API Client...
echo  Make sure API server is running first!
python chatgpt_api_client.py
goto menu

:start_both
echo.
echo  Starting both Server and Client...
echo.
echo Starting API Server in background...
start "ChatGPT API Server" python chatgpt_api_server.py
echo.
echo Waiting 5 seconds for server to start...
timeout /t 5 /nobreak >nul
echo.
echo Starting API Client...
python chatgpt_api_client.py
goto menu

:open_docs
echo.
echo  Opening API Documentation...
echo  Make sure API server is running first!
start http://localhost:8000/docs
goto menu

:invalid_choice
echo.
echo  Invalid choice. Please enter a number between 1-8.
timeout /t 2 /nobreak >nul
goto menu

:menu
echo.
echo ============================================================
set /p continue="Press Enter to return to menu or type 'exit' to quit: "
if /i "%continue%"=="exit" goto exit
cls
goto start

:exit
echo.
echo Goodbye!
exit /b 0

:start
goto menu
