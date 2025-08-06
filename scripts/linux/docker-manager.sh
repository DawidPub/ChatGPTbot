#!/bin/bash

# ChatGPT Bot - Docker Management Script
# Comprehensive Docker management for all environments

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

COMPOSE_FILE="docker-compose.yml"
PROJECT_NAME="chatgpt-bot"

show_header() {
    clear
    echo "============================================================"
    echo -e "${CYAN}🐳 ChatGPT Bot - Docker Management${NC}"
    echo "============================================================"
    echo ""
}

show_menu() {
    echo -e "${CYAN}Choose your option:${NC}"
    echo ""
    echo -e "${YELLOW}📦 Basic Operations:${NC}"
    echo "  1. 🚀 Start Production (API + GUI access)"
    echo "  2. 🛠️ Start Development (with hot reload)"
    echo "  3. ⏹️ Stop All Services"
    echo "  4. 🔄 Restart Services"
    echo "  5. 📋 Show Status"
    echo ""
    echo -e "${YELLOW}🏗️ Advanced Operations:${NC}"
    echo "  6. 🏭 Start Full Stack (API + Redis + Nginx)"
    echo "  7. 📊 Start with Monitoring (+ Prometheus + Grafana)"
    echo "  8. 🗄️ Start with Database (+ PostgreSQL)"
    echo "  9. 🔧 Development Mode (all services)"
    echo ""
    echo -e "${YELLOW}🛠️ Maintenance:${NC}"
    echo "  10. 🏗️ Build Images"
    echo "  11. 🧹 Clean Up (remove containers, volumes)"
    echo "  12. 📊 View Logs"
    echo "  13. 🔍 Execute Shell in Container"
    echo "  14. 📈 Show Resource Usage"
    echo ""
    echo -e "${YELLOW}🌐 Access URLs:${NC}"
    echo "  15. 🌍 Show All Access URLs"
    echo "  16. 🖥️ Connect to VNC (GUI access)"
    echo ""
    echo "  17. ❌ Exit"
    echo ""
    echo -n "Enter your choice (1-17): "
}

start_production() {
    echo -e "${BLUE}🚀 Starting Production environment...${NC}"
    docker-compose -p $PROJECT_NAME up -d chatgpt-api
    show_access_info
    
    echo -e "${GREEN}✅ Production environment started!${NC}"
    echo -e "${YELLOW}🔗 API available at: http://localhost:8008${NC}"
    echo -e "${YELLOW}🖥️ VNC available at: localhost:5900${NC}"
}

start_development() {
    echo -e "${BLUE}🛠️ Starting Development environment...${NC}"
    docker-compose -p $PROJECT_NAME --profile dev up -d chatgpt-api-dev
    
    echo -e "${GREEN}✅ Development environment started!${NC}"
    echo -e "${YELLOW}🔗 API available at: http://localhost:8001${NC}"
    echo -e "${YELLOW}🖥️ VNC available at: localhost:5901${NC}"
    echo -e "${YELLOW}📓 Jupyter available at: http://localhost:8888${NC}"
}

stop_all() {
    echo -e "${BLUE}⏹️ Stopping all services...${NC}"
    docker-compose -p $PROJECT_NAME down
    echo -e "${GREEN}✅ All services stopped!${NC}"
}

restart_services() {
    echo -e "${BLUE}🔄 Restarting services...${NC}"
    docker-compose -p $PROJECT_NAME restart
    echo -e "${GREEN}✅ Services restarted!${NC}"
}

show_status() {
    echo -e "${BLUE}📋 Current Status:${NC}"
    echo ""
    docker-compose -p $PROJECT_NAME ps
    echo ""
    
    echo -e "${BLUE}🐳 Docker Images:${NC}"
    docker images | grep chatgpt
    echo ""
    
    echo -e "${BLUE}💾 Volumes:${NC}"
    docker volume ls | grep chatgpt
}

start_full_stack() {
    echo -e "${BLUE}🏭 Starting Full Stack (API + Redis + Nginx)...${NC}"
    docker-compose -p $PROJECT_NAME --profile redis --profile nginx up -d
    show_access_info
    
    echo -e "${GREEN}✅ Full stack started!${NC}"
    echo -e "${YELLOW}🔗 Nginx proxy: http://localhost:80${NC}"
    echo -e "${YELLOW}🔗 Direct API: http://localhost:8008${NC}"
    echo -e "${YELLOW}🔗 Redis: localhost:6379${NC}"
}

start_monitoring() {
    echo -e "${BLUE}📊 Starting with Monitoring...${NC}"
    docker-compose -p $PROJECT_NAME --profile monitoring up -d
    
    echo -e "${GREEN}✅ Monitoring started!${NC}"
    echo -e "${YELLOW}📊 Prometheus: http://localhost:9090${NC}"
    echo -e "${YELLOW}📈 Grafana: http://localhost:3000 (admin/admin)${NC}"
}

start_database() {
    echo -e "${BLUE}🗄️ Starting with Database...${NC}"
    docker-compose -p $PROJECT_NAME --profile database up -d
    
    echo -e "${GREEN}✅ Database started!${NC}"
    echo -e "${YELLOW}🗄️ PostgreSQL: localhost:5432${NC}"
}

