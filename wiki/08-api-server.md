# 🌐 API Server

## 🎯 Przegląd

API Server to serce systemu ChatGPT Bot w trybie API, zbudowany na FastAPI. Zapewnia RESTful endpoints do zarządzania instancjami botów i komunikacji z ChatGPT.

## 🚀 Uruchomienie

### Metoda 1: Python Script
```bash
python chatgpt_api_server.py
```

### Metoda 2: Uvicorn
```bash
uvicorn chatgpt_api_server:app --host 0.0.0.0 --port 8000 --reload
```

### Metoda 3: Makefile
```bash
make server
```

### Metoda 4: Docker
```bash
docker run -p 8000:8000 chatgpt-bot-api
```

## 🏗️ Architektura

### FastAPI Application
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="ChatGPT Bot API",
    description="REST API for ChatGPT automation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Session Management
```python
from typing import Dict
from datetime import datetime
import uuid

# Global session storage
bot_instances: Dict[str, ChatGPTBot] = {}
session_metadata: Dict[str, dict] = {}

def create_session_id() -> str:
    """Generuje unikalny ID sesji"""
    return str(uuid.uuid4())

def get_or_create_bot(session_id: str) -> ChatGPTBot:
    """Pobiera lub tworzy instancję bota"""
    if session_id not in bot_instances:
        bot_instances[session_id] = ChatGPTBot()
        session_metadata[session_id] = {
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "status": "created"
        }
    return bot_instances[session_id]
```

## 📊 Data Models

### Request Models
```python
from pydantic import BaseModel
from typing import Optional

class LaunchRequest(BaseModel):
    headless: bool = False
    session_id: Optional[str] = None

class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class StateRequest(BaseModel):
    session_id: str

class SessionCreateRequest(BaseModel):
    session_name: Optional[str] = None
    headless: bool = False
```

### Response Models
```python
class BotResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class SessionInfo(BaseModel):
    session_id: str
    session_name: Optional[str]
    created_at: datetime
    last_activity: datetime
    status: str

class QuestionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    timestamp: Optional[datetime] = None
```

## 🛣️ API Endpoints

### Bot Management

