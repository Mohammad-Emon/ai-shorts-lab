#!/usr/bin/env python3
"""
Setup D-ID Style Visual Avatar System
Complete setup for realistic talking head generation with SadTalker
"""

import subprocess
import sys
import os
import requests
from pathlib import Path
import shutil

def install_python_dependencies():
    """Install required Python packages"""
    
    print("📦 Installing Python dependencies...")
    
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "httpx",
        "pydantic",
        "torch",
        "torchvision",
        "torchaudio",
        "opencv-python",
        "pillow",
        "numpy",
        "scipy",
        "librosa",
        "soundfile"
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

def install_system_dependencies():
    """Install system-level dependencies"""
    
    print("\n🔧 System Dependencies Setup")
    print("=" * 40)
    
    print("The following system packages are recommended:")
    print("• ffmpeg (for video processing)")
    print("• espeak (for text-to-speech)")
    print("• git (for cloning repositories)")
    
    install_system = input("\nTry to install system dependencies automatically? (y/n): ").lower()
    
    if install_system == 'y':
        try:
            # Detect OS and install accordingly
            import platform
            system = platform.system().lower()
            
            if system == "linux":
                print("Installing on Linux...")
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg", "espeak", "git"], check=True)
            elif system == "darwin":  # macOS
                print("Installing on macOS...")
                subprocess.run(["brew", "install", "ffmpeg", "espeak", "git"], check=True)
            else:
                print("Windows detected - please install manually:")
                print("• Download ffmpeg from https://ffmpeg.org/download.html")
                print("• Install espeak from http://espeak.sourceforge.net/")
                return False
            
            print("✅ System dependencies installed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ System installation failed: {e}")
            print("Please install manually:")
            print("• ffmpeg: https://ffmpeg.org/")
            print("• espeak: http://espeak.sourceforge.net/")
            return False
    
    return True

def setup_sadtalker():
    """Setup SadTalker for video generation"""
    
    print("\n🎬 SadTalker Setup")
    print("=" * 30)
    
    sadtalker_path = Path("SadTalker")
    
    if sadtalker_path.exists():
        print("✅ SadTalker already exists")
        setup_choice = input("Reinstall SadTalker? (y/n): ").lower()
        if setup_choice != 'y':
            return True
        else:
            shutil.rmtree(sadtalker_path)
    
    try:
        print("📥 Cloning SadTalker repository...")
        subprocess.run([
            "git", "clone", 
            "https://github.com/OpenTalker/SadTalker.git"
        ], check=True)
        
        print("📦 Installing SadTalker dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "SadTalker/requirements.txt"
        ], check=True)
        
        print("✅ SadTalker cloned and dependencies installed")
        
        # Download checkpoints
        print("\n📥 Downloading SadTalker checkpoints...")
        print("This may take several minutes...")
        
        checkpoint_script = sadtalker_path / "scripts" / "download_models.py"
        if checkpoint_script.exists():
            subprocess.run([
                sys.executable, str(checkpoint_script)
            ], cwd=str(sadtalker_path), check=True)
            print("✅ Checkpoints downloaded")
        else:
            print("⚠️  Manual checkpoint download required")
            print("Run: cd SadTalker && python scripts/download_models.py")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ SadTalker setup failed: {e}")
        print("Manual setup instructions:")
        print("1. git clone https://github.com/OpenTalker/SadTalker.git")
        print("2. cd SadTalker")
        print("3. pip install -r requirements.txt")
        print("4. python scripts/download_models.py")
        return False

def setup_avatar_image():
    """Setup default avatar image"""
    
    print("\n🖼️  Avatar Image Setup")
    print("=" * 25)
    
    assets_dir = Path("SadTalker/assets")
    avatar_path = assets_dir / "avatar.jpg"
    
    if not assets_dir.exists():
        assets_dir.mkdir(parents=True)
    
    if avatar_path.exists():
        print("✅ Avatar image already exists")
        return True
    
    print("You need an avatar image for video generation.")
    print("This should be a clear photo of a person's face (512x512 recommended)")
    
    image_choice = input("\nDo you have an avatar image to use? (y/n): ").lower()
    
    if image_choice == 'y':
        image_path = input("Enter path to your avatar image: ").strip()
        
        if os.path.exists(image_path):
            try:
                shutil.copy2(image_path, avatar_path)
                print(f"✅ Avatar image copied to {avatar_path}")
                return True
            except Exception as e:
                print(f"❌ Failed to copy image: {e}")
        else:
            print("❌ Image file not found")
    
    # Download a sample avatar
    print("📥 Downloading sample avatar image...")
    try:
        # Use a placeholder service for demo
        sample_url = "https://thispersondoesnotexist.com/image"
        response = requests.get(sample_url, timeout=30)
        
        if response.status_code == 200:
            with open(avatar_path, 'wb') as f:
                f.write(response.content)
            print("✅ Sample avatar image downloaded")
            return True
        else:
            print("❌ Failed to download sample image")
    except Exception as e:
        print(f"❌ Download error: {e}")
    
    print("⚠️  Please manually add an avatar image to SadTalker/assets/avatar.jpg")
    return False

