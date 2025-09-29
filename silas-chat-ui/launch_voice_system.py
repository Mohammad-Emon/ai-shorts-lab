#!/usr/bin/env python3
"""
Quick launcher for Silas Voice System
Starts backend and opens D-ID style interface with full voice capabilities
"""

import webbrowser
import subprocess
import sys
import time
from pathlib import Path

def launch_voice_system():
    """Launch the complete voice-enabled Silas system"""
    
    print("🎤 Launching Silas Voice System...")
    print("🚀 Starting backend server...")
    
    # Start backend
    try:
        backend_process = subprocess.Popen([
            sys.executable, "start_backend.py"
        ], cwd="silas-chat-ui")
        time.sleep(3)
        print("✅ Backend running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return
    
    # Open interface
    print("🌐 Opening D-ID style interface...")
    try:
        html_path = Path("silas-chat-ui/frontend/did-style.html").absolute()
        webbrowser.open(f"file://{html_path}")
        print("✅ Voice interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open interface: {e}")
        return
    
    print("\n🎯 Voice System Ready!")
    print("=" * 40)
    print("🎤 Voice Input: Click mic or press SPACE")
    print("🔊 Voice Output: AI speaks responses")
    print("⌨️  Shortcuts: P=Pause, S=Stop, ESC=Cancel")
    print("🎭 Avatar: Animates during speech")
    print("=" * 40)
    
    try:
        input("\nPress Enter to stop the system...")
    except KeyboardInterrupt:
        pass
    
    # Cleanup
    try:
        backend_process.terminate()
        print("✅ System stopped")
    except:
        pass

if __name__ == "__main__":
    launch_voice_system()