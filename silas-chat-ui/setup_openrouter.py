#!/usr/bin/env python3
"""
Setup OpenRouter API key for Silas Chat UI
"""

import os
from pathlib import Path
import requests

def check_openrouter_key(api_key):
    """Test if OpenRouter API key is valid"""
    try:
        from openai import OpenAI
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="microsoft/wizardlm-2-8x22b",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        return True, "API key is valid!"
        
    except Exception as e:
        return False, f"API key test failed: {str(e)}"

def setup_openrouter():
    """Setup OpenRouter API key"""
    print("🔑 OpenRouter API Key Setup")
    print("=" * 50)
    
    # Check if key already exists
    env_file = Path("backend/.env")
    current_key = None
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                if line.startswith('OPENROUTER_API_KEY=') and not line.endswith('your_openrouter_api_key_here'):
                    current_key = line.split('=', 1)[1].strip()
                    break
    
    if current_key:
        print(f"✅ Found existing API key: {current_key[:20]}...")
        
        # Test existing key
        print("🧪 Testing existing API key...")
        valid, message = check_openrouter_key(current_key)
        
        if valid:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            print("Let's set up a new API key.")
    
    # Get new API key
    print("\n📋 To get your free OpenRouter API key:")
    print("1. Visit: https://openrouter.ai/keys")
    print("2. Sign up for a free account")
    print("3. Create a new API key")
    print("4. Copy the key (starts with 'sk-or-v1-')")
    
    print("\n🆓 Free Models Available:")
    print("• Microsoft WizardLM 2 8x22B")
    print("• Google Gemma 7B IT")
    print("• Mistral 7B Instruct")
    print("• Zephyr 7B Beta")
    print("• OpenChat 7B")
    
    # Get API key from user
    api_key = input("\n🔑 Enter your OpenRouter API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    if not api_key.startswith('sk-or-v1-'):
        print("⚠️  Warning: API key doesn't look like an OpenRouter key")
        proceed = input("Continue anyway? (y/n): ").lower().strip()
        if proceed != 'y':
            return False
    
    # Test the API key
    print("🧪 Testing API key...")
    valid, message = check_openrouter_key(api_key)
    
    if not valid:
        print(f"❌ {message}")
        return False
    
    print(f"✅ {message}")
    
    # Save to .env file
    print("💾 Saving API key to .env file...")
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace or add the API key line
        lines = content.split('\n')
        updated = False
        
        for i, line in enumerate(lines):
            if line.startswith('OPENROUTER_API_KEY=') or line.startswith('# OPENROUTER_API_KEY='):
                lines[i] = f"OPENROUTER_API_KEY={api_key}"
                updated = True
                break
        
        if not updated:
            lines.append(f"OPENROUTER_API_KEY={api_key}")
        
        with open(env_file, 'w') as f:
            f.write('\n'.join(lines))
    else:
        with open(env_file, 'w') as f:
            f.write(f"OPENROUTER_API_KEY={api_key}\n")
    
    print("✅ API key saved successfully!")
    
    print("\n🚀 Next Steps:")
    print("1. Run: python run_full_system.py")
    print("2. Test the multi-agent system")
    print("3. Enjoy free LLM-powered conversations!")
    
    return True

if __name__ == "__main__":
    success = setup_openrouter()
    if success:
        print("\n🎉 Setup complete! Your Silas Chat UI is ready with OpenRouter LLM!")
    else:
        print("\n❌ Setup failed. Please try again.")
        exit(1)