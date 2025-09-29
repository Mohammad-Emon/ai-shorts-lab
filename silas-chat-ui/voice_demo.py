#!/usr/bin/env python3
"""
Voice System Demo Script
Demonstrates all voice features with guided tour
"""

import webbrowser
import subprocess
import sys
import time
from pathlib import Path

def voice_demo():
    """Interactive demo of voice system features"""
    
    print("🎤 Silas Voice System Demo")
    print("=" * 50)
    
    print("This demo will show you all voice features:")
    print("1. 🎤 Speech Recognition (Voice Input)")
    print("2. 🔊 Text-to-Speech (Voice Output)")
    print("3. ⌨️  Keyboard Controls")
    print("4. 🎭 Avatar Animation")
    print("5. 🎮 Voice Controls")
    
    input("\nPress Enter to start demo...")
    
    # Start system
    print("\n🚀 Starting Silas Voice System...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "start_backend.py"
        ], cwd="silas-chat-ui")
        time.sleep(3)
        
        html_path = Path("silas-chat-ui/frontend/did-style.html").absolute()
        webbrowser.open(f"file://{html_path}")
        print("✅ System launched!")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Demo steps
    print("\n🎯 Demo Steps:")
    print("=" * 30)
    
    print("\n1️⃣ VOICE INPUT TEST")
    print("   • Click the microphone button 🎤")
    print("   • Or press SPACEBAR")
    print("   • Say: 'Hello Silas, how are you?'")
    print("   • Watch real-time transcription")
    print("   • Message auto-sends after speech")
    input("   Press Enter when ready for next step...")
    
    print("\n2️⃣ VOICE OUTPUT TEST")
    print("   • Type: 'Tell me a joke'")
    print("   • Press Enter to send")
    print("   • Listen to AI voice response")
    print("   • Watch avatar animation")
    input("   Press Enter when ready for next step...")
    
    print("\n3️⃣ KEYBOARD SHORTCUTS")
    print("   • Start voice input with SPACEBAR")
    print("   • During speech: Press P to pause")
    print("   • Press P again to resume")
    print("   • Press S to stop speech")
    print("   • Press ESC to cancel voice input")
    input("   Press Enter when ready for next step...")
    
    print("\n4️⃣ VOICE CONTROLS")
    print("   • Send another message")
    print("   • Notice pause ⏸️ and stop ⏹️ buttons appear")
    print("   • Click pause to pause speech")
    print("   • Click resume to continue")
    print("   • Click stop to end speech")
    input("   Press Enter when ready for next step...")
    
    print("\n5️⃣ ADVANCED FEATURES")
    print("   • Try continuous conversation")
    print("   • Use voice input for multiple messages")
    print("   • Notice status indicators change colors")
    print("   • Watch avatar breathing animation")
    print("   • Test different voice commands")
    
    print("\n🎉 Demo Complete!")
    print("=" * 30)
    print("✅ Speech Recognition: Real-time voice input")
    print("✅ Text-to-Speech: High-quality voice output")
    print("✅ Keyboard Shortcuts: Quick voice controls")
    print("✅ Avatar Animation: Visual speech feedback")
    print("✅ Voice Controls: Pause/resume/stop speech")
    
    print("\n💡 Pro Tips:")
    print("• Use Chrome or Edge for best experience")
    print("• Allow microphone permissions")
    print("• Speak clearly at normal pace")
    print("• Use headphones to prevent feedback")
    
    input("\nPress Enter to exit demo...")
    
    # Cleanup
    try:
        backend_process.terminate()
        print("✅ Demo ended")
    except:
        pass

if __name__ == "__main__":
    voice_demo()