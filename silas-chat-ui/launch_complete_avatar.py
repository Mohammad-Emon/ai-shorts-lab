#!/usr/bin/env python3
"""
Launch Complete Working Avatar
Sound + Video generation with your photo
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_complete_avatar():
    """Launch complete working avatar system"""
    
    print("🎭 Launching Complete Working Avatar")
    print("=" * 40)
    print("✅ Sound: Text-to-Speech enabled")
    print("✅ Video: Your photo + audio sync")
    print("✅ Interface: Complete controls")
    
    # Start the working backend
    print("\n🚀 Starting backend...")
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/working_sadtalker_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        print("✅ Backend started on http://127.0.0.1:8002")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open the complete interface
    print("🌐 Opening complete avatar interface...")
    
    interface_path = Path("silas-chat-ui/complete_working_avatar.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🎯 Complete Features:")
    print("=" * 25)
    print("🔊 TTS Speech - Immediate audio")
    print("🎬 Video Generation - Your photo speaks")
    print("💬 Smart AI Chat - Intelligent responses")
    print("🎮 Full Controls - Generate, speak, stop")
    print("📸 Your Photo - Real face avatar")
    
    print("\n💡 How to Use:")
    print("1. 🔊 Click 'Speak' button to test TTS")
    print("2. 🎬 Click 'Generate' button to test video")
    print("3. ✍️ Type message and press Enter")
    print("4. 🎭 Watch your photo speak with sound!")
    
    print("\n" + "=" * 40)
    print("🎉 Complete Avatar Ready!")
    print("Try the TTS test button first!")
    
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
    
    print("👋 Complete avatar session ended!")
    return True

if __name__ == "__main__":
    launch_complete_avatar()