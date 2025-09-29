#!/usr/bin/env python3
"""
Show D-ID Style Visual Agent Interface
"""

import webbrowser
from pathlib import Path

def show_visual_agent():
    """Open the D-ID style visual agent interface"""
    print("🎭 Opening Silas Visual Agent - D-ID Style")
    print("=" * 50)
    
    # Get absolute path to D-ID style interface
    ui_file = Path.cwd() / "frontend" / "did-style.html"
    
    if ui_file.exists():
        # Open in browser
        webbrowser.open(f"file://{ui_file}")
        print("✅ D-ID style visual agent opened!")
        
        print("\n🌟 D-ID Style Features:")
        print("• Realistic talking avatar layout")
        print("• Side-by-side video + chat interface")
        print("• Glassmorphism chat panel")
        print("• Real-time conversation flow")
        print("• OpenRouter LLM integration")
        print("• SadTalker video generation ready")
        
        print("\n🎯 Interface Layout:")
        print("• Left: Avatar video area with controls")
        print("• Right: Glassmorphism chat panel")
        print("• Status indicator shows system state")
        print("• Message input with send button")
        
        print("\n🔧 To Complete Setup:")
        print("1. Start backend: python run_full_system.py")
        print("2. Install SadTalker: python setup_sadtalker.py")
        print("3. Test visual conversations")
        
        return True
    else:
        print("❌ D-ID style interface file not found")
        return False

if __name__ == "__main__":
    show_visual_agent()