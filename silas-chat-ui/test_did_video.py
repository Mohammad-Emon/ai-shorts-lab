#!/usr/bin/env python3
"""
Test D-ID Video Generation
Create a real talking head video with your photo
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the current directory to path
sys.path.append('silas-chat-ui')

async def test_video_generation():
    """Test actual D-ID video generation"""
    
    print("🎬 Testing D-ID Video Generation")
    print("=" * 40)
    
    # Load environment
    load_dotenv("silas-chat-ui/.env")
    
    # Import the D-ID generator
    from simple_did_backend import SimpleDIDGenerator
    
    # Create generator
    generator = SimpleDIDGenerator()
    
    if not generator.api_key:
        print("❌ D-ID API key not found")
        return False
    
    print(f"✅ D-ID API key loaded: {generator.api_key[:20]}...")
    
    # Check for photo
    photo_paths = [
        "silas-chat-ui/my_photo.jpg",
        "SadTalker/assets/avatar.jpg"
    ]
    
    user_photo = None
    for photo_path in photo_paths:
        if os.path.exists(photo_path):
            user_photo = photo_path
            break
    
    if not user_photo:
        print("❌ No user photo found")
        return False
    
    print(f"✅ Using photo: {user_photo}")
    
    # Test message
    test_message = "Hello! I'm your D-ID powered AI avatar. Watch me speak with your real face and perfect lip synchronization. This is a test of professional talking head video generation!"
    
    print(f"🎭 Generating video with message: {test_message[:50]}...")
    
    try:
        # Generate video
        video_url = await generator.generate_talking_head(test_message, user_photo)
        
        if video_url:
            print(f"✅ Video generated successfully!")
            print(f"🎬 Video URL: {video_url}")
            
            # Check if video file exists locally
            if video_url.startswith('/'):
                local_path = f"generated_videos{video_url}"
                if os.path.exists(local_path):
                    file_size = os.path.getsize(local_path) / 1024 / 1024  # MB
                    print(f"📁 Local file: {local_path}")
                    print(f"📏 File size: {file_size:.2f} MB")
            
            return True
        else:
            print("❌ Video generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Video generation error: {e}")
        return False

async def main():
    """Main test function"""
    
    print("🎭 D-ID Talking Head Video Test")
    print("=" * 50)
    
    success = await test_video_generation()
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 SUCCESS! D-ID Video Generation Working!")
        print("✅ Your API key is valid")
        print("✅ Photo upload successful")
        print("✅ Video generation complete")
        print("✅ Real talking head created!")
        
        print("\n🚀 Ready to use:")
        print("python silas-chat-ui/launch_simple_did.py")
        
        print("\n💡 In the browser interface:")
        print("1. Type any message")
        print("2. Watch D-ID generate your talking head video")
        print("3. See your real face speak with perfect lip-sync!")
        
    else:
        print("❌ Video generation test failed")
        print("💡 Check your D-ID credits and API key")

if __name__ == "__main__":
    asyncio.run(main())