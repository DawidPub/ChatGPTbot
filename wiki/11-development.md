# 🛠️ Development Guide

## 🎯 Development Environment Setup

### Prerequisites
- **Python 3.7+**: Latest stable version recommended
- **Git**: For version control
- **IDE/Editor**: VS Code, PyCharm, or your preferred editor
- **Chrome/Chromium**: For browser automation testing

### Environment Setup
```bash
# Clone repository
git clone https://github.com/your-repo/chatgpt-bot.git
cd chatgpt-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Development Dependencies
```txt
# requirements-dev.txt
# Core dependencies
-r requirements.txt

# Development tools
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.991
pre-commit>=2.20.0

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0

# Testing
pytest-asyncio>=0.21.0
httpx>=0.24.0
pytest-mock>=3.10.0
```

## 🏗️ Project Architecture

### Code Organization
```
chatgpt-bot/
├── src/                     # Source code
│   ├── chatgpt_bot/        # Main package
│   │   ├── __init__.py
│   │   ├── core/           # Core functionality
│   │   ├── gui/            # GUI components
│   │   ├── api/            # API components
│   │   └── utils/          # Utility functions
├── tests/                   # Test files
├── docs/                    # Documentation
├── scripts/                 # Build/deployment scripts
└── examples/                # Usage examples
```

### Design Patterns

#### Singleton Pattern (Bot Manager)
```python
class BotManager:
    _instance = None
    _bots = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_bot(self, session_id: str) -> ChatGPTBot:
        if session_id not in self._bots:
            self._bots[session_id] = ChatGPTBot()
        return self._bots[session_id]
```

#### Observer Pattern (Event System)
```python
from typing import Callable, List
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: dict):
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def notify(self, event: str, data: dict):
        for observer in self._observers:
            observer.update(event, data)
```

#### Factory Pattern (Response Handlers)
```python
class ResponseHandlerFactory:
    _handlers = {}
    
    @classmethod
    def register(cls, response_type: str, handler_class):
        cls._handlers[response_type] = handler_class
    
    @classmethod
    def create_handler(cls, response_type: str):
        handler_class = cls._handlers.get(response_type)
        if handler_class:
            return handler_class()
        raise ValueError(f"Unknown response type: {response_type}")
```

## 🧪 Testing Strategy

### Test Structure
```
tests/
├── unit/                    # Unit tests
│   ├── test_bot_core.py
│   ├── test_api_server.py
│   └── test_gui.py
├── integration/             # Integration tests
│   ├── test_api_integration.py
│   └── test_browser_integration.py
├── e2e/                     # End-to-end tests
│   └── test_full_workflow.py
├── fixtures/                # Test fixtures
└── conftest.py             # Pytest configuration
```

### Unit Testing
```python
# tests/unit/test_bot_core.py
import pytest
from unittest.mock import Mock, patch
from chatgpt_bot_core import ChatGPTBot

class TestChatGPTBot:
    def setup_method(self):
        self.bot = ChatGPTBot()
    
    @patch('selenium.webdriver.Chrome')
    def test_launch_browser_success(self, mock_chrome):
        # Arrange
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        # Act
        result = self.bot.launch_browser(headless=True)
        
        # Assert
        assert result is True
        assert self.bot.driver is not None
        mock_chrome.assert_called_once()
    
    def test_ask_question_without_browser(self):
        # Act & Assert
        with pytest.raises(Exception):
            self.bot.ask_question_and_get_response("test question")
```

### API Testing
```python
# tests/integration/test_api_integration.py
import pytest
from fastapi.testclient import TestClient
from chatgpt_api_server import app

client = TestClient(app)

class TestAPIIntegration:
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_launch_browser_endpoint(self):
        response = client.post("/bot/launch", 
                              json={"headless": True})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data["data"]
    
    @pytest.mark.asyncio
    async def test_ask_question_endpoint(self):
        # First launch browser
        launch_response = client.post("/bot/launch", 
                                     json={"headless": True})
        session_id = launch_response.json()["data"]["session_id"]
        
        # Then ask question
        response = client.post("/bot/ask", 
                              json={
                                  "question": "Hello",
                                  "session_id": session_id
                              })
        assert response.status_code == 200
```

### Mocking External Dependencies
```python
# tests/conftest.py
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_webdriver():
    with patch('selenium.webdriver.Chrome') as mock:
        driver_mock = Mock()
        mock.return_value = driver_mock
        yield driver_mock

@pytest.fixture
def mock_chatgpt_response():
    return "This is a mocked ChatGPT response for testing."

@pytest.fixture
def api_client():
    from fastapi.testclient import TestClient
    from chatgpt_api_server import app
    return TestClient(app)
```

## 🔧 Code Quality Tools

### Linting Configuration

#### .flake8
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    venv,
    .venv,
    build,
    dist
```

#### pyproject.toml (Black configuration)
```toml
[tool.black]
line-length = 88
target-version = ['py37', 'py38', 'py39']
include = '\.pyi?$'
exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.7"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  