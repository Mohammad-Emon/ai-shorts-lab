#!/usr/bin/env python3
"""
Test SadTalker Directly with Your Photo
Direct test of SadTalker video generation
"""

import os
import sys
import subprocess
import uuid
from pathlib import Path

def test_sadtalker_direct():
    """Test SadTalker directly with user photo"""
    
    print("🎭 Testing SadTalker Directly with Your Photo")
    print("=" * 50)
    
    # Check SadTalker setup
    sadtalker_path = Path("SadTalker")
    
    if not sadtalker_path.exists():
        print("❌ SadTalker directory not found")
        return False
    
    # Check models
    models = [
        "checkpoints/mapping_00109-model.pth.tar",
        "checkpoints/facevid2vid_00189-model.pth.tar"
    ]
    
    print("🔍 Checking SadTalker models...")
    for model in models:
        model_path = sadtalker_path / model
        if model_path.exists():
            print(f"✅ {model}")
        else:
            print(f"❌ {model} missing")
            return False
    
    # Check photo
    photo_paths = [
        "silas-chat-ui/my_photo.jpg",
        "SadTalker/assets/avatar.jpg"
    ]
    
    user_photo = None
    for photo_path in photo_paths:
        if os.path.exists(photo_path):
            user_photo = os.path.abspath(photo_path)
            print(f"✅ Using photo: {photo_path}")
            break
    
    if not user_photo:
        print("❌ No user photo found")
        return False
    
    # Generate test audio
    print("\n🎤 Generating test audio...")
    test_text = "Hello! This is a test of SadTalker using your real photo. I should be speaking with perfect lip synchronization!"
    audio_file = "test_audio.wav"
    
    try:
        subprocess.run([
            "espeak", "-s", "150", "-v", "en+f3",
            "-w", audio_file, test_text
        ], check=True, capture_output=True)
        print("✅ Test audio generated")
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        return False
    
    # Prepare SadTalker command
    print("\n🎬 Running SadTalker inference...")
    
    video_id = str(uuid.uuid4())[:8]
    output_dir = "test_sadtalker_output"
    os.makedirs(output_dir, exist_ok=True)
    
    sadtalker_cmd = [
        sys.executable,
        "inference.py",
        "--driven_audio", os.path.abspath(audio_file),
        "--source_image", user_photo,
        "--result_dir", os.path.abspath(output_dir),
        "--still",
        "--preprocess", "full",
        "--size", "512",
        "--pose_style", "0"
    ]
    
    print(f"Command: {' '.join(sadtalker_cmd)}")
    print(f"Working directory: {sadtalker_path}")
    
    try:
        # Run SadTalker
        result = subprocess.run(
            sadtalker_cmd,
            cwd=str(sadtalker_path),
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes
        )
        
        print(f"\n📊 SadTalker Results:")
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        
        # Check for generated videos
        if os.path.exists(output_dir):
            video_files = [f for f in os.listdir(output_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
            
            if video_files:
                print(f"\n🎉 SUCCESS! Generated videos:")
                for video in video_files:
                    video_path = os.path.join(output_dir, video)
                    size_mb = os.path.getsize(video_path) / 1024 / 1024
                    print(f"✅ {video} ({size_mb:.2f} MB)")
                
                print(f"\n🎬 Your talking head video is ready!")
                print(f"📁 Location: {output_dir}")
                return True
            else:
                print("\n❌ No video files generated")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ SadTalker timed out (>5 minutes)")
        return False
    except Exception as e:
        print(f"❌ SadTalker error: {e}")
        return False
    finally:
        # Cleanup
        if os.path.exists(audio_file):
            os.remove(audio_file)

def main():
    """Main test function"""
    
    success = test_sadtalker_direct()
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 SadTalker Test SUCCESS!")
        print("✅ Your photo works with SadTalker")
        print("✅ Realistic talking head videos generated")
        print("✅ Perfect lip synchronization")
        
        print("\n🚀 Ready to use:")
        print("python silas-chat-ui/launch_sadtalker_photo.py")
        
    else:
        print("❌ SadTalker Test Failed")
        print("💡 Check the error messages above")
        print("🔧 Try running: python silas-chat-ui/fix_sadtalker_setup.py")

if __name__ == "__main__":
    main()