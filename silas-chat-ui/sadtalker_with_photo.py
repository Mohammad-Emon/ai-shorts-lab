#!/usr/bin/env python3
"""
SadTalker with Your Photo
Generate real talking head videos using your actual photo
"""

import os
import sys
import subprocess
import uuid
import time
import asyncio
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

# Add SadTalker to path
SADTALKER_PATH = os.path.abspath("SadTalker")
if os.path.exists(SADTALKER_PATH):
    sys.path.insert(0, SADTALKER_PATH)

app = FastAPI(title="SadTalker with Your Photo API")

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
    method_used: str = "sadtalker"

class SadTalkerGenerator:
    """SadTalker video generation with user photo"""
    
    def __init__(self):
        self.sadtalker_path = Path(SADTALKER_PATH)
        self.checkpoints_available = self.check_models()
        
        if self.checkpoints_available:
            print("✅ SadTalker models available")
        else:
            print("⚠️  SadTalker models missing")
    
    def check_models(self):
        """Check if SadTalker models are available"""
        
        required_models = [
            "checkpoints/mapping_00109-model.pth.tar",
            "checkpoints/facevid2vid_00189-model.pth.tar"
        ]
        
        for model in required_models:
            model_path = self.sadtalker_path / model
            if not model_path.exists():
                return False
        
        return True
    
    async def generate_tts_audio(self, text: str, output_path: str) -> bool:
        """Generate TTS audio for SadTalker"""
        
        try:
            print(f"🎤 Generating TTS audio: {text[:50]}...")
            
            # Use espeak for TTS
            subprocess.run([
                "espeak", "-s", "150", "-v", "en+f3", "-p", "50",
                "-w", output_path, text
            ], check=True, capture_output=True, timeout=30)
            
            print("✅ TTS audio generated")
            return True
            
        except Exception as e:
            print(f"❌ TTS generation failed: {e}")
            return False
    
    async def generate_talking_head(self, text: str, session_id: str) -> Optional[str]:
        """Generate talking head video using SadTalker with user photo"""
        
        if not self.checkpoints_available:
            print("❌ SadTalker models not available")
            return None
        
        try:
            print(f"🎭 Generating SadTalker video: {text[:50]}...")
            
            # Create unique filenames
            video_id = str(uuid.uuid4())[:8]
            audio_file = f"temp_audio_{video_id}.wav"
            video_file = f"generated_videos/sadtalker_{video_id}.mp4"
            
            # Ensure output directory
            os.makedirs("generated_videos", exist_ok=True)
            
            # Generate TTS audio
            if not await self.generate_tts_audio(text, audio_file):
                return None
            
            # Find user photo
            photo_paths = [
                "silas-chat-ui/my_photo.jpg",
                "SadTalker/assets/avatar.jpg"
            ]
            
            user_photo = None
            for photo_path in photo_paths:
                if os.path.exists(photo_path):
                    user_photo = os.path.abspath(photo_path)
                    break
            
            if not user_photo:
                print("❌ No user photo found")
                return None
            
            print(f"📸 Using photo: {user_photo}")
            
            # Prepare SadTalker command
            sadtalker_cmd = [
                sys.executable,
                os.path.join(SADTALKER_PATH, "inference.py"),
                "--driven_audio", os.path.abspath(audio_file),
                "--source_image", user_photo,
                "--result_dir", os.path.abspath("generated_videos"),
                "--still",
                "--preprocess", "full",
                "--size", "512",
                "--pose_style", "0",
                "--facerender", "facevid2vid",
                "--verbose"
            ]
            
            print("🎬 Running SadTalker inference...")
            print(f"Command: {' '.join(sadtalker_cmd)}")
            
            # Run SadTalker
            start_time = time.time()
            result = subprocess.run(
                sadtalker_cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max
                cwd=SADTALKER_PATH
            )
            
            generation_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ SadTalker completed in {generation_time:.1f}s")
                
                # Find the generated video
                video_files = []
                for file in os.listdir("generated_videos"):
                    if file.endswith(('.mp4', '.avi', '.mov')):
                        file_path = os.path.join("generated_videos", file)
                        # Check if file was created recently
                        if os.path.getctime(file_path) > start_time - 10:
                            video_files.append(file)
                
                if video_files:
                    # Use the most recent video
                    latest_video = max(video_files, 
                        key=lambda x: os.path.getctime(os.path.join("generated_videos", x)))
                    
                    # Rename to include session info
                    final_name = f"sadtalker_{video_id}.mp4"
                    final_path = os.path.join("generated_videos", final_name)
                    
                    if latest_video != final_name:
                        os.rename(os.path.join("generated_videos", latest_video), final_path)
                    
                    print(f"✅ SadTalker video generated: {final_name}")
                    return f"/{final_name}"
                
                print("⚠️  Video files not found in output directory")
                
            else:
                print(f"❌ SadTalker failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
            
            return None
            
        except subprocess.TimeoutExpired:
            print("❌ SadTalker timed out (>5 minutes)")
            return None
        except Exception as e:
            print(f"❌ SadTalker generation error: {e}")
            return None
        finally:
            # Cleanup temp files
            if os.path.exists(audio_file):
                os.remove(audio_file)

# Initialize SadTalker generator
sadtalker_generator = SadTalkerGenerator()

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
            "hello": "Hello! I'm your SadTalker powered AI avatar. I create realistic talking head videos using your actual photo with perfect lip-sync!",
            "hi": "Hi there! Watch me bring your photo to life with SadTalker's advanced talking head technology!",
            "test": "Testing my SadTalker video generation! I create incredibly realistic talking head videos using your actual photo.",
            "video": "I generate stunning talking head videos using SadTalker AI. Your face will speak with perfect lip synchronization!",
            "face": "I use your real face photo with SadTalker technology to create lifelike talking head videos. No cartoon avatars!",
            "real": "Absolutely! I create ultra-realistic talking head videos using SadTalker and your actual face photo with natural expressions.",
            "generate": "I'll generate an amazing realistic talking head video using SadTalker and your real face photo!",
            "sadtalker": "I'm powered by SadTalker AI, creating the most realistic talking head videos with perfect lip-sync!",
            "photo": "Your photo is processed by SadTalker to create incredibly realistic talking head videos with natural movements!",
            "lip": "My lip-sync is powered by SadTalker AI, creating natural mouth movements that perfectly match the audio!"
        }
        
        # Find best match
        for keyword, response in responses.items():
            if keyword in message_lower:
                return response
        
        # Default response
        return "I'm your SadTalker powered AI avatar. I create incredibly realistic talking head videos using your real face with perfect lip-sync!"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    sadtalker_available = sadtalker_generator.checkpoints_available
    photo_available = any(os.path.exists(path) for path in [
        "silas-chat-ui/my_photo.jpg",
        "SadTalker/assets/avatar.jpg"
    ])
    
    return {
        "status": "healthy",
        "sadtalker_available": sadtalker_available,
        "photo_available": photo_available,
        "video_generation": "enabled" if sadtalker_available else "disabled"
    }

