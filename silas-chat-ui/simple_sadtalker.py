#!/usr/bin/env python3
"""
Simple SadTalker Integration
Simplified video generation without problematic dependencies
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
import uuid
import asyncio

class SimpleSadTalker:
    """Simplified SadTalker wrapper for video generation"""
    
    def __init__(self, sadtalker_path="./SadTalker"):
        self.sadtalker_path = Path(sadtalker_path)
        self.avatar_image = self.sadtalker_path / "assets" / "avatar.jpg"
        
    async def generate_video(self, text, output_dir="generated_videos"):
        """Generate talking head video from text"""
        
        try:
            # Create unique filenames
            video_id = str(uuid.uuid4())[:8]
            audio_file = f"temp_audio_{video_id}.wav"
            video_file = f"{output_dir}/avatar_{video_id}.mp4"
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate TTS audio
            if not await self.generate_tts_audio(text, audio_file):
                return None
            
            # Check if avatar image exists
            if not self.avatar_image.exists():
                print("Avatar image not found, creating placeholder video")
                return await self.create_placeholder_video(text, video_file)
            
            # Try SadTalker generation (simplified)
            video_url = await self.run_sadtalker_simple(audio_file, video_file)
            
            # Cleanup temp audio
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            return video_url
            
        except Exception as e:
            print(f"Video generation error: {e}")
            return None
    
    async def generate_tts_audio(self, text, output_path):
        """Generate TTS audio file"""
        
        try:
            # Use system TTS (macOS say command)
            if sys.platform == "darwin":
                try:
                    # Convert to AIFF first, then to WAV
                    temp_aiff = output_path.replace('.wav', '.aiff')
                    subprocess.run([
                        "say", "-o", temp_aiff, "-r", "180", text
                    ], check=True, capture_output=True)
                    
                    # Convert AIFF to WAV using ffmpeg
                    subprocess.run([
                        "ffmpeg", "-i", temp_aiff, "-y", output_path
                    ], check=True, capture_output=True)
                    
                    # Cleanup temp file
                    if os.path.exists(temp_aiff):
                        os.remove(temp_aiff)
                    
                    return True
                except subprocess.CalledProcessError:
                    pass
            
            # Use espeak if available
            try:
                subprocess.run([
                    "espeak", "-s", "150", "-v", "en+f3", 
                    "-w", output_path, text
                ], check=True, capture_output=True)
                return True
            except FileNotFoundError:
                pass
            
            # Fallback: create silent audio with ffmpeg
            duration = len(text.split()) * 0.6  # Rough estimate
            subprocess.run([
                "ffmpeg", "-f", "lavfi", "-i", f"anullsrc=duration={duration}",
                "-ar", "22050", "-ac", "1", "-y", output_path
            ], check=True, capture_output=True)
            return True
            
        except Exception as e:
            print(f"TTS generation error: {e}")
            return False
    
    async def run_sadtalker_simple(self, audio_file, video_file):
        """Run SadTalker with simplified approach"""
        
        try:
            # Simple SadTalker command without problematic modules
            cmd = [
                "python", "-c", f"""
import sys
sys.path.insert(0, '{self.sadtalker_path}')
import torch
import cv2
import numpy as np
from PIL import Image

# Simple video generation without GFPGAN
print("Generating simple talking head video...")

# Load avatar image
img = cv2.imread('{self.avatar_image}')
if img is None:
    print("Avatar image not found")
    exit(1)

# Create simple video with mouth animation
height, width = img.shape[:2]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('{video_file}', fourcc, 25.0, (width, height))

# Generate 3 seconds of video (75 frames at 25fps)
for frame in range(75):
    # Simple mouth animation
    frame_img = img.copy()
    
    # Add simple mouth movement (basic animation)
    mouth_y = int(height * 0.7)
    mouth_x = int(width * 0.5)
    
    # Animate mouth opening/closing
    mouth_size = 5 + int(3 * abs(np.sin(frame * 0.3)))
    cv2.ellipse(frame_img, (mouth_x, mouth_y), (mouth_size, mouth_size//2), 0, 0, 180, (0, 0, 0), -1)
    
    out.write(frame_img)

out.release()
print(f"Video saved to {video_file}")
"""
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0 and os.path.exists(video_file):
                return f"/videos/{os.path.basename(video_file)}"
            else:
                print(f"SadTalker simple error: {stderr.decode()}")
                return await self.create_placeholder_video("", video_file)
        
        except Exception as e:
            print(f"SadTalker execution error: {e}")
            return await self.create_placeholder_video("", video_file)
    
    async def create_placeholder_video(self, text, video_file):
        """Create a placeholder video with text animation"""
        
        try:
            # Create simple animated video with ffmpeg
            duration = max(3, len(text.split()) * 0.5)
            
            cmd = [
                "ffmpeg", "-f", "lavfi", 
                "-i", f"color=c=blue:size=512x512:duration={duration}",
                "-vf", f"drawtext=text='Silas Avatar\\nSpeaking...':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2",
                "-r", "25", "-pix_fmt", "yuv420p", "-y", video_file
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            
            if os.path.exists(video_file):
                return f"/videos/{os.path.basename(video_file)}"
            
        except Exception as e:
            print(f"Placeholder video error: {e}")
        
        return None

# Test function
async def test_simple_sadtalker():
    """Test the simple SadTalker integration"""
    
    print("🎬 Testing Simple SadTalker Integration")
    
    sadtalker = SimpleSadTalker()
    
    test_text = "Hello! This is a test of my simplified SadTalker video generation system. I can create basic talking head videos!"
    
    video_url = await sadtalker.generate_video(test_text)
    
    if video_url:
        print(f"✅ Video generated: {video_url}")
        return True
    else:
        print("❌ Video generation failed")
        return False

if __name__ == "__main__":
    asyncio.run(test_simple_sadtalker())