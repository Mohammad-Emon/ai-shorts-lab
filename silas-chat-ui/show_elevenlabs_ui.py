#!/usr/bin/env python3
"""
Show the exact ElevenLabs-style Silas Chat UI
"""

import webbrowser
import os
from pathlib import Path

def show_elevenlabs_ui():
    """Open the ElevenLabs-style interface"""
    print("🎨 Opening Silas Chat UI - ElevenLabs Style")
    print("=" * 50)
    
    # Get absolute path to the ElevenLabs-style file
    ui_file = Path.cwd() / "frontend" / "elevenlabs-style.html"
    
    if ui_file.exists():
        # Open in browser
        webbrowser.open(f"file://{ui_file}")
        print("✅ ElevenLabs-style UI opened in browser!")
        
        print("\n🌟 ElevenLabs-Style Features:")
        print("• Exact dark theme with minimal design")
        print("• Centered blue metallic orb with rotation")
        print("• 'Call AI agent' button overlay")
        print("• Clean top bar with SilasLabs branding")
        print("• Smooth state transitions")
        print("• Chat interface with glassmorphism")
        
        print("\n🎭 Interactive Flow:")
        print("1. Click the blue orb to activate")
        print("2. 'Ready to start chatting?' screen")
        print("3. Full chat interface with multi-agent system")
        print("4. 'End chat' returns to main orb")
        
        print("\n✨ Visual Effects:")
        print("• Rotating conic gradient on the orb")
        print("• Radial gradient with metallic shine")
        print("• Subtle glow and shadow effects")
        print("• Smooth hover animations")
        print("• Glassmorphism chat bubbles")
        
        return True
    else:
        print("❌ ElevenLabs-style UI file not found")
        return False

if __name__ == "__main__":
    show_elevenlabs_ui()