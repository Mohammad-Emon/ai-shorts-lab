#!/usr/bin/env python3
"""
Simple server starter for Silas Chat UI
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting Silas Chat UI Backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    try:
        # Start uvicorn server
        cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
        print(f"Running: {' '.join(cmd)}")
        
        process = subprocess.Popen(cmd)
        
        print("✅ Backend server starting...")
        print("   URL: http://127.0.0.1:8000")
        print("   API Docs: http://127.0.0.1:8000/docs")
        print("   Health: http://127.0.0.1:8000/health")
        print("\n🎨 Frontend:")
        print("   Open: frontend/index.html in your browser")
        print("\n⏹️  Press Ctrl+C to stop the server")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        process.terminate()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_backend()