#### POST /bot/launch
```python
@app.post("/bot/launch", response_model=BotResponse)
async def launch_browser(request: LaunchRequest):
    """Uruchamia przeglądarkę"""
    try:
        session_id = request.session_id or create_session_id()
        bot = get_or_create_bot(session_id)
        
        success = bot.launch_browser(headless=request.headless)
        
        if success:
            session_metadata[session_id]["status"] = "running"
            session_metadata[session_id]["last_activity"] = datetime.now()
            
            return BotResponse(
                success=True,
                message="Browser launched successfully",
                data={
                    "session_id": session_id,
                    "browser_status": "running"
                }
            )
        else:
            raise HTTPException(status_code=500, 
                              detail="Failed to launch browser")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### POST /bot/ask
```python
@app.post("/bot/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Wysyła pytanie do ChatGPT"""
    try:
        session_id = request.session_id
        if not session_id or session_id not in bot_instances:
            raise HTTPException(status_code=404, 
                              detail="Session not found")
        
        bot = bot_instances[session_id]
        
        # Check if browser is running
        if not bot.driver:
            raise HTTPException(status_code=400, 
                              detail="Browser not launched")
        
        # Ask question
        answer = bot.ask_question_and_get_response(request.question)
        
        # Update session metadata
        session_metadata[session_id]["last_activity"] = datetime.now()
        
        return QuestionResponse(
            success=True,
            message="Question processed successfully",
            data={
                "question": request.question,
                "answer": answer,
                "timestamp": datetime.now(),
                "session_id": session_id
            },
            question=request.question,
            answer=answer,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### GET /bot/status
```python
@app.get("/bot/status", response_model=BotResponse)
async def get_bot_status(session_id: Optional[str] = None):
    """Sprawdza status bota"""
    try:
        if session_id:
            if session_id not in bot_instances:
                raise HTTPException(status_code=404, 
                                  detail="Session not found")
            
            bot = bot_instances[session_id]
            metadata = session_metadata[session_id]
            
            return BotResponse(
                success=True,
                message="Status retrieved successfully",
                data={
                    "session_id": session_id,
                    "browser_running": bot.driver is not None,
                    "last_activity": metadata["last_activity"],
                    "status": metadata["status"],
                    "created_at": metadata["created_at"]
                }
            )
        else:
            # Return all sessions status
            all_sessions = []
            for sid, metadata in session_metadata.items():
                bot = bot_instances.get(sid)
                all_sessions.append({
                    "session_id": sid,
                    "browser_running": bot.driver is not None if bot else False,
                    "last_activity": metadata["last_activity"],
                    "status": metadata["status"],
                    "created_at": metadata["created_at"]
                })
            
            return BotResponse(
                success=True,
                message="All sessions status retrieved",
                data={"sessions": all_sessions}
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Session Management

#### GET /sessions
```python
@app.get("/sessions", response_model=BotResponse)
async def list_sessions():
    """Lista wszystkich sesji"""
    try:
        sessions = []
        for session_id, metadata in session_metadata.items():
            sessions.append({
                "session_id": session_id,
                "created_at": metadata["created_at"],
                "last_activity": metadata["last_activity"],
                "status": metadata["status"]
            })
        
        return BotResponse(
            success=True,
            message="Sessions retrieved successfully",
            data={
                "sessions": sessions,
                "total_count": len(sessions)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### POST /sessions/create
```python
@app.post("/sessions/create", response_model=BotResponse)
async def create_session(request: SessionCreateRequest):
    """Tworzy nową sesję"""
    try:
        session_id = create_session_id()
        
        # Create bot instance
        bot = ChatGPTBot()
        bot_instances[session_id] = bot
        
        # Create metadata
        session_metadata[session_id] = {
            "session_name": request.session_name or f"Session {session_id[:8]}",
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "status": "created",
            "headless": request.headless
        }
        
        return BotResponse(
            success=True,
            message="Session created successfully",
            data={
                "session_id": session_id,
                "session_name": session_metadata[session_id]["session_name"],
                "created_at": session_metadata[session_id]["created_at"]
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### DELETE /sessions/{session_id}
```python
@app.delete("/sessions/{session_id}", response_model=BotResponse)
async def delete_session(session_id: str):
    """Usuwa sesję"""
    try:
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, 
                              detail="Session not found")
        
        # Close browser if running
        bot = bot_instances[session_id]
        if bot.driver:
            bot.close_browser()
        
        # Remove from storage
        del bot_instances[session_id]
        del session_metadata[session_id]
        
        return BotResponse(
            success=True,
            message="Session deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 🛡️ Error Handling

### Global Exception Handler
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Globalny handler błędów"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc),
            "path": str(request.url)
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler dla HTTPException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )
```

### Validation Error Handler
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler dla błędów walidacji"""
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation error",
            "detail": exc.errors()
        }
    )
```

## 🔧 Middleware

### Logging Middleware
```python
import time
import logging

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware do logowania requestów"""
    start_time = time.time()
    
    # Log request
    logging.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logging.info(f"Response: {response.status_code} in {process_time:.4f}s")
    
    return response
```

### Session Cleanup Middleware
```python
@app.middleware("http")
async def cleanup_inactive_sessions(request: Request, call_next):
    """Czyści nieaktywne sesje"""
    # Clean up sessions older than 1 hour
    cutoff_time = datetime.now() - timedelta(hours=1)
    
    sessions_to_remove = []
    for session_id, metadata in session_metadata.items():
        if metadata["last_activity"] < cutoff_time:
            sessions_to_remove.append(session_id)
    
    for session_id in sessions_to_remove:
        try:
            bot = bot_instances.get(session_id)
            if bot and bot.driver:
                bot.close_browser()
            del bot_instances[session_id]
            del session_metadata[session_id]
            logging.info(f"Cleaned up inactive session: {session_id}")
        except Exception as e:
            logging.error(f"Error cleaning up session {session_id}: {e}")
    
    response = await call_next(request)
    return response
```

## 📊 Health Checks

### Health Endpoint
```python
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "active_sessions": len(bot_instances),
        "version": "1.0.0"
    }

@app.get("/metrics")
async def get_metrics():
    """Metryki systemu"""
    active_browsers = sum(1 for bot in bot_instances.values() 
                         if bot.driver is not None)
    
    return {
        "total_sessions": len(bot_instances),
        "active_browsers": active_browsers,
        "memory_usage": "N/A",  # Można dodać psutil
        "uptime": "N/A"
    }
```

## 🔧 Configuration

### Environment Configuration
```python
import os
from typing import Optional

class Settings:
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    MAX_SESSIONS: int = int(os.getenv("MAX_SESSIONS", 10))
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", 3600))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")

settings = Settings()
```

### Server Startup
```python
if __name__ == "__main__":
    uvicorn.run(
        "chatgpt_api_server:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )
```

## 🧪 Testing

### Test Client
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_launch_browser():
    response = client.post("/bot/launch", 
                          json={"headless": True})
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_ask_question():
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

## 📈 Performance Optimization

### Async Operations
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@app.post("/bot/ask-async")
async def ask_question_async(request: QuestionRequest):
    """Asynchroniczne wysyłanie pytania"""
    loop = asyncio.get_event_loop()
    
    def ask_sync():
        bot = bot_instances[request.session_id]
        return bot.ask_question_and_get_response(request.question)
    
    answer = await loop.run_in_executor(executor, ask_sync)
    
    return QuestionResponse(
        success=True,
        answer=answer,
        question=request.question
    )
```

### Caching
```python
from functools import lru_cache
import redis

# Redis cache (optional)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=100)
def get_cached_response(question: str) -> str:
    """Cache dla często zadawanych pytań"""
    # Implementation here
    pass
```