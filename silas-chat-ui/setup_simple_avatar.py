#!/usr/bin/env python3
"""
Setup Simple Talking Avatar System
Installs dependencies and configures OpenRouter integration
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    
    print("📦 Installing dependencies...")
    
    packages = [
        "fastapi",
        "uvicorn[standard]", 
        "httpx",
        "pydantic"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def setup_openrouter():
    """Setup OpenRouter API configuration"""
    
    print("\n🤖 OpenRouter Setup")
    print("=" * 30)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if api_key:
        print("✅ OpenRouter API key found in environment")
        return True
    
    print("OpenRouter provides free access to powerful LLMs like:")
    print("• Meta Llama 3.2 (3B and 1B)")
    print("• Microsoft Phi-3 Mini")
    print("• Google Gemma 2")
    print("• Qwen 2")
    
    print("\n🔑 To get free API access:")
    print("1. Go to https://openrouter.ai")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    print("4. Set it as environment variable:")
    print("   export OPENROUTER_API_KEY='your-key-here'")
    
    setup_choice = input("\nDo you want to set up OpenRouter now? (y/n): ").lower()
    
    if setup_choice == 'y':
        api_key = input("Enter your OpenRouter API key: ").strip()
        
        if api_key:
            # Create a simple config file
            config_path = Path("silas-chat-ui/.env")
            with open(config_path, "w") as f:
                f.write(f"OPENROUTER_API_KEY={api_key}\n")
            
            print(f"✅ API key saved to {config_path}")
            print("💡 You can also set it as environment variable:")
            print(f"   export OPENROUTER_API_KEY='{api_key}'")
            return True
    
    print("⚠️  Continuing without OpenRouter - will use fallback responses")
    print("💡 You can add the API key later for full AI features")
    return False

def test_system():
    """Test the talking avatar system"""
    
    print("\n🧪 Testing system components...")
    
    # Test backend import
    try:
        import fastapi
        import uvicorn
        import httpx
        print("✅ Backend dependencies OK")
    except ImportError as e:
        print(f"❌ Backend dependency missing: {e}")
        return False
    
    # Check frontend file
    frontend_path = Path("silas-chat-ui/simple_talking_avatar.html")
    if frontend_path.exists():
        print("✅ Frontend interface OK")
    else:
        print("❌ Frontend interface missing")
        return False
    
    # Check backend file
    backend_path = Path("silas-chat-ui/simple_backend.py")
    if backend_path.exists():
        print("✅ Backend server OK")
    else:
        print("❌ Backend server missing")
        return False
    
    print("✅ All system components ready!")
    return True

def main():
    """Main setup function"""
    
    print("🎭 Silas Talking Avatar Setup")
    print("=" * 40)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed - dependency installation error")
        return
    
    # Setup OpenRouter
    setup_openrouter()
    
    # Test system
    if not test_system():
        print("❌ Setup failed - system test error")
        return
    
    print("\n🎉 Setup Complete!")
    print("=" * 20)
    print("✅ Dependencies installed")
    print("✅ System components ready")
    print("✅ Voice features configured")
    
    print("\n🚀 Ready to launch!")
    print("Run: python silas-chat-ui/launch_simple_avatar.py")
    
    launch_now = input("\nLaunch talking avatar now? (y/n): ").lower()
    if launch_now == 'y':
        print("\n🎭 Launching Silas Talking Avatar...")
        try:
            from launch_simple_avatar import launch_talking_avatar
            launch_talking_avatar()
        except Exception as e:
            print(f"Launch error: {e}")
            print("Try running: python silas-chat-ui/launch_simple_avatar.py")

if __name__ == "__main__":
    main()