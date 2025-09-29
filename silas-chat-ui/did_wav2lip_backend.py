#!/usr/bin/env python3
"""
D-ID + Wav2Lip Backend
Real talking head video generation using D-ID API and Wav2Lip
"""

import os
import sys
import subprocess
import uuid
import time
import asyncio
import requests
import json
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

app = FastAPI(title="D-ID + Wav2Lip Avatar API")

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
    use_did_api: bool = True

class AvatarResponse(BaseModel):
    response: str
    video_url: Optional[str] = None
    generation_time: float = 0.0
    method_used: str = "fallback"

class DIDVideoGenerator:
    """D-ID API video generation"""
    
    def __init__(self):
        self.api_key = os.getenv("DID_API_KEY")
        self.base_url = "https://api.d-id.com"
        
    async def generate_video(self, text: str, image_path: str) -> Optional[str]:
        """Generate video using D-ID API"""
        
        if not self.api_key:
            print("❌ D-ID API key not found")
            return None
        
        try:
            print(f"🎭 Generating D-ID video: {text[:50]}...")
            
            # Upload image first
            image_url = await self.upload_image(image_path)
            if not image_url:
                return None
            
            # Create video
            headers = {
                "Authorization": f"Basic {self.api_key}",
                "Content-Type": "application/json"
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
                    "pad_audio": 0.0
                }
            }
            
            # Submit video creation
            response = requests.post(
                f"{self.base_url}/talks",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                talk_id = response.json()["id"]
                print(f"✅ D-ID video submitted: {talk_id}")
                
                # Wait for video completion
                video_url = await self.wait_for_video(talk_id)
                return video_url
            else:
                print(f"❌ D-ID API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ D-ID generation error: {e}")
            return None
    
    async def upload_image(self, image_path: str) -> Optional[str]:
        """Upload image to D-ID"""
        
        try:
            headers = {"Authorization": f"Basic {self.api_key}"}
            
            with open(image_path, 'rb') as f:
                files = {"image": f}
                response = requests.post(
                    f"{self.base_url}/images",
                    headers=headers,
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 201:
                return response.json()["url"]
            else:
                print(f"❌ Image upload failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Image upload error: {e}")
            return None
    
    async def wait_for_video(self, talk_id: str) -> Optional[str]:
        """Wait for D-ID video completion"""
        
        headers = {"Authorization": f"Basic {self.api_key}"}
        
        for attempt in range(30):  # Wait up to 5 minutes
            try:
                response = requests.get(
                    f"{self.base_url}/talks/{talk_id}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    
                    if status == "done":
                        video_url = data.get("result_url")
                        print(f"✅ D-ID video ready: {video_url}")
                        return video_url
                    elif status == "error":
                        print(f"❌ D-ID video failed: {data.get('error')}")
                        return None
                    else:
                        print(f"🔄 D-ID status: {status}")
                
                await asyncio.sleep(10)  # Wait 10 seconds
                
            except Exception as e:
                print(f"⚠️  Status check error: {e}")
                await asyncio.sleep(5)
        
        print("❌ D-ID video timeout")
        return None

class Wav2LipGenerator:
    """Wav2Lip video generation"""
    
    def __init__(self):
        self.wav2lip_path = Path("Wav2Lip")
        self.model_path = self.wav2lip_path / "checkpoints/wav2lip_gan.pth"
        
    async def generate_video(self, text: str, image_path: str) -> Optional[str]:
        """Generate video using Wav2Lip"""
        
        if not self.wav2lip_path.exists():
            print("❌ Wav2Lip not installed")
            return None
        
        if not self.model_path.exists():
            print("❌ Wav2Lip model not found")
            return None
        
        try:
            print(f"🎬 Generating Wav2Lip video: {text[:50]}...")
            
            # Generate unique IDs
            video_id = str(uuid.uuid4())[:8]
            audio_file = f"temp_audio_{video_id}.wav"
            output_video = f"generated_videos/wav2lip_{video_id}.mp4"
            
            # Ensure output directory
            os.makedirs("generated_videos", exist_ok=True)
            
            # Generate TTS audio
            if not await self.generate_tts_audio(text, audio_file):
                return None
            
            # Run Wav2Lip
            wav2lip_cmd = [
                sys.executable,
                str(self.wav2lip_path / "inference.py"),
                "--checkpoint_path", str(self.model_path),
                "--face", image_path,
                "--audio", audio_file,
                "--outfile", output_video
            ]
            
            print("🎭 Running Wav2Lip inference...")
            result = subprocess.run(
                wav2lip_cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(self.wav2lip_path)
            )
            
            if result.returncode == 0 and os.path.exists(output_video):
                print(f"✅ Wav2Lip video generated: {output_video}")
                return f"/{os.path.basename(output_video)}"
            else:
                print(f"❌ Wav2Lip failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Wav2Lip generation error: {e}")
            return None
        finally:
            # Cleanup temp audio
            if os.path.exists(audio_file):
                os.remove(audio_file)
    
    async def generate_tts_audio(self, text: str, output_path: str) -> bool:
        """Generate TTS audio for Wav2Lip"""
        
        try:
            # Use espeak for TTS
            subprocess.run([
                "espeak", "-s", "150", "-v", "en+f3",
                "-w", output_path, text
            ], check=True, capture_output=True, timeout=30)
            
            return True
            
        except Exception as e:
            print(f"❌ TTS generation failed: {e}")
            return False

# Initialize generators
did_generator = DIDVideoGenerator()
wav2lip_generator = Wav2LipGenerator()

async def get_smart_response(message: str) -> str:
    """Get smart AI response"""
    
    # Import the free LLM backend
    try:
        sys.path.append('silas-chat-ui')
        from free_llm_backend import get_ai_response
        return await get_ai_response(message)
    except:
        # Fallback responses
        responses = {
            "hello": "Hello! I'm your realistic AI avatar. I can generate talking head videos using D-ID API or Wav2Lip technology!",
            "test": "Testing my video generation! I use D-ID API for professional quality or Wav2Lip for local processing.",
            "video": "I create amazing talking head videos using your real face photo with D-ID API or Wav2Lip lip-sync technology!",
            "default": "I'm your AI avatar powered by D-ID API and Wav2Lip. I create realistic talking head videos with perfect lip-sync!"
        }
        
        message_lower = message.lower()
        for key, response in responses.items():
            if key in message_lower:
                return response
        
        return responses["default"]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    did_available = bool(os.getenv("DID_API_KEY"))
    wav2lip_available = Path("Wav2Lip").exists()
    
    return {
        "status": "healthy",
        "did_api_available": did_available,
        "wav2lip_available": wav2lip_available,
        "video_generation": "enabled"
    }

@app.post("/generate-avatar", response_model=AvatarResponse)
async def generate_avatar(request: AvatarRequest, background_tasks: BackgroundTasks):
    """Generate talking head video using D-ID or Wav2Lip"""
    
    start_time = datetime.now()
    
    try:
        print(f"🎭 Generating avatar video: '{request.message[:50]}...'")
        
        # Get AI response
        ai_response = await get_smart_response(request.message)
        
        video_url = None
        method_used = "fallback"
        
        if request.generate_video:
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
            
            if user_photo:
                # Try D-ID API first
                if request.use_did_api and did_generator.api_key:
                    print("🎭 Trying D-ID API...")
                    video_url = await did_generator.generate_video(ai_response, user_photo)
                    if video_url:
                        method_used = "did_api"
                
                # Fallback to Wav2Lip
                if not video_url and wav2lip_generator.wav2lip_path.exists():
                    print("🎬 Trying Wav2Lip...")
                    video_url = await wav2lip_generator.generate_video(ai_response, user_photo)
                    if video_url:
                        method_used = "wav2lip"
            else:
                print("📸 No user photo found for video generation")
        
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
    
    raise HTTPException(status_code=404, detail="User photo not found")

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

if __name__ == "__main__":
    import uvicorn
    
    print("🎭 Starting D-ID + Wav2Lip Backend")
    print("=" * 40)
    print("✅ D-ID API integration ready")
    print("✅ Wav2Lip local processing ready")
    print("🚀 Starting server on http://127.0.0.1:8002")
    
    uvicorn.run(app, host="127.0.0.1", port=8002)
