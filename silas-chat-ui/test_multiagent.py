#!/usr/bin/env python3
"""
Test Multi-Agent System
Test the OpenRouter multi-agent workflow
"""

import subprocess
import time
import sys
import requests
import json

def test_multiagent():
    """Test multi-agent workflow"""
    
    print("🤖 Testing Multi-Agent Workflow")
    print("=" * 40)
    
    # Start backend
    print("🚀 Starting backend...")
    backend_process = subprocess.Popen([
        sys.executable, "silas-chat-ui/sadtalker_backend.py"
    ])
    
    time.sleep(5)
    
    try:
        # Test different types of messages to trigger different agents
        test_cases = [
            {
                "name": "Creative Request",
                "message": "Tell me a creative story about AI avatars",
                "expected_agent": "creative"
            },
            {
                "name": "Technical Question", 
                "message": "How does video generation work in code?",
                "expected_agent": "technical"
            },
            {
                "name": "Research Query",
                "message": "What is the latest information about AI technology?",
                "expected_agent": "research"
            },
            {
                "name": "Casual Chat",
                "message": "Hi there! How are you doing today?",
                "expected_agent": "conversational"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: {test_case['name']}")
            print(f"   Message: {test_case['message']}")
            
            try:
                response = requests.post(
                    "http://127.0.0.1:8002/generate-avatar",
                    json={
                        "message": test_case['message'],
                        "session_id": f"test_{i}",
                        "generate_video": False  # Focus on AI response
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Response: {result['response']}")
                    print(f"   Time: {result.get('generation_time', 0):.2f}s")
                else:
                    print(f"❌ Failed: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\n🎉 Multi-Agent Test Complete!")
        
    finally:
        # Cleanup
        print(f"\n🛑 Stopping backend...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except:
            backend_process.kill()
        print("✅ Backend stopped")

if __name__ == "__main__":
    test_multiagent()