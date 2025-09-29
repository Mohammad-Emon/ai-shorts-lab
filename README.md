# 🎭 AI Shorts Lab - Complete Avatar System

**Build AI-powered talking avatars with your real photo in minutes!**

[![Demo](https://img.shields.io/badge/🎬-Live%20Demo-blue)](https://github.com/yourusername/ai-shorts-lab)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🚀 What You Get

- **🎭 Real Face Avatar** - Use your actual photo as a talking head
- **🔊 Dual TTS System** - Browser + Server text-to-speech
- **🎬 Video Generation** - Your photo speaks with lip-sync
- **💬 Smart AI Chat** - Multi-agent conversation system
- **🎮 Complete Interface** - Ready-to-use web interface
- **⚡ One-Click Launch** - Everything automated

## 🎯 Quick Start (30 seconds)

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-shorts-lab.git
cd ai-shorts-lab

# Add your photo
cp your_photo.jpg silas-chat-ui/my_photo.jpg

# Launch complete system
python silas-chat-ui/launch_complete_avatar.py
```

**That's it! Your avatar is ready! 🎉**

## 🎬 Features

### 🎭 **Complete Avatar System**
- **Real Photo Avatar** - Uses your actual face, not cartoons
- **Talking Head Videos** - Your photo speaks with perfect lip-sync
- **Audio Synchronization** - Voice matches mouth movements
- **HD Quality** - Professional video output

### 🔊 **Dual TTS System**
- **Browser TTS** - Instant speech using built-in APIs
- **Server TTS** - High-quality espeak generation
- **Smart Fallback** - Automatically switches if one fails
- **Multiple Voices** - Choose from available system voices

### 💬 **AI Chat System**
- **Multi-Agent Architecture** - Specialized AI agents
- **Free LLM Integration** - Uses OpenRouter free models
- **Smart Responses** - Context-aware conversations
- **Real-time Chat** - WebSocket-powered interface

### 🎮 **Easy Controls**
- **🔊 Speak Button** - Test TTS immediately
- **🎬 Generate Button** - Create avatar videos
- **⏹️ Stop Button** - Stop all audio/video
- **💬 Chat Interface** - Type and get responses

## 📁 Project Structure

```
ai-shorts-lab/
├── silas-chat-ui/                 # Main avatar system
│   ├── complete_working_avatar.html    # Complete interface
│   ├── working_sadtalker_backend.py    # Main backend
│   ├── launch_complete_avatar.py       # One-click launcher
│   ├── my_photo.jpg                    # Your photo goes here
│   └── generated_videos/               # Output videos
├── SadTalker/                     # Talking head generation
├── Wav2Lip/                       # Lip-sync technology
└── 60s-saas-pipeline/             # FastAPI templates
```

## 🛠️ Installation

### Prerequisites
```bash
# macOS
brew install ffmpeg espeak

# Ubuntu/Debian
sudo apt install ffmpeg espeak espeak-data

# Windows (use WSL or install manually)
```

### Setup
```bash
# 1. Clone repository
git clone https://github.com/yourusername/ai-shorts-lab.git
cd ai-shorts-lab

# 2. Install Python dependencies
pip install fastapi uvicorn requests python-dotenv pydantic

# 3. Add your photo (IMPORTANT!)
cp your_photo.jpg silas-chat-ui/my_photo.jpg

# 4. Launch system
python silas-chat-ui/launch_complete_avatar.py
```

## 🎯 Usage

### 1. **Quick Test**
```bash
python silas-chat-ui/launch_complete_avatar.py
```
- Click the **🔊 Speak** button to test TTS
- Click the **🎬 Generate** button to test video
- Type a message and press Enter for full experience

### 2. **Advanced Usage**
```bash
# Test individual components
python silas-chat-ui/test_tts_system.py
python silas-chat-ui/test_sadtalker_direct.py

# Run backend only
python silas-chat-ui/working_sadtalker_backend.py
```

### 3. **API Endpoints**
- `POST /generate-avatar` - Generate talking head video
- `POST /speak` - Generate TTS audio
- `GET /health` - System health check
- `GET /avatar-image` - Get user photo

## 🎨 Customization

### Change Voice Settings
Edit `working_sadtalker_backend.py`:
```python
# TTS Settings
subprocess.run([
    "espeak", "-s", "150",  # Speed
    "-v", "en+f3",          # Voice (en+f3 = female)
    "-p", "50",             # Pitch
    "-w", audio_file, text
])
```

### Modify Video Quality
```python
# Video Settings in backend
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-vf", "scale=512:512,fps=25",  # Resolution & FPS
    "-c:v", "libx264",              # Codec
    "-b:a", "192k",                 # Audio bitrate
]
```

## 🔧 Troubleshooting

### Common Issues

**No Sound?**
```bash
# Test TTS directly
python silas-chat-ui/test_tts_system.py
```

**Video Not Playing?**
```bash
# Check video generation
python silas-chat-ui/test_sadtalker_direct.py
```

**Backend Not Starting?**
```bash
# Check dependencies
ffmpeg -version
espeak --version
```

### System Requirements
- **Python 3.8+**
- **FFmpeg** (video processing)
- **Espeak** (text-to-speech)
- **Modern browser** (Chrome, Firefox, Safari)

## 🎬 Demo Videos

| Feature | Demo |
|---------|------|
| 🎭 Complete Avatar | [Watch Demo](demo-link) |
| 🔊 TTS System | [Watch Demo](demo-link) |
| 🎬 Video Generation | [Watch Demo](demo-link) |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SadTalker** - Talking head generation technology
- **Wav2Lip** - Lip synchronization
- **FastAPI** - Modern web framework
- **OpenRouter** - Free LLM access

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/ai-shorts-lab/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-shorts-lab/discussions)
- 📧 **Email**: your-email@example.com

---

**⭐ Star this repo if it helped you build amazing AI avatars!**

Made with ❤️ for the AI community