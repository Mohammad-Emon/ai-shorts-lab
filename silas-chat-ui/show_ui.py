#!/usr/bin/env python3
"""
Show the Silas Chat UI Glassmorphism Demo
"""

import webbrowser
import os
from pathlib import Path
import time

def show_ui():
    """Open the glassmorphism demo in browser"""
    print("🎨 Opening Silas Chat UI - Glassmorphism Demo")
    print("=" * 50)
    
    # Get absolute path to demo file
    demo_file = Path.cwd() / "demo.html"
    
    if demo_file.exists():
        # Open in browser
        webbrowser.open(f"file://{demo_file}")
        print("✅ Demo opened in browser!")
        
        print("\n🌟 Glassmorphism Features:")
        print("• Dark theme with animated background")
        print("• Glass morphism effects with backdrop blur")
        print("• Translucent containers and buttons")
        print("• Animated gradients and particles")
        print("• Multi-agent workflow indicators")
        print("• Smooth hover and transition effects")
        
        print("\n🎭 Interactive Elements:")
        print("• Hover over buttons to see glow effects")
        print("• Notice the rotating gradient on avatar")
        print("• Glass morphism message bubbles")
        print("• Animated typing indicator")
        print("• Translucent input container")
        
        print("\n📱 Also try:")
        main_ui = Path.cwd() / "frontend" / "index.html"
        if main_ui.exists():
            print(f"Full interactive UI: file://{main_ui}")
            
            # Ask if user wants to open the full UI too
            response = input("\nOpen full interactive UI too? (y/n): ").lower().strip()
            if response == 'y':
                webbrowser.open(f"file://{main_ui}")
                print("✅ Full UI opened!")
        
        return True
    else:
        print("❌ Demo file not found")
        return False

if __name__ == "__main__":
    show_ui()