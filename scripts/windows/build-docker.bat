@echo off
echo 🏗️ Building ChatGPT Bot Docker image...
docker-compose build --no-cache
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ Build completed successfully!
) else (
    echo ❌ Build failed!
)
pause
