from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import time
import uuid
from datetime import datetime
import json
from openai import OpenAI
from dotenv import load_dotenv
import aiofiles
import asyncio
# from agents import MultiAgentOrchestrator, AgentRole  # Temporarily disabled for testing

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Silas Chat API",
    description="Backend API for Silas Avatar Chat System",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class ChatMessage(BaseModel):
    content: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    use_multi_agent: Optional[bool] = True

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    response_time_ms: int
    avatar_video_url: Optional[str] = None
    audio_url: Optional[str] = None
    model_used: Optional[str] = None
    workflow_type: Optional[str] = None
    agents_used: Optional[List[str]] = None
    workflow_id: Optional[str] = None

class SessionInfo(BaseModel):
    session_id: str
    created_at: str
    message_count: int
    last_activity: str

# OpenRouter client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Free models available on OpenRouter
FREE_MODELS = [
    "microsoft/wizardlm-2-8x22b",
    "google/gemma-7b-it:free",
    "mistralai/mistral-7b-instruct:free",
    "huggingfaceh4/zephyr-7b-beta:free",
    "openchat/openchat-7b:free"
]

# Initialize multi-agent orchestrator (temporarily disabled)
# orchestrator = MultiAgentOrchestrator(client, FREE_MODELS)

# In-memory storage (replace with database in production)
chat_sessions = {}
message_history = {}

# Avatar and voice configuration
AVATAR_CONFIG = {
    "sadtalker_enabled": True,
    "voice_enabled": True,
    "default_voice": "en-US-AriaNeural",  # Free Azure voice
    "avatar_image": "/static/silas_avatar.jpg"
}

@app.get("/")
async def root():
    return {
        "message": "Silas Chat API is running! 🤖",
        "version": "1.0.0",
        "endpoints": ["/message", "/session", "/health"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(chat_sessions)
    }

@app.post("/message", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    start_time = time.time()
    
    # Generate session ID if not provided
    session_id = message.session_id or str(uuid.uuid4())
    
    # Initialize session if new
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            "created_at": datetime.now().isoformat(),
            "message_count": 0,
            "last_activity": datetime.now().isoformat()
        }
        message_history[session_id] = []
    
    # Store user message
    user_message = {
        "type": "user",
        "content": message.content,
        "timestamp": datetime.now().isoformat()
    }
    message_history[session_id].append(user_message)
    
    # Generate bot response using multi-agent system or single LLM
    if message.use_multi_agent:
        response_data = await orchestrator.process_query(message.content, session_id)
        bot_response_text = response_data["response"]
        workflow_type = response_data.get("workflow_type", "single_agent")
        agents_used = response_data.get("agents_used", [])
        workflow_id = response_data.get("workflow_id")
        model_used = response_data.get("metadata", {}).get("model", "multi-agent")
    else:
        # Fallback to single agent
        single_response = await generate_bot_response(message.content, session_id)
        bot_response_text = single_response["text"]
        workflow_type = "single_agent"
        agents_used = ["single"]
        workflow_id = None
        model_used = single_response.get("model_used", "fallback")
    
    # Generate avatar video and voice (async)
    avatar_task = generate_avatar_video(bot_response_text, session_id)
    voice_task = generate_voice_audio(bot_response_text, session_id)
    
    # Wait for avatar and voice generation
    avatar_url, audio_url = await asyncio.gather(avatar_task, voice_task)
    
    # Store bot response
    bot_message = {
        "type": "bot",
        "content": bot_response_text,
        "timestamp": datetime.now().isoformat(),
        "model_used": response_data.get("model_used"),
        "avatar_url": avatar_url,
        "audio_url": audio_url
    }
    message_history[session_id].append(bot_message)
    
    # Update session info
    chat_sessions[session_id]["message_count"] += 2
    chat_sessions[session_id]["last_activity"] = datetime.now().isoformat()
    
    response_time = int((time.time() - start_time) * 1000)
    
    return ChatResponse(
        response=bot_response_text,
        session_id=session_id,
        timestamp=datetime.now().isoformat(),
        response_time_ms=response_time,
        avatar_video_url=avatar_url,
        audio_url=audio_url,
        model_used=model_used,
        workflow_type=workflow_type,
        agents_used=agents_used,
        workflow_id=workflow_id
    )

@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = chat_sessions[session_id]
    messages = message_history.get(session_id, [])
    
    return {
        "session_info": SessionInfo(
            session_id=session_id,
            created_at=session_data["created_at"],
            message_count=session_data["message_count"],
            last_activity=session_data["last_activity"]
        ),
        "messages": messages
    }

@app.get("/sessions")
async def list_sessions():
    return {
        "total_sessions": len(chat_sessions),
        "sessions": [
            {
                "session_id": sid,
                "created_at": data["created_at"],
                "message_count": data["message_count"],
                "last_activity": data["last_activity"]
            }
            for sid, data in chat_sessions.items()
        ]
    }

@app.get("/models")
async def list_available_models():
    """List available free models"""
    return {
        "free_models": FREE_MODELS,
        "avatar_config": AVATAR_CONFIG,
        "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY"))
    }

