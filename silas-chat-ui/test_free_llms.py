#!/usr/bin/env python3
"""
Test Free LLM APIs - Google Gemini and Groq
Quick test to verify API keys and responses
"""

import asyncio
import os
from pathlib import Path

async def test_gemini():
    """Test Google Gemini API"""
    
    print("🔹 Testing Google Gemini...")
    
    try:
        import google.generativeai as genai
        
        google_key = os.getenv("GOOGLE_API_KEY")
        if not google_key:
            print("❌ GOOGLE_API_KEY not found in environment")
            return False
        
        genai.configure(api_key=google_key)
        model = genai.GenerativeModel('gemini-pro')
        
        test_prompt = "You are Silas, a realistic AI avatar. Say hello and mention your video generation capabilities in one sentence."
        
        response = await asyncio.to_thread(model.generate_content, test_prompt)
        
        if response and response.text:
            print(f"✅ Gemini Response: {response.text.strip()}")
            return True
        else:
            print("❌ Gemini returned empty response")
            return False
            
    except ImportError:
        print("❌ google-generativeai package not installed")
        print("💡 Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return False

async def test_groq():
    """Test Groq API"""
    
    print("\n🔹 Testing Groq...")
    
    try:
        from groq import Groq
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            print("❌ GROQ_API_KEY not found in environment")
            return False
        
        client = Groq(api_key=groq_key)
        
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are Silas, a realistic AI avatar that creates talking head videos."
                },
                {
                    "role": "user",
                    "content": "Say hello and mention your video capabilities in one sentence."
                }
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        if response.choices and response.choices[0].message:
            print(f"✅ Groq Response: {response.choices[0].message.content.strip()}")
            return True
        else:
            print("❌ Groq returned empty response")
            return False
            
    except ImportError:
        print("❌ groq package not installed")
        print("💡 Run: pip install groq")
        return False
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return False

async def test_free_llm_backend():
    """Test the integrated free LLM backend"""
    
    print("\n🔹 Testing Integrated Free LLM Backend...")
    
    try:
        # Import the free LLM backend
        import sys
        sys.path.append('silas-chat-ui')
        from free_llm_backend import get_ai_response
        
        test_messages = [
            "Hello! Can you generate a video?",
            "Test my real face avatar",
            "How does your AI work?"
        ]
        
        for message in test_messages:
            print(f"\n📝 Testing: {message}")
            response = await get_ai_response(message)
            print(f"🤖 Response: {response}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Free LLM backend import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Free LLM backend error: {e}")
        return False

def check_environment():
    """Check environment setup"""
    
    print("🔍 Checking Environment Setup...")
    
    # Check .env file
    env_file = Path("silas-chat-ui/.env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv(env_file)
        
        # Check API keys
        google_key = os.getenv("GOOGLE_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")
        
        print(f"🔑 Google API Key: {'✅ Set' if google_key else '❌ Missing'}")
        print(f"🔑 Groq API Key: {'✅ Set' if groq_key else '❌ Missing'}")
        
        return bool(google_key or groq_key)
    else:
        print("❌ .env file not found")
        print("💡 Run: python silas-chat-ui/setup_free_llm_apis.py")
        return False

async def main():
    """Main test function"""
    
    print("🧪 Testing Free LLM APIs")
    print("=" * 40)
    
    # Check environment
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ Environment setup required")
        print("Run: python silas-chat-ui/setup_free_llm_apis.py")
        return
    
    # Test individual APIs
    gemini_ok = await test_gemini()
    groq_ok = await test_groq()
    
    # Test integrated backend
    backend_ok = await test_free_llm_backend()
    
    print("\n" + "=" * 40)
    print("🎯 Test Results:")
    print(f"Google Gemini: {'✅ Working' if gemini_ok else '❌ Failed'}")
    print(f"Groq: {'✅ Working' if groq_ok else '❌ Failed'}")
    print(f"Integrated Backend: {'✅ Working' if backend_ok else '❌ Failed'}")
    
    if gemini_ok or groq_ok:
        print("\n🎉 Free LLM APIs are working!")
        print("✅ No more OpenRouter rate limits")
        print("✅ High-quality AI responses ready")
        print("\n🚀 Launch your avatar:")
        print("python silas-chat-ui/launch_real_face_avatar.py")
    else:
        print("\n⚠️  API setup needed")
        print("💡 Check your API keys and try again")

if __name__ == "__main__":
    asyncio.run(main())