# 🎭 Silas Simple Talking Avatar

A complete voice-enabled AI avatar system with OpenRouter free LLMs integration.

## ✨ Features

### 🎤 Voice Input
- Real-time speech recognition
- Click microphone or press SPACE
- Auto-sends messages after speech
- Works in Chrome and Edge

### 🔊 Voice Output  
- High-quality text-to-speech
- Automatic voice selection
- Pause/resume/stop controls
- Avatar animation during speech

### 🤖 AI Integration
- Free OpenRouter LLMs:
  - Meta Llama 3.2 (3B/1B)
  - Microsoft Phi-3 Mini
  - Google Gemma 2
  - Qwen 2
- Fallback responses without API key
- Conversational personality

### 🎮 Controls
- **SPACE**: Toggle voice input
- **P**: Pause/Resume speech
- **S**: Stop speech
- **Click**: All buttons work with mouse
- **Type**: Normal text input

## 🚀 Quick Start

### 1. Setup System
```bash
python silas-chat-ui/setup_simple_avatar.py
```

### 2. Launch Avatar
```bash
python silas-chat-ui/launch_simple_avatar.py
```

### 3. Start Chatting!
- Click microphone and speak
- Or type messages normally
- Avatar responds with voice + animation

## 🔧 Manual Setup

### Install Dependencies
```bash
pip install fastapi uvicorn httpx pydantic
```

### Get OpenRouter API Key (Optional)
1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Sign up for free account
3. Get API key from dashboard
4. Set environment variable:
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### Launch Components
```bash
# Start backend
python silas-chat-ui/simple_backend.py

# Open frontend
open silas-chat-ui/simple_talking_avatar.html
```

## 🎯 Usage Guide

### Voice Conversation
1. **Start Voice**: Click 🎤 or press SPACE
2. **Speak**: Say your message clearly
3. **Listen**: Avatar responds with voice
4. **Control**: Use P to pause, S to stop

### Text Conversation  
1. **Type**: Enter message in text box
2. **Send**: Click ➤ or press Enter
3. **Listen**: Avatar speaks the response
4. **Control**: Same pause/stop controls

### Keyboard Shortcuts
- **SPACE**: Toggle voice input (when not typing)
- **P**: Pause/Resume current speech
- **S**: Stop speech immediately
- **Enter**: Send typed message

## 🌐 Browser Support

### Full Support ✅
- **Chrome**: Complete voice features
- **Edge**: Complete voice features

### Partial Support ⚠️
- **Firefox**: TTS only (no speech recognition)
- **Safari**: Limited TTS support

### Recommended
- Use Chrome or Edge for best experience
- Allow microphone permissions
- Use headphones to prevent feedback

## 🔧 Technical Details

### Architecture
```
Frontend (HTML/JS) ←→ Backend (FastAPI) ←→ OpenRouter API
       ↓                    ↓                    ↓
   Web Speech API      HTTP/JSON           Free LLMs
```

### Components
- **Frontend**: `simple_talking_avatar.html`
- **Backend**: `simple_backend.py` 
- **Launcher**: `launch_simple_avatar.py`
- **Setup**: `setup_simple_avatar.py`

### API Endpoints
- `GET /`: System status
- `GET /health`: Health check
- `POST /chat`: Main chat endpoint
- `GET /models`: Available models
- `POST /test-voice`: Voice test

## 🎭 Avatar Personality

Silas is designed to be:
- **Conversational**: Natural, engaging dialogue
- **Helpful**: Knowledgeable and informative
- **Concise**: Keeps responses under 100 words for voice
- **Expressive**: Animated and personable
- **Friendly**: Always ready to chat

## 🚨 Troubleshooting

### No Voice Input
- Check microphone permissions
- Use Chrome or Edge browser
- Verify microphone hardware

### No Voice Output
- Check system volume
- Verify browser audio permissions
- Try different browser

### API Errors
- Check OpenRouter API key
- Verify internet connection
- System works with fallback responses

### Backend Issues
- Check if port 8001 is available
- Verify Python dependencies installed
- Look at console output for errors

## 📁 File Structure

```
silas-chat-ui/
├── simple_talking_avatar.html    # Frontend interface
├── simple_backend.py             # Backend server
├── launch_simple_avatar.py       # System launcher
├── setup_simple_avatar.py        # Setup script
└── SIMPLE_AVATAR_README.md       # This file
```

## 🔮 Future Enhancements

### Planned Features
- SadTalker video generation integration
- Custom voice training
- Multi-language support
- Emotion detection
- Advanced avatar animations

### Integration Options
- ElevenLabs premium voices
- Azure Speech Services
- Google Cloud Speech
- Custom AI models

## 💡 Tips & Tricks

### Best Practices
- Speak clearly at normal pace
- Use headphones to prevent feedback
- Allow microphone permissions
- Keep messages conversational

### Performance
- Close other audio applications
- Use wired headphones for best quality
- Ensure stable internet for AI responses
- Clear browser cache if issues occur

### Customization
- Edit system prompt in `simple_backend.py`
- Modify avatar appearance in HTML/CSS
- Add new voice commands in JavaScript
- Extend API with new endpoints

---

## 🎉 Success Metrics

✅ **Voice Input**: Real-time speech recognition  
✅ **Voice Output**: High-quality TTS synthesis  
✅ **AI Integration**: Free OpenRouter LLMs  
✅ **Controls**: Keyboard and mouse shortcuts  
✅ **Avatar**: Animated visual feedback  
✅ **Fallbacks**: Works without API key  
✅ **Cross-platform**: Windows, Mac, Linux  
✅ **Simple**: Easy setup and launch  

**Status: Ready for use! 🚀**