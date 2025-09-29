
// Real Face Video Handler
class RealFaceVideoHandler {
    constructor() {
        this.isRealFace = false;
    }
    
    async playRealFaceVideo(videoUrl, text) {
        console.log('🎭 Playing REAL FACE video:', videoUrl);
        
        // Hide any cartoon placeholders
        const placeholders = document.querySelectorAll('.placeholder-avatar, .avatar-placeholder');
        placeholders.forEach(p => p.style.display = 'none');
        
        // Create or get video element
        let video = document.getElementById('realFaceVideo');
        if (!video) {
            video = document.createElement('video');
            video.id = 'realFaceVideo';
            video.style.cssText = `
                width: 100%;
                height: 100%;
                object-fit: cover;
                border-radius: 20px;
                z-index: 10;
            `;
            video.autoplay = true;
            video.muted = false;
            video.playsInline = true;
            
            const container = document.getElementById('talkingHeadContainer') || 
                            document.getElementById('avatarContainer');
            if (container) {
                container.appendChild(video);
            }
        }
        
        // Set video source and play
        video.src = `http://127.0.0.1:8002${videoUrl}`;
        video.style.display = 'block';
        this.isRealFace = true;
        
        // Handle video events
        video.onloadeddata = () => {
            console.log('✅ Real face video loaded');
            video.play().catch(e => {
                console.log('Autoplay prevented:', e);
                this.showPlayButton(video);
            });
        };
        
        video.onended = () => {
            console.log('🏁 Real face video ended');
            setTimeout(() => {
                video.style.display = 'none';
                this.isRealFace = false;
            }, 1000);
        };
        
        return video;
    }
    
    showPlayButton(video) {
        const playBtn = document.createElement('div');
        playBtn.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            border-radius: 50%;
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 20;
            font-size: 30px;
            color: white;
        `;
        playBtn.innerHTML = '▶️';
        playBtn.onclick = () => {
            video.play();
            playBtn.remove();
        };
        
        video.parentElement.appendChild(playBtn);
    }
}

// Initialize real face handler
window.realFaceHandler = new RealFaceVideoHandler();
