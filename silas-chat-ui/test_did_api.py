#!/usr/bin/env python3
"""
Test D-ID API directly
Verify the API key and basic functionality
"""

import os
import asyncio
import requests
from dotenv import load_dotenv

async def test_did_api():
    """Test D-ID API directly"""
    
    print("🧪 Testing D-ID API")
    print("=" * 30)
    
    # Load environment
    load_dotenv("silas-chat-ui/.env")
    
    api_key = os.getenv("DID_API_KEY")
    
    if not api_key:
        print("❌ D-ID API key not found in .env file")
        return False
    
    print(f"✅ D-ID API key loaded: {api_key[:20]}...")
    
    # Test API connection
    base_url = "https://api.d-id.com"
    
    try:
        # Test with a simple API call
        headers = {
            "Authorization": f"Basic {api_key}",
            "Accept": "application/json"
        }
        
        print("🔄 Testing D-ID API connection...")
        
        # Test with credits endpoint instead
        response = requests.get(
            f"{base_url}/credits",
            headers=headers,
            timeout=10
        )
        
        print(f"📡 API Response: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ D-ID API connection successful!")
            return True
        elif response.status_code == 401:
            print("❌ D-ID API key invalid or expired")
            print("💡 Check your API key at: https://studio.d-id.com/account-settings")
            return False
        else:
            print(f"⚠️  D-ID API returned: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ D-ID API test failed: {e}")
        return False

async def test_photo_upload():
    """Test photo upload to D-ID"""
    
    print("\n📸 Testing Photo Upload")
    print("=" * 30)
    
    # Load environment
    load_dotenv("silas-chat-ui/.env")
    api_key = os.getenv("DID_API_KEY")
    
    if not api_key:
        print("❌ No API key")
        return False
    
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
        print("💡 Save your photo as 'silas-chat-ui/my_photo.jpg'")
        return False
    
    print(f"✅ Using photo: {user_photo}")
    
    try:
        headers = {
            "Authorization": f"Basic {api_key}",
            "Accept": "application/json"
        }
        
        with open(user_photo, 'rb') as f:
            files = {"image": (os.path.basename(user_photo), f, "image/jpeg")}
            
            print("🔄 Uploading photo to D-ID...")
            
            response = requests.post(
                "https://api.d-id.com/images",
                headers=headers,
                files=files,
                timeout=30
            )
        
        print(f"📡 Upload Response: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            image_url = data.get("url")
            print(f"✅ Photo uploaded successfully!")
            print(f"🔗 Image URL: {image_url}")
            return image_url
        else:
            print(f"❌ Photo upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Photo upload error: {e}")
        return False

async def main():
    """Main test function"""
    
    print("🎭 D-ID API Complete Test")
    print("=" * 40)
    
    # Test 1: API connection
    api_ok = await test_did_api()
    
    # Test 2: Photo upload
    if api_ok:
        photo_ok = await test_photo_upload()
    else:
        photo_ok = False
    
    print("\n" + "=" * 40)
    print("🎯 Test Results:")
    print(f"D-ID API Connection: {'✅ Working' if api_ok else '❌ Failed'}")
    print(f"Photo Upload: {'✅ Working' if photo_ok else '❌ Failed'}")
    
    if api_ok and photo_ok:
        print("\n🎉 D-ID API is ready for video generation!")
        print("✅ Your API key works")
        print("✅ Photo upload successful")
        print("✅ Ready to create talking head videos")
        
        print("\n🚀 Next step:")
        print("python silas-chat-ui/launch_simple_did.py")
        
    elif api_ok:
        print("\n⚠️  API works but photo upload failed")
        print("💡 Check your photo file and try again")
        
    else:
        print("\n❌ D-ID API setup needed")
        print("💡 Check your API key and credits")
        print("🔗 Visit: https://studio.d-id.com/account-settings")

if __name__ == "__main__":
    asyncio.run(main())