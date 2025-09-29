#!/usr/bin/env python3
"""
Test TTS System
Test both browser and server TTS functionality
"""

import subprocess
import sys
import time
import requests
import webbrowser
from pathlib import Path

def test_tts_system():
    """Test the complete TTS system"""
    
    print("🔊 Testing TTS System")
    print("=" * 30)
    
    # Start backend
    print("🚀 Starting backend...")
    backend_process = subprocess.Popen([
        sys.executable, "silas-chat-ui/working_sadtalker_backend.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    time.sleep(3)
    print("✅ Backend started")
    
    try:
        # Test server TTS endpoint
        print("\n🔊 Testing Server TTS...")
        
        response = requests.post(
            "http://127.0.0.1:8002/speak",
            json={"text": "Hello! This is a test of the server TTS system."},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server TTS: {data['status']}")
            print(f"📁 Audio URL: {data['audio_url']}")
        else:
            print(f"❌ Server TTS failed: {response.status_code}")
        
        # Test health endpoint
        print("\n🏥 Testing Health Check...")
        health_response = requests.get("http://127.0.0.1:8002/health", timeout=5)
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Health: {health_data['status']}")
            print(f"🔊 TTS Available: {health_data.get('talking_head_available', False)}")
            print(f"📸 Photo Available: {health_data.get('photo_available', False)}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
        
        # Open test interface
        print("\n🌐 Opening test interface...")
        interface_path = Path("silas-chat-ui/complete_working_avatar.html").absolute()
        webbrowser.open(f"file://{interface_path}")
        
        print("\n🎯 Test Instructions:")
        print("=" * 20)
        print("1. 🔊 Click the 'Speak' button (🔊)")
        print("2. 🎧 Listen for TTS audio")
        print("3. 🔄 If browser TTS fails, server TTS will try")
        print("4. ✍️ Type a message and press Enter")
        print("5. 🎭 Test video generation")
        
        print("\n✅ TTS System Test Complete!")
        print("The interface is now open - try the TTS button!")
        
        input("\nPress Enter to stop the test...")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        print("\n🛑 Stopping backend...")
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

if __name__ == "__main__":
    test_tts_system()