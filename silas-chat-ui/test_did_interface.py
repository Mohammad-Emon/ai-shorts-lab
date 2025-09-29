#!/usr/bin/env python3
"""
Test D-ID Style Interface
Quick test of the complete D-ID style visual avatar interface
"""

import webbrowser
import subprocess
import time
import sys
from pathlib import Path

def test_did_interface():
    """Test the D-ID style interface"""
    
    print("🎭 Testing D-ID Style Interface")
    print("=" * 40)
    
    # Start backend (with fallback responses)
    print("🚀 Starting D-ID backend...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/sadtalker_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        print("✅ Backend started on http://127.0.0.1:8002")
        
    except Exception as e:
        print(f"❌ Backend failed: {e}")
        return
    
    # Open D-ID interface
    print("🌐 Opening D-ID style interface...")
    try:
        html_path = Path("silas-chat-ui/did_style_complete.html").absolute()
        webbrowser.open(f"file://{html_path}")
        print("✅ D-ID interface opened")
        
    except Exception as e:
        print(f"❌ Interface failed: {e}")
        backend_process.terminate()
        return
    
    print("\n🎯 D-ID Style Features to Test:")
    print("=" * 40)
    print("✅ Glassmorphism Interface: Dark liquid morphism style")
    print("✅ Side-by-Side Layout: Avatar video + chat panel")
    print("✅ Voice Input: Click microphone or press SPACE")
    print("✅ Voice Output: TTS with avatar animation")
    print("✅ AI Chat: OpenRouter LLM responses")
    print("✅ Video Controls: Pause, stop, replay buttons")
    print("✅ Keyboard Shortcuts: P=Pause, S=Stop, R=Replay")
    
    print("\n💬 Test Messages:")
    print("• 'Hello Silas, how are you?'")
    print("• 'Tell me about your video capabilities'")
    print("• 'Generate a realistic avatar video'")
    print("• 'Test your voice synthesis'")
    
    print("\n🎬 Expected Behavior:")
    print("• Messages appear in glassmorphism chat panel")
    print("• AI responds with fallback messages")
    print("• Avatar animates during speech")
    print("• Voice controls appear during TTS")
    print("• Status indicators change colors")
    
    print("\n🎨 UI Features:")
    print("• Dark glassmorphism background")
    print("• Blurred glass panels")
    print("• Smooth animations")
    print("• Professional D-ID style layout")
    print("• Responsive design")
    
    try:
        input("\nPress Enter when done testing...")
    except KeyboardInterrupt:
        pass
    
    # Cleanup
    print("\n🛑 Stopping test...")
    try:
        backend_process.terminate()
        print("✅ Backend stopped")
    except:
        pass
    
    print("✅ D-ID interface test complete!")

if __name__ == "__main__":
    test_did_interface()