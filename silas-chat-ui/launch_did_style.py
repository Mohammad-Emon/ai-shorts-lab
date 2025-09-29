#!/usr/bin/env python3
"""
Launch D-ID Style Visual Avatar System
Complete realistic talking head avatar with SadTalker + OpenRouter
"""

import subprocess
import webbrowser
import time
import sys
import os
from pathlib import Path

def check_system_ready():
    """Check if system components are ready"""
    
    print("🔍 Checking system components...")
    
    # Check SadTalker
    sadtalker_path = Path("SadTalker")
    if not sadtalker_path.exists():
        print("❌ SadTalker not found")
        print("💡 Run: python silas-chat-ui/setup_did_style.py")
        return False
    
    # Check avatar image
    avatar_path = sadtalker_path / "assets" / "avatar.jpg"
    if not avatar_path.exists():
        print("⚠️  Avatar image missing - video generation may fail")
        print("💡 Add avatar image to SadTalker/assets/avatar.jpg")
    
    # Check backend files
    required_files = [
        "silas-chat-ui/did_style_complete.html",
        "silas-chat-ui/sadtalker_backend.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ {file_path} missing")
            return False
    
    print("✅ System components ready")
    return True

def launch_did_style_avatar():
    """Launch the complete D-ID style avatar system"""
    
    print("🎭 Launching D-ID Style Visual Avatar")
    print("=" * 50)
    
    # Check system readiness
    if not check_system_ready():
        print("❌ System not ready - run setup first")
        return
    
    # Load environment variables
    env_file = Path("silas-chat-ui/.env")
    if env_file.exists():
        print("📄 Loading environment configuration...")
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Start SadTalker backend
    print("🎬 Starting SadTalker backend server...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/sadtalker_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(5)
        print("✅ SadTalker backend started on http://127.0.0.1:8002")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return
    
    # Open D-ID style interface
    print("🌐 Opening D-ID style interface...")
    try:
        html_path = Path("silas-chat-ui/did_style_complete.html").absolute()
        webbrowser.open(f"file://{html_path}")
        print("✅ Interface opened in browser")
        
    except Exception as e:
        print(f"❌ Failed to open interface: {e}")
        backend_process.terminate()
        return
    
    print("\n🎯 D-ID Style Avatar Features:")
    print("=" * 40)
    print("📹 Realistic Video: SadTalker lip-sync generation")
    print("🎤 Voice Input: Click microphone or press SPACE")
    print("🔊 Voice Output: Natural TTS with video sync")
    print("💬 Chat Interface: Glassmorphism D-ID style")
    print("🤖 AI Brain: Free OpenRouter LLMs")
    print("🎮 Video Controls: Pause, stop, replay videos")
    
    print("\n⌨️  Keyboard Shortcuts:")
    print("• SPACE: Toggle voice input")
    print("• P: Pause/Resume video")
    print("• S: Stop video")
    print("• R: Replay video")
    
    print("\n🎬 Video Generation:")
    print("• Realistic lip-sync with SadTalker")
    print("• Natural facial expressions")
    print("• HD quality output")
    print("• Automatic audio synchronization")
    
    print("\n💡 Usage Tips:")
    print("• Use Chrome or Edge for best experience")
    print("• Allow microphone permissions")
    print("• Video generation takes 10-30 seconds")
    print("• Keep messages under 80 words for best results")
    print("• First video generation may take longer")
    
    print("\n🔧 Technical Stack:")
    print("• Frontend: D-ID style HTML/CSS/JS")
    print("• Backend: FastAPI with SadTalker integration")
    print("• Video: SadTalker realistic talking heads")
    print("• AI: OpenRouter free LLM models")
    print("• Voice: Web Speech API + TTS")
    
    print("\n" + "=" * 50)
    print("🎉 D-ID Style Avatar System Ready!")
    print("Try saying: 'Hello Silas, generate a video for me!'")
    
    try:
        input("\nPress Enter to stop the system...")
    except KeyboardInterrupt:
        pass
    
    # Cleanup
    print("\n🛑 Stopping system...")
    try:
        backend_process.terminate()
        print("✅ Backend stopped")
    except:
        pass
    
    print("👋 D-ID Style Avatar session ended!")

def show_system_status():
    """Show current system status"""
    
    print("📊 D-ID Style Avatar System Status")
    print("=" * 40)
    
    # Check SadTalker
    sadtalker_path = Path("SadTalker")
    print(f"SadTalker: {'✅ Ready' if sadtalker_path.exists() else '❌ Not found'}")
    
    # Check avatar image
    avatar_path = sadtalker_path / "assets" / "avatar.jpg"
    print(f"Avatar Image: {'✅ Ready' if avatar_path.exists() else '❌ Missing'}")
    
    # Check OpenRouter
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"OpenRouter API: {'✅ Configured' if api_key else '⚠️  Not configured'}")
    
    # Check system dependencies
    deps = ["ffmpeg", "git"]
    for dep in deps:
        try:
            subprocess.run([dep, "--version"], 
                         capture_output=True, check=True)
            print(f"{dep}: ✅ Available")
        except:
            print(f"{dep}: ⚠️  Not found")
    
    # Check Python packages
    try:
        import torch, cv2, fastapi
        print("Python Deps: ✅ Ready")
    except ImportError:
        print("Python Deps: ❌ Missing packages")
    
    print("\n💡 If any components show errors:")
    print("Run: python silas-chat-ui/setup_did_style.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_system_status()
    else:
        launch_did_style_avatar()