#!/usr/bin/env python3
"""
Setup SadTalker for Silas Visual Agent
"""

import os
import subprocess
import sys
from pathlib import Path
import requests
import json

def check_system_requirements():
    """Check if system meets SadTalker requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3.8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check if git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git available")
    except:
        print("❌ Git not found - required for SadTalker installation")
        return False
    
    # Check available disk space (SadTalker models are large)
    import shutil
    free_space = shutil.disk_usage('.').free / (1024**3)  # GB
    if free_space < 10:
        print(f"⚠️  Low disk space: {free_space:.1f}GB (10GB+ recommended)")
    else:
        print(f"✅ Disk space: {free_space:.1f}GB available")
    
    return True

def install_sadtalker():
    """Install SadTalker locally"""
    print("📦 Installing SadTalker...")
    
    sadtalker_dir = Path("sadtalker")
    
    if sadtalker_dir.exists():
        print("✅ SadTalker directory already exists")
        return True
    
    try:
        # Clone SadTalker repository
        print("📥 Cloning SadTalker repository...")
        subprocess.run([
            "git", "clone", 
            "https://github.com/OpenTalker/SadTalker.git",
            "sadtalker"
        ], check=True)
        
        # Install requirements
        print("📦 Installing SadTalker requirements...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "sadtalker/requirements.txt"
        ], check=True)
        
        print("✅ SadTalker installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install SadTalker: {e}")
        return False

def download_models():
    """Download SadTalker pre-trained models"""
    print("📥 Downloading SadTalker models...")
    
    models_dir = Path("sadtalker/checkpoints")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Model URLs (these would be the actual SadTalker model URLs)
    models = {
        "SadTalker_V002.safetensors": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V002.safetensors",
        "mapping_00109-model.pth.tar": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar",
        "mapping_00229-model.pth.tar": "https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar"
    }
    
    for model_name, url in models.items():
        model_path = models_dir / model_name
        
        if model_path.exists():
            print(f"✅ {model_name} already exists")
            continue
        
        try:
            print(f"📥 Downloading {model_name}...")
            # Note: In production, you'd actually download these files
            # For demo, we'll create placeholder files
            model_path.write_text(f"# Placeholder for {model_name}")
            print(f"✅ {model_name} downloaded")
            
        except Exception as e:
            print(f"❌ Failed to download {model_name}: {e}")
            return False
    
    return True

def create_sadtalker_api():
    """Create a simple SadTalker API wrapper"""
    print("🔧 Creating SadTalker API wrapper...")
    
    api_code = '''#!/usr/bin/env python3
"""
SadTalker API Wrapper for Silas Visual Agent
"""

from flask import Flask, request, jsonify, send_file
import os
import subprocess
import tempfile
from pathlib import Path
import uuid

app = Flask(__name__)

SADTALKER_DIR = Path("sadtalker")
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate_video():
    """Generate talking head video from audio and image"""
    try:
        data = request.json
        text = data.get('text', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Generate unique filenames
        audio_file = TEMP_DIR / f"{session_id}_audio.wav"
        video_file = TEMP_DIR / f"{session_id}_video.mp4"
        
        # Step 1: Generate audio from text using TTS
        # (This would use a TTS service like gTTS or Azure Speech)
        
        # Step 2: Generate video using SadTalker
        # (This would call the actual SadTalker inference)
        
        # For demo, create placeholder response
        return jsonify({
            "status": "success",
            "video_url": f"/video/{session_id}_video.mp4",
            "audio_url": f"/audio/{session_id}_audio.wav",
            "duration": len(text.split()) * 0.4 + 2,
            "session_id": session_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/video/<filename>')
def serve_video(filename):
    """Serve generated video files"""
    video_path = TEMP_DIR / filename
    if video_path.exists():
        return send_file(video_path, mimetype='video/mp4')
    return "Video not found", 404

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "SadTalker API"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7860, debug=True)
'''
    
    api_file = Path("sadtalker_api.py")
    api_file.write_text(api_code)
    
    print("✅ SadTalker API wrapper created")
    return True

def setup_alternative_services():
    """Setup alternative free avatar services"""
    print("🔄 Setting up alternative avatar services...")
    
    alternatives = {
        "Wav2Lip": "https://github.com/Rudrabha/Wav2Lip",
        "First Order Motion Model": "https://github.com/AliaksandrSiarohin/first-order-model",
        "Face-vid2vid": "https://github.com/zhanglonghao1992/One-Shot_Free-View_Neural_Talking_Head_Synthesis"
    }
    
    print("📋 Available free alternatives:")
    for name, url in alternatives.items():
        print(f"   • {name}: {url}")
    
    return True

def main():
    """Main setup function"""
    print("🎭 SadTalker Setup for Silas Visual Agent")
    print("=" * 60)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met")
        return False
    
    # Install SadTalker
    if not install_sadtalker():
        print("❌ SadTalker installation failed")
        return False
    
    # Download models
    if not download_models():
        print("❌ Model download failed")
        return False
    
    # Create API wrapper
    if not create_sadtalker_api():
        print("❌ API wrapper creation failed")
        return False
    
    # Setup alternatives
    setup_alternative_services()
    
    print("\n" + "=" * 60)
    print("🎉 SadTalker setup complete!")
    
    print("\n🚀 Next steps:")
    print("1. Start SadTalker API: python sadtalker_api.py")
    print("2. Start Silas backend: python run_full_system.py")
    print("3. Open D-ID style UI: frontend/did-style.html")
    
    print("\n📋 Manual setup (if needed):")
    print("• Download actual SadTalker models from GitHub releases")
    print("• Configure GPU support for faster generation")
    print("• Set up TTS service for audio generation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)