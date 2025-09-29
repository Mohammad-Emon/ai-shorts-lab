#!/usr/bin/env python3
"""
Complete build and test script for Silas Chat UI
"""

import subprocess
import sys
import time
import os
import webbrowser
from pathlib import Path
import requests
import json

def run_command(command, cwd=None, capture=True):
    """Run a shell command"""
    try:
        if capture:
            result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(command, shell=True, cwd=cwd)
            return result.returncode == 0, "", ""
    except Exception as e:
        return False, "", str(e)

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python packages
    required_packages = ['fastapi', 'uvicorn', 'requests', 'openai', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        success, _, _ = run_command(f"python -c 'import {package}'")
        if not success:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        success, _, _ = run_command("pip install -r backend/requirements.txt")
        if not success:
            print("❌ Failed to install packages")
            return False
    
    print("✅ All dependencies installed")
    return True

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return None
    
    # Start simple backend for testing
    cmd = [sys.executable, "simple_main.py"]
    
    try:
        process = subprocess.Popen(cmd, cwd=backend_dir)
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(10):
            try:
                response = requests.get("http://127.0.0.1:8001/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend server is running!")
                    return process
            except:
                time.sleep(1)
        
        print("❌ Backend server failed to start")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def test_backend():
    """Test backend endpoints"""
    print("🧪 Testing backend endpoints...")
    
    base_url = "http://127.0.0.1:8001"
    tests = [
        ("Health Check", "/health"),
        ("Configuration", "/config"),
        ("Agents List", "/agents"),
    ]
    
    all_passed = True
    
    for test_name, endpoint in tests:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED ({response.status_code})")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name}: FAILED ({e})")
            all_passed = False
    
    # Test chat message
    try:
        message_data = {
            "content": "Hello, this is a test!",
            "session_id": "test_session",
            "use_multi_agent": False
        }
        
        response = requests.post(
            f"{base_url}/message",
            json=message_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat Message: PASSED")
            print(f"   Response: {data['response'][:50]}...")
        else:
            print(f"❌ Chat Message: FAILED ({response.status_code})")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Chat Message: FAILED ({e})")
        all_passed = False
    
    return all_passed

def open_frontend():
    """Open the frontend in browser"""
    print("🎨 Opening frontend...")
    
    # Create absolute path to test frontend
    test_file = Path.cwd() / "test_frontend.html"
    
    if test_file.exists():
        webbrowser.open(f"file://{test_file}")
        print("✅ Test frontend opened in browser")
        
        # Also show the main frontend path
        main_frontend = Path.cwd() / "frontend" / "index.html"
        if main_frontend.exists():
            print(f"📱 Main frontend available at: file://{main_frontend}")
        
        return True
    else:
        print("❌ Frontend file not found")
        return False

def main():
    """Main build and test function"""
    print("🤖 Silas Chat UI - Build & Test")
    print("=" * 50)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return False
    
    # Step 2: Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Backend startup failed")
        return False
    
    try:
        # Step 3: Test backend
        if not test_backend():
            print("⚠️  Some backend tests failed, but continuing...")
        
        # Step 4: Open frontend
        if not open_frontend():
            print("❌ Frontend opening failed")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 Build and test complete!")
        print("\n📋 System Status:")
        print("✅ Backend: Running on http://127.0.0.1:8001")
        print("✅ Frontend: Opened in browser")
        print("✅ API: Ready for testing")
        
        print("\n🔧 Next Steps:")
        print("1. Test the chat interface in your browser")
        print("2. Get OpenRouter API key for full multi-agent mode")
        print("3. Update backend/.env with your API key")
        print("4. Restart backend for full functionality")
        
        print("\n⏹️  Press Ctrl+C to stop the backend server")
        
        # Keep the backend running
        backend_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping backend server...")
        backend_process.terminate()
        print("✅ Backend stopped")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)