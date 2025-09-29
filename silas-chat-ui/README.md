# Silas Chat UI - AI Avatar Chat System

A modern chat interface featuring free LLM integration, avatar video generation, and voice synthesis.

## 🚀 Features

- **Multi-Agent AI System**: Specialized AI agents collaborate on complex queries
- **Free LLM Integration**: Uses OpenRouter's free models (Mistral, Gemma, WizardLM, etc.)
- **Avatar Video Generation**: SadTalker integration for talking avatar videos
- **Voice Synthesis**: Free TTS for voice responses
- **Real-time Chat**: WebSocket and REST API support
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Session Management**: Persistent chat history
- **Fallback Mode**: Works offline with local responses

### 🤖 Multi-Agent Workflow

The system includes specialized AI agents:

- **Coordinator Agent**: Routes queries and synthesizes responses
- **Research Agent**: Gathers factual information and data
- **Creative Agent**: Generates creative ideas and content
- **Technical Agent**: Solves programming and technical problems
- **Analyst Agent**: Analyzes data and provides insights
- **Summarizer Agent**: Synthesizes multi-agent responses

**Workflow Types:**
- **Single Agent**: Simple queries handled by one specialist
- **Parallel**: Multiple agents work simultaneously
- **Collaborative**: Agents work sequentially, building on each other's responses

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: FastAPI (Python)
- **LLM**: OpenRouter (free models)
- **Avatar**: SadTalker (free)
- **Voice**: Azure TTS / Edge TTS (free)
- **Deployment**: Vercel (frontend), Railway (backend)

## 📂 Project Structure

```
silas-chat-ui/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── assets/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── config/
└── README.md
```

## 🚀 Quick Start

### 1. Setup Backend
```bash
cd backend
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Add your OpenRouter API key to .env
# Get free key from: https://openrouter.ai/keys
echo "OPENROUTER_API_KEY=your_key_here" >> .env

# Run backend
uvicorn main:app --reload
```

### 2. Setup Frontend
```bash
cd frontend
# Open index.html in browser or use live server
# Or use Python's built-in server:
python -m http.server 3000
```

### 3. Get Free API Keys

**OpenRouter (Required for LLM)**
- Visit [OpenRouter](https://openrouter.ai/keys)
- Sign up and get free API key
- Free models: Mistral 7B, Gemma 7B, WizardLM, etc.

**Optional Integrations**
- **SadTalker**: For avatar videos (can run locally)
- **Azure Speech**: For voice synthesis (free tier available)

## 🎯 Development Phases

- [x] Phase 1: Planning & Setup
- [ ] Phase 2: Frontend Development
- [ ] Phase 3: Backend Development
- [ ] Phase 4: Database Integration
- [ ] Phase 5: Authentication
- [ ] Phase 6: Admin Dashboard
- [ ] Phase 7: Deployment & Testing
- [ ] Phase 8: Launch & Scale