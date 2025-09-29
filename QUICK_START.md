# 🚀 Quick Start Guide

**Get your AI avatar running in 30 seconds!**

## ⚡ Super Quick Setup

```bash
# 1. Clone and enter directory
git clone https://github.com/yourusername/ai-shorts-lab.git
cd ai-shorts-lab

# 2. Add your photo (REQUIRED!)
cp your_photo.jpg silas-chat-ui/my_photo.jpg

# 3. Launch complete system
python silas-chat-ui/launch_complete_avatar.py
```

## 🎯 What Happens Next

1. **Backend starts** on `http://127.0.0.1:8002`
2. **Browser opens** with your avatar interface
3. **Ready to use!** Click buttons to test

## 🎮 First Tests

### Test TTS (Text-to-Speech)
- Click the **🔊 Speak** button
- Should hear: "Hello! I'm testing my text-to-speech capabilities..."

### Test Video Generation
- Click the **🎬 Generate** button  
- Your photo will speak with audio!

### Full Conversation
- Type: "Hello, tell me about yourself"
- Press Enter
- Get AI response + your photo speaking!

## 🔧 If Something Goes Wrong

### No Sound?
```bash
# Install audio dependencies
brew install espeak          # macOS
sudo apt install espeak      # Linux
```

### No Video?
```bash
# Install video dependencies  
brew install ffmpeg          # macOS
sudo apt install ffmpeg      # Linux
```

### Backend Won't Start?
```bash
# Install Python dependencies
pip install fastapi uvicorn requests python-dotenv pydantic
```

## 📸 Photo Requirements

Your photo should be:
- **Clear face** - Good lighting, facing camera
- **JPG format** - Named `my_photo.jpg`
- **Square-ish** - Will be cropped to 512x512
- **Good quality** - Higher resolution = better results

## 🎉 Success!

If you see:
- ✅ Backend started on http://127.0.0.1:8002
- ✅ Interface opened in browser
- 🔊 TTS test works
- 🎬 Video generation works

**You're all set! Your AI avatar is ready! 🎭**

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed setup
- Run `python silas-chat-ui/test_tts_system.py` for diagnostics
- Open an issue if you're stuck

**Happy avatar building! 🚀**