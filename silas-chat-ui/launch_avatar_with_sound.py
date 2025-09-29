#!/usr/bin/env python3
"""
Launch Avatar with Sound
D-ID style avatar with working text-to-speech
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_avatar_with_sound():
    """Launch avatar system with working audio"""
    
    print("🔊 Launching Avatar with Sound")
    print("=" * 40)
    
    # Start backend
    print("🚀 Starting backend...")
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/simple_did_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        # Check backend
        import requests
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend ready on http://127.0.0.1:8002")
            else:
                raise Exception("Backend not responding")
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open interface with sound
    print("🌐 Opening avatar interface with sound...")
    
    interface_path = Path("silas-chat-ui/avatar_with_sound.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🔊 Sound Features:")
    print("=" * 30)
    print("✅ Text-to-Speech for all responses")
    print("✅ Visual speaking animation")
    print("✅ Voice controls (enable/disable)")
    print("✅ Natural voice synthesis")
    print("✅ Speaking status indicators")
    
    print("\n💡 How to Use:")
    print("1. Type your message")
    print("2. AI responds with text")
    print("3. Avatar speaks the response aloud")
    print("4. Visual animation shows speaking")
    print("5. Use 🔊 button to toggle sound")
    
    print("\n🎯 Controls:")
    print("🔊 - Toggle speech on/off")
    print("⏹️ - Stop current speech")
    print("🎤 - Voice input (future feature)")
    
    print("\n" + "=" * 40)
    print("🎉 Avatar with Sound Ready!")
    print("Try typing: 'Hello! Please speak this message!'")
    
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
    
    print("👋 Avatar session ended!")
    return True

if __name__ == "__main__":
    launch_avatar_with_sound()