#!/usr/bin/env python3
"""
Save User Photo for D-ID
Help save your photo from the chat for D-ID video generation
"""

import os
from pathlib import Path

def save_user_photo():
    """Instructions to save user photo"""
    
    print("📸 Save Your Photo for D-ID Avatar")
    print("=" * 40)
    
    print("🎯 I can see your photo in the chat above!")
    print("To use it for D-ID talking head videos:")
    
    print("\n📋 Step-by-Step Instructions:")
    print("1. Right-click on your photo in the chat")
    print("2. Select 'Save image as...'")
    print("3. Navigate to the 'silas-chat-ui' folder")
    print("4. Save it as 'my_photo.jpg' (exactly this name)")
    
    print("\n📏 Photo Requirements for D-ID:")
    print("• Clear front-facing photo")
    print("• Face clearly visible and well-lit")
    print("• At least 256x256 pixels")
    print("• Good quality (not blurry)")
    print("• Face takes up most of the frame")
    print("• No sunglasses or face coverings")
    
    print("\n💡 D-ID Face Detection:")
    print("• D-ID needs to detect a clear human face")
    print("• The current avatar.jpg is too simple for D-ID")
    print("• Your real photo will work perfectly")
    
    # Check if photo exists
    target_path = Path("silas-chat-ui/my_photo.jpg")
    
    if target_path.exists():
        print(f"\n✅ Photo found: {target_path}")
        
        # Get file info
        file_size = target_path.stat().st_size / 1024  # KB
        print(f"📏 File size: {file_size:.1f} KB")
        
        print("\n🎉 Ready for D-ID video generation!")
        print("Run: python silas-chat-ui/test_did_video.py")
        
        return True
    else:
        print(f"\n📸 Please save your photo as: {target_path}")
        print("Then run this script again to verify")
        
        # Create a reminder file
        reminder = f"""
# Photo Setup Reminder

Save your photo from the chat as: {target_path}

Requirements:
- Clear front-facing photo
- Face clearly visible
- Good lighting
- At least 256x256 pixels

After saving, run:
python silas-chat-ui/save_user_photo.py

Then test D-ID:
python silas-chat-ui/test_did_video.py
"""
        
        with open("silas-chat-ui/PHOTO_REMINDER.txt", "w") as f:
            f.write(reminder)
        
        print("📝 Reminder saved to: silas-chat-ui/PHOTO_REMINDER.txt")
        
        return False

def test_photo_for_did():
    """Test if photo is suitable for D-ID"""
    
    photo_path = Path("silas-chat-ui/my_photo.jpg")
    
    if not photo_path.exists():
        print("❌ Photo not found")
        return False
    
    try:
        from PIL import Image
        
        # Open and check the photo
        img = Image.open(photo_path)
        width, height = img.size
        
        print(f"\n🔍 Photo Analysis:")
        print(f"📏 Dimensions: {width}x{height}")
        print(f"📊 Format: {img.format}")
        print(f"🎨 Mode: {img.mode}")
        
        # Check D-ID requirements
        issues = []
        
        if width < 256 or height < 256:
            issues.append("Resolution too low for D-ID (minimum 256x256)")
        
        if width < 512 or height < 512:
            issues.append("Consider higher resolution for better D-ID results")
        
        if img.mode not in ['RGB', 'RGBA']:
            issues.append("Color mode may cause D-ID issues")
        
        if issues:
            print("\n⚠️  Recommendations:")
            for issue in issues:
                print(f"• {issue}")
        else:
            print("\n✅ Photo looks perfect for D-ID!")
        
        print("\n🎭 D-ID Face Detection:")
        print("• D-ID will analyze your photo for face detection")
        print("• Clear, front-facing photos work best")
        print("• Good lighting improves success rate")
        
        return True
        
    except ImportError:
        print("⚠️  PIL not available for photo analysis")
        print("✅ Photo exists and should work with D-ID")
        return True
    except Exception as e:
        print(f"❌ Error analyzing photo: {e}")
        return False

if __name__ == "__main__":
    print("📸 D-ID Photo Setup Assistant")
    print("=" * 50)
    
    # Check if photo is saved
    photo_saved = save_user_photo()
    
    # If photo exists, analyze it
    if photo_saved:
        test_photo_for_did()
        
        print("\n🚀 Next Steps:")
        print("1. python silas-chat-ui/test_did_video.py  # Test video generation")
        print("2. python silas-chat-ui/launch_simple_did.py  # Launch full system")
    else:
        print("\n📸 Save your photo first, then run this script again!")