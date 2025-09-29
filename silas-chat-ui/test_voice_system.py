#!/usr/bin/env python3
"""
Voice System Test Script
Tests all voice features: TTS, Speech Recognition, and Voice Controls
"""

import webbrowser
import time
import subprocess
import sys
from pathlib import Path

def test_voice_system():
    """Test the complete voice system with D-ID style interface"""
    
    print("🎤 Testing Silas Voice System")
    print("=" * 50)
    
    # Start backend server
    print("1. Starting backend server...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/start_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        print("✅ Backend server started")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open D-ID style interface
    print("2. Opening D-ID style interface...")
    try:
        html_path = Path("silas-chat-ui/frontend/did-style.html").absolute()
        webbrowser.open(f"file://{html_path}")
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open interface: {e}")
        return False
    
    print("\n🎯 Voice System Features to Test:")
    print("=" * 50)
    
    print("📢 TTS (Text-to-Speech):")
    print("  • Send a message and listen to AI response")
    print("  • Check voice quality and clarity")
    print("  • Test pause/resume controls")
    print("  • Test stop speech control")
    
    print("\n🎤 Speech Recognition:")
    print("  • Click microphone button or press SPACE")
    print("  • Speak your message clearly")
    print("  • Watch real-time transcription")
    print("  • Message auto-sends after speech")
    
    print("\n⌨️ Keyboard Shortcuts:")
    print("  • SPACE: Toggle voice input")
    print("  • P: Pause/Resume speech")
    print("  • S: Stop speech")
    print("  • ENTER: Focus input field")
    print("  • ESC: Stop voice input")
    
    print("\n🎭 Avatar Animation:")
    print("  • Watch avatar animate while speaking")
    print("  • Check speaking status indicators")
    print("  • Verify smooth transitions")
    
    print("\n🔊 Voice Controls:")
    print("  • Pause/Resume buttons appear during speech")
    print("  • Stop button works immediately")
    print("  • Voice hints show keyboard shortcuts")
    
    print("\n🌐 Browser Compatibility:")
    print("  • Chrome/Edge: Full support")
    print("  • Firefox: TTS only (no speech recognition)")
    print("  • Safari: Limited support")
    
    print("\n" + "=" * 50)
    print("🚀 Test Instructions:")
    print("1. Wait for 'Ready' status")
    print("2. Try voice input with microphone")
    print("3. Send text messages to test TTS")
    print("4. Use keyboard shortcuts")
    print("5. Test pause/resume/stop controls")
    print("6. Check avatar animations")
    
    print("\n💡 Tips:")
    print("• Speak clearly and at normal pace")
    print("• Use Chrome for best experience")
    print("• Allow microphone permissions")
    print("• Check browser console for debug info")
    
    input("\nPress Enter when done testing...")
    
    # Cleanup
    try:
        backend_process.terminate()
        print("✅ Backend server stopped")
    except:
        pass
    
    return True

if __name__ == "__main__":
    test_voice_system()