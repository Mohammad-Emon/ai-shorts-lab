#!/usr/bin/env python3
"""
Launch Working SadTalker System
Talking head videos using your actual photo
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_working_sadtalker():
    """Launch working talking head system with user photo"""
    
    print("🎭 Launching Working Talking Head System")
    print("=" * 50)
    
    # Check photo
    photo_paths = [
        "silas-chat-ui/my_photo.jpg",
        "SadTalker/assets/avatar.jpg"
    ]
    
    user_photo = None
    for photo_path in photo_paths:
        if os.path.exists(photo_path):
            user_photo = photo_path
            break
    
    print("🔍 System Status:")
    print(f"Your Photo: {'✅ Found' if user_photo else '❌ Missing'}")
    
    # Check dependencies
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("FFmpeg: ✅ Available")
    except:
        print("FFmpeg: ❌ Missing")
    
    try:
        subprocess.run(["espeak", "--version"], capture_output=True, check=True)
        print("Espeak: ✅ Available")
    except:
        print("Espeak: ❌ Missing")
    
    if not user_photo:
        print("\n📸 Photo needed:")
        print("Save your photo as 'silas-chat-ui/my_photo.jpg'")
        return False
    
    # Start backend
    print("\n🎬 Starting talking head backend...")
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/working_sadtalker_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        # Check backend
        import requests
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend ready on http://127.0.0.1:8002")
                print(f"Video Generation: {'✅' if data.get('talking_head_available') else '❌'}")
                print(f"Photo Available: {'✅' if data.get('photo_available') else '❌'}")
            else:
                raise Exception("Backend not responding")
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open interface
    print("\n🌐 Opening talking head interface...")
    
    interface_path = Path("silas-chat-ui/realtime_did_avatar.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🎭 Talking Head Features:")
    print("=" * 30)
    print("✅ Your real photo as talking head")
    print("✅ Synchronized audio with video")
    print("✅ Natural speech timing")
    print("✅ HD video output (512x512)")
    print("✅ Local processing (no API costs)")
    print("✅ Works with any photo")
    
    print("\n💡 How It Works:")
    print("1. Type your message")
    print("2. AI generates intelligent response")
    print("3. System creates TTS audio")
    print("4. FFmpeg generates video with your photo")
    print("5. Audio and video perfectly synchronized")
    print("6. Your photo appears to be speaking!")
    
    print("\n🎬 Video Generation:")
    print(f"📸 Using photo: {user_photo}")
    print("🎤 TTS audio generation")
    print("🎬 FFmpeg video creation")
    print("🔄 Audio-video synchronization")
    print("📹 HD output with your face")
    
    print("\n" + "=" * 50)
    print("🎉 Working Talking Head System Ready!")
    print("Try typing: 'Create a video where I speak this message!'")
    
    print("\nPress Enter to stop the system...")
    
    try:
        input()
    except KeyboardInterrupt:
        pass
    
    print("\n🛑 Stopping system...")
    
    try:
        backend_process.terminate()
        backend_process.wait(timeout=5)
        print("✅ Backend stopped")
    except:
        try:
            backend_process.kill()
            print("✅ Backend force stopped")
        except:
            print("⚠️  Backend may still be running")
    
    print("👋 Talking head session ended!")
    return True

if __name__ == "__main__":
    launch_working_sadtalker()