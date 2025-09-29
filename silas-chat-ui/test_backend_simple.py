#!/usr/bin/env python3
"""
Simple Backend Test
Quick test to verify the SadTalker backend is working
"""

import subprocess
import time
import sys
import requests
import json

def test_backend_simple():
    """Simple test of the backend"""
    
    print("🧪 Simple Backend Test")
    print("=" * 30)
    
    # Start backend
    print("🚀 Starting backend...")
    try:
        # Start backend in background
        backend_process = subprocess.Popen([
            sys.executable, "silas-chat-ui/sadtalker_backend.py"
        ])
        
        # Wait for startup
        print("⏳ Waiting for backend to start...")
        time.sleep(8)  # Give more time for startup
        
        # Test health endpoint
        print("🔍 Testing health endpoint...")
        try:
            response = requests.get("http://127.0.0.1:8002/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint working")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health endpoint error: {e}")
        
        # Test root endpoint
        print("🔍 Testing root endpoint...")
        try:
            response = requests.get("http://127.0.0.1:8002/", timeout=5)
            if response.status_code == 200:
                print("✅ Root endpoint working")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
        
        # Test simple avatar generation
        print("🎬 Testing simple avatar generation...")
        try:
            test_data = {
                "message": "Hello test",
                "session_id": "test123",
                "generate_video": False  # Start with no video
            }
            
            response = requests.post(
                "http://127.0.0.1:8002/generate-avatar",
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Avatar generation working")
                print(f"   Response: {result['response'][:50]}...")
            else:
                print(f"❌ Avatar generation failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Avatar generation error: {e}")
        
    except Exception as e:
        print(f"❌ Backend startup failed: {e}")
        return
    
    # Cleanup
    print("\n🛑 Stopping backend...")
    try:
        backend_process.terminate()
        backend_process.wait(timeout=5)
        print("✅ Backend stopped")
    except:
        backend_process.kill()
        print("✅ Backend killed")

if __name__ == "__main__":
    test_backend_simple()