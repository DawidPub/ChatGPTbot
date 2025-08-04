from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict
import time
import uvicorn
from chatgpt_bot_core import ChatGPTBot
import uuid

app = FastAPI(title="ChatGPT Bot API", version="1.0.0")

# Global bot instance and storage
bot_instances: Dict[str, ChatGPTBot] = {}
bot_responses: Dict[str, str] = {}
bot_logs: Dict[str, list] = {}

# Pydantic models for API requests/responses
class BotCreateRequest(BaseModel):
    session_id: Optional[str] = None

class BotCreateResponse(BaseModel):
    session_id: str
    status: str
    message: str

class QuestionRequest(BaseModel):
    question: str
    session_id: str

class QuestionResponse(BaseModel):
    session_id: str
    response: Optional[str]
    status: str
    message: str

class StatusResponse(BaseModel):
    session_id: str
    status: str
    logs: list
    current_response: Optional[str]

class BrowserActionRequest(BaseModel):
    session_id: str

class BrowserActionResponse(BaseModel):
    session_id: str
    success: bool
    message: str

class QuestionWithAnswerRequest(BaseModel):
    question: str
    session_id: str

class QuestionWithAnswerResponse(BaseModel):
    session_id: str
    question: str
    answer: str
    status: str
    message: str

def create_status_callback(session_id: str):
    """Create a status callback function for a specific session"""
    def callback(message: str):
        if session_id not in bot_logs:
            bot_logs[session_id] = []
        bot_logs[session_id].append({
            "timestamp": time.strftime('%H:%M:%S'),
            "message": message
        })
        # Keep only last 100 log entries
        if len(bot_logs[session_id]) > 100:
            bot_logs[session_id] = bot_logs[session_id][-100:]
    return callback

def create_response_callback(session_id: str):
    """Create a response callback function for a specific session"""
    def callback(text: str):
        bot_responses[session_id] = text
    return callback

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "ChatGPT Bot API", 
        "version": "1.0.0",
        "endpoints": {
            "POST /bot/create": "Create a new bot session",
            "POST /bot/launch": "Launch browser for a session",
            "POST /bot/load_state": "Load browser state for a session",
            "POST /bot/save_state": "Save browser state for a session",
            "POST /bot/ask": "Ask a question to ChatGPT",
            "POST /bot/ask_with_answer": "Ask a question and get complete answer immediately",
            "GET /bot/status/{session_id}": "Get session status and logs",
            "POST /bot/close": "Close browser for a session",
            "DELETE /bot/{session_id}": "Delete a bot session"
        }
    }

@app.post("/bot/create", response_model=BotCreateResponse)
async def create_bot(request: BotCreateRequest = None):
    """Create a new ChatGPT bot session"""
    try:
        # Generate session ID if not provided
        session_id = request.session_id if request and request.session_id else str(uuid.uuid4())
        
        if session_id in bot_instances:
            raise HTTPException(status_code=409, detail=f"Session {session_id} already exists")
        
        # Create bot instance with callbacks
        status_callback = create_status_callback(session_id)
        response_callback = create_response_callback(session_id)
        
        bot = ChatGPTBot(
            status_callback=status_callback,
            response_callback=response_callback
        )
        
        bot_instances[session_id] = bot
        bot_responses[session_id] = ""
        bot_logs[session_id] = []
        
        status_callback(f"Bot session {session_id} created successfully")
        
        return BotCreateResponse(
            session_id=session_id,
            status="created",
            message=f"Bot session {session_id} created successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating bot: {str(e)}")

@app.post("/bot/launch", response_model=BrowserActionResponse)
async def launch_browser(request: BrowserActionRequest, background_tasks: BackgroundTasks):
    """Launch browser for a bot session"""
    try:
        session_id = request.session_id
        
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        bot = bot_instances[session_id]
        
        def launch_task():
            success = bot.launch_browser()
            if success:
                # Auto-load browser state after launch
                bot.load_browser_state()
        
        # Launch in background
        background_tasks.add_task(launch_task)
        
        return BrowserActionResponse(
            session_id=session_id,
            success=True,
            message="Browser launch initiated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error launching browser: {str(e)}")

@app.post("/bot/load_state", response_model=BrowserActionResponse)
async def load_browser_state(request: BrowserActionRequest, background_tasks: BackgroundTasks):
    """Load browser state for a bot session"""
    try:
        session_id = request.session_id
        
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        bot = bot_instances[session_id]
        
        def load_task():
            bot.load_browser_state()
        
        background_tasks.add_task(load_task)
        
        return BrowserActionResponse(
            session_id=session_id,
            success=True,
            message="Browser state loading initiated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading browser state: {str(e)}")

