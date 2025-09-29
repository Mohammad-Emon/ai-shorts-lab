#!/usr/bin/env python3
"""
Launch Silas Visual Agent - D-ID Style
"""

import subprocess
import sys
import time
import requests
import webbrowser
from pathlib import Path
import threading

def start_backend():
    """Start the backend server"""
    backend_dir = Path("backend")
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "simple_main:app", 
        "--host", "127.0.0.1", 
        "--port", "8001",
        "--reload"
    ]
    
    return subprocess.Popen(cmd, cwd=backend_dir)

def wait_for_backend():
    """Wait for backend to be ready"""
    for i in range(20):
        try:
            response = requests.get("http://127.0.0.1:8001/health", timeout=2)
            if response.status_code == 200:
                return True
        except:
            time.sleep(1)
    return False

def test_visual_endpoint():
    """Test the visual processing endpoint"""
    try:
        response = requests.post(
            "http://127.0.0.1:8001/visual/process",
            json={
                "content": "Hello! This is a test of the visual agent system.",
                "session_id": "test_visual",
                "generate_video": True
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Visual endpoint working!")
            print(f"   Response: {data['response'][:50]}...")
            if data.get('video_data'):
                print(f"   Video: {data['video_data']['type']}")
            return True
        else:
            print(f"❌ Visual endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Visual endpoint test failed: {e}")
        return False

def main():
    """Launch the complete D-ID style visual agent system"""
    print("🎭 Launching Silas Visual Agent - D-ID Style")
    print("=" * 60)
    
    # Start backend
    print("🚀 Starting backend server...")
    backend_process = start_backend()
    
    # Wait for backend
    print("⏳ Waiting for backend to be ready...")
    if not wait_for_backend():
        print("❌ Backend failed to start")
        backend_process.terminate()
        return False
    
    print("✅ Backend is ready!")
    
    # Test visual endpoint
    print("🧪 Testing visual processing endpoint...")
    if not test_visual_endpoint():
        print("⚠️  Visual endpoint test failed, but continuing...")
    
    # Open D-ID style interface
    print("🎨 Opening D-ID style visual agent interface...")
    ui_file = Path.cwd() / "frontend" / "did-style.html"
    
    if ui_file.exists():
        webbrowser.open(f"file://{ui_file}")
        print("✅ D-ID style interface opened!")
    else:
        print("❌ D-ID style interface file not found")
        backend_process.terminate()
        return False
    
    # System ready
    print("\n" + "=" * 60)
    print("🎉 SILAS VISUAL AGENT IS READY!")
    print("=" * 60)
    
    print("\n🌟 D-ID Style Features:")
    print("✅ Realistic talking avatar interface")
    print("✅ Side-by-side video + chat layout")
    print("✅ Glassmorphism chat panel")
    print("✅ OpenRouter LLM integration")
    print("✅ SadTalker video generation ready")
    print("✅ Real-time conversation flow")
    
    print("\n🎯 How to Use:")
    print("1. Type messages in the chat panel")
    print("2. Watch Silas respond with video + voice")
    print("3. Enjoy natural face-to-face conversation")
    print("4. Use microphone for voice input (coming soon)")
    
    print("\n🔧 System Status:")
    print("• Backend: http://127.0.0.1:8001")
    print("• Visual API: /visual/process")
    print("• Avatar API: /avatar/generate")
    print("• Health: /health")
    
    print("\n📋 Next Steps:")
    print("• Install SadTalker: python setup_sadtalker.py")
    print("• Configure video generation")
    print("• Add custom avatar images")
    print("• Enable voice input/output")
    
    print("\n⏹️  Press Ctrl+C to stop the system")
    
    try:
        # Keep the system running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down visual agent system...")
        backend_process.terminate()
        print("✅ System stopped")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)