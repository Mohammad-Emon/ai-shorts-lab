# Project Structure & Organization

## Repository Layout

```
ai-shorts-lab/
├── silas-chat-ui/           # Main project - AI avatar chat system
├── SadTalker/               # Talking head video generation
├── Wav2Lip/                 # Lip-sync video generation  
├── 60s-saas-pipeline/       # FastAPI + Docker SaaS template
├── slack-support-bot/       # AI support automation
├── prompt-chains/           # Prompt engineering templates
├── long-forms/              # Tutorial scripts and resources
├── generated_videos/        # Output directory for generated content
└── test_sadtalker_output/   # SadTalker test outputs
```

## Silas Chat UI Structure (Primary Project)

```
silas-chat-ui/
├── frontend/
│   ├── index.html           # Main chat interface
│   ├── styles.css           # Responsive styling
│   ├── script.js            # Chat logic and WebSocket handling
│   ├── did-style.html       # DID-style avatar interface
│   ├── elevenlabs-style.html # ElevenLabs voice integration
│   └── test-elevenlabs.html # Voice testing interface
├── backend/
│   ├── main.py              # Full multi-agent FastAPI server
│   ├── simple_main.py       # Simplified API for testing
│   ├── agents.py            # Multi-agent orchestrator
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── .env                 # Local environment (gitignored)
├── launch_*.py              # Component launchers (avatar, voice, etc.)
├── setup_*.py               # Setup scripts for different features
├── test_*.py                # Test scripts for components
├── build_and_test.py        # Complete system build script
└── *.html                   # Various UI implementations
```

## File Naming Conventions

### Python Scripts
- **`launch_*.py`** - Start specific system components
- **`setup_*.py`** - Configure and install features
- **`test_*.py`** - Test individual components
- **`fix_*.py`** - Repair/troubleshoot utilities
- **`*_backend.py`** - Backend service implementations

### HTML Files
- **`index.html`** - Main application interface
- **`*_style.html`** - Themed UI variations
- **`test_*.html`** - Testing interfaces
- **`demo.html`** - Demonstration pages

### Documentation
- **`README.md`** - Main project documentation
- **`README_QUICK_START.md`** - Getting started guide
- **`*_COMPLETE.md`** - Feature completion status
- **`*_STATUS.md`** - Current implementation status
- **`*_SUMMARY.md`** - Feature summaries

## Directory Purposes

### `/frontend/`
- Pure client-side code (HTML/CSS/JS)
- No server dependencies
- Responsive design components
- WebSocket client implementations

### `/backend/`
- FastAPI server implementations
- Multi-agent orchestration
- API endpoint definitions
- Environment configuration

### `/generated_videos/`
- Output from SadTalker and Wav2Lip
- Temporary video files
- Avatar generation results

### Root Level Scripts
- System orchestration and setup
- Integration between components
- Testing and validation utilities
- Quick launch commands

## Configuration Management

### Environment Files
- **`.env`** - Local development secrets (gitignored)
- **`.env.example`** - Template with required variables
- **`backend/.env`** - Backend-specific configuration

### API Keys Required
- **OPENROUTER_API_KEY** - For LLM access
- **AZURE_SPEECH_KEY** - For voice synthesis (optional)
- **DID_API_KEY** - For DID avatar service (optional)

## Integration Patterns

### Multi-Agent System
- Coordinator routes queries to specialized agents
- Agents work in parallel or collaborative workflows
- Responses synthesized by Summarizer agent

### Avatar Generation
- SadTalker for talking head videos
- Wav2Lip for lip-sync generation
- DID API for cloud-based avatars

### Voice Integration
- Azure TTS for high-quality synthesis
- Edge TTS for free alternative
- Real-time audio streaming support

## Development Workflow

1. **Setup**: Run `setup.py` or component-specific setup scripts
2. **Development**: Use `build_and_test.py` for complete system testing
3. **Testing**: Individual `test_*.py` scripts for component validation
4. **Launch**: Component-specific `launch_*.py` scripts for focused development
5. **Integration**: Full system via `run_full_system.py`