@app.post("/avatar/generate")
async def generate_avatar_endpoint(request: dict):
    """Generate avatar video from text"""
    text = request.get("text", "")
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    video_url = await generate_avatar_video(text, session_id)
    audio_url = await generate_voice_audio(text, session_id)
    
    return {
        "video_url": video_url,
        "audio_url": audio_url,
        "text": text,
        "session_id": session_id
    }

@app.get("/config")
async def get_config():
    """Get system configuration"""
    return {
        "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
        "available_models": FREE_MODELS,
        "avatar_enabled": AVATAR_CONFIG["sadtalker_enabled"],
        "voice_enabled": AVATAR_CONFIG["voice_enabled"],
        "features": {
            "real_time_chat": True,
            "avatar_generation": True,
            "voice_synthesis": True,
            "free_llm": True,
            "multi_agent_workflow": True
        },
        "available_agents": [role.value for role in AgentRole]
    }

@app.get("/agents")
async def list_agents():
    """List available AI agents and their roles"""
    return {
        "agents": [
            {
                "role": role.value,
                "description": orchestrator.agents[role].system_prompt.split('\n')[0],
                "model": orchestrator.agents[role].model
            }
            for role in AgentRole
        ]
    }

@app.get("/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get the status of a specific multi-agent workflow"""
    workflow = orchestrator.get_workflow_status(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {
        "workflow_id": workflow.task_id,
        "status": workflow.status,
        "user_query": workflow.user_query,
        "required_agents": [role.value for role in workflow.required_agents],
        "current_step": workflow.current_step,
        "results": workflow.results
    }

@app.get("/workflows")
async def list_active_workflows():
    """List all active multi-agent workflows"""
    workflows = orchestrator.list_active_workflows()
    return {
        "active_workflows": len(workflows),
        "workflows": [
            {
                "workflow_id": w.task_id,
                "status": w.status,
                "user_query": w.user_query[:100] + "..." if len(w.user_query) > 100 else w.user_query,
                "agents_count": len(w.required_agents)
            }
            for w in workflows
        ]
    }

async def generate_bot_response(user_message: str, session_id: str) -> dict:
    """
    Generate bot response using OpenRouter free LLM
    """
    try:
        # Get conversation history for context
        history = message_history.get(session_id, [])
        
        # Build conversation context
        messages = [
            {
                "role": "system", 
                "content": "You are Silas, a friendly and helpful AI assistant. Keep responses conversational, engaging, and under 150 words. Be personable and show genuine interest in helping the user."
            }
        ]
        
        # Add recent conversation history (last 6 messages for context)
        recent_history = history[-6:] if len(history) > 6 else history
        for msg in recent_history:
            role = "user" if msg["type"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Try free models in order of preference
        for model in FREE_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=150,
                    temperature=0.7,
                    timeout=10
                )
                
                bot_response = response.choices[0].message.content.strip()
                
                return {
                    "text": bot_response,
                    "model_used": model,
                    "success": True
                }
                
            except Exception as model_error:
                print(f"Model {model} failed: {model_error}")
                continue
        
        # Fallback to simple responses if all models fail
        return {
            "text": get_fallback_response(user_message, session_id),
            "model_used": "fallback",
            "success": False
        }
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return {
            "text": "I'm having some technical difficulties right now. Could you please try again?",
            "model_used": "error",
            "success": False
        }

def get_fallback_response(user_message: str, session_id: str) -> str:
    """Fallback responses when LLM is unavailable"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm Silas, your AI assistant. How can I help you today?"
    
    if 'help' in message_lower:
        return "I'm here to help! What would you like to know or discuss?"
    
    if any(word in message_lower for word in ['what', 'how', 'why', '?']):
        return "That's an interesting question! I'd be happy to help you explore that topic."
    
    return "Thanks for sharing that with me. What else would you like to talk about?"

async def generate_avatar_video(text: str, session_id: str) -> Optional[str]:
    """
    Generate avatar video using SadTalker or similar free service
    This is a placeholder - integrate with actual SadTalker API
    """
    try:
        # Placeholder for SadTalker integration
        # In production, this would call SadTalker API with:
        # - Source image (Silas avatar)
        # - Audio file (generated from text)
        # - Return video URL
        
        # For now, return a placeholder
        return f"/api/avatar/video/{session_id}_{int(time.time())}.mp4"
        
    except Exception as e:
        print(f"Avatar generation error: {e}")
        return None

async def generate_voice_audio(text: str, session_id: str) -> Optional[str]:
    """
    Generate voice audio using free TTS service
    """
    try:
        # Placeholder for free TTS integration
        # Options: 
        # - Azure Cognitive Services (free tier)
        # - Google Cloud TTS (free tier)
        # - Edge TTS (completely free)
        # - Festival TTS (open source)
        
        # For now, return a placeholder
        return f"/api/voice/audio/{session_id}_{int(time.time())}.mp3"
        
    except Exception as e:
        print(f"Voice generation error: {e}")
        return None

# Optional: WebSocket endpoint for real-time chat
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message
            response = await generate_bot_response(message_data["content"], session_id)
            
            # Send response back
            await manager.send_personal_message(
                json.dumps({
                    "type": "bot_response",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                }),
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)