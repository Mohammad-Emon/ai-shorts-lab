// Silas Chat UI - Main JavaScript
class SilasChat {
    constructor() {
        this.isConnected = false;
        this.sessionId = this.generateSessionId();
        this.messageHistory = [];
        this.apiBaseUrl = 'http://127.0.0.1:8001';
        this.avatarEnabled = true;
        this.voiceEnabled = true;
        this.currentAudio = null;
        this.multiAgentMode = true;
        
        this.initializeElements();
        this.bindEvents();
        this.initializeChat();
    }

    initializeElements() {
        // Main elements
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.avatarContainer = document.getElementById('avatarContainer');
        this.avatarPlaceholder = document.getElementById('avatarPlaceholder');
        this.charCount = document.getElementById('charCount');
        
        // Control buttons
        this.multiAgentBtn = document.getElementById('multiAgentBtn');
        this.settingsBtn = document.getElementById('settingsBtn');
        this.fullscreenBtn = document.getElementById('fullscreenBtn');
        this.muteBtn = document.getElementById('muteBtn');
        this.cameraBtn = document.getElementById('cameraBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.emojiBtn = document.getElementById('emojiBtn');
    }

    bindEvents() {
        // Message input events
        this.messageInput.addEventListener('input', (e) => this.handleInputChange(e));
        this.messageInput.addEventListener('keypress', (e) => this.handleKeyPress(e));
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Control button events
        this.multiAgentBtn.addEventListener('click', () => this.toggleMultiAgent());
        this.settingsBtn.addEventListener('click', () => this.openSettings());
        this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        this.muteBtn.addEventListener('click', () => this.toggleMute());
        this.cameraBtn.addEventListener('click', () => this.toggleCamera());
        this.voiceBtn.addEventListener('click', () => this.toggleVoiceInput());
        this.emojiBtn.addEventListener('click', () => this.openEmojiPicker());
        
        // Window events
        window.addEventListener('beforeunload', () => this.cleanup());
    }

    async initializeChat() {
        this.showLoading(true);
        
        try {
            // Check backend connection
            const backendConnected = await this.checkBackendConnection();
            
            if (backendConnected) {
                // Get system configuration
                const configResponse = await fetch(`${this.apiBaseUrl}/config`);
                const config = await configResponse.json();
                
                this.avatarEnabled = config.avatar_enabled;
                this.voiceEnabled = config.voice_enabled;
                
                console.log('Connected to Silas backend:', config);
            } else {
                console.warn('Backend not available, using fallback mode');
            }
            
            // Initialize avatar
            await this.initializeAvatar();
            
            // Mark as connected
            this.isConnected = true;
            this.showLoading(false);
            
            // Send welcome message
            setTimeout(() => {
                const welcomeMessage = backendConnected 
                    ? "✨ Welcome! I'm Silas, your multi-agent AI assistant. I have 6 specialized AI agents ready to collaborate on your queries. Try asking me something complex to see the magic happen!"
                    : "👋 Hello! I'm Silas. I'm running in offline mode right now, but I'm still here to chat with you!";
                
                this.addBotMessage(welcomeMessage, {
                    modelUsed: backendConnected ? 'multi-agent-system' : 'offline'
                });
            }, 800);
            
        } catch (error) {
            console.error('Failed to initialize chat:', error);
            this.showError('Failed to connect to Silas. Using offline mode.');
            this.isConnected = true; // Allow offline usage
            this.showLoading(false);
        }
    }

    async initializeAvatar() {
        // Placeholder for D-ID integration
        // In production, this would initialize the D-ID iframe
        const placeholder = this.avatarPlaceholder;
        placeholder.innerHTML = `
            <div class="avatar-ready">
                <div class="avatar-circle">
                    <span>S</span>
                </div>
                <p>Silas is ready</p>
            </div>
        `;
        
        // Add some styling for the ready state
        const style = document.createElement('style');
        style.textContent = `
            .avatar-ready {
                text-align: center;
                color: rgba(255, 255, 255, 0.9);
                position: relative;
                z-index: 2;
            }
            .avatar-circle {
                width: 90px;
                height: 90px;
                border-radius: 50%;
                background: rgba(120, 119, 198, 0.2);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border: 2px solid rgba(120, 119, 198, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px;
                font-size: 36px;
                font-weight: 700;
                box-shadow: 
                    0 20px 40px rgba(120, 119, 198, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
                animation: pulse 3s infinite ease-in-out;
                position: relative;
            }
            .avatar-circle::before {
                content: '';
                position: absolute;
                inset: -3px;
                background: conic-gradient(from 0deg, 
                    rgba(120, 119, 198, 0.8), 
                    rgba(255, 119, 198, 0.8), 
                    rgba(120, 219, 255, 0.8), 
                    rgba(120, 119, 198, 0.8));
                border-radius: 50%;
                z-index: -1;
                animation: rotate 8s linear infinite;
                opacity: 0.6;
            }
            .avatar-ready p {
                font-size: 14px;
                opacity: 0.8;
                font-weight: 500;
            }
        `;
        document.head.appendChild(style);
    }

    handleInputChange(e) {
        const length = e.target.value.length;
        this.charCount.textContent = `${length}/500`;
        
        // Update send button state
        this.sendBtn.disabled = length === 0;
        
        // Change color when approaching limit
        if (length > 450) {
            this.charCount.style.color = '#ef4444';
        } else if (length > 400) {
            this.charCount.style.color = '#f59e0b';
        } else {
            this.charCount.style.color = '#64748b';
        }
    }

    handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.isConnected) return;

