#!/usr/bin/env python3
"""
Save Your Photo for Real Face Avatar
Helps you set up your photo for SadTalker talking head generation
"""

import os
import shutil
from pathlib import Path

def save_user_photo():
    """Instructions and setup for user photo"""
    
    print("📸 Setting Up Your Photo for Real Face Avatar")
    print("=" * 50)
    
    print("\n🎯 To use your real face in the talking head:")
    print("1. Take or find a clear photo of yourself")
    print("2. Make sure it's front-facing and well-lit")
    print("3. Save it as 'my_photo.jpg' in the silas-chat-ui folder")
    
    print("\n📋 Photo Requirements:")
    print("• Format: JPG, JPEG, or PNG")
    print("• Size: At least 256x256 pixels (512x512 recommended)")
    print("• Face should be clearly visible")
    print("• Good lighting (avoid shadows)")
    print("• Front-facing (not profile)")
    print("• Neutral expression works best")
    
    print("\n💡 Photo Tips:")
    print("• Use a passport-style photo")
    print("• Face should take up most of the frame")
    print("• Avoid sunglasses or face coverings")
    print("• Plain background works better")
    print("• Higher resolution = better results")
    
    # Check if photo already exists
    photo_path = Path("silas-chat-ui/my_photo.jpg")
    
    if photo_path.exists():
        print(f"\n✅ Photo found: {photo_path}")
        print(f"📏 File size: {photo_path.stat().st_size / 1024:.1f} KB")
        
        # Copy to SadTalker assets
        assets_dir = Path("SadTalker/assets")
        assets_dir.mkdir(exist_ok=True)
        
        target_path = assets_dir / "avatar.jpg"
        shutil.copy2(photo_path, target_path)
        print(f"✅ Photo copied to SadTalker: {target_path}")
        
        print("\n🎉 Your photo is ready for real face generation!")
        print("Run: python silas-chat-ui/launch_real_face_avatar.py")
        
    else:
        print(f"\n📸 Please save your photo as: {photo_path}")
        print("Then run this script again to verify setup")
        
        # Create example instructions file
        instructions = """
# Photo Setup Instructions

1. Save your photo as 'silas-chat-ui/my_photo.jpg'

2. Photo should be:
   - Clear front-facing shot
   - Good lighting
   - At least 256x256 pixels
   - Face clearly visible
   - Neutral expression

3. After saving, run:
   python silas-chat-ui/save_my_photo.py

4. Then launch the system:
   python silas-chat-ui/launch_real_face_avatar.py

Your real face will be used to generate talking head videos!
"""
        
        with open("silas-chat-ui/photo_setup_instructions.txt", "w") as f:
            f.write(instructions)
        
        print("📝 Instructions saved to: silas-chat-ui/photo_setup_instructions.txt")

def test_photo_quality():
    """Test if the photo is suitable for SadTalker"""
    
    photo_path = Path("silas-chat-ui/my_photo.jpg")
    
    if not photo_path.exists():
        print("❌ Photo not found")
        return False
    
    try:
        from PIL import Image
        
        # Open and analyze the photo
        img = Image.open(photo_path)
        width, height = img.size
        
        print(f"\n🔍 Photo Analysis:")
        print(f"📏 Dimensions: {width}x{height}")
        print(f"📊 Format: {img.format}")
        print(f"🎨 Mode: {img.mode}")
        
        # Check quality
        issues = []
        
        if width < 256 or height < 256:
            issues.append("Resolution too low (minimum 256x256)")
        
        if width != height:
            issues.append("Photo is not square (may be cropped)")
        
        if img.mode not in ['RGB', 'RGBA']:
            issues.append("Color mode may cause issues")
        
        if issues:
            print("\n⚠️  Potential Issues:")
            for issue in issues:
                print(f"• {issue}")
            print("\n💡 Consider using a higher quality square photo")
        else:
            print("\n✅ Photo looks good for SadTalker!")
        
        return len(issues) == 0
        
    except ImportError:
        print("⚠️  PIL not available for photo analysis")
        return True
    except Exception as e:
        print(f"❌ Error analyzing photo: {e}")
        return False

if __name__ == "__main__":
    save_user_photo()
    
    # Test photo quality if available
    if Path("silas-chat-ui/my_photo.jpg").exists():
        test_photo_quality()