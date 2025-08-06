# ChatGPT Bot - Makefile for Linux/Unix systems
# Usage: make <target>

.PHONY: help install install-api check-deps clean test run-api run-bot server client both docs

# Default Python command
PYTHON := $(shell command -v python3 2> /dev/null || command -v python 2> /dev/null)

# Default target
help:
	@echo "============================================================"
	@echo "            🚀 ChatGPT Bot - Available Commands"
	@echo "============================================================"
	@echo ""
	@echo "📦 Installation:"
	@echo "  make install        - Install all dependencies"
	@echo "  make install-api    - Install API dependencies only"
	@echo "  make check-deps     - Check installed dependencies"
	@echo ""
	@echo "🚀 Running:"
	@echo "  make run-api        - Launch API system menu" 
	@echo "  make run-bot        - Run original ChatGPT Bot"
	@echo "  make server         - Start API server only"
	@echo "  make client         - Start API client only"
	@echo "  make both           - Start server and client"
	@echo "  make docs           - Open API documentation"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test           - Run API tests"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make clean          - Clean temporary files"
	@echo "  make permissions    - Fix script permissions"
	@echo ""

# Check if Python is available
check-python:
	@if [ -z "$(PYTHON)" ]; then \
		echo "❌ Python not found. Please install Python 3.7+"; \
		exit 1; \
	fi
	@echo "🐍 Using Python: $(shell $(PYTHON) --version)"

# Fix permissions for shell scripts
permissions:
	@echo "🔧 Setting executable permissions..."
	@chmod +x *.sh
	@echo "✅ Permissions set"

# Install all dependencies
install: check-python permissions
	@echo "📦 Installing all dependencies..."
	@./install_all_dependencies.sh

# Install API dependencies only
install-api: check-python permissions
	@echo "🔧 Installing API dependencies..."
	@./install_api_dependencies.sh

# Check dependencies status
check-deps: check-python permissions
	@echo "🔍 Checking dependencies..."
	@./check_dependencies.sh

# Run API system launcher
run-api: check-python permissions
	@echo "🚀 Starting API system..."
	@./run_chatgpt_api.sh

# Run original bot
run-bot: check-python permissions
	@echo "🤖 Starting ChatGPT Bot..."
	@./run_chatgpt_bot_working.sh

# Start API server only
server: check-python
	@echo "🖥️ Starting API server..."
	@$(PYTHON) chatgpt_api_server.py

# Start API client only
client: check-python
	@echo "💻 Starting API client..."
	@$(PYTHON) chatgpt_api_client.py

# Start both server and client
both: check-python
	@echo "🚀 Starting both server and client..."
	@$(PYTHON) chatgpt_api_server.py &
	@sleep 5
	@$(PYTHON) chatgpt_api_client.py

# Open API documentation
docs:
	@echo "📖 Opening API documentation..."
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:8008/docs; \
	elif command -v open >/dev/null 2>&1; then \
		open http://localhost:8008/docs; \
	else \
		echo "Please open: http://localhost:8008/docs"; \
	fi

# Run API tests
test: check-python
	@echo "🧪 Running API tests..."
	@$(PYTHON) test/test_api.py

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	@rm -rf __pycache__/
	@rm -rf .pytest_cache/
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -f *.pyc
	@rm -f *.pyo
	@rm -f check_packages.py
	@rm -f chatgpt_cookies.pkl
	@rm -f chatgpt_session.json
	@rm -f chatgpt_answer.txt
	@rm -f chatgpt_api_answer.txt
	@echo "✅ Cleanup complete"

# Development targets
dev-install: install
	@echo "🛠️ Installing development dependencies..."
	@$(PYTHON) -m pip install pytest black flake8

lint: check-python
	@echo "🔍 Running code linting..."
	@$(PYTHON) -m flake8 *.py || echo "⚠️ Linting issues found"

format: check-python
	@echo "✨ Formatting code..."
	@$(PYTHON) -m black *.py || echo "⚠️ Black not installed"

# Show system information
info: check-python
	@echo "============================================================"
	@echo "                   📊 System Information"
	@echo "============================================================"
	@echo "🐍 Python: $(shell $(PYTHON) --version)"
	@echo "📦 Pip: $(shell $(PYTHON) -m pip --version | head -n1)"
	@echo "💻 OS: $(shell uname -s) $(shell uname -r)"
	@echo "🏠 Directory: $(shell pwd)"
	@echo "📁 Files: $(shell ls -1 *.py | wc -l) Python files"
	@echo "============================================================"
