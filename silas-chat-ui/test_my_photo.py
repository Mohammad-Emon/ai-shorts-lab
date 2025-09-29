#!/usr/bin/env python3
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
            
            print("\n✅ Your real face talking head is ready!")
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
