#!/usr/bin/env python3
"""
Real SadTalker Backend - Uses Actual Photos for Talking Heads
No more cartoon avatars - real face lip-sync generation
"""

import os
import sys
import subprocess
import uuid
import time
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import sys
sys.path.append('silas-chat-ui')
from free_llm_backend import get_ai_response as get_free_llm_response

# Add SadTalker to path
SADTALKER_PATH = os.path.abspath("SadTalker")
if os.path.exists(SADTALKER_PATH):
    sys.path.insert(0, SADTALKER_PATH)

app = FastAPI(title="Real SadTalker Avatar API")

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
    use_real_face: bool = True

class AvatarResponse(BaseModel):
    response: str
    video_url: Optional[str] = None
    generation_time: float = 0.0
    is_real_face: bool = False

# Fallback responses for API errors
SMART_RESPONSES = {
    "hello": "Hello! I'm your personal talking head avatar using your real face. Watch me speak with natural lip movements!",
    "hi": "Hi there! I use your actual photo to create realistic talking head videos with perfect lip-sync.",
    "test": "This is a test of my real face generation system. I create videos using your actual photo with SadTalker technology!",
    "how are you": "I'm doing excellent! My real face video generation is working perfectly with your photo.",
    "demo": "Welcome to your personal real face demo! I transform your photo into a talking head with natural expressions.",
    "video": "I generate realistic videos using your actual face photo. SadTalker creates natural lip movements that match my speech perfectly.",
    "face": "I use your real face photo to create talking head videos. No more cartoon avatars - just your actual face speaking!",
    "photo": "Your photo is processed by SadTalker to create realistic talking head videos with perfect lip synchronization.",
    "default": "I'm your personal AI avatar using your real face photo. I create natural-looking talking head videos with perfect lip-sync!"
}

async def get_smart_response(message: str) -> str:
    """Get intelligent response based on message content"""
    
    message_lower = message.lower()
    
    # Check for specific keywords
    for keyword, response in SMART_RESPONSES.items():
        if keyword in message_lower:
            return response
    
    # Generate contextual response
    if any(word in message_lower for word in ["generate", "create", "make"]):
        return "I'll generate a realistic talking head video using your actual face photo with perfect lip-sync!"
    
    if any(word in message_lower for word in ["real", "realistic", "natural"]):
        return "Yes! I create realistic talking head videos using your real face photo. No cartoon avatars - just your natural face speaking!"
    
    if any(word in message_lower for word in ["lip", "sync", "mouth"]):
        return "I provide perfect lip synchronization using SadTalker technology. Your mouth movements match the speech exactly!"
    
    return SMART_RESPONSES["default"]

async def generate_tts_audio(text: str, output_path: str) -> bool:
    """Generate high-quality TTS audio"""
    
    try:
        print(f"🎤 Generating TTS audio: {text[:50]}...")
        
        # Try espeak first (fast and reliable)
        try:
            subprocess.run([
                "espeak", "-s", "140", "-v", "en+f3", "-p", "50",
                "-w", output_path, text
            ], check=True, capture_output=True, timeout=30)
            
            print("✅ TTS audio generated with espeak")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            # Fallback: create silent audio with estimated duration
            duration = max(2, len(text.split()) * 0.6)  # Estimate speaking time
            
            subprocess.run([
                "ffmpeg", "-f", "lavfi", "-i", f"anullsrc=duration={duration}:sample_rate=22050",
                "-y", output_path
            ], check=True, capture_output=True, timeout=30)
            
            print(f"✅ Silent audio created ({duration}s)")
            return True
            
    except Exception as e:
        print(f"❌ TTS generation failed: {e}")
        return False

