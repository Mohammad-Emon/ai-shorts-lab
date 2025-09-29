#!/usr/bin/env python3
"""
Run the complete Silas Chat UI system with backend integration
"""

import subprocess
import sys
import time
import requests
import webbrowser
from pathlib import Path
import threading

def start_backend():
    """Start the backend server in a separate thread"""
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

def test_backend():
    """Test backend functionality"""
    try:
        # Test health
        health = requests.get("http://127.0.0.1:8001/health", timeout=5)
        print(f"✅ Health check: {health.status_code}")
        
        # Test message
        message_response = requests.post(
            "http://127.0.0.1:8001/message",
            json={
                "content": "Test multi-agent system",
                "session_id": "test_session",
                "use_multi_agent": True
            },
            timeout=10
        )
        
        if message_response.status_code == 200:
            data = message_response.json()
            print(f"✅ Message API: {data['workflow_type']} workflow")
            return True
        else:
            print(f"❌ Message API failed: {message_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def main():
    """Main function to run the complete system"""
    print("🤖 Silas Chat UI - Complete System Startup")
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
    
    # Test backend
    print("🧪 Testing backend functionality...")
    if not test_backend():
        print("❌ Backend tests failed")
        backend_process.terminate()
        return False
    
    # Open frontend
    print("🎨 Opening frontend...")
    frontend_file = Path.cwd() / "frontend" / "test-elevenlabs.html"
    
    if frontend_file.exists():
        webbrowser.open(f"file://{frontend_file}")
        print("✅ Frontend opened!")
    else:
        print("❌ Frontend file not found")
        backend_process.terminate()
        return False
    
    # System ready
    print("\n" + "=" * 60)
    print("🎉 SILAS CHAT UI SYSTEM IS READY!")
    print("=" * 60)
    
    print("\n🌟 System Status:")
    print("✅ Backend: Running on http://127.0.0.1:8001")
    print("✅ Frontend: ElevenLabs-style interface opened")
    print("✅ Multi-Agent: Ready for complex queries")
    print("✅ API Integration: Frontend ↔ Backend connected")
    
    print("\n🎯 How to Use:")
    print("1. Click the blue orb in your browser")
    print("2. Click 'Start Chat' to begin")
    print("3. Type messages - they'll be processed by the backend")
    print("4. See multi-agent workflow indicators")
    print("5. Enjoy the glassmorphism chat experience!")
    
    print("\n🔧 API Endpoints:")
    print("• Health: http://127.0.0.1:8001/health")
    print("• Docs: http://127.0.0.1:8001/docs")
    print("• Message: POST http://127.0.0.1:8001/message")
    
    print("\n⏹️  Press Ctrl+C to stop the system")
    
    try:
        # Keep the system running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")
        backend_process.terminate()
        print("✅ System stopped")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)