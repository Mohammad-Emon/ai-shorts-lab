#!/usr/bin/env python3
"""
Test script for Silas Chat UI backend
"""

import requests
import json
import time

def test_backend():
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Silas Chat UI Backend")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Configuration
    try:
        print("\n2. Testing configuration endpoint...")
        response = requests.get(f"{base_url}/config", timeout=5)
        if response.status_code == 200:
            config = response.json()
            print("✅ Configuration loaded")
            print(f"   Multi-agent: {config.get('features', {}).get('multi_agent_workflow', False)}")
            print(f"   OpenRouter: {config.get('openrouter_configured', False)}")
        else:
            print(f"❌ Configuration failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
    
    # Test 3: Agents list
    try:
        print("\n3. Testing agents endpoint...")
        response = requests.get(f"{base_url}/agents", timeout=5)
        if response.status_code == 200:
            agents = response.json()
            print("✅ Agents loaded")
            print(f"   Available agents: {len(agents.get('agents', []))}")
            for agent in agents.get('agents', [])[:3]:  # Show first 3
                print(f"   - {agent['role']}: {agent['description'][:50]}...")
        else:
            print(f"❌ Agents failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Agents failed: {e}")
    
    # Test 4: Chat message (without OpenRouter key)
    try:
        print("\n4. Testing chat message (fallback mode)...")
        message_data = {
            "content": "Hello, test message!",
            "session_id": "test_session_123",
            "use_multi_agent": False  # Use fallback mode
        }
        
        response = requests.post(
            f"{base_url}/message", 
            json=message_data,
            timeout=10
        )
        
        if response.status_code == 200:
            chat_response = response.json()
            print("✅ Chat message processed")
            print(f"   Response: {chat_response['response'][:100]}...")
            print(f"   Workflow: {chat_response.get('workflow_type', 'N/A')}")
        else:
            print(f"❌ Chat message failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Chat message failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Backend testing complete!")
    print("\n📝 Next steps:")
    print("1. Get OpenRouter API key: https://openrouter.ai/keys")
    print("2. Update backend/.env with your key")
    print("3. Open frontend/index.html in browser")
    print("4. Test the full multi-agent system!")
    
    return True

if __name__ == "__main__":
    test_backend()