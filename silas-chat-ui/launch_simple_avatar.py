#!/usr/bin/env python3
"""
Launch Simple Talking Avatar System
Complete voice-enabled AI avatar with OpenRouter integration
"""

import subprocess
import webbrowser
import time
import sys
from pathlib import Path

def launch_talking_avatar():
    """Launch the complete talking avatar system"""
    
    print("🎭 Launching Silas Talking Avatar System")
    print("=" * 50)
    
    # Start backend
    print("🚀 Starting backend server...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/simple_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        print("✅ Backend server started on http://127.0.0.1:8001")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return
    
    # Open frontend
    print("🌐 Opening talking avatar interface...")
    try:
        html_path = Path("silas-chat-ui/simple_talking_avatar.html").absolute()
        webbrowser.open(f"file://{html_path}")
        print("✅ Interface opened in browser")
        
    except Exception as e:
        print(f"❌ Failed to open interface: {e}")
        backend_process.terminate()
        return
    
    print("\n🎯 Talking Avatar Features:")
    print("=" * 30)
    print("🎤 Voice Input: Click microphone or press SPACE")
    print("🔊 Voice Output: AI speaks all responses")
    print("💬 Text Chat: Type messages normally")
    print("⌨️  Shortcuts: SPACE=Voice, P=Pause, S=Stop")
    print("🤖 AI Brain: Free OpenRouter LLMs")
    print("🎭 Avatar: Animated visual feedback")
    
    print("\n💡 Usage Tips:")
    print("• Use Chrome or Edge for best voice support")
    print("• Allow microphone permissions when prompted")
    print("• Voice input auto-sends messages")
    print("• Pause/resume speech with P key")
    print("• Stop speech anytime with S key")
    
    print("\n🔧 Technical Info:")
    print("• Backend: FastAPI with OpenRouter integration")
    print("• Frontend: Pure HTML/CSS/JS with Web Speech API")
    print("• Voice: Browser native TTS and speech recognition")
    print("• AI: Free Llama 3.2, Phi-3, Gemma models")
    
    try:
        input("\n🎉 System ready! Press Enter to stop...")
    except KeyboardInterrupt:
        pass
    
    # Cleanup
    print("\n🛑 Stopping system...")
    try:
        backend_process.terminate()
        print("✅ Backend stopped")
    except:
        pass
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    launch_talking_avatar()