async def generate_real_talking_head(text: str, session_id: str) -> Optional[str]:
    """Generate real talking head video using user's actual photo"""
    
    try:
        print(f"🎭 Generating REAL talking head with user photo...")
        
        # Create unique identifiers
        video_id = str(uuid.uuid4())[:8]
        audio_file = f"temp_audio_{video_id}.wav"
        
        # Ensure directories exist
        os.makedirs("generated_videos", exist_ok=True)
        
        # Check for user photo
        user_photo_paths = [
            "silas-chat-ui/my_photo.jpg",
            "SadTalker/assets/avatar.jpg",
            "my_photo.jpg",
            "user_photo.jpg"
        ]
        
        source_image = None
        for photo_path in user_photo_paths:
            if os.path.exists(photo_path):
                source_image = os.path.abspath(photo_path)
                print(f"✅ Using photo: {photo_path}")
                break
        
        if not source_image:
            print("❌ No user photo found. Please save your photo as 'silas-chat-ui/my_photo.jpg'")
            return None
        
        # Generate TTS audio
        if not await generate_tts_audio(text, audio_file):
            return None
        
        # Prepare SadTalker command
        result_dir = os.path.abspath("generated_videos")
        audio_path = os.path.abspath(audio_file)
        
        sadtalker_cmd = [
            sys.executable,
            os.path.join(SADTALKER_PATH, "inference.py"),
            "--driven_audio", audio_path,
            "--source_image", source_image,
            "--result_dir", result_dir,
            "--still",
            "--preprocess", "full",
            "--size", "512"
        ]
        
        # Add enhancer if available
        if shutil.which("gfpgan") or os.path.exists(os.path.join(SADTALKER_PATH, "gfpgan")):
            sadtalker_cmd.extend(["--enhancer", "gfpgan"])
        
        print("🎬 Running SadTalker inference with real face...")
        print(f"Command: {' '.join(sadtalker_cmd)}")
        
        # Run SadTalker
        start_time = time.time()
        result = subprocess.run(
            sadtalker_cmd, 
            capture_output=True, 
            text=True, 
            timeout=180,  # 3 minutes max
            cwd=SADTALKER_PATH
        )
        
        generation_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ SadTalker completed in {generation_time:.1f}s")
            
            # Find the generated video
            video_files = []
            for file in os.listdir(result_dir):
                if file.endswith(('.mp4', '.avi', '.mov')):
                    file_path = os.path.join(result_dir, file)
                    # Check if file was created recently
                    if os.path.getctime(file_path) > start_time - 10:
                        video_files.append(file)
            
            if video_files:
                # Use the most recent video
                latest_video = max(video_files, 
                    key=lambda x: os.path.getctime(os.path.join(result_dir, x)))
                
                # Rename to include session info
                final_name = f"real_face_{video_id}.mp4"
                final_path = os.path.join(result_dir, final_name)
                
                shutil.move(os.path.join(result_dir, latest_video), final_path)
                
                print(f"✅ Real talking head generated: {final_name}")
                return f"/{final_name}"
            
            print("⚠️  Video files not found in output directory")
            
        else:
            print(f"❌ SadTalker failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
        
        return None
        
    except subprocess.TimeoutExpired:
        print("❌ SadTalker timed out (>3 minutes)")
        return None
    except Exception as e:
        print(f"❌ Real talking head generation error: {e}")
        return None
    finally:
        # Cleanup temp files
        if os.path.exists(audio_file):
            os.remove(audio_file)

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    sadtalker_available = os.path.exists(SADTALKER_PATH)
    user_photo_available = any(os.path.exists(path) for path in [
        "silas-chat-ui/my_photo.jpg",
        "SadTalker/assets/avatar.jpg"
    ])
    
    return {
        "status": "healthy",
        "sadtalker_available": sadtalker_available,
        "user_photo_available": user_photo_available,
        "real_face_mode": "enabled"
    }

@app.post("/generate-avatar", response_model=AvatarResponse)
async def generate_real_avatar(request: AvatarRequest, background_tasks: BackgroundTasks):
    """Generate real talking head avatar using user's photo"""
    
    start_time = datetime.now()
    
    try:
        print(f"🎭 Generating real face avatar for: '{request.message[:50]}...'")
        
        # Get intelligent response
        ai_response = await get_free_llm_response(request.message)
        
        video_url = None
        is_real_face = False
        
        if request.generate_video and request.use_real_face:
            # Generate real talking head video
            video_url = await generate_real_talking_head(ai_response, request.session_id)
            is_real_face = video_url is not None
            
            if video_url:
                print(f"✅ Real face video generated: {video_url}")
            else:
                print("⚠️  Real face generation failed, check photo setup")
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        return AvatarResponse(
            response=ai_response,
            video_url=video_url,
            generation_time=generation_time,
            is_real_face=is_real_face
        )
        
    except Exception as e:
        print(f"❌ Real avatar generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/setup-photo")
async def setup_photo_instructions():
    """Get instructions for setting up user photo"""
    
    return {
        "instructions": [
            "Save your photo as 'silas-chat-ui/my_photo.jpg'",
            "Use a clear, front-facing photo",
            "Ensure good lighting and face visibility",
            "Photo should be at least 256x256 pixels",
            "Face should take up most of the frame"
        ],
        "supported_formats": ["jpg", "jpeg", "png"],
        "recommended_size": "512x512 pixels",
        "current_photo_available": os.path.exists("silas-chat-ui/my_photo.jpg")
    }

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
    
    raise HTTPException(status_code=404, detail="User photo not found. Please upload your photo.")

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

@app.get("/test-real-face")
async def test_real_face():
    """Test real face generation"""
    
    test_text = "Hello! This is a test of my real face talking head generation. I'm using your actual photo to create this video!"
    
    video_url = await generate_real_talking_head(test_text, "test_session")
    
    return {
        "message": "Real face test",
        "text": test_text,
        "video_url": video_url,
        "status": "success" if video_url else "failed",
        "photo_available": os.path.exists("silas-chat-ui/my_photo.jpg")
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🎭 Starting Real SadTalker Backend")
    print("=" * 40)
    print("✅ Real face mode enabled")
    print("📸 Place your photo at: silas-chat-ui/my_photo.jpg")
    print("🎬 SadTalker will use your actual face")
    print("🚀 Starting server on http://127.0.0.1:8002")
    
    uvicorn.run(app, host="127.0.0.1", port=8002)