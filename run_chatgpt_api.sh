#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo "============================================================"
echo "             🚀 ChatGPT Bot API System Launcher"
echo "============================================================"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found. Please install Python 3.7+${NC}"
    exit 1
fi

show_menu() {
    echo ""
    echo -e "${CYAN}Choose your option:${NC}"
    echo ""
    echo -e "${YELLOW}1.${NC} 📦 Install ALL Dependencies (from requirements.txt)"
    echo -e "${YELLOW}2.${NC} 🔧 Install API Dependencies Only (FastAPI, uvicorn, pydantic, requests)"
    echo -e "${YELLOW}3.${NC} 🎛️ Launch API Launcher (GUI for managing server + client)"
    echo -e "${YELLOW}4.${NC} 🖥️ Start API Server Only"
    echo -e "${YELLOW}5.${NC} 💻 Start API Client Only"
    echo -e "${YELLOW}6.${NC} 🚀 Start Both Server and Client"
    echo -e "${YELLOW}7.${NC} 📖 Open API Documentation"
    echo -e "${YELLOW}8.${NC} 🔍 Check Dependencies Status"
    echo -e "${YELLOW}9.${NC} 🧪 Run API Tests"
    echo -e "${YELLOW}10.${NC} ❌ Exit"
    echo ""
    echo -n "Enter your choice (1-10): "
}

install_all_deps() {
    echo ""
    echo -e "${BLUE}📦 Installing ALL dependencies from requirements.txt...${NC}"
    ./install_all_dependencies.sh
    return_to_menu
}

install_api_deps() {
    echo ""
    echo -e "${BLUE}🔧 Installing API dependencies only...${NC}"
    ./install_api_dependencies.sh
    return_to_menu
}

launch_gui() {
    echo ""
    echo -e "${BLUE}🎛️ Starting API Launcher GUI...${NC}"
    $PYTHON_CMD chatgpt_api_launcher.py
    return_to_menu
}

start_server() {
    echo ""
    echo -e "${BLUE}🖥️ Starting API Server...${NC}"
    echo -e "${CYAN}📖 API Documentation will be available at: http://localhost:8000/docs${NC}"
    echo -e "${CYAN}🔗 API Root: http://localhost:8000/${NC}"
    echo ""
    $PYTHON_CMD chatgpt_api_server.py
    return_to_menu
}

start_client() {
    echo ""
    echo -e "${BLUE}💻 Starting API Client...${NC}"
    echo -e "${YELLOW}💡 Make sure API server is running first!${NC}"
    $PYTHON_CMD chatgpt_api_client.py
    return_to_menu
}

start_both() {
    echo ""
    echo -e "${BLUE}🚀 Starting both Server and Client...${NC}"
    echo ""
    echo "Starting API Server in background..."
    $PYTHON_CMD chatgpt_api_server.py &
    SERVER_PID=$!
    echo "Server PID: $SERVER_PID"
    echo ""
    echo "Waiting 5 seconds for server to start..."
    sleep 5
    echo ""
    echo "Starting API Client..."
    $PYTHON_CMD chatgpt_api_client.py
    
    # Kill server when client exits
    echo ""
    echo "Stopping API Server (PID: $SERVER_PID)..."
    kill $SERVER_PID 2>/dev/null
    return_to_menu
}

open_docs() {
    echo ""
    echo -e "${BLUE}📖 Opening API Documentation...${NC}"
    echo -e "${YELLOW}💡 Make sure API server is running first!${NC}"
    
    # Try different browsers
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8000/docs
    elif command -v gnome-open &> /dev/null; then
        gnome-open http://localhost:8000/docs
    elif command -v firefox &> /dev/null; then
        firefox http://localhost:8000/docs &
    elif command -v chromium-browser &> /dev/null; then
        chromium-browser http://localhost:8000/docs &
    elif command -v google-chrome &> /dev/null; then
        google-chrome http://localhost:8000/docs &
    else
        echo -e "${YELLOW}Could not find browser. Please open: http://localhost:8000/docs${NC}"
    fi
    return_to_menu
}

check_deps() {
    echo ""
    echo -e "${BLUE}🔍 Checking dependencies status...${NC}"
    ./check_dependencies.sh
    return_to_menu
}

run_tests() {
    echo ""
    echo -e "${BLUE}🧪 Running API tests...${NC}"
    echo -e "${YELLOW}💡 Make sure API server is running first!${NC}"
    echo ""
    echo "Press Enter to continue or Ctrl+C to cancel..."
    read
    $PYTHON_CMD test_api.py
    return_to_menu
}

return_to_menu() {
    echo ""
    echo "============================================================"
    echo -n "Press Enter to return to menu or type 'exit' to quit: "
    read continue_choice
    if [ "$continue_choice" = "exit" ] || [ "$continue_choice" = "quit" ] || [ "$continue_choice" = "q" ]; then
        exit_script
    fi
    clear
    main_loop
}

exit_script() {
    echo ""
    echo -e "${GREEN}👋 Goodbye!${NC}"
    exit 0
}

invalid_choice() {
    echo ""
    echo -e "${RED}❌ Invalid choice. Please enter a number between 1-10.${NC}"
    sleep 2
    clear
    main_loop
}

main_loop() {
    show_menu
    read choice
    
    case $choice in
        1) install_all_deps ;;
        2) install_api_deps ;;
        3) launch_gui ;;
        4) start_server ;;
        5) start_client ;;
        6) start_both ;;
        7) open_docs ;;
        8) check_deps ;;
        9) run_tests ;;
        10) exit_script ;;
        *) invalid_choice ;;
    esac
}

# Make sure scripts are executable
chmod +x install_all_dependencies.sh 2>/dev/null
chmod +x install_api_dependencies.sh 2>/dev/null
chmod +x check_dependencies.sh 2>/dev/null

# Start main loop
main_loop
