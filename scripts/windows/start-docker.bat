@echo off
echo 🐳 Starting ChatGPT Bot Docker...
docker-compose up -d
echo.
echo ✅ ChatGPT Bot started!
echo 🔗 API: http://localhost:8008
echo 🖥️ VNC: localhost:5900
echo 📖 Docs: http://localhost:8008/docs
echo.
pause
