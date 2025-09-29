#!/usr/bin/env python3
"""
Simple D-ID Backend
Focus on D-ID API for reliable talking head generation
"""

import os
import sys
import asyncio
import requests
import json
import uuid
import time
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Simple D-ID Avatar API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AvatarRequest(BaseModel):
    message: str
    session_id: str = "default"
    generate_video: bool = True

class AvatarResponse(BaseModel):
    response: str
    video_url: Optional[str] = None
    generation_time: float = 0.0
    method_used: str = "fallback"

class SimpleDIDGenerator:
    """Simple D-ID API integration"""
    
    def __init__(self):
        # Load environment variables explicitly
        from dotenv import load_dotenv
        load_dotenv("silas-chat-ui/.env")
        
        self.api_key = os.getenv("DID_API_KEY")
        self.base_url = "https://api.d-id.com"
        
        if self.api_key:
            print(f"✅ D-ID API key loaded: {self.api_key[:20]}...")
        else:
            print("⚠️  D-ID API key not found")
            print("💡 Check silas-chat-ui/.env file")
    
    async def generate_talking_head(self, text: str, image_path: str) -> Optional[str]:
        """Generate talking head video using D-ID API"""
        
        if not self.api_key:
            print("❌ D-ID API key required")
            return None
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return None
        
        try:
            print(f"🎭 Creating D-ID talking head: {text[:50]}...")
            
            # Step 1: Upload image
            image_url = await self.upload_image(image_path)
            if not image_url:
                return None
            
            # Step 2: Create talking video
            video_url = await self.create_video(image_url, text)
            return video_url
            
        except Exception as e:
            print(f"❌ D-ID generation error: {e}")
            return None
    
    async def upload_image(self, image_path: str) -> Optional[str]:
        """Upload image to D-ID"""
        
        try:
            headers = {
                "Authorization": f"Basic {self.api_key}",
                "Accept": "application/json"
            }
            
            with open(image_path, 'rb') as f:
                files = {"image": (os.path.basename(image_path), f, "image/jpeg")}
                
                response = await asyncio.to_thread(
                    requests.post,
                    f"{self.base_url}/images",
                    headers=headers,
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 201:
                data = response.json()
                image_url = data.get("url")
                print(f"✅ Image uploaded: {image_url}")
                return image_url
            else:
                print(f"❌ Image upload failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Image upload error: {e}")
            return None
    
    async def create_video(self, image_url: str, text: str) -> Optional[str]:
        """Create talking video with D-ID"""
        
        try:
            headers = {
                "Authorization": f"Basic {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            payload = {
                "source_url": image_url,
                "script": {
                    "type": "text",
                    "input": text,
                    "provider": {
                        "type": "microsoft",
                        "voice_id": "en-US-JennyNeural"
                    }
                },
                "config": {
                    "fluent": True,
                    "pad_audio": 0.0,
                    "stitch": True
                }
            }
            
            # Submit video creation
            response = await asyncio.to_thread(
                requests.post,
                f"{self.base_url}/talks",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                talk_id = data.get("id")
                print(f"✅ D-ID video submitted: {talk_id}")
                
                # Wait for completion
                video_url = await self.wait_for_completion(talk_id)
                return video_url
            else:
                print(f"❌ Video creation failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Video creation error: {e}")
            return None
    
    async def wait_for_completion(self, talk_id: str) -> Optional[str]:
        """Wait for D-ID video completion"""
        
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Accept": "application/json"
        }
        
        max_attempts = 60  # 10 minutes max
        
        for attempt in range(max_attempts):
            try:
                response = await asyncio.to_thread(
                    requests.get,
                    f"{self.base_url}/talks/{talk_id}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    
                    print(f"🔄 D-ID status: {status} (attempt {attempt + 1})")
                    
                    if status == "done":
                        video_url = data.get("result_url")
                        print(f"✅ D-ID video ready: {video_url}")
                        
                        # Download video locally
                        local_video = await self.download_video(video_url, talk_id)
                        return local_video or video_url
                        
                    elif status == "error":
                        error_msg = data.get("error", "Unknown error")
                        print(f"❌ D-ID video failed: {error_msg}")
                        return None
                    
                    # Still processing, wait
                    await asyncio.sleep(10)
                else:
                    print(f"⚠️  Status check failed: {response.status_code}")
                    await asyncio.sleep(5)
                
            except Exception as e:
                print(f"⚠️  Status check error: {e}")
                await asyncio.sleep(5)
        
        print("❌ D-ID video timeout after 10 minutes")
        return None
    
    async def download_video(self, video_url: str, talk_id: str) -> Optional[str]:
        """Download D-ID video locally"""
        
        try:
            # Create local filename
            local_filename = f"did_video_{talk_id}.mp4"
            local_path = f"generated_videos/{local_filename}"
            
            # Ensure directory exists
            os.makedirs("generated_videos", exist_ok=True)
            
            # Download video
            response = await asyncio.to_thread(
                requests.get,
                video_url,
                timeout=60
            )
            
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Video downloaded: {local_path}")
                return f"/{local_filename}"
            else:
                print(f"⚠️  Video download failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️  Video download error: {e}")
            return None

# Initialize D-ID generator
did_generator = SimpleDIDGenerator()

async def get_smart_response(message: str) -> str:
    """Get smart AI response"""
    
    # Try to use the free LLM backend
    try:
        sys.path.append('silas-chat-ui')
        from free_llm_backend import get_ai_response
        return await get_ai_response(message)
    except Exception as e:
        print(f"⚠️  LLM backend error: {e}")
        
        # Enhanced fallback responses
        message_lower = message.lower()
        
        responses = {
            "hello": "Hello! I'm your D-ID powered AI avatar. I create professional talking head videos using your real face with perfect lip-sync!",
            "hi": "Hi there! Watch me bring your photo to life with D-ID's advanced talking head technology!",
            "test": "Testing my D-ID video generation! I create incredibly realistic talking head videos using your actual photo.",
            "video": "I generate stunning talking head videos using D-ID's professional API. Your face will speak with perfect lip synchronization!",
            "face": "I use your real face photo with D-ID technology to create lifelike talking head videos. No cartoon avatars - just your authentic face!",
            "real": "Absolutely! I create ultra-realistic talking head videos using D-ID API and your actual face photo with natural expressions.",
            "generate": "I'll generate an amazing professional talking head video using D-ID API and your real face photo!",
            "did": "I'm powered by D-ID's professional talking head API, creating broadcast-quality videos with perfect lip-sync!",
            "professional": "My D-ID integration provides professional-grade talking head videos used by major studios and content creators!",
            "quality": "D-ID delivers the highest quality talking head videos with natural expressions and flawless lip synchronization!"
        }
        
        # Find best match
        for keyword, response in responses.items():
            if keyword in message_lower:
                return response
        
        # Contextual responses
        if any(word in message_lower for word in ["create", "make", "build"]):
            return "I'll create a professional talking head video using D-ID's advanced API and your real face photo!"
        
        if any(word in message_lower for word in ["natural", "realistic", "lifelike"]):
            return "D-ID creates incredibly natural and lifelike talking head videos that are indistinguishable from real recordings!"
        
        # Default response
        return "I'm your D-ID powered AI avatar. I create professional talking head videos using your real face with broadcast-quality results!"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    # Reload environment to ensure we have latest values
    from dotenv import load_dotenv
    load_dotenv("silas-chat-ui/.env")
    
    did_key = os.getenv("DID_API_KEY")
    did_available = bool(did_key)
    
    return {
        "status": "healthy",
        "did_api_available": did_available,
        "did_key_preview": did_key[:20] + "..." if did_key else "Not found",
        "video_generation": "enabled" if did_available else "disabled"
    }

@app.post("/generate-avatar", response_model=AvatarResponse)
async def generate_avatar(request: AvatarRequest, background_tasks: BackgroundTasks):
    """Generate D-ID talking head video"""
    
    start_time = datetime.now()
    
    try:
        print(f"🎭 Processing D-ID request: '{request.message[:50]}...'")
        
        # Get AI response
        ai_response = await get_smart_response(request.message)
        
        video_url = None
        method_used = "fallback"
        
        if request.generate_video and did_generator.api_key:
            # Find user photo
            photo_paths = [
                "silas-chat-ui/my_photo.jpg",
                "SadTalker/assets/avatar.jpg"
            ]
            
            user_photo = None
            for photo_path in photo_paths:
                if os.path.exists(photo_path):
                    user_photo = photo_path
                    print(f"📸 Using photo: {photo_path}")
                    break
            
            if user_photo:
                # Generate D-ID video
                video_url = await did_generator.generate_talking_head(ai_response, user_photo)
                if video_url:
                    method_used = "did_api"
                    print(f"✅ D-ID video generated successfully")
                else:
                    print("❌ D-ID video generation failed")
            else:
                print("📸 No user photo found - save your photo as 'silas-chat-ui/my_photo.jpg'")
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        return AvatarResponse(
            response=ai_response,
            video_url=video_url,
            generation_time=generation_time,
            method_used=method_used
        )
        
    except Exception as e:
        print(f"❌ Avatar generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/avatar-image")
async def get_avatar_image():
    """Serve the user's avatar image"""
    
    photo_paths = [
        "silas-chat-ui/my_photo.jpg",
        "SadTalker/assets/avatar.jpg"
    ]
    
    for photo_path in photo_paths:
        if os.path.exists(photo_path):
            return FileResponse(photo_path, media_type="image/jpeg")
    
    raise HTTPException(status_code=404, detail="User photo not found. Please save your photo as 'silas-chat-ui/my_photo.jpg'")

@app.get("/{video_filename}")
async def serve_video(video_filename: str):
    """Serve generated video files"""
    
    if not video_filename.endswith(('.mp4', '.avi', '.mov')):
        raise HTTPException(status_code=404, detail="Invalid video file")
    
    video_path = os.path.join("generated_videos", video_filename)
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        headers={
            "Accept-Ranges": "bytes",
            "Content-Type": "video/mp4",
            "Cache-Control": "no-cache"
        }
    )

@app.get("/test-did")
async def test_did():
    """Test D-ID API"""
    
    # Reload environment
    from dotenv import load_dotenv
    load_dotenv("silas-chat-ui/.env")
    
    api_key = os.getenv("DID_API_KEY")
    
    if not api_key:
        return {"error": "D-ID API key not configured", "env_file": "silas-chat-ui/.env"}
    
    # Check for user photo
    photo_paths = [
        "silas-chat-ui/my_photo.jpg",
        "SadTalker/assets/avatar.jpg"
    ]
    
    user_photo = None
    for photo_path in photo_paths:
        if os.path.exists(photo_path):
            user_photo = photo_path
            break
    
    if not user_photo:
        return {"error": "No user photo found. Save your photo as 'silas-chat-ui/my_photo.jpg'"}
    
    # Test video generation
    test_text = "Hello! This is a test of my D-ID powered talking head generation. I can create professional quality videos with perfect lip-sync!"
    
    # Create a fresh generator with the API key
    test_generator = SimpleDIDGenerator()
    video_url = await test_generator.generate_talking_head(test_text, user_photo)
    
    return {
        "message": "D-ID API test",
        "text": test_text,
        "photo_used": user_photo,
        "api_key_preview": api_key[:20] + "..." if api_key else "None",
        "video_url": video_url,
        "status": "success" if video_url else "failed"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🎭 Starting Simple D-ID Backend")
    print("=" * 40)
    
    if did_generator.api_key:
        print("✅ D-ID API ready for professional talking heads")
    else:
        print("⚠️  D-ID API key needed for video generation")
        print("💡 Add DID_API_KEY to silas-chat-ui/.env")
    
    print("🚀 Starting server on http://127.0.0.1:8002")
    
    uvicorn.run(app, host="127.0.0.1", port=8002)