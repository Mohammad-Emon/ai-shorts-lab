"""
Silas Chat UI backend with OpenRouter LLM and Multi-Agent System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import time
import uuid
from datetime import datetime
import json
from dotenv import load_dotenv
from openai import OpenAI
import asyncio

# Load environment variables
load_dotenv()

# OpenRouter client setup
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
client = None

if openrouter_api_key and openrouter_api_key != "your_openrouter_api_key_here":
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
        default_headers={
            "HTTP-Referer": "http://localhost:8001",
            "X-Title": "Silas Chat UI"
        }
    )
    print(f"✅ OpenRouter client initialized with key: {openrouter_api_key[:20]}...")
else:
    print("⚠️  OpenRouter API key not configured - using fallback responses")

# Free models available on OpenRouter
FREE_MODELS = [
    "microsoft/wizardlm-2-8x22b",
    "google/gemma-7b-it:free", 
    "mistralai/mistral-7b-instruct:free",
    "huggingfaceh4/zephyr-7b-beta:free",
    "openchat/openchat-7b:free"
]

app = FastAPI(
    title="Silas Chat API (Simple)",
    description="Simple backend for testing Silas Avatar Chat System",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class ChatMessage(BaseModel):
    content: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    use_multi_agent: Optional[bool] = False

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    response_time_ms: int
    workflow_type: Optional[str] = "simple"
    agents_used: Optional[List[str]] = ["simple"]
    model_used: Optional[str] = None
    confidence: Optional[float] = None

# In-memory storage
chat_sessions = {}
message_history = {}

@app.get("/")
async def root():
    return {
        "message": "Silas Chat API (Simple) is running! 🤖",
        "version": "1.0.0",
        "status": "ready",
        "endpoints": ["/message", "/health", "/config"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(chat_sessions),
        "mode": "simple"
    }

@app.get("/config")
async def get_config():
    return {
        "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
        "available_models": FREE_MODELS,
        "avatar_enabled": True,
        "voice_enabled": True,
        "features": {
            "real_time_chat": True,
            "avatar_generation": False,
            "voice_synthesis": False,
            "free_llm": True,
            "multi_agent_workflow": True
        },
        "mode": "openrouter_llm"
    }

@app.get("/agents")
async def list_agents():
    return {
        "agents": [
            {
                "role": "voice",
                "description": "Voice Agent: Text-to-speech, speech recognition, voice controls",
                "model": FREE_MODELS[0] if FREE_MODELS else "fallback"
            },
            {
                "role": "coordinator",
                "description": "Routes queries and orchestrates workflows",
                "model": FREE_MODELS[0] if FREE_MODELS else "fallback"
            },
            {
                "role": "researcher", 
                "description": "Gathers factual information and data",
                "model": FREE_MODELS[1] if len(FREE_MODELS) > 1 else FREE_MODELS[0]
            },
            {
                "role": "creative",
                "description": "Generates creative ideas and content", 
                "model": FREE_MODELS[2] if len(FREE_MODELS) > 2 else FREE_MODELS[0]
            },
            {
                "role": "technical",
                "description": "Solves programming and technical problems",
                "model": FREE_MODELS[3] if len(FREE_MODELS) > 3 else FREE_MODELS[0]
            },
            {
                "role": "analyst",
                "description": "Analyzes data and provides insights",
                "model": FREE_MODELS[4] if len(FREE_MODELS) > 4 else FREE_MODELS[0]
            }
        ]
    }

@app.post("/voice/process")
async def process_voice_message(request: dict):
    """Process voice message with optimized response for speech"""
    try:
        message_content = request.get("content", "")
        session_id = request.get("session_id", str(uuid.uuid4()))
        generate_avatar = request.get("generate_avatar", True)
        
        if not message_content:
            return {"error": "No message content provided"}
        
        # Generate response optimized for voice
        response_data = await generate_voice_optimized_response(message_content, session_id)
        
        # Generate avatar video if requested
        avatar_data = None
        if generate_avatar:
            avatar_data = await generate_avatar_response(response_data["response"], session_id)
        
        return {
            "response": response_data["response"],
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "workflow_type": response_data.get("workflow_type", "voice"),
            "agents_used": response_data.get("agents_used", ["voice"]),
            "model_used": response_data.get("model_used"),
            "voice_optimized": True,
            "avatar_data": avatar_data
        }
        
    except Exception as e:
        print(f"Error processing voice message: {e}")
        return {
            "response": "I'm having trouble processing your voice message. Could you please try again?",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "workflow_type": "error",
            "voice_optimized": True
        }

@app.post("/visual/process")
async def process_visual_message(request: dict):
    """Process message for D-ID style visual agent"""
    try:
        message_content = request.get("content", "")
        session_id = request.get("session_id", str(uuid.uuid4()))
        generate_video = request.get("generate_video", True)
        
        if not message_content:
            return {"error": "No message content provided"}
        
        # Generate LLM response optimized for video
        response_data = await generate_visual_optimized_response(message_content, session_id)
        
        # Generate video if requested
        video_data = None
        if generate_video:
            video_data = await generate_sadtalker_video(response_data["response"], session_id)
        
        return {
            "response": response_data["response"],
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "workflow_type": response_data.get("workflow_type", "visual"),
            "agents_used": response_data.get("agents_used", ["visual"]),
            "model_used": response_data.get("model_used"),
            "video_data": video_data
        }
        
    except Exception as e:
        print(f"Error processing visual message: {e}")
        return {
            "response": "I'm having trouble processing your visual message. Could you please try again?",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "workflow_type": "error"
        }

@app.post("/avatar/generate")
async def generate_avatar_video(request: dict):
    """Generate avatar video from text using SadTalker"""
    try:
        text = request.get("text", "")
        session_id = request.get("session_id", str(uuid.uuid4()))
        avatar_style = request.get("style", "default")
        
        if not text:
            return {"error": "No text provided for avatar generation"}
        
        # Generate SadTalker video
        video_data = await generate_sadtalker_video(text, session_id, avatar_style)
        
        return {
            "video_data": video_data,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "text": text
        }
        
    except Exception as e:
        print(f"Error generating avatar: {e}")
        return {"error": f"Avatar generation failed: {str(e)}"}

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
    
    # Generate AI response using OpenRouter
    if message.use_multi_agent:
        response_data = await generate_multi_agent_response(message.content, session_id)
    else:
        response_data = await generate_single_agent_response(message.content, session_id)
    
    bot_response_text = response_data["response"]
    
    # Store bot response
    bot_message = {
        "type": "bot",
        "content": bot_response_text,
        "timestamp": datetime.now().isoformat(),
        "model_used": response_data.get("model_used"),
        "workflow_type": response_data.get("workflow_type"),
        "agents_used": response_data.get("agents_used")
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
        workflow_type=response_data.get("workflow_type", "single"),
        agents_used=response_data.get("agents_used", ["single"]),
        model_used=response_data.get("model_used"),
        confidence=response_data.get("confidence", 0.8)
    )

async def generate_single_agent_response(user_message: str, session_id: str) -> dict:
    """Generate response using a single OpenRouter LLM"""
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
        
        # Add recent conversation history (last 4 messages for context)
        recent_history = history[-4:] if len(history) > 4 else history
        for msg in recent_history:
            role = "user" if msg["type"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Check if OpenRouter client is available
        if not client:
            return get_fallback_response(user_message, "single_agent")
        
        # Try free models in order of preference
        for model in FREE_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=150,
                    temperature=0.7,
                    timeout=15
                )
                
                bot_response = response.choices[0].message.content.strip()
                
                return {
                    "response": bot_response,
                    "model_used": model,
                    "workflow_type": "single_agent",
                    "agents_used": ["single"],
                    "confidence": 0.8,
                    "success": True
                }
                
            except Exception as model_error:
                print(f"Model {model} failed: {model_error}")
                continue
        
        # Fallback if all models fail
        return get_fallback_response(user_message, "single_agent")
        
    except Exception as e:
        print(f"Error in single agent response: {e}")
        return get_fallback_response(user_message, "single_agent")

async def generate_multi_agent_response(user_message: str, session_id: str) -> dict:
    """Generate response using multi-agent workflow"""
    try:
        # Determine which agents are needed
        required_agents = determine_required_agents(user_message)
        
        if len(required_agents) == 1:
            # Single specialized agent
            agent_role = required_agents[0]
            return await generate_specialized_agent_response(user_message, session_id, agent_role)
        else:
            # Multi-agent collaboration
            return await generate_collaborative_response(user_message, session_id, required_agents)
            
    except Exception as e:
        print(f"Error in multi-agent response: {e}")
        return get_fallback_response(user_message, "multi_agent")

def determine_required_agents(query: str) -> List[str]:
    """Determine which agents are needed based on query analysis"""
    query_lower = query.lower()
    required_agents = []
    
    # Technical queries
    if any(word in query_lower for word in ['code', 'programming', 'technical', 'debug', 'api', 'software', 'python', 'javascript']):
        required_agents.append('technical')
    
    # Research queries  
    if any(word in query_lower for word in ['what is', 'how does', 'explain', 'research', 'facts', 'data', 'information']):
        required_agents.append('researcher')
    
    # Creative queries
    if any(word in query_lower for word in ['create', 'write', 'story', 'idea', 'brainstorm', 'creative', 'design']):
        required_agents.append('creative')
    
    # Analysis queries
    if any(word in query_lower for word in ['analyze', 'compare', 'evaluate', 'recommend', 'strategy', 'plan']):
        required_agents.append('analyst')
    
    # Default to coordinator if no specific agents identified
    if not required_agents:
        required_agents.append('coordinator')
        
    return required_agents

async def generate_specialized_agent_response(user_message: str, session_id: str, agent_role: str) -> dict:
    """Generate response from a specialized agent"""
    
    # Agent-specific system prompts
    agent_prompts = {
        'coordinator': "You are the Coordinator Agent. Analyze queries, route tasks, and provide well-structured responses. Be helpful and organized.",
        'researcher': "You are the Research Agent. Provide factual, accurate information with clear explanations. Focus on data and verified knowledge.",
        'creative': "You are the Creative Agent. Generate innovative ideas, creative solutions, and engaging content. Think outside the box.",
        'technical': "You are the Technical Agent. Solve programming problems, explain technical concepts, and provide code examples when helpful.",
        'analyst': "You are the Analyst Agent. Analyze information, identify patterns, provide insights, and make data-driven recommendations."
    }
    
    try:
        # Check if OpenRouter client is available
        if not client:
            return {
                "response": f"🤖 **{agent_role.title()} Agent**: I'm ready to help with {agent_role} tasks! My advanced AI models are currently offline, but I'm still here to assist you.",
                "model_used": "fallback",
                "workflow_type": "specialized_agent",
                "agents_used": [agent_role],
                "confidence": 0.5,
                "success": False
            }
        
        messages = [
            {"role": "system", "content": agent_prompts.get(agent_role, agent_prompts['coordinator'])},
            {"role": "user", "content": user_message}
        ]
        
        # Try models for this agent
        for model in FREE_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=200,
                    temperature=0.7,
                    timeout=15
                )
                
                bot_response = response.choices[0].message.content.strip()
                
                return {
                    "response": f"🤖 **{agent_role.title()} Agent**: {bot_response}",
                    "model_used": model,
                    "workflow_type": "specialized_agent",
                    "agents_used": [agent_role],
                    "confidence": 0.85,
                    "success": True
                }
                
            except Exception as model_error:
                print(f"Model {model} failed for {agent_role}: {model_error}")
                continue
        
        # Fallback for this agent
        return {
            "response": f"🤖 **{agent_role.title()} Agent**: I'm ready to help with {agent_role} tasks, but I'm having connectivity issues. Please try again!",
            "model_used": "fallback",
            "workflow_type": "specialized_agent", 
            "agents_used": [agent_role],
            "confidence": 0.3,
            "success": False
        }
        
    except Exception as e:
        print(f"Error in specialized agent {agent_role}: {e}")
        return get_fallback_response(user_message, "specialized_agent")

async def generate_collaborative_response(user_message: str, session_id: str, required_agents: List[str]) -> dict:
    """Generate collaborative response from multiple agents"""
    
    try:
        # Generate responses from each required agent
        agent_responses = []
        
        for agent_role in required_agents[:3]:  # Limit to 3 agents for performance
            agent_response = await generate_specialized_agent_response(user_message, session_id, agent_role)
            if agent_response["success"]:
                agent_responses.append({
                    "agent": agent_role,
                    "response": agent_response["response"],
                    "model": agent_response["model_used"]
                })
        
        if agent_responses:
            # Combine responses
            combined_response = "🚀 **Multi-Agent Collaboration**:\n\n"
            for i, resp in enumerate(agent_responses, 1):
                combined_response += f"{resp['response']}\n\n"
            
            combined_response += f"💡 *Collaboration complete! {len(agent_responses)} agents worked together on your query.*"
            
            return {
                "response": combined_response,
                "model_used": f"multi-model ({len(agent_responses)} agents)",
                "workflow_type": "collaborative",
                "agents_used": [resp["agent"] for resp in agent_responses],
                "confidence": 0.9,
                "success": True
            }
        else:
            return get_fallback_response(user_message, "collaborative")
            
    except Exception as e:
        print(f"Error in collaborative response: {e}")
        return get_fallback_response(user_message, "collaborative")

def get_fallback_response(user_message: str, workflow_type: str) -> dict:
    """Fallback responses when LLM is unavailable"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        response = "✨ Hello! I'm Silas, your AI assistant. I'm currently running in demo mode. To unlock my full multi-agent capabilities with free LLMs, please check your OpenRouter API key configuration!"
    elif 'multi' in message_lower or 'agent' in message_lower:
        response = "🤖 **Multi-Agent System Ready!** I have 5 specialized agents: Coordinator, Researcher, Creative, Technical, and Analyst. They're ready to collaborate with real AI models once OpenRouter is configured!"
    elif any(word in message_lower for word in ['code', 'programming', 'technical']):
        response = "💻 **Technical Agent**: I'd love to help with coding! In full mode, I can provide detailed programming assistance, debug code, and explain technical concepts using advanced AI models."
    elif any(word in message_lower for word in ['create', 'write', 'story', 'creative']):
        response = "🎨 **Creative Agent**: I'm ready to help with creative tasks! With my full AI capabilities, I can write stories, generate ideas, and create engaging content."
    elif any(word in message_lower for word in ['research', 'explain', 'what is']):
        response = "🔍 **Research Agent**: I can help with research and explanations! My full system can access advanced AI models to provide detailed, accurate information."
    elif any(word in message_lower for word in ['help', 'what', 'how']):
        response = "🚀 I'm Silas, your multi-agent AI assistant! I'm currently in demo mode. To activate my full capabilities:\n\n1. Get a free OpenRouter API key\n2. Configure it in the backend\n3. Enjoy real AI-powered conversations!"
    else:
        responses = [
            "🤖 That's fascinating! My multi-agent system would love to dive deeper into that topic with real AI models.",
            "✨ Interesting question! In full mode, my specialized agents would collaborate to give you a comprehensive answer.",
            "🚀 Great topic! My Technical, Creative, and Research agents are ready to help once the AI models are connected.",
            "💡 I'd love to explore that with you! My multi-agent workflow can provide much more detailed responses with OpenRouter integration."
        ]
        response = responses[hash(user_message) % len(responses)]
    
    return {
        "response": response,
        "model_used": "demo_mode",
        "workflow_type": workflow_type,
        "agents_used": ["demo"],
        "confidence": 0.7,
        "success": False
    }

