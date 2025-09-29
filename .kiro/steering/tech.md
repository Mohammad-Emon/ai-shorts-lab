---
inclusion: always
---

# Technology Stack & Development Guidelines

## Core Technologies

### Backend Stack
- **Python 3.8+** with FastAPI for async APIs
- **Uvicorn** ASGI server with WebSocket support
- **Pydantic** models for data validation and API contracts
- **OpenRouter SDK** for free LLM access (Mistral, Gemma, WizardLM)

### Frontend Stack
- **Vanilla JavaScript** - No framework dependencies
- **WebSocket Client** for real-time communication
- **Responsive CSS** with mobile-first design

### AI/ML Integration
- **SadTalker** - Local talking head generation (PyTorch)
- **Wav2Lip** - Lip-sync video processing
- **Azure TTS/Edge TTS** - Voice synthesis
- **DID API** - Cloud avatar services (optional)

## Architecture Patterns

### Multi-Agent System
- **Coordinator Agent** routes queries to specialized agents
- **Specialized Agents** (Researcher, Creative, Technical, Analyst)
- **Summarizer Agent** synthesizes responses
- Agents work in parallel with async/await patterns

### File Organization
- `launch_*.py` - Component startup scripts
- `setup_*.py` - Feature configuration and installation
- `test_*.py` - Component validation scripts
- `*_backend.py` - Service implementations
- `*_style.html` - Themed UI variations

### API Design
- RESTful endpoints with FastAPI automatic documentation
- WebSocket endpoints for real-time features
- Pydantic models for request/response validation
- Graceful error handling with fallback responses

## Development Workflow

### Setup Commands
```bash
# Quick system setup
python setup.py

# Component-specific setup
python setup_openrouter.py
python setup_sadtalker.py

# Complete system test
python build_and_test.py
```

### Testing Strategy
```bash
# Backend API testing
python test_backend.py
python test_openrouter_backend.py

# Component testing
python test_sadtalker_direct.py
python test_voice_system.py
python test_did_api.py

# Frontend testing
python show_ui.py  # Launch test interface
```

### Launch Patterns
```bash
# Full system
python run_full_system.py

# Specific components
python launch_complete_avatar.py
python launch_voice_system.py
python launch_did_style.py
```

## Code Standards

### Python Conventions
- **Type hints** required for all function signatures
- **Async/await** for I/O operations and API calls
- **Pydantic models** for data structures and API contracts
- **Error handling** with try/catch and graceful fallbacks

### Environment Management
- `.env` files for local secrets (never commit)
- `.env.example` templates with required variables
- Environment-specific configurations for dev/prod

### API Integration
- **OpenRouter** for free LLM access with API key rotation
- **Rate limiting** and retry logic for external APIs
- **Fallback models** when primary services fail

## Required Environment Variables
```bash
OPENROUTER_API_KEY=your_key_here
AZURE_SPEECH_KEY=optional_for_tts
DID_API_KEY=optional_for_cloud_avatars
ENVIRONMENT=development
```

## Performance Guidelines
- Use async patterns for concurrent API calls
- Implement caching for repeated LLM requests
- Stream responses for real-time chat experience
- Optimize video generation with proper GPU utilization