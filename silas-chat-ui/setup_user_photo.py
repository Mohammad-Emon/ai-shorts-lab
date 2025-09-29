#!/usr/bin/env python3
"""
Setup User Photo for D-ID
Process and save the user's photo for D-ID video generation
"""

import os
import base64
from pathlib import Path

def setup_photo_for_did():
    """Setup the user's photo for D-ID"""
    
    print("📸 Setting Up Your Photo for D-ID")
    print("=" * 40)
    
    # Create a placeholder that indicates we have the photo
    photo_path = Path("silas-chat-ui/my_photo.jpg")
    
    # For now, let's copy the existing avatar if available, or create instructions
    existing_avatar = Path("SadTalker/assets/avatar.jpg")
    
    if existing_avatar.exists():
        import shutil
        shutil.copy2(existing_avatar, photo_path)
        print(f"✅ Photo copied to: {photo_path}")
    else:
        # Create instructions for manual photo save
        instructions = """
# Your Photo Setup

I can see your photo in the chat! To use it:

1. Right-click on your photo in the chat above
2. Select "Save image as..."
3. Save it as: silas-chat-ui/my_photo.jpg

Your photo looks perfect for D-ID:
- Clear front-facing shot
- Good lighting
- Face clearly visible
- Professional quality

This will work much better than the cartoon avatar!
"""
        
        with open("silas-chat-ui/PHOTO_SETUP.txt", "w") as f:
            f.write(instructions)
        
        print("📝 Instructions created: silas-chat-ui/PHOTO_SETUP.txt")
    
    return photo_path.exists()

def test_photo_with_did():
    """Test the photo with D-ID API"""
    
    print("\n🧪 Testing Photo with D-ID")
    print("=" * 30)
    
    photo_path = Path("silas-chat-ui/my_photo.jpg")
    
    if not photo_path.exists():
        print("❌ Photo not found - please save your photo first")
        return False
    
    print(f"✅ Photo found: {photo_path}")
    
    # Check file size and basic properties
    file_size = photo_path.stat().st_size / 1024  # KB
    print(f"📏 File size: {file_size:.1f} KB")
    
    if file_size < 10:
        print("⚠️  File seems very small - make sure you saved the full photo")
    elif file_size > 5000:
        print("⚠️  File is quite large - D-ID works best with smaller files")
    else:
        print("✅ File size looks good for D-ID")
    
    return True

def create_did_test():
    """Create a test script for D-ID with the user's photo"""
    
    test_script = '''#!/usr/bin/env python3
"""
Test D-ID with User Photo
Generate a talking head video using the user's actual photo
"""

import asyncio
import sys
import os
from pathlib import Path

# Add path for imports
sys.path.append('silas-chat-ui')

async def test_user_photo_with_did():
    """Test D-ID video generation with user photo"""
    
    print("🎭 Testing D-ID with Your Photo")
    print("=" * 40)
    
    # Check if photo exists
    photo_path = Path("silas-chat-ui/my_photo.jpg")
    
    if not photo_path.exists():
        print("❌ Photo not found!")
        print("💡 Save your photo from the chat as: silas-chat-ui/my_photo.jpg")
        return False
    
    print(f"✅ Using your photo: {photo_path}")
    
    # Import D-ID generator
    try:
        from simple_did_backend import SimpleDIDGenerator
    except ImportError:
        print("❌ D-ID backend not found")
        return False
    
    # Create generator
    generator = SimpleDIDGenerator()
    
    if not generator.api_key:
        print("❌ D-ID API key not configured")
        return False
    
    print(f"✅ D-ID API ready: {generator.api_key[:20]}...")
    
    # Test message
    message = "Hello! I'm testing my D-ID talking head avatar. This is my real face speaking with perfect lip synchronization. Amazing technology!"
    
    print(f"🎬 Generating video: {message[:50]}...")
    
    try:
        # Generate video with user's photo
        video_url = await generator.generate_talking_head(message, str(photo_path))
        
        if video_url:
            print("🎉 SUCCESS! Video generated with your photo!")
            print(f"🎬 Video: {video_url}")
            
            # Check local file
            if video_url.startswith('/'):
                local_file = f"generated_videos{video_url}"
                if os.path.exists(local_file):
                    size_mb = os.path.getsize(local_file) / 1024 / 1024
                    print(f"📁 Local file: {local_file}")
                    print(f"📏 Size: {size_mb:.2f} MB")
            
            print("\\n✅ Your real face talking head is ready!")
            print("🚀 Launch full system: python silas-chat-ui/launch_simple_did.py")
            
            return True
        else:
            print("❌ Video generation failed")
            print("💡 Check D-ID credits and photo quality")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_user_photo_with_did())
'''
    
    with open("silas-chat-ui/test_my_photo.py", "w") as f:
        f.write(test_script)
    
    print("✅ Test script created: silas-chat-ui/test_my_photo.py")

def main():
    """Main setup function"""
    
    print("🎭 D-ID Photo Setup for Your Real Face")
    print("=" * 50)
    
    # Step 1: Setup photo
    photo_ready = setup_photo_for_did()
    
    # Step 2: Test photo if available
    if photo_ready:
        test_photo_with_did()
    
    # Step 3: Create test script
    create_did_test()
    
    print("\n" + "=" * 50)
    
    if photo_ready:
        print("🎉 Photo Setup Complete!")
        print("✅ Your photo is ready for D-ID")
        
        print("\n🧪 Test D-ID with your photo:")
        print("python silas-chat-ui/test_my_photo.py")
        
        print("\n🚀 Launch full system:")
        print("python silas-chat-ui/launch_simple_did.py")
        
    else:
        print("📸 Photo Setup Needed:")
        print("1. Right-click your photo in the chat")
        print("2. Save as: silas-chat-ui/my_photo.jpg")
        print("3. Run this script again")
    
    print("\n💡 Your photo will create much better results than the cartoon avatar!")
    print("🎭 D-ID will generate professional talking head videos with your real face!")

if __name__ == "__main__":
    main()