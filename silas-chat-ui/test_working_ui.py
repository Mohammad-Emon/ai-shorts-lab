#!/usr/bin/env python3
"""
Test the working ElevenLabs-style UI
"""

import webbrowser
from pathlib import Path

def test_ui():
    """Open the test UI"""
    print("🧪 Testing ElevenLabs-style UI with Debug")
    print("=" * 50)
    
    ui_file = Path.cwd() / "frontend" / "test-elevenlabs.html"
    
    if ui_file.exists():
        webbrowser.open(f"file://{ui_file}")
        print("✅ Test UI opened!")
        print("\n🔍 Debug Features:")
        print("• Console logging for all interactions")
        print("• Step-by-step state transitions")
        print("• Element detection verification")
        
        print("\n🎯 Test Flow:")
        print("1. Click blue orb → Should show 'Ready to start chatting?'")
        print("2. Click 'Start Chat' → Should show chat interface")
        print("3. Type message → Should show chat bubbles")
        print("4. Click 'End chat' → Should return to blue orb")
        
        print("\n🛠️ If issues persist:")
        print("• Open browser console (F12) to see debug logs")
        print("• Check for JavaScript errors")
        print("• Verify all elements are found")
        
        return True
    else:
        print("❌ Test UI file not found")
        return False

if __name__ == "__main__":
    test_ui()