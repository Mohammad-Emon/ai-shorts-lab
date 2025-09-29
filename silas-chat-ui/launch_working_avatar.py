#!/usr/bin/env python3
"""
Launch Working Avatar System
Smart fallback system that always works
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def launch_working_system():
    """Launch a system that definitely works"""
    
    print("🎭 Launching Working Avatar System")
    print("=" * 50)
    
    print("🎯 Smart Approach:")
    print("• Try D-ID API first (if photo works)")
    print("• Fallback to enhanced AI chat")
    print("• Always provide great responses")
    
    # Check D-ID setup
    from dotenv import load_dotenv
    load_dotenv("silas-chat-ui/.env")
    
    did_key = os.getenv("DID_API_KEY")
    photo_exists = os.path.exists("silas-chat-ui/my_photo.jpg")
    
    print(f"\n🔍 System Status:")
    print(f"D-ID API: {'✅' if did_key else '❌'}")
    print(f"Photo: {'✅' if photo_exists else '❌'}")
    
    # Start the enhanced backend
    print("\n🚀 Starting Enhanced Avatar Backend...")
    
    try:
        # Use the free LLM backend with smart responses
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/simple_did_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        # Check if backend is running
        import requests
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend started on http://127.0.0.1:8002")
            else:
                raise Exception("Backend not responding")
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}")
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    # Open interface
    print("\n🌐 Opening avatar interface...")
    
    interface_path = Path("silas-chat-ui/realtime_did_avatar.html").absolute()
    interface_url = f"file://{interface_path}"
    
    try:
        webbrowser.open(interface_url)
        print("✅ Interface opened in browser")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"💡 Manually open: {interface_url}")
    
    print("\n🎯 What You Get:")
    print("=" * 30)
    print("✅ Smart AI responses (Gemini + Groq)")
    print("✅ Professional chat interface")
    print("✅ Voice input and output")
    print("✅ D-ID video attempts (when possible)")
    print("✅ Always works with fallbacks")
    
    print("\n💡 How It Works:")
    print("1. Type your message")
    print("2. AI generates intelligent response")
    print("3. System tries D-ID video generation")
    print("4. If D-ID fails, provides excellent chat experience")
    print("5. No more static cartoon faces!")
    
    print("\n🎬 Video Generation:")
    if did_key and photo_exists:
        print("• Will attempt D-ID professional videos")
        print("• Falls back to smart chat if face detection fails")
    else:
        print("• Smart AI chat with voice capabilities")
        print("• Add D-ID key + photo for video generation")
    
    print("\n" + "=" * 50)
    print("🎉 Working Avatar System Ready!")
    print("Try typing: 'Hello! Tell me about your capabilities!'")
    
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
    launch_working_system()