#!/usr/bin/env python3
"""
Launch D-ID + Wav2Lip Avatar System
Real talking head videos using D-ID API or Wav2Lip
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_did_wav2lip_system():
    """Launch the D-ID + Wav2Lip avatar system"""
    
    print("🎭 Launching D-ID + Wav2Lip Avatar System")
    print("=" * 50)
    
    # Check setup
    did_key = os.getenv("DID_API_KEY")
    wav2lip_available = Path("Wav2Lip").exists()
    
    print("🔍 System Status:")
    print(f"D-ID API: {'✅ Configured' if did_key else '❌ Not configured'}")
    print(f"Wav2Lip: {'✅ Available' if wav2lip_available else '❌ Not installed'}")
    
    if not did_key and not wav2lip_available:
        print("⚠️  No video generation methods available!")
        print("Run: python silas-chat-ui/setup_did_wav2lip.py")
        return False
    
    # Start backend
    print("\n🎬 Starting D-ID + Wav2Lip backend...")
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/did_wav2lip_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        # Check if backend is running
        import requests
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend started on http://127.0.0.1:8002")
                print(f"D-ID API: {'✅' if data.get('did_api_available') else '❌'}")
                print(f"Wav2Lip: {'✅' if data.get('wav2lip_available') else '❌'}")
            else:
                raise Exception("Backend not responding")
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open interface
    print("\n🌐 Opening avatar interface...")
    
    interface_path = Path("silas-chat-ui/realtime_did_avatar.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🎯 D-ID + Wav2Lip Features:")
    print("=" * 40)
    print("🎭 D-ID API: Professional quality talking heads")
    print("🎬 Wav2Lip: Local lip-sync processing")
    print("📸 Uses your real photo for avatar")
    print("🤖 Smart AI responses with Gemini/Groq")
    print("🎮 Full video controls and interface")
    
    print("\n💡 How It Works:")
    print("1. Type your message")
    print("2. AI generates smart response")
    print("3. D-ID API or Wav2Lip creates video")
    print("4. Watch your real face speak!")
    
    print("\n" + "=" * 50)
    print("🎉 D-ID + Wav2Lip Avatar System Ready!")
    print("Try: 'Generate a video with my real face!'")
    
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
    
    print("👋 D-ID + Wav2Lip session ended!")
    return True

if __name__ == "__main__":
    launch_did_wav2lip_system()
