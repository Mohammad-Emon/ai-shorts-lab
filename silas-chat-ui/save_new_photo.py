#!/usr/bin/env python3
"""
Save New Photo for D-ID
This photo should work much better with D-ID face detection
"""

import os
from pathlib import Path

def save_new_photo():
    """Instructions to save the new photo"""
    
    print("📸 Saving Your New Photo for D-ID")
    print("=" * 40)
    
    print("✅ This photo looks perfect for D-ID!")
    print("• Clear face visibility")
    print("• Good lighting")
    print("• Front-facing angle")
    print("• High quality")
    
    print("\n📋 To use this photo:")
    print("1. Right-click on the photo above")
    print("2. Select 'Save image as...'")
    print("3. Save as: silas-chat-ui/my_photo.jpg")
    print("4. Replace the existing file")
    
    print("\n💡 Why this photo will work better:")
    print("• Much clearer face than the previous one")
    print("• Better lighting and contrast")
    print("• D-ID face detection should work perfectly")
    print("• Professional quality for video generation")
    
    # Check current photo
    current_photo = Path("silas-chat-ui/my_photo.jpg")
    
    if current_photo.exists():
        file_size = current_photo.stat().st_size / 1024
        print(f"\n📁 Current photo: {file_size:.1f} KB")
        print("💡 Replace it with the new photo for better results")
    
    print("\n🎬 After saving the new photo:")
    print("python silas-chat-ui/test_my_photo.py  # Test D-ID generation")
    print("python silas-chat-ui/launch_working_avatar.py  # Launch system")

if __name__ == "__main__":
    save_new_photo()