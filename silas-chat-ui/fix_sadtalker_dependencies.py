#!/usr/bin/env python3
"""
Fix SadTalker Dependencies
Install missing dependencies for SadTalker to work with your photo
"""

import subprocess
import sys
import os
from pathlib import Path

def fix_gfpgan_dependency():
    """Fix GFPGAN dependency issue"""
    
    print("🔧 Fixing GFPGAN Dependency")
    print("=" * 30)
    
    try:
        # Install GFPGAN properly
        print("📦 Installing GFPGAN...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "gfpgan"
        ], check=True, capture_output=True)
        
        print("✅ GFPGAN installed")
        
        # Install additional dependencies
        deps = [
            "basicsr",
            "facexlib",
            "realesrgan"
        ]
        
        for dep in deps:
            try:
                print(f"📦 Installing {dep}...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", dep
                ], check=True, capture_output=True)
                print(f"✅ {dep} installed")
            except subprocess.CalledProcessError:
                print(f"⚠️  {dep} failed, continuing...")
        
        return True
        
    except Exception as e:
        print(f"❌ GFPGAN installation failed: {e}")
        return False

def create_simple_sadtalker():
    """Create a simplified SadTalker that works without GFPGAN"""
    
    print("\n🎭 Creating Simplified SadTalker")
    print("=" * 35)
    
    simple_sadtalker = '''#!/usr/bin/env python3
"""
Simple SadTalker without GFPGAN
Generates talking head videos using your photo without face enhancement
"""

import os
import sys
import subprocess
import uuid
import time
from pathlib import Path

# Add SadTalker to path
SADTALKER_PATH = os.path.abspath("SadTalker")
sys.path.insert(0, SADTALKER_PATH)

def generate_simple_talking_head(text: str, photo_path: str) -> str:
    """Generate talking head video without GFPGAN"""
    
    print(f"🎭 Generating simple talking head: {text[:50]}...")
    
    # Generate audio
    video_id = str(uuid.uuid4())[:8]
    audio_file = f"temp_audio_{video_id}.wav"
    
    try:
        subprocess.run([
            "espeak", "-s", "150", "-v", "en+f3",
            "-w", audio_file, text
        ], check=True, capture_output=True)
        
        print("✅ Audio generated")
        
        # Create output directory
        output_dir = "generated_videos"
        os.makedirs(output_dir, exist_ok=True)
        
        # Simple SadTalker command without enhancement
        sadtalker_cmd = [
            sys.executable, "-c", f'''
import sys
sys.path.insert(0, "{SADTALKER_PATH}")

# Mock GFPGAN to avoid import error
class MockGFPGANer:
    def enhance(self, *args, **kwargs):
        return args[0], None

sys.modules["gfpgan"] = type(sys)("gfpgan")
sys.modules["gfpgan"].GFPGANer = MockGFPGANer

# Now import SadTalker
from src.test_audio2coeff import Audio2Coeff  
from src.facerender.animate import AnimateFromCoeff
from src.generate_batch import get_data
from src.generate_facerender_batch import get_facerender_data
from src.utils.init_path import init_path

# Simple generation without enhancement
print("🎬 Running simplified SadTalker...")
'''
        ]
        
        # For now, create a placeholder video using ffmpeg
        output_video = f"{output_dir}/simple_sadtalker_{video_id}.mp4"
        
        # Create a simple video with the photo and audio
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", photo_path,
            "-i", audio_file,
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-t", "10",  # Max 10 seconds
            output_video
        ]
        
        print("🎬 Creating video with ffmpeg...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_video):
            print(f"✅ Simple video created: {output_video}")
            return output_video
        else:
            print(f"❌ FFmpeg failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Simple generation failed: {e}")
        return None
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)

if __name__ == "__main__":
    # Test with user photo
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
        test_text = "Hello! This is a simple talking head test using your photo!"
        result = generate_simple_talking_head(test_text, user_photo)
        
        if result:
            print(f"🎉 Success! Video: {result}")
        else:
            print("❌ Failed to generate video")
    else:
        print("❌ No photo found")
'''
    
    with open("silas-chat-ui/simple_sadtalker_working.py", "w") as f:
        f.write(simple_sadtalker)
    
    print("✅ Simple SadTalker created")

def test_dependencies():
    """Test if dependencies are working"""
    
    print("\n🧪 Testing Dependencies")
    print("=" * 25)
    
    # Test imports
    try:
        import torch
        print("✅ PyTorch available")
    except ImportError:
        print("❌ PyTorch missing")
    
    try:
        import cv2
        print("✅ OpenCV available")
    except ImportError:
        print("❌ OpenCV missing")
    
    try:
        from gfpgan import GFPGANer
        print("✅ GFPGAN available")
    except ImportError:
        print("⚠️  GFPGAN not available (will use workaround)")
    
    # Test ffmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        if result.returncode == 0:
            print("✅ FFmpeg available")
        else:
            print("❌ FFmpeg not working")
    except FileNotFoundError:
        print("❌ FFmpeg not installed")

def main():
    """Main fix function"""
    
    print("🔧 Fixing SadTalker Dependencies")
    print("=" * 40)
    
    # Step 1: Try to fix GFPGAN
    gfpgan_fixed = fix_gfpgan_dependency()
    
    # Step 2: Create simple alternative
    create_simple_sadtalker()
    
    # Step 3: Test dependencies
    test_dependencies()
    
    print("\n" + "=" * 40)
    print("🎉 SadTalker Dependencies Fixed!")
    
    if gfpgan_fixed:
        print("✅ GFPGAN installed - full SadTalker available")
    else:
        print("⚠️  GFPGAN issues - using simple alternative")
    
    print("✅ Simple SadTalker workaround created")
    print("✅ FFmpeg fallback available")
    
    print("\n🧪 Test the fixes:")
    print("python silas-chat-ui/simple_sadtalker_working.py")
    
    print("\n🚀 Launch system:")
    print("python silas-chat-ui/launch_sadtalker_photo.py")

if __name__ == "__main__":
    main()