start_dev_full() {
    echo -e "${BLUE}🔧 Starting Full Development Stack...${NC}"
    docker-compose -p $PROJECT_NAME --profile dev --profile redis --profile monitoring up -d
    
    echo -e "${GREEN}✅ Full development stack started!${NC}"
    show_access_info
}

build_images() {
    echo -e "${BLUE}🏗️ Building Docker images...${NC}"
    docker-compose -p $PROJECT_NAME build --no-cache
    echo -e "${GREEN}✅ Images built successfully!${NC}"
}

cleanup() {
    echo -e "${YELLOW}⚠️ This will remove all containers, networks, and volumes!${NC}"
    echo -n "Are you sure? (y/N): "
    read confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}🧹 Cleaning up...${NC}"
        docker-compose -p $PROJECT_NAME down -v --remove-orphans
        docker system prune -f
        docker volume prune -f
        echo -e "${GREEN}✅ Cleanup completed!${NC}"
    else
        echo -e "${YELLOW}Cleanup cancelled.${NC}"
    fi
}

view_logs() {
    echo -e "${BLUE}📊 Available services:${NC}"
    docker-compose -p $PROJECT_NAME ps --services
    echo ""
    echo -n "Enter service name (or 'all' for all services): "
    read service
    
    if [ "$service" = "all" ]; then
        docker-compose -p $PROJECT_NAME logs -f
    else
        docker-compose -p $PROJECT_NAME logs -f $service
    fi
}

exec_shell() {
    echo -e "${BLUE}🔍 Available containers:${NC}"
    docker-compose -p $PROJECT_NAME ps
    echo ""
    echo -n "Enter container name: "
    read container
    
    echo -e "${BLUE}Connecting to $container...${NC}"
    docker exec -it $container /bin/bash
}

show_resources() {
    echo -e "${BLUE}📈 Resource Usage:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
}

show_access_info() {
    echo ""
    echo -e "${CYAN}🌍 Access Information:${NC}"
    echo "┌─────────────────────────────────────────────────────────┐"
    echo "│ 🔗 API Server:      http://localhost:8008              │"
    echo "│ 📖 API Docs:        http://localhost:8008/docs         │"
    echo "│ 🖥️ VNC GUI:         localhost:5900 (password: none)    │"
    echo "│ 🔄 Health Check:    http://localhost:8008/             │"
    echo "└─────────────────────────────────────────────────────────┘"
}

show_all_urls() {
    show_access_info
    echo ""
    echo -e "${CYAN}🌐 All Possible URLs:${NC}"
    echo "┌─────────────────────────────────────────────────────────┐"
    echo "│ 🏭 Production API:   http://localhost:8008              │"
    echo "│ 🛠️ Development API:  http://localhost:8001              │"
    echo "│ 🌐 Nginx Proxy:     http://localhost:80               │"
    echo "│ 🔴 Redis:           localhost:6379                     │"
    echo "│ 🗄️ PostgreSQL:      localhost:5432                     │"
    echo "│ 📊 Prometheus:      http://localhost:9090              │"
    echo "│ 📈 Grafana:         http://localhost:3000              │"
    echo "│ 📓 Jupyter:         http://localhost:8888              │"
    echo "│ 🖥️ VNC (Prod):      localhost:5900                     │"
    echo "│ 🖥️ VNC (Dev):       localhost:5901                     │"
    echo "└─────────────────────────────────────────────────────────┘"
}

connect_vnc() {
    echo -e "${BLUE}🖥️ VNC Connection Instructions:${NC}"
    echo ""
    echo "1. Install VNC viewer:"
    echo "   • Windows: TightVNC, RealVNC, or UltraVNC"
    echo "   • Linux: vinagre, remmina, or tightvncviewer"
    echo "   • macOS: Screen Sharing or VNC Viewer"
    echo ""
    echo "2. Connect to:"
    echo "   • Production: localhost:5900"
    echo "   • Development: localhost:5901"
    echo ""
    echo "3. No password required"
    echo ""
    echo "4. You should see the Chrome browser in GUI environment"
}

main_loop() {
    while true; do
        show_header
        show_menu
        read choice
        
        case $choice in
            1) start_production ;;
            2) start_development ;;
            3) stop_all ;;
            4) restart_services ;;
            5) show_status ;;
            6) start_full_stack ;;
            7) start_monitoring ;;
            8) start_database ;;
            9) start_dev_full ;;
            10) build_images ;;
            11) cleanup ;;
            12) view_logs ;;
            13) exec_shell ;;
            14) show_resources ;;
            15) show_all_urls ;;
            16) connect_vnc ;;
            17) echo -e "${GREEN}👋 Goodbye!${NC}"; exit 0 ;;
            *) echo -e "${RED}❌ Invalid choice. Please try again.${NC}" ;;
        esac
        
        echo ""
        echo "Press Enter to continue..."
        read
    done
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed!${NC}"
    echo "Please install Docker Compose first: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create necessary directories
mkdir -p data logs sessions docker/ssl

# Start main loop
main_loop
