#!/usr/bin/env python3
"""
Start the Silas Chat UI Backend
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def start_backend():
    """Start the backend server"""
    print("🚀 Starting Silas Chat UI Backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    try:
        # Start the backend server
        print("📡 Starting server on http://127.0.0.1:8001")
        
        # Use uvicorn directly
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "simple_main:app", 
            "--host", "127.0.0.1", 
            "--port", "8001",
            "--reload"
        ]
        
        process = subprocess.Popen(cmd, cwd=backend_dir)
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(15):
            try:
                response = requests.get("http://127.0.0.1:8001/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend server is running!")
                    print("   Health: http://127.0.0.1:8001/health")
                    print("   API Docs: http://127.0.0.1:8001/docs")
                    print("   Test Message: http://127.0.0.1:8001/")
                    
                    # Test the message endpoint
                    try:
                        test_response = requests.post(
                            "http://127.0.0.1:8001/message",
                            json={
                                "content": "Hello backend!",
                                "session_id": "test_session",
                                "use_multi_agent": False
                            },
                            timeout=5
                        )
                        if test_response.status_code == 200:
                            print("✅ Message endpoint working!")
                        else:
                            print("⚠️  Message endpoint issue")
                    except:
                        print("⚠️  Message endpoint not responding")
                    
                    print("\n🎨 Frontend ready at:")
                    print("   file://" + str(Path.cwd() / "frontend" / "test-elevenlabs.html"))
                    
                    return process
            except:
                time.sleep(1)
        
        print("❌ Backend server failed to start")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

if __name__ == "__main__":
    process = start_backend()
    if process:
        try:
            print("\n⏹️  Press Ctrl+C to stop the server")
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping backend server...")
            process.terminate()
            print("✅ Backend stopped")
    else:
        print("❌ Failed to start backend")
        sys.exit(1)