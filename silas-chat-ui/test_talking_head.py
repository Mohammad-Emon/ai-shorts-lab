#!/usr/bin/env python3
"""
Test Talking Head Video Generation
Specific test for realistic lip-sync talking head videos
"""

import subprocess
import time
import sys
import requests
import json

def test_talking_head():
    """Test enhanced talking head video generation"""
    
    print("🎬 Testing Enhanced Talking Head Generation")
    print("=" * 50)
    
    # Start backend
    print("🚀 Starting enhanced SadTalker backend...")
    backend_process = subprocess.Popen([
        sys.executable, "silas-chat-ui/sadtalker_backend.py"
    ])
    
    time.sleep(8)  # Give more time for startup
    
    try:
        # Test talking head generation
        test_message = "Hello! I am your realistic AI avatar with enhanced lip-sync technology. Watch my mouth move as I speak these words!"
        
        print(f"🎭 Testing talking head with message:")
        print(f"   '{test_message}'")
        
        response = requests.post(
            "http://127.0.0.1:8002/generate-avatar",
            json={
                "message": test_message,
                "session_id": "talking_head_test",
                "generate_video": True,
                "video_quality": "hd"
            },
            timeout=120  # Longer timeout for video generation
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Talking Head Generation Results:")
            print(f"   AI Response: {result['response'][:60]}...")
            print(f"   Video URL: {result.get('video_url', 'None')}")
            print(f"   Generation Time: {result.get('generation_time', 0):.2f}s")
            
            if result.get('video_url'):
                print(f"\n🎉 SUCCESS! Talking head video generated!")
                print(f"   Video file: {result['video_url']}")
                print(f"   This video should show:")
                print(f"   • Real human face from avatar image")
                print(f"   • Moving lips synchronized with speech")
                print(f"   • Natural head movements and blinking")
                print(f"   • Enhanced mouth animation based on audio")
                
                # Test video accessibility
                video_response = requests.get(f"http://127.0.0.1:8002{result['video_url']}")
                if video_response.status_code == 200:
                    print(f"   ✅ Video file accessible ({len(video_response.content)} bytes)")
                else:
                    print(f"   ❌ Video file not accessible")
            else:
                print(f"\n⚠️  No video generated - check backend logs")
        else:
            print(f"❌ Request failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
        
        # Test system status
        print(f"\n🔍 System Status:")
        status_response = requests.get("http://127.0.0.1:8002/health")
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"   Backend: {status['status']}")
            print(f"   SadTalker: {'✅' if status['sadtalker_available'] else '❌'}")
            print(f"   OpenRouter: {'✅' if status['openrouter_configured'] else '❌'}")
            print(f"   Video Gen: {status['video_generation']}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        # Cleanup
        print(f"\n🛑 Stopping backend...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except:
            backend_process.kill()
        print("✅ Backend stopped")
    
    print(f"\n🎭 Talking Head Test Complete!")
    print("=" * 50)
    print("If successful, you should now have:")
    print("• Enhanced talking head video with lip-sync")
    print("• Real human face with moving mouth")
    print("• Natural head movements and blinking")
    print("• Audio-synchronized lip animation")
    print("\nOpen the D-ID interface and send a message to see it in action!")

if __name__ == "__main__":
    test_talking_head()