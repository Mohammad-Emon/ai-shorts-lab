#!/usr/bin/env python3
"""
Silas Chat UI Setup Script
Automates the setup process for the avatar chat system
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def setup_backend():
    """Setup the backend environment"""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Install requirements
    print("📦 Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt", cwd=backend_dir):
        return False
    
    # Setup environment file
    env_file = backend_dir / ".env"
    env_example = backend_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file...")
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("✅ Created .env file from template")
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Setup the frontend"""
    print("\n🎨 Setting up frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    print("✅ Frontend setup complete!")
    return True

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API configuration...")
    
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    if "your_openrouter_api_key_here" in content:
        print("⚠️  OpenRouter API key not configured")
        print("   Get your free key from: https://openrouter.ai/keys")
        print("   Then edit backend/.env file")
        return False
    
    print("✅ API keys configured")
    return True

def start_services():
    """Start the backend and frontend services"""
    print("\n🚀 Starting services...")
    
    print("Backend will start on: http://localhost:8000")
    print("Frontend will be available at: frontend/index.html")
    print("\nTo start backend manually:")
    print("  cd backend && uvicorn main:app --reload")
    print("\nTo start frontend manually:")
    print("  cd frontend && python -m http.server 3000")
    
    # Ask if user wants to start backend now
    response = input("\nStart backend server now? (y/n): ").lower().strip()
    if response == 'y':
        print("Starting backend server...")
        try:
            subprocess.Popen(["uvicorn", "main:app", "--reload"], cwd="backend")
            print("✅ Backend server started!")
            print("   Access API docs at: http://localhost:8000/docs")
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            print("   Run manually: cd backend && uvicorn main:app --reload")

def main():
    """Main setup function"""
    print("🤖 Silas Chat UI Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        return False
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        return False
    
    # Check API keys
    api_configured = check_api_keys()
    
    # Start services
    start_services()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    
    if not api_configured:
        print("\n⚠️  Don't forget to configure your OpenRouter API key in backend/.env")
    
    print("\n📚 Next steps:")
    print("1. Get OpenRouter API key: https://openrouter.ai/keys")
    print("2. Edit backend/.env with your API key")
    print("3. Open frontend/index.html in your browser")
    print("4. Start chatting with Silas!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)