@app.post("/bot/save_state", response_model=BrowserActionResponse)
async def save_browser_state(request: BrowserActionRequest, background_tasks: BackgroundTasks):
    """Save browser state for a bot session"""
    try:
        session_id = request.session_id
        
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        bot = bot_instances[session_id]
        
        def save_task():
            bot.save_browser_state()
        
        background_tasks.add_task(save_task)
        
        return BrowserActionResponse(
            session_id=session_id,
            success=True,
            message="Browser state saving initiated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving browser state: {str(e)}")

@app.post("/bot/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest, background_tasks: BackgroundTasks):
    """Ask a question to ChatGPT"""
    try:
        session_id = request.session_id
        question = request.question.strip()
        
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        bot = bot_instances[session_id]
        
        def ask_task():
            response = bot.ask_question_and_get_response(question)
            bot_responses[session_id] = response or "No response received"
            # Auto-save state after successful interaction
            if response:
                bot.save_browser_state()
        
        # Clear previous response
        bot_responses[session_id] = ""
        
        # Ask question in background
        background_tasks.add_task(ask_task)
        
        return QuestionResponse(
            session_id=session_id,
            response=None,  # Response will be available via status endpoint
            status="processing",
            message="Question submitted, check status endpoint for response"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error asking question: {str(e)}")

@app.post("/bot/ask_with_answer", response_model=QuestionWithAnswerResponse)
async def ask_question_with_answer(request: QuestionWithAnswerRequest):
    """Ask a question to ChatGPT and return the complete answer immediately"""
    try:
        session_id = request.session_id
        question = request.question.strip()
        
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        bot = bot_instances[session_id]
        
        # Ask question synchronously and get complete response
        response = bot.ask_question_and_get_response(question)
        
        if response:
            # Auto-save state after successful interaction
            bot.save_browser_state()
            
            return QuestionWithAnswerResponse(
                session_id=session_id,
                question=question,
                answer=response,
                status="completed",
                message="Question answered successfully"
            )
        else:
            return QuestionWithAnswerResponse(
                session_id=session_id,
                question=question,
                answer="No response received",
                status="failed",
                message="Failed to get response from ChatGPT"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error asking question: {str(e)}")

@app.get("/bot/status/{session_id}", response_model=StatusResponse)
async def get_bot_status(session_id: str):
    """Get status and logs for a bot session"""
    try:
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        bot = bot_instances[session_id]
        logs = bot_logs.get(session_id, [])
        current_response = bot_responses.get(session_id, "")
        
        # Determine status based on bot state
        status = "idle"
        if bot.driver is None:
            status = "created"
        elif current_response and not current_response.startswith("[WARNING"):
            status = "completed"
        elif current_response:
            status = "processing"
        
        return StatusResponse(
            session_id=session_id,
            status=status,
            logs=logs,
            current_response=current_response if current_response else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

@app.post("/bot/close", response_model=BrowserActionResponse)
async def close_browser(request: BrowserActionRequest, background_tasks: BackgroundTasks):
    """Close browser for a bot session"""
    try:
        session_id = request.session_id
        
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        bot = bot_instances[session_id]
        
        def close_task():
            bot.close_browser()
        
        background_tasks.add_task(close_task)
        
        return BrowserActionResponse(
            session_id=session_id,
            success=True,
            message="Browser close initiated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error closing browser: {str(e)}")

@app.delete("/bot/{session_id}")
async def delete_bot_session(session_id: str):
    """Delete a bot session and cleanup resources"""
    try:
        if session_id not in bot_instances:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        bot = bot_instances[session_id]
        
        # Close browser if still open
        if bot.driver:
            bot.close_browser()
        
        # Clean up session data
        del bot_instances[session_id]
        if session_id in bot_responses:
            del bot_responses[session_id]
        if session_id in bot_logs:
            del bot_logs[session_id]
        
        return {"message": f"Session {session_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")

@app.get("/bot/sessions")
async def list_sessions():
    """List all active bot sessions"""
    sessions = []
    for session_id, bot in bot_instances.items():
        status = "idle"
        if bot.driver is None:
            status = "created"
        elif bot_responses.get(session_id):
            status = "completed"
        
        sessions.append({
            "session_id": session_id,
            "status": status,
            "browser_active": bot.driver is not None,
            "logs_count": len(bot_logs.get(session_id, []))
        })
    
    return {"sessions": sessions, "total": len(sessions)}

if __name__ == "__main__":
    print("🚀 Starting ChatGPT Bot API Server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔗 API Root: http://localhost:8000/")
    uvicorn.run(app, host="0.0.0.0", port=8000)