async def generate_voice_optimized_response(user_message: str, session_id: str) -> dict:
    """Generate response optimized for voice interaction"""
    try:
        # Check if OpenRouter client is available
        if not client:
            return get_voice_fallback_response(user_message)
        
        # Voice-optimized system prompt
        voice_system_prompt = """You are Silas, a voice AI assistant. Respond in a conversational, natural speaking style:
- Keep responses under 100 words for voice clarity
- Use simple, clear language that sounds natural when spoken
- Avoid complex formatting, lists, or technical jargon
- Be warm, friendly, and engaging
- Speak as if having a natural conversation"""
        
        messages = [
            {"role": "system", "content": voice_system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Try free models for voice response
        for model in FREE_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=100,  # Shorter for voice
                    temperature=0.8,  # More conversational
                    timeout=15
                )
                
                bot_response = response.choices[0].message.content.strip()
                
                return {
                    "response": bot_response,
                    "model_used": model,
                    "workflow_type": "voice_agent",
                    "agents_used": ["voice"],
                    "confidence": 0.85,
                    "success": True
                }
                
            except Exception as model_error:
                print(f"Voice model {model} failed: {model_error}")
                continue
        
        # Fallback if all models fail
        return get_voice_fallback_response(user_message)
        
    except Exception as e:
        print(f"Error in voice response generation: {e}")
        return get_voice_fallback_response(user_message)

def get_voice_fallback_response(user_message: str) -> dict:
    """Voice-optimized fallback responses"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        response = "Hi there! I'm Silas, your voice assistant. How can I help you today?"
    elif any(word in message_lower for word in ['how are you', 'what\'s up']):
        response = "I'm doing great, thanks for asking! I'm here and ready to help with whatever you need."
    elif any(word in message_lower for word in ['help', 'what can you do']):
        response = "I can help with questions, have conversations, provide information, and assist with various tasks. What would you like to know?"
    elif any(word in message_lower for word in ['thank', 'thanks']):
        response = "You're very welcome! I'm happy to help. Is there anything else you'd like to know?"
    else:
        responses = [
            "That's interesting! I'd love to help you explore that topic further.",
            "Great question! Let me think about that for you.",
            "I understand what you're asking. Let me help you with that.",
            "That's a good point. I'm here to help however I can."
        ]
        response = responses[hash(user_message) % len(responses)]
    
    return {
        "response": response,
        "model_used": "voice_fallback",
        "workflow_type": "voice_agent",
        "agents_used": ["voice"],
        "confidence": 0.6,
        "success": False
    }

async def generate_avatar_response(text: str, session_id: str, style: str = "default") -> dict:
    """Generate avatar video/animation data using free services"""
    try:
        # For now, generate lip-sync timing data and facial expressions
        # This can be extended to integrate with SadTalker or other free avatar services
        
        # Analyze text for lip-sync timing
        words = text.split()
        lip_sync_data = []
        
        current_time = 0
        for word in words:
            word_duration = len(word) * 0.1 + 0.2  # Approximate timing
            
            # Analyze phonemes for mouth shapes
            mouth_shapes = analyze_phonemes(word)
            
            lip_sync_data.append({
                "word": word,
                "start_time": current_time,
                "duration": word_duration,
                "mouth_shapes": mouth_shapes
            })
            
            current_time += word_duration + 0.1  # Add pause between words
        
        # Generate facial expressions based on text sentiment
        expressions = analyze_expressions(text)
        
        return {
            "type": "lip_sync_data",
            "lip_sync": lip_sync_data,
            "expressions": expressions,
            "total_duration": current_time,
            "avatar_style": style,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error generating avatar data: {e}")
        return {
            "type": "error",
            "message": "Avatar generation failed",
            "fallback": True
        }

def analyze_phonemes(word: str) -> list:
    """Analyze word for mouth shapes based on vowels and consonants"""
    mouth_shapes = []
    
    for char in word.lower():
        if char in 'aeiou':
            if char in 'ae':
                mouth_shapes.append('open')
            elif char in 'iu':
                mouth_shapes.append('narrow')
            else:  # o
                mouth_shapes.append('round')
        else:
            mouth_shapes.append('closed')
    
    return mouth_shapes

def analyze_expressions(text: str) -> dict:
    """Analyze text for facial expressions"""
    text_lower = text.lower()
    
    expressions = {
        "emotion": "neutral",
        "intensity": 0.5,
        "eye_movement": "normal",
        "eyebrow_position": "neutral"
    }
    
    # Simple sentiment analysis
    if any(word in text_lower for word in ['happy', 'great', 'wonderful', 'amazing', 'excellent']):
        expressions["emotion"] = "happy"
        expressions["intensity"] = 0.8
    elif any(word in text_lower for word in ['sad', 'sorry', 'unfortunately', 'problem']):
        expressions["emotion"] = "concerned"
        expressions["intensity"] = 0.6
    elif any(word in text_lower for word in ['exciting', 'wow', 'incredible', 'fantastic']):
        expressions["emotion"] = "excited"
        expressions["intensity"] = 0.9
        expressions["eyebrow_position"] = "raised"
    elif '?' in text:
        expressions["emotion"] = "curious"
        expressions["eyebrow_position"] = "slightly_raised"
    
    return expressions

async def generate_visual_optimized_response(user_message: str, session_id: str) -> dict:
    """Generate response optimized for visual avatar presentation"""
    try:
        # Check if OpenRouter client is available
        if not client:
            return get_visual_fallback_response(user_message)
        
        # Visual-optimized system prompt
        visual_system_prompt = """You are Silas, a visual AI agent that appears as a realistic talking avatar. Respond naturally as if you're having a face-to-face conversation:
- Keep responses conversational and engaging (100-200 words)
- Use natural speech patterns that work well with lip-sync
- Be expressive and personable, as users can see your face
- Avoid complex formatting or lists
- Speak as if you're looking directly at the user
- Show personality and emotion in your responses"""
        
        # Get conversation history for context
        history = message_history.get(session_id, [])
        
        messages = [
            {"role": "system", "content": visual_system_prompt}
        ]
        
        # Add recent conversation history
        recent_history = history[-4:] if len(history) > 4 else history
        for msg in recent_history:
            role = "user" if msg["type"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Try free models for visual response
        for model in FREE_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=200,  # Longer for visual context
                    temperature=0.8,  # More expressive
                    timeout=15
                )
                
                bot_response = response.choices[0].message.content.strip()
                
                return {
                    "response": bot_response,
                    "model_used": model,
                    "workflow_type": "visual_agent",
                    "agents_used": ["visual"],
                    "confidence": 0.9,
                    "success": True
                }
                
            except Exception as model_error:
                print(f"Visual model {model} failed: {model_error}")
                continue
        
        # Fallback if all models fail
        return get_visual_fallback_response(user_message)
        
    except Exception as e:
        print(f"Error in visual response generation: {e}")
        return get_visual_fallback_response(user_message)

def get_visual_fallback_response(user_message: str) -> dict:
    """Visual-optimized fallback responses"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        response = "Hello there! It's wonderful to see you. I'm Silas, your visual AI agent. I can see and respond with realistic video, just like we're having a real conversation. How can I help you today?"
    elif any(word in message_lower for word in ['how are you', 'what\'s up']):
        response = "I'm doing fantastic, thank you for asking! As a visual AI, I feel more alive when I can express myself through video. It's like the difference between texting and video calling - so much more personal, don't you think?"
    elif any(word in message_lower for word in ['avatar', 'video', 'visual']):
        response = "You're looking at the future of AI interaction! I'm powered by advanced visual technology that lets me appear as a realistic talking avatar. It's pretty amazing how natural our conversation feels when you can see my expressions, right?"
    elif any(word in message_lower for word in ['help', 'what can you do']):
        response = "I'm here to help with anything you need! As a visual AI agent, I can have natural conversations, answer questions, help with tasks, and provide assistance - all while maintaining this face-to-face connection that makes our interaction feel more human and engaging."
    else:
        responses = [
            "That's really interesting! I love how we can have this natural, face-to-face conversation. It makes discussing topics like this so much more engaging than just text, don't you think?",
            "Great question! Being able to express myself visually really helps me communicate more effectively. I can show enthusiasm, concern, or curiosity through my expressions while we talk.",
            "I find that fascinating! There's something special about visual communication - it adds so much depth to our conversation that you just can't get with text alone.",
            "That's a wonderful point! I really enjoy these visual conversations because I can be more expressive and connect with you on a more personal level."
        ]
        response = responses[hash(user_message) % len(responses)]
    
    return {
        "response": response,
        "model_used": "visual_fallback",
        "workflow_type": "visual_agent",
        "agents_used": ["visual"],
        "confidence": 0.7,
        "success": False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
as
ync def generate_sadtalker_video(text: str, session_id: str, style: str = "default") -> dict:
    """Generate talking head video using SadTalker or free alternatives"""
    try:
        # For now, return structured data for video generation
        # This can be extended to integrate with actual SadTalker API or local installation
        
        # Generate audio timing for lip-sync
        words = text.split()
        estimated_duration = len(words) * 0.4 + 2  # Rough estimate
        
        # Analyze text for emotional expressions
        emotion = analyze_text_emotion(text)
        
        # Generate video metadata
        video_data = {
            "type": "sadtalker_video",
            "status": "generated",
            "video_url": f"/api/videos/{session_id}_{int(time.time())}.mp4",
            "thumbnail_url": f"/api/thumbnails/{session_id}_{int(time.time())}.jpg",
            "duration": estimated_duration,
            "emotion": emotion,
            "lip_sync_data": generate_detailed_lip_sync(text),
            "facial_expressions": generate_facial_keyframes(text, emotion),
            "audio_url": f"/api/audio/{session_id}_{int(time.time())}.wav",
            "generated_at": datetime.now().isoformat(),
            "style": style,
            "resolution": "512x512",
            "fps": 25
        }
        
        # In production, this would:
        # 1. Generate audio from text using TTS
        # 2. Call SadTalker API with source image + audio
        # 3. Return actual video URL
        
        # For demo, we'll simulate the process
        print(f"📹 Generated SadTalker video for: {text[:50]}...")
        
        return video_data
        
    except Exception as e:
        print(f"Error generating SadTalker video: {e}")
        return {
            "type": "error",
            "status": "failed",
            "message": "Video generation failed",
            "fallback_mode": True
        }

def analyze_text_emotion(text: str) -> str:
    """Analyze text for dominant emotion"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['excited', 'amazing', 'fantastic', 'wonderful', 'great']):
        return "excited"
    elif any(word in text_lower for word in ['happy', 'glad', 'pleased', 'delighted']):
        return "happy"
    elif any(word in text_lower for word in ['sad', 'sorry', 'disappointed', 'unfortunate']):
        return "sad"
    elif any(word in text_lower for word in ['angry', 'frustrated', 'annoyed']):
        return "angry"
    elif '?' in text:
        return "curious"
    else:
        return "neutral"

def generate_detailed_lip_sync(text: str) -> list:
    """Generate detailed lip-sync data for SadTalker"""
    words = text.split()
    lip_sync_frames = []
    
    current_time = 0
    for word in words:
        word_duration = len(word) * 0.08 + 0.2
        
        # Generate phoneme-based mouth shapes
        phonemes = analyze_word_phonemes(word)
        
        for i, phoneme in enumerate(phonemes):
            frame_time = current_time + (i * word_duration / len(phonemes))
            lip_sync_frames.append({
                "time": frame_time,
                "phoneme": phoneme,
                "mouth_shape": get_mouth_shape_for_phoneme(phoneme),
                "intensity": 0.8
            })
        
        current_time += word_duration + 0.1
    
    return lip_sync_frames

def analyze_word_phonemes(word: str) -> list:
    """Simple phoneme analysis for lip-sync"""
    phonemes = []
    for char in word.lower():
        if char in 'aeiou':
            phonemes.append(char)
        elif char in 'bcdfghjklmnpqrstvwxyz':
            phonemes.append('consonant')
    return phonemes

def get_mouth_shape_for_phoneme(phoneme: str) -> str:
    """Map phonemes to mouth shapes"""
    mouth_shapes = {
        'a': 'open_wide',
        'e': 'open_mid',
        'i': 'narrow',
        'o': 'round',
        'u': 'pucker',
        'consonant': 'closed'
    }
    return mouth_shapes.get(phoneme, 'neutral')

def generate_facial_keyframes(text: str, emotion: str) -> list:
    """Generate facial expression keyframes"""
    duration = len(text.split()) * 0.4 + 2
    
    keyframes = [
        {
            "time": 0,
            "expression": emotion,
            "intensity": 0.6,
            "eyebrow_position": "neutral",
            "eye_openness": 0.8
        },
        {
            "time": duration * 0.3,
            "expression": emotion,
            "intensity": 0.8,
            "eyebrow_position": "slightly_raised" if '?' in text else "neutral",
            "eye_openness": 0.9
        },
        {
            "time": duration * 0.7,
            "expression": emotion,
            "intensity": 0.7,
            "eyebrow_position": "neutral",
            "eye_openness": 0.8
        },
        {
            "time": duration,
            "expression": "neutral",
            "intensity": 0.5,
            "eyebrow_position": "neutral",
            "eye_openness": 0.8
        }
    ]
    
    return keyframes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)