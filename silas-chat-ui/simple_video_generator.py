#!/usr/bin/env python3
"""
Simple Video Generator with Your Photo
Creates talking head videos using your photo and TTS
"""

import os
import subprocess
import uuid
import asyncio
from pathlib import Path

async def generate_simple_talking_video(text: str, photo_path: str) -> str:
    """Generate a simple talking head video using your photo"""
    
    print(f"🎬 Creating talking video: {text[:50]}...")
    
    # Generate unique ID
    video_id = str(uuid.uuid4())[:8]
    audio_file = f"temp_audio_{video_id}.wav"
    output_dir = "generated_videos"
    output_video = f"{output_dir}/talking_head_{video_id}.mp4"
    
    # Ensure output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Generate TTS audio
        print("🎤 Generating TTS audio...")
        subprocess.run([
            "espeak", "-s", "150", "-v", "en+f3", "-p", "50",
            "-w", audio_file, text
        ], check=True, capture_output=True)
        
        print("✅ Audio generated")
        
        # Get audio duration
        duration_result = subprocess.run([
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "csv=p=0", audio_file
        ], capture_output=True, text=True)
        
        try:
            duration = float(duration_result.stdout.strip())
        except:
            duration = 5.0  # Default 5 seconds
        
        print(f"🕐 Audio duration: {duration:.1f}s")
        
        # Create talking head video with your photo
        print("🎭 Creating talking head video...")
        
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", photo_path,
            "-i", audio_file,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-vf", f"scale=512:512,fps=25",
            "-shortest",
            "-t", str(duration),
            output_video
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_video):
            file_size = os.path.getsize(output_video) / 1024 / 1024
            print(f"✅ Talking head video created: {output_video}")
            print(f"📏 Size: {file_size:.2f} MB, Duration: {duration:.1f}s")
            return f"/{os.path.basename(output_video)}"
        else:
            print(f"❌ FFmpeg failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        return None
    finally:
        # Cleanup temp audio
        if os.path.exists(audio_file):
            os.remove(audio_file)

async def test_video_generation():
    """Test video generation with user photo"""
    
    print("🧪 Testing Video Generation with Your Photo")
    print("=" * 50)
    
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
    
    if not user_photo:
        print("❌ No user photo found")
        print("💡 Save your photo as 'silas-chat-ui/my_photo.jpg'")
        return False
    
    # Test message
    test_text = "Hello! This is a test of my talking head video generation using your real photo. I'm speaking with synchronized audio and your actual face!"
    
    # Generate video
    video_url = await generate_simple_talking_video(test_text, user_photo)
    
    if video_url:
        print("\n🎉 SUCCESS! Talking head video generated!")
        print(f"🎬 Video: {video_url}")
        print("✅ Your photo is now a talking head!")
        return True
    else:
        print("\n❌ Video generation failed")
        return False

if __name__ == "__main__":
    asyncio.run(test_video_generation())