        // Add user message to chat
        this.addUserMessage(message);
        
        // Clear input
        this.messageInput.value = '';
        this.handleInputChange({ target: { value: '' } });
        
        // Show typing indicator
        this.showTyping(true);
        
        try {
            // Call backend API
            const response = await fetch(`${this.apiBaseUrl}/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: message,
                    session_id: this.sessionId,
                    use_multi_agent: this.multiAgentMode
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Hide typing indicator
            this.showTyping(false);
            
            // Add bot message with avatar and voice
            this.addBotMessage(data.response, {
                avatarUrl: data.avatar_video_url,
                audioUrl: data.audio_url,
                modelUsed: data.model_used,
                workflowType: data.workflow_type,
                agentsUsed: data.agents_used,
                workflowId: data.workflow_id
            });
            
        } catch (error) {
            console.error('Error getting bot response:', error);
            this.showTyping(false);
            
            // Fallback to local response
            const fallbackResponse = await this.getFallbackResponse(message);
            this.addBotMessage(fallbackResponse);
        }
    }

    addUserMessage(message) {
        const messageElement = this.createMessageElement(message, 'user');
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({
            type: 'user',
            content: message,
            timestamp: new Date().toISOString()
        });
    }

    addBotMessage(message, options = {}) {
        const messageElement = this.createMessageElement(message, 'bot', options);
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
        
        // Play avatar video if available
        if (options.avatarUrl && this.avatarEnabled) {
            this.playAvatarVideo(options.avatarUrl);
        }
        
        // Play voice audio if available
        if (options.audioUrl && this.voiceEnabled) {
            this.playVoiceAudio(options.audioUrl);
        }
        
        // Store in history
        this.messageHistory.push({
            type: 'bot',
            content: message,
            timestamp: new Date().toISOString(),
            modelUsed: options.modelUsed
        });
    }

    createMessageElement(content, type, options = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = type === 'user' ? 'U' : 'S';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const textP = document.createElement('p');
        textP.textContent = content;
        
        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = this.formatTime(new Date());
        
        // Add workflow info if available
        if (type === 'bot' && (options.modelUsed || options.workflowType)) {
            const infoDiv = document.createElement('div');
            infoDiv.className = 'message-info';
            infoDiv.style.fontSize = '10px';
            infoDiv.style.opacity = '0.6';
            infoDiv.style.marginTop = '5px';
            
            let infoText = '';
            
            if (options.workflowType === 'collaborative') {
                infoText = `🤖 Multi-Agent: ${options.agentsUsed?.join(', ') || 'multiple agents'}`;
            } else if (options.workflowType === 'parallel') {
                infoText = `⚡ Parallel: ${options.agentsUsed?.join(', ') || 'multiple agents'}`;
            } else if (options.modelUsed) {
                infoText = `🧠 ${options.modelUsed}`;
            }
            
            if (infoText) {
                infoDiv.textContent = infoText;
                contentDiv.appendChild(infoDiv);
            }
        }
        
        contentDiv.appendChild(textP);
        contentDiv.appendChild(timeSpan);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        
        return messageDiv;
    }

    async getFallbackResponse(userMessage) {
        // Fallback responses when API is unavailable
        const responses = [
            "I'm having some connection issues, but I'm still here to chat!",
            "My connection is a bit spotty, but I can still help you.",
            "I'm working with limited connectivity, but let's keep talking!",
            "Despite some technical difficulties, I'm happy to continue our conversation."
        ];
        
        const lowerMessage = userMessage.toLowerCase();
        
        if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
            return "Hello! I'm experiencing some connection issues, but I'm still here to chat with you.";
        }
        
        if (lowerMessage.includes('help')) {
            return "I'd love to help! I'm having some technical difficulties connecting to my main systems, but I can still have a conversation with you.";
        }
        
        return responses[Math.floor(Math.random() * responses.length)];
    }

    async playAvatarVideo(videoUrl) {
        try {
            // Update avatar container with video
            const videoElement = document.createElement('video');
            videoElement.src = videoUrl;
            videoElement.autoplay = true;
            videoElement.muted = false;
            videoElement.style.width = '100%';
            videoElement.style.height = '100%';
            videoElement.style.objectFit = 'cover';
            
            // Replace placeholder with video
            this.avatarPlaceholder.innerHTML = '';
            this.avatarPlaceholder.appendChild(videoElement);
            
            // Reset to placeholder when video ends
            videoElement.addEventListener('ended', () => {
                setTimeout(() => {
                    this.resetAvatarPlaceholder();
                }, 1000);
            });
            
        } catch (error) {
            console.error('Error playing avatar video:', error);
        }
    }

    async playVoiceAudio(audioUrl) {
        try {
            // Stop current audio if playing
            if (this.currentAudio) {
                this.currentAudio.pause();
                this.currentAudio = null;
            }
            
            // Play new audio
            this.currentAudio = new Audio(audioUrl);
            this.currentAudio.play();
            
            // Update mute button state
            this.muteBtn.textContent = '🔊';
            
        } catch (error) {
            console.error('Error playing voice audio:', error);
        }
    }

    resetAvatarPlaceholder() {
        this.avatarPlaceholder.innerHTML = `
            <div class="avatar-ready">
                <div class="avatar-circle">
                    <span>S</span>
                </div>
                <p>Silas is ready</p>
            </div>
        `;
    }

    async checkBackendConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            return response.ok;
        } catch (error) {
            console.error('Backend connection failed:', error);
            return false;
        }
    }

    showTyping(show) {
        if (show) {
            this.typingIndicator.classList.add('show');
            this.scrollToBottom();
        } else {
            this.typingIndicator.classList.remove('show');
        }
    }

    showLoading(show) {
        if (show) {
            this.loadingOverlay.classList.add('show');
        } else {
            this.loadingOverlay.classList.remove('show');
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message bot-message error';
        errorDiv.innerHTML = `
            <div class="message-avatar">!</div>
            <div class="message-content">
                <p style="color: #ef4444;">${message}</p>
                <span class="message-time">${this.formatTime(new Date())}</span>
            </div>
        `;
        this.chatMessages.appendChild(errorDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    // Control button handlers
    toggleMultiAgent() {
        this.multiAgentMode = !this.multiAgentMode;
        this.multiAgentBtn.style.background = this.multiAgentMode 
            ? 'rgba(16, 185, 129, 0.3)' 
            : 'rgba(255, 255, 255, 0.2)';
        
        const mode = this.multiAgentMode ? 'Multi-Agent' : 'Single Agent';
        this.addSystemMessage(`Switched to ${mode} mode`);
    }

    addSystemMessage(message) {
        const systemDiv = document.createElement('div');
        systemDiv.className = 'system-message';
        systemDiv.style.textAlign = 'center';
        systemDiv.style.padding = '12px 20px';
        systemDiv.style.fontSize = '13px';
        systemDiv.style.color = 'rgba(255, 255, 255, 0.6)';
        systemDiv.style.background = 'rgba(255, 255, 255, 0.05)';
        systemDiv.style.backdropFilter = 'blur(10px)';
        systemDiv.style.webkitBackdropFilter = 'blur(10px)';
        systemDiv.style.border = '1px solid rgba(255, 255, 255, 0.1)';
        systemDiv.style.borderRadius = '16px';
        systemDiv.style.margin = '10px auto';
        systemDiv.style.maxWidth = '300px';
        systemDiv.style.fontWeight = '500';
        systemDiv.textContent = message;
        
        this.chatMessages.appendChild(systemDiv);
        this.scrollToBottom();
    }

    openSettings() {
        alert('Settings panel coming soon!');
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    toggleMute() {
        // Toggle mute state
        const isMuted = this.muteBtn.textContent === '🔇';
        this.muteBtn.textContent = isMuted ? '🔊' : '🔇';
        
        // Mute/unmute current audio
        if (this.currentAudio) {
            this.currentAudio.muted = !isMuted;
        }
        
        // Update voice enabled state
        this.voiceEnabled = isMuted;
    }

    toggleCamera() {
        // Toggle camera state
        const isOff = this.cameraBtn.textContent === '📹';
        this.cameraBtn.textContent = isOff ? '🚫' : '📹';
    }

    toggleVoiceInput() {
        // Placeholder for voice input functionality
        alert('Voice input coming soon!');
    }

    openEmojiPicker() {
        // Simple emoji insertion
        const emojis = ['😊', '😂', '🤔', '👍', '❤️', '🎉', '🔥', '💡'];
        const emoji = emojis[Math.floor(Math.random() * emojis.length)];
        this.messageInput.value += emoji;
        this.handleInputChange({ target: { value: this.messageInput.value } });
        this.messageInput.focus();
    }

    // Utility functions
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    cleanup() {
        // Cleanup when page is unloaded
        if (this.messageHistory.length > 0) {
            localStorage.setItem('silas_chat_history', JSON.stringify(this.messageHistory));
        }
    }
}

// Initialize the chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.silasChat = new SilasChat();
});

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    });
}