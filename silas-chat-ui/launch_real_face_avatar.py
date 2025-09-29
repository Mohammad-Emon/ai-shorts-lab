#!/usr/bin/env python3
"""
Launch Real Face Avatar System
Uses your actual photo instead of cartoon avatars
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_user_photo():
    """Check if user photo is available"""
    
    photo_paths = [
        "silas-chat-ui/my_photo.jpg",
        "SadTalker/assets/avatar.jpg",
        "my_photo.jpg"
    ]
    
    for photo_path in photo_paths:
        if os.path.exists(photo_path):
            print(f"✅ Found user photo: {photo_path}")
            return True
    
    print("📸 User photo setup needed:")
    print("1. Save your photo as 'silas-chat-ui/my_photo.jpg'")
    print("2. Use a clear front-facing photo")
    print("3. Ensure good lighting and face visibility")
    print("4. Photo should be at least 256x256 pixels")
    
    return False

def launch_real_face_system():
    """Launch the real face avatar system"""
    
    print("🎭 Launching Real Face Avatar System")
    print("=" * 50)
    
    # Check photo availability
    photo_available = check_user_photo()
    
    if not photo_available:
        print("\n⚠️  No user photo found!")
        print("Please save your photo as 'silas-chat-ui/my_photo.jpg' first")
        
        response = input("\nContinue anyway? (y/n): ").lower()
        if response != 'y':
            return False
    
    # Start real SadTalker backend
    print("\n🎬 Starting Real Face SadTalker backend...")
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/real_sadtalker_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give backend time to start
        time.sleep(3)
        
        # Check if backend is running
        import requests
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Real Face backend started on http://127.0.0.1:8002")
                print(f"📸 User photo available: {data.get('user_photo_available', False)}")
                print(f"🎭 SadTalker available: {data.get('sadtalker_available', False)}")
            else:
                raise Exception("Backend not responding properly")
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}")
            print("💡 Continuing anyway...")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open the real-time interface
    print("\n🌐 Opening real face avatar interface...")
    
    interface_path = Path("silas-chat-ui/realtime_did_avatar.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🎯 Real Face Avatar Features:")
    print("=" * 40)
    print("📸 Uses YOUR actual photo for talking head")
    print("🎭 Real face lip-sync with SadTalker")
    print("🎤 Voice input and natural TTS output")
    print("💬 D-ID style glassmorphism interface")
    print("🎮 Full video controls (pause, stop, replay)")
    
    print("\n💡 How It Works:")
    print("1. Your photo is processed by SadTalker")
    print("2. AI generates intelligent responses")
    print("3. Real talking head video created with your face")
    print("4. Perfect lip-sync with natural expressions")
    print("5. No more cartoon avatars - just your real face!")
    
    print("\n🔧 Technical Features:")
    print("• Real face processing with SadTalker")
    print("• Perfect lip synchronization")
    print("• Natural facial expressions")
    print("• HD video output (512x512)")
    print("• Fallback responses (no API rate limits)")
    print("• Browser autoplay handling")
    
    print("\n" + "=" * 50)
    print("🎉 Real Face Avatar System Ready!")
    print("Try saying: 'Generate a video with my real face!'")
    
    if not photo_available:
        print("\n📸 To use your real face:")
        print("1. Save your photo as 'silas-chat-ui/my_photo.jpg'")
        print("2. Restart the system")
        print("3. Watch your actual face speak!")
    
    print("\nPress Enter to stop the system...")
    
    try:
        input()
    except KeyboardInterrupt:
        pass
    
    print("\n🛑 Stopping system...")
    
    # Stop backend
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
    
    print("👋 Real face avatar session ended!")
    return True

if __name__ == "__main__":
    launch_real_face_system()