#!/usr/bin/env python3
"""
Launch Avatar with Lip-Sync Animation
Visual lip-sync animation while TTS is speaking
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_lipsync_avatar():
    """Launch avatar with visual lip-sync animation"""
    
    print("👄 Launching Avatar with Lip-Sync Animation")
    print("=" * 50)
    
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
    
    # Open lip-sync interface
    print("🌐 Opening avatar with lip-sync animation...")
    
    interface_path = Path("silas-chat-ui/avatar_with_lipsync.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n👄 Lip-Sync Features:")
    print("=" * 30)
    print("✅ Visual mouth movement animation")
    print("✅ Eye blinking effects")
    print("✅ Speaking glow and pulse effects")
    print("✅ Synchronized with TTS speech")
    print("✅ Your real photo as avatar")
    print("✅ Professional talking head look")
    
    print("\n💡 How It Works:")
    print("1. Type your message")
    print("2. AI responds with intelligent text")
    print("3. TTS speaks the response aloud")
    print("4. Visual lip-sync animation plays")
    print("5. Mouth moves, eyes blink, avatar glows")
    print("6. Looks like real talking head!")
    
    print("\n🎯 Visual Effects:")
    print("👄 Mouth animation - Opens/closes with speech")
    print("👁️ Eye blinking - Natural blinking pattern")
    print("✨ Speaking glow - Blue border when talking")
    print("📏 Scaling effect - Slight size increase")
    print("🎵 Synchronized - All effects match TTS timing")
    
    print("\n" + "=" * 50)
    print("🎉 Avatar with Lip-Sync Ready!")
    print("Try typing: 'Hello! Please show me your lip-sync animation!'")
    
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
    
    print("👋 Lip-sync avatar session ended!")
    return True

if __name__ == "__main__":
    launch_lipsync_avatar()