#!/usr/bin/env python3
"""
Simple Backend for Talking Avatar
Integrates OpenRouter free LLMs with voice capabilities
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import json
from typing import Optional

app = FastAPI(title="Silas Talking Avatar Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    use_voice: bool = True

class ChatResponse(BaseModel):
    response: str
    voice_enabled: bool = True

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Free models available on OpenRouter
FREE_MODELS = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "meta-llama/llama-3.2-1b-instruct:free", 
    "microsoft/phi-3-mini-128k-instruct:free",
    "google/gemma-2-9b-it:free",
    "qwen/qwen-2-7b-instruct:free"
]

async def call_openrouter(message: str, model: str = None) -> str:
    """Call OpenRouter API with free models"""
    
    if not model:
        model = FREE_MODELS[0]  # Default to Llama 3.2 3B
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8001",
        "X-Title": "Silas Talking Avatar"
    }
    
    # System prompt for avatar personality
    system_prompt = """You are Silas, a friendly AI talking avatar. You are:
- Conversational and engaging
- Helpful and knowledgeable  
- Concise but informative (keep responses under 100 words for voice)
- Expressive and personable
- Always ready to chat about any topic

Respond naturally as if you're having a face-to-face conversation."""

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                print(f"OpenRouter API error: {response.status_code} - {response.text}")
                return get_fallback_response(message)
                
    except Exception as e:
        print(f"Error calling OpenRouter: {e}")
        return get_fallback_response(message)

def get_fallback_response(message: str) -> str:
    """Fallback responses when API is unavailable"""
    
    fallbacks = {
        "hello": "Hello! I'm Silas, your AI talking avatar. Great to meet you!",
        "how are you": "I'm doing wonderful! Thanks for asking. How are you doing today?",
        "what can you do": "I can chat with you using both text and voice! I can discuss any topic, answer questions, or just have a friendly conversation.",
        "tell me a joke": "Why don't scientists trust atoms? Because they make up everything! 😄",
        "goodbye": "Goodbye! It was great chatting with you. Come back anytime!",
        "test": "I'm working perfectly! Voice and text are both ready to go.",
        "default": "I'm having trouble connecting to my brain right now, but I'm still here to chat! Try asking me something else."
    }
    
    message_lower = message.lower()
    
    for key, response in fallbacks.items():
        if key in message_lower:
            return response
    
    return fallbacks["default"]

@app.get("/")
async def root():
    return {"message": "Silas Talking Avatar Backend", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "voice_enabled": True}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with OpenRouter integration"""
    
    try:
        # Get response from OpenRouter
        if OPENROUTER_API_KEY:
            response_text = await call_openrouter(request.message)
        else:
            print("No OpenRouter API key found, using fallback responses")
            response_text = get_fallback_response(request.message)
        
        return ChatResponse(
            response=response_text,
            voice_enabled=request.use_voice
        )
        
    except Exception as e:
        print(f"Chat error: {e}")
        return ChatResponse(
            response="I'm having a small technical issue, but I'm still here to help!",
            voice_enabled=request.use_voice
        )

@app.get("/models")
async def get_models():
    """Get available free models"""
    return {"free_models": FREE_MODELS}

@app.post("/test-voice")
async def test_voice():
    """Test voice functionality"""
    return ChatResponse(
        response="This is a voice test. If you can hear this, the text-to-speech is working perfectly!",
        voice_enabled=True
    )

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Silas Talking Avatar Backend...")
    print("🤖 Free OpenRouter LLMs integrated")
    print("🎤 Voice features enabled")
    print("📡 Server starting on http://127.0.0.1:8001")
    
    if not OPENROUTER_API_KEY:
        print("⚠️  No OpenRouter API key found - using fallback responses")
        print("💡 Set OPENROUTER_API_KEY environment variable for full AI features")
    else:
        print("✅ OpenRouter API key configured")
    
    uvicorn.run(app, host="127.0.0.1", port=8001)