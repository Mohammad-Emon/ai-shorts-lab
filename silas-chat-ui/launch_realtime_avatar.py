#!/usr/bin/env python3
"""
Launch Real-Time D-ID Style Talking Head Avatar
Creates a realistic talking head system like in the D-ID screenshots
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_realtime_avatar():
    """Launch the real-time talking head avatar system"""
    
    print("🎭 Launching Real-Time D-ID Style Talking Head")
    print("=" * 60)
    
    # Check if SadTalker backend is available
    print("🔍 Checking system components...")
    
    # Start SadTalker backend
    print("🎬 Starting SadTalker backend server...")
    
    try:
        # Start the backend in the background
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/sadtalker_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give backend time to start
        time.sleep(3)
        
        # Check if backend is running
        import requests
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=5)
            if response.status_code == 200:
                print("✅ SadTalker backend started on http://127.0.0.1:8002")
            else:
                raise Exception("Backend not responding properly")
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}")
            print("💡 Continuing anyway - system may work with fallbacks")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        print("💡 You can start it manually: python silas-chat-ui/sadtalker_backend.py")
        return False
    
    # Open the real-time talking head interface
    print("🌐 Opening real-time talking head interface...")
    
    interface_path = Path("silas-chat-ui/realtime_did_avatar.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🎯 Real-Time Talking Head Features:")
    print("=" * 50)
    print("📹 Realistic Video: SadTalker generates talking heads with moving lips")
    print("🎤 Voice Input: Click microphone or press SPACE")
    print("🔊 Voice Output: Natural TTS synchronized with video")
    print("💬 Chat Interface: D-ID style glassmorphism design")
    print("🤖 AI Brain: OpenRouter LLMs for intelligent responses")
    print("🎮 Video Controls: Pause, stop, replay realistic videos")
    
    print("\n⌨️  Keyboard Shortcuts:")
    print("• SPACE: Toggle voice input")
    print("• P: Pause/Resume video")
    print("• S: Stop video")
    print("• R: Replay video")
    
    print("\n🎬 How It Works:")
    print("1. Type or speak your message")
    print("2. AI generates intelligent response")
    print("3. SadTalker creates realistic talking head video")
    print("4. Watch avatar speak with perfect lip-sync")
    print("5. Natural facial expressions and head movements")
    
    print("\n💡 Usage Tips:")
    print("• Use Chrome or Edge for best video support")
    print("• Allow microphone permissions for voice input")
    print("• Video generation takes 10-30 seconds")
    print("• Keep messages under 80 words for optimal results")
    print("• First video may take longer to generate")
    
    print("\n🔧 Technical Features:")
    print("• Real-time video generation with SadTalker")
    print("• Perfect lip-sync matching speech audio")
    print("• Natural facial expressions and micro-movements")
    print("• HD quality output (512x512 resolution)")
    print("• Automatic fallback to TTS if video fails")
    print("• Browser autoplay restriction handling")
    
    print("\n" + "=" * 60)
    print("🎉 Real-Time D-ID Style Talking Head Ready!")
    print("Try saying: 'Hello! Show me your realistic talking head!'")
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
    
    print("👋 Real-time talking head session ended!")

if __name__ == "__main__":
    launch_realtime_avatar()