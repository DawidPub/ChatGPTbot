# 🌐 API Reference

## 📋 Przegląd API

ChatGPT Bot API to RESTful API zbudowane na FastAPI, umożliwiające zdalne zarządzanie instancjami ChatGPT Bot.

**Base URL**: `http://localhost:8008`
**Content-Type**: `application/json`

## 🔐 Uwierzytelnianie

Obecnie API nie wymaga uwierzytelniania. W przyszłych wersjach planowane jest dodanie:
- API Keys
- JWT Tokens
- OAuth 2.0

## 🤖 Bot Management Endpoints

### POST /bot/launch
Uruchamia nową instancję przeglądarki.

**Request Body:**
```json
{
    "headless": false,
    "session_id": "optional-session-id"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Browser launched successfully",
    "data": {
        "session_id": "generated-session-id",
        "browser_status": "running"
    }
}
```

### POST /bot/close
Zamyka instancję przeglądarki.

**Request Body:**
```json
{
    "session_id": "session-id"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Browser closed successfully"
}
```

### POST /bot/ask
Wysyła pytanie do ChatGPT.

**Request Body:**
```json
{
    "question": "What is artificial intelligence?",
    "session_id": "session-id"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Question processed successfully",
    "data": {
        "question": "What is artificial intelligence?",
        "answer": "Artificial intelligence (AI) refers to...",
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

### GET /bot/status
Sprawdza status bota.

**Query Parameters:**
- `session_id` (optional): ID sesji

**Response:**
```json
{
    "success": true,
    "data": {
        "session_id": "session-id",
        "browser_running": true,
        "last_activity": "2024-01-15T10:30:00Z",
        "status": "ready"
    }
}
```

### POST /bot/load-state
Ładuje zapisany stan sesji.

**Request Body:**
```json
{
    "session_id": "session-id"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Browser state loaded successfully"
}
```

### POST /bot/save-state
Zapisuje aktualny stan sesji.

**Request Body:**
```json
{
    "session_id": "session-id"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Browser state saved successfully"
}
```

## 📊 Session Management Endpoints

### GET /sessions
Lista wszystkich aktywnych sesji.

**Response:**
```json
{
    "success": true,
    "data": {
        "sessions": [
            {
                "session_id": "session-1",
                "created_at": "2024-01-15T10:00:00Z",
                "last_activity": "2024-01-15T10:30:00Z",
                "status": "active"
            }
        ],
        "total_count": 1
    }
}
```

### POST /sessions/create
Tworzy nową sesję.

**Request Body:**
```json
{
    "session_name": "My Session",
    "headless": false
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "session_id": "new-session-id",
        "session_name": "My Session",
        "created_at": "2024-01-15T10:30:00Z"
    }
}
```

### DELETE /sessions/{session_id}
Usuwa sesję.

**Response:**
```json
{
    "success": true,
    "message": "Session deleted successfully"
}
```

## 📝 Data Models

### LaunchRequest
```python
class LaunchRequest(BaseModel):
    headless: bool = False
    session_id: Optional[str] = None
```

### QuestionRequest
```python
class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
```

### BotResponse
```python
class BotResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
```

### SessionInfo
```python
class SessionInfo(BaseModel):
    session_id: str
    created_at: datetime
    last_activity: datetime
    status: str
```

## ❌ Error Responses

### 400 Bad Request
```json
{
    "success": false,
    "error": "Invalid request data",
    "detail": "Missing required field: question"
}
```

### 404 Not Found
```json
{
    "success": false,
    "error": "Session not found",
    "detail": "Session with ID 'invalid-id' does not exist"
}
```

### 500 Internal Server Error
```json
{
    "success": false,
    "error": "Internal server error",
    "detail": "WebDriver initialization failed"
}
```

## 🔄 WebSocket Endpoints (Planowane)

### /ws/bot/{session_id}
Real-time komunikacja z botem.

**Messages:**
```json
// Outgoing
{
    "type": "question",
    "data": {
        "question": "Hello ChatGPT"
    }
}

// Incoming
{
    "type": "response",
    "data": {
        "answer": "Hello! How can I help you?",
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

## 📚 SDK Examples

### Python Client
```python
import requests

class ChatGPTAPIClient:
    def __init__(self, base_url="http://localhost:8008"):
        self.base_url = base_url
        self.session_id = None
    
    def launch_browser(self, headless=False):
        response = requests.post(
            f"{self.base_url}/bot/launch",
            json={"headless": headless}
        )
        data = response.json()
        if data["success"]:
            self.session_id = data["data"]["session_id"]
        return data
    
    def ask_question(self, question):
        return requests.post(
            f"{self.base_url}/bot/ask",
            json={
                "question": question,
                "session_id": self.session_id
            }
        ).json()
```

### JavaScript Client
```javascript
class ChatGPTAPIClient {
    constructor(baseUrl = 'http://localhost:8008') {
        this.baseUrl = baseUrl;
        this.sessionId = null;
    }
    
    async launchBrowser(headless = false) {
        const response = await fetch(`${this.baseUrl}/bot/launch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ headless })
        });
        const data = await response.json();
        if (data.success) {
            this.sessionId = data.data.session_id;
        }
        return data;
    }
    
    async askQuestion(question) {
        return fetch(`${this.baseUrl}/bot/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question,
                session_id: this.sessionId
            })
        }).then(r => r.json());
    }
}
```

## 🧪 Testing API

### Using curl
```bash
# Launch browser
curl -X POST http://localhost:8008/bot/launch \
  -H "Content-Type: application/json" \
  -d '{"headless": false}'

# Ask question
curl -X POST http://localhost:8008/bot/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello", "session_id": "your-session-id"}'

# Check status
curl http://localhost:8008/bot/status?session_id=your-session-id
```

### Using Python requests
```python
import requests

# Launch browser
response = requests.post('http://localhost:8008/bot/launch', 
                        json={'headless': False})
session_id = response.json()['data']['session_id']

# Ask question
response = requests.post('http://localhost:8008/bot/ask', 
                        json={
                            'question': 'What is Python?',
                            'session_id': session_id
                        })
print(response.json())
```

## 📊 Rate Limiting (Planowane)

```json
{
    "rate_limit": {
        "requests_per_minute": 60,
        "requests_per_hour": 1000,
        "concurrent_sessions": 10
    }
}
```

## 🔧 Configuration

### Environment Variables
```bash
API_HOST=localhost
API_PORT=8008
DEBUG=false
MAX_SESSIONS=10
SESSION_TIMEOUT=3600
```

### API Documentation
Dostępna pod adresem: `http://localhost:8008/docs` (Swagger UI)
Alternatywnie: `http://localhost:8008/redoc` (ReDoc)
