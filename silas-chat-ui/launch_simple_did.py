#!/usr/bin/env python3
"""
Launch Simple D-ID Avatar System
Professional talking head videos using D-ID API
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_simple_did_system():
    """Launch the simple D-ID avatar system"""
    
    print("🎭 Launching Simple D-ID Avatar System")
    print("=" * 50)
    
    # Check D-ID API key
    from dotenv import load_dotenv
    load_dotenv("silas-chat-ui/.env")
    
    did_key = os.getenv("DID_API_KEY")
    
    print("🔍 System Status:")
    print(f"D-ID API: {'✅ Configured' if did_key else '❌ Not configured'}")
    
    if not did_key:
        print("\n⚠️  D-ID API key required!")
        print("1. Get your free key at: https://studio.d-id.com/account-settings")
        print("2. Add it to silas-chat-ui/.env as: DID_API_KEY=your_key_here")
        print("3. Run this script again")
        return False
    
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
    
    print(f"📸 User Photo: {'✅ Found' if user_photo else '❌ Missing'}")
    
    if not user_photo:
        print("\n📸 Photo Setup Needed:")
        print("1. Save your photo as 'silas-chat-ui/my_photo.jpg'")
        print("2. Use a clear front-facing photo")
        print("3. Restart this system")
        
        response = input("\nContinue anyway? (y/n): ").lower()
        if response != 'y':
            return False
    
    # Start D-ID backend
    print("\n🎬 Starting D-ID backend...")
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/simple_did_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        # Check if backend is running
        import requests
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ D-ID backend started on http://127.0.0.1:8002")
                print(f"API Status: {'✅ Ready' if data.get('did_api_available') else '❌ Not configured'}")
            else:
                raise Exception("Backend not responding")
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open interface
    print("\n🌐 Opening D-ID avatar interface...")
    
    interface_path = Path("silas-chat-ui/realtime_did_avatar.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🎯 D-ID Avatar Features:")
    print("=" * 40)
    print("🎭 Professional D-ID talking head videos")
    print("📸 Uses your real photo for avatar")
    print("🤖 Smart AI responses (Gemini + Groq)")
    print("💬 D-ID style glassmorphism interface")
    print("🎮 Full video controls and playback")
    
    print("\n💡 How It Works:")
    print("1. Type your message in the chat")
    print("2. AI generates intelligent response")
    print("3. D-ID API creates professional talking head video")
    print("4. Watch your real face speak with perfect lip-sync!")
    print("5. No more static images - real video generation!")
    
    print("\n🎬 D-ID Quality:")
    print("• Broadcast-quality talking head videos")
    print("• Perfect lip synchronization")
    print("• Natural facial expressions")
    print("• Professional studio results")
    print("• Used by major content creators")
    
    print("\n" + "=" * 50)
    print("🎉 D-ID Avatar System Ready!")
    print("Try: 'Generate a professional talking head video!'")
    
    if user_photo:
        print(f"📸 Using your photo: {user_photo}")
    else:
        print("📸 Add your photo for video generation")
    
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
    
    print("👋 D-ID avatar session ended!")
    return True

if __name__ == "__main__":
    launch_simple_did_system()