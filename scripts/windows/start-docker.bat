@echo off
echo 🐳 Starting ChatGPT Bot Docker...
docker-compose up -d
echo.
echo ✅ ChatGPT Bot started!
echo 🔗 API: http://localhost:8000
echo 🖥️ VNC: localhost:5900
echo 📖 Docs: http://localhost:8000/docs
echo.
pause
