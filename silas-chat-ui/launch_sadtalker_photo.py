#!/usr/bin/env python3
"""
Launch SadTalker with Your Photo
Real talking head videos using your actual photo
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_sadtalker_with_photo():
    """Launch SadTalker system with user photo"""
    
    print("🎭 Launching SadTalker with Your Photo")
    print("=" * 50)
    
    # Check SadTalker setup
    sadtalker_path = Path("SadTalker")
    models_available = all([
        (sadtalker_path / "checkpoints/mapping_00109-model.pth.tar").exists(),
        (sadtalker_path / "checkpoints/facevid2vid_00189-model.pth.tar").exists()
    ])
    
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
    print(f"SadTalker Models: {'✅ Available' if models_available else '❌ Missing'}")
    print(f"Your Photo: {'✅ Found' if user_photo else '❌ Missing'}")
    
    if not models_available:
        print("\n⚠️  SadTalker models missing!")
        print("Run: python silas-chat-ui/fix_sadtalker_setup.py")
        return False
    
    if not user_photo:
        print("\n📸 Photo needed:")
        print("Save your photo as 'silas-chat-ui/my_photo.jpg'")
        return False
    
    # Start SadTalker backend
    print("\n🎬 Starting SadTalker backend with your photo...")
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/sadtalker_with_photo.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)  # SadTalker needs more time to load
        
        # Check backend
        import requests
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("✅ SadTalker backend ready on http://127.0.0.1:8002")
                print(f"Models: {'✅' if data.get('sadtalker_available') else '❌'}")
                print(f"Photo: {'✅' if data.get('photo_available') else '❌'}")
            else:
                raise Exception("Backend not responding")
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open interface
    print("\n🌐 Opening SadTalker interface...")
    
    interface_path = Path("silas-chat-ui/realtime_did_avatar.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🎭 SadTalker Features:")
    print("=" * 30)
    print("✅ Real talking head videos with your photo")
    print("✅ Perfect lip synchronization")
    print("✅ Natural facial expressions")
    print("✅ Head movements and micro-expressions")
    print("✅ High-quality video output")
    print("✅ Local processing (no API costs)")
    
    print("\n💡 How It Works:")
    print("1. Type your message")
    print("2. AI generates intelligent response")
    print("3. SadTalker creates TTS audio")
    print("4. SadTalker generates video with your face")
    print("5. Perfect lip-sync with natural expressions")
    print("6. Real talking head video plays!")
    
    print("\n🎬 Video Generation:")
    print(f"📸 Using photo: {user_photo}")
    print("🎭 SadTalker AI processing")
    print("👄 Perfect lip synchronization")
    print("😊 Natural facial expressions")
    print("📹 HD video output (512x512)")
    
    print("\n" + "=" * 50)
    print("🎉 SadTalker with Your Photo Ready!")
    print("Try typing: 'Generate a realistic video with my face!'")
    
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
    
    print("👋 SadTalker session ended!")
    return True

if __name__ == "__main__":
    launch_sadtalker_with_photo()