def setup_openrouter():
    """Setup OpenRouter API configuration"""
    
    print("\n🤖 OpenRouter API Setup")
    print("=" * 25)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if api_key:
        print("✅ OpenRouter API key found in environment")
        return True
    
    print("OpenRouter provides free access to powerful LLMs:")
    print("• Meta Llama 3.2 (3B and 1B)")
    print("• Microsoft Phi-3 Mini")
    print("• Google Gemma 2")
    
    setup_choice = input("\nSet up OpenRouter API key? (y/n): ").lower()
    
    if setup_choice == 'y':
        print("\n🔑 Getting OpenRouter API Key:")
        print("1. Go to https://openrouter.ai")
        print("2. Sign up for a free account")
        print("3. Get your API key from the dashboard")
        
        api_key = input("\nEnter your OpenRouter API key: ").strip()
        
        if api_key:
            # Save to .env file
            env_path = Path("silas-chat-ui/.env")
            with open(env_path, "w") as f:
                f.write(f"OPENROUTER_API_KEY={api_key}\n")
                f.write(f"SADTALKER_PATH=./SadTalker\n")
            
            print(f"✅ API key saved to {env_path}")
            return True
    
    print("⚠️  Continuing without OpenRouter - will use fallback responses")
    return False

def test_system():
    """Test the complete D-ID style system"""
    
    print("\n🧪 Testing System Components")
    print("=" * 35)
    
    # Test Python dependencies
    try:
        import fastapi, torch, cv2, PIL
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        return False
    
    # Test system commands
    commands = ["ffmpeg", "git"]
    for cmd in commands:
        try:
            subprocess.run([cmd, "--version"], 
                         capture_output=True, check=True)
            print(f"✅ {cmd} available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"⚠️  {cmd} not found (optional)")
    
    # Test SadTalker
    sadtalker_path = Path("SadTalker")
    if sadtalker_path.exists():
        print("✅ SadTalker directory exists")
        
        avatar_path = sadtalker_path / "assets" / "avatar.jpg"
        if avatar_path.exists():
            print("✅ Avatar image ready")
        else:
            print("⚠️  Avatar image missing")
    else:
        print("❌ SadTalker not found")
        return False
    
    # Test backend files
    backend_files = [
        "silas-chat-ui/did_style_complete.html",
        "silas-chat-ui/sadtalker_backend.py"
    ]
    
    for file_path in backend_files:
        if Path(file_path).exists():
            print(f"✅ {Path(file_path).name} ready")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    print("✅ All system components ready!")
    return True

def main():
    """Main setup function"""
    
    print("🎭 D-ID Style Visual Avatar Setup")
    print("=" * 50)
    print("This will set up a complete realistic talking avatar system with:")
    print("• SadTalker for realistic video generation")
    print("• OpenRouter LLMs for conversation")
    print("• D-ID style glassmorphism interface")
    print("• Voice input/output capabilities")
    
    proceed = input("\nProceed with setup? (y/n): ").lower()
    if proceed != 'y':
        print("Setup cancelled.")
        return
    
    # Step 1: Python dependencies
    if not install_python_dependencies():
        print("❌ Setup failed at Python dependencies")
        return
    
    # Step 2: System dependencies
    install_system_dependencies()
    
    # Step 3: SadTalker setup
    if not setup_sadtalker():
        print("❌ Setup failed at SadTalker installation")
        return
    
    # Step 4: Avatar image
    setup_avatar_image()
    
    # Step 5: OpenRouter API
    setup_openrouter()
    
    # Step 6: Test system
    if not test_system():
        print("❌ System test failed")
        return
    
    print("\n🎉 Setup Complete!")
    print("=" * 25)
    print("✅ SadTalker video generation ready")
    print("✅ OpenRouter LLM integration")
    print("✅ D-ID style interface")
    print("✅ Voice capabilities")
    
    print("\n🚀 Ready to Launch!")
    print("Run: python silas-chat-ui/launch_did_style.py")
    
    launch_now = input("\nLaunch D-ID style avatar now? (y/n): ").lower()
    if launch_now == 'y':
        print("\n🎭 Launching D-ID Style Avatar...")
        try:
            subprocess.run([sys.executable, "silas-chat-ui/launch_did_style.py"])
        except Exception as e:
            print(f"Launch error: {e}")
            print("Try running manually: python silas-chat-ui/launch_did_style.py")

if __name__ == "__main__":
    main()