@app.post("/generate-avatar", response_model=AvatarResponse)
async def generate_avatar(request: AvatarRequest, background_tasks: BackgroundTasks):
    """Generate SadTalker talking head video with user photo"""
    
    start_time = datetime.now()
    
    try:
        print(f"🎭 Processing SadTalker request: '{request.message[:50]}...'")
        
        # Get AI response
        ai_response = await get_smart_response(request.message)
        
        video_url = None
        method_used = "fallback"
        
        if request.generate_video and sadtalker_generator.checkpoints_available:
            # Generate SadTalker video with user photo
            video_url = await sadtalker_generator.generate_talking_head(ai_response, request.session_id)
            if video_url:
                method_used = "sadtalker"
                print(f"✅ SadTalker video generated successfully")
            else:
                print("❌ SadTalker video generation failed")
        
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

@app.get("/test-sadtalker")
async def test_sadtalker():
    """Test SadTalker with user photo"""
    
    if not sadtalker_generator.checkpoints_available:
        return {"error": "SadTalker models not available"}
    
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
        return {"error": "No user photo found"}
    
    # Test video generation
    test_text = "Hello! This is a test of my SadTalker powered talking head generation using your real photo. Watch me speak with perfect lip-sync!"
    
    video_url = await sadtalker_generator.generate_talking_head(test_text, "test_session")
    
    return {
        "message": "SadTalker test",
        "text": test_text,
        "photo_used": user_photo,
        "video_url": video_url,
        "status": "success" if video_url else "failed"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🎭 Starting SadTalker with Your Photo")
    print("=" * 40)
    
    if sadtalker_generator.checkpoints_available:
        print("✅ SadTalker models ready")
    else:
        print("⚠️  SadTalker models missing")
    
    print("📸 Will use your photo for realistic talking heads")
    print("🚀 Starting server on http://127.0.0.1:8002")
    
    uvicorn.run(app, host="127.0.0.1", port=8002)