"""
Proactive AI Decisions - 60s Script

A script that analyzes KPIs and suggests top actions using OpenAI's GPT model.
"""
import os
import json
import requests
import pandas as pd
from typing import List, Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class ActionItem:
    action: str
    impact: float
    effort: float

def rank_actions(
    csv_path: str, 
    goal: str, 
    api_key: Optional[str] = None,
    model: str = "openai/gpt-3.5-turbo"  # Default to free model
) -> List[Dict]:
    """
    Analyze KPIs and suggest top 3 actions with impact and effort scores.
    
    Args:
        csv_path: Path to the CSV file containing KPIs
        goal: The business goal to achieve
        api_key: Optional API key for OpenRouter (defaults to OPENROUTER_API_KEY env var)
        model: Model to use (defaults to free tier model)
        
    Returns:
        List of dictionaries containing action, impact, and effort
    """
    # Read the KPI data
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")
    
    # Prepare the prompt
    prompt = (
        f"Analyze these KPIs and suggest the top 3 most impactful actions "
        f"to achieve: {goal}\n\n"
        f"KPI Data:\n{df.to_string()}\n\n"
        "For each action, provide:\n"
        "1. A specific, actionable recommendation\n"
        "2. Impact score (1-10, 10 being highest impact)\n"
        "3. Effort score (1-10, 1 being lowest effort)\n\n"
        "Format as a numbered list with each action on a new line."
    )
    
    # Get API key from args or environment
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "No API key provided. Set OPENROUTER_API_KEY environment variable or use --api-key"
        )
    
    # Call OpenRouter API
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Mohammad-Emon/ai-shorts-lab",  # Optional, for analytics
            "X-Title": "Proactive AI Decisions"  # Optional, for analytics
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a data-driven business analyst that provides clear, actionable insights."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        # Check for errors
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Handle rate limiting
        remaining_requests = int(response.headers.get('x-ratelimit-remaining', 0))
        if remaining_requests < 5:
            print(f"⚠️  Warning: Only {remaining_requests} requests remaining in the current window")
            
        return parse_actions(content)
        
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {e}")

def parse_actions(response_text: str) -> List[Dict]:
    """Parse the AI response into structured action items."""
    lines = [line.strip() for line in response_text.split('\n') if line.strip()]
    actions = []
    
    for line in lines:
        if line[0].isdigit() and '.' in line:
            try:
                # Extract action text
                action_text = line.split('.', 1)[1].strip()
                
                # Extract impact and effort scores
                impact = 0
                effort = 0
                
                # Look for impact/effort indicators
                if 'impact' in action_text.lower() and 'effort' in action_text.lower():
                    # Try to find numbers after "impact" and "effort"
                    import re
                    nums = [float(x) for x in re.findall(r'\d+\.?\d*', action_text)]
                    if len(nums) >= 2:
                        impact = min(10, max(1, nums[0]))  # Clamp to 1-10
                        effort = min(10, max(1, nums[1]))  # Clamp to 1-10
                
                actions.append({
                    'action': action_text,
                    'impact': impact,
                    'effort': effort,
                    'priority': impact / effort if effort > 0 else 0  # Priority score (impact/effort)
                })
            except Exception as e:
                print(f"Warning: Could not parse line: {line}")
    
    # Sort by priority (highest first)
    return sorted(actions, key=lambda x: x['priority'], reverse=True)[:3]

def generate_sample_data(output_path: str = "sample_kpi_data.csv"):
    """Generate sample KPI data for testing."""
    import random
    
    data = {
        'KPI': [
            'Monthly Active Users',
            'Customer Acquisition Cost',
            'Customer Lifetime Value',
            'Churn Rate',
            'Conversion Rate',
            'Average Order Value',
            'Monthly Recurring Revenue',
            'Net Promoter Score'
        ],
        'Current': [
            random.randint(1000, 10000),
            round(random.uniform(50, 200), 2),
            round(random.uniform(500, 2000), 2),
            round(random.uniform(0.01, 0.2), 2),
            round(random.uniform(0.01, 0.1), 2),
            round(random.uniform(50, 200), 2),
            random.randint(10000, 100000),
            random.randint(1, 10)
        ],
        'Target': [
            'Increase',
            'Decrease',
            'Increase',
            'Decrease',
            'Increase',
            'Increase',
            'Increase',
            'Increase'
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Sample KPI data saved to {output_path}")
    return output_path

def get_available_models(api_key: str) -> List[Dict]:
    """Get list of available models from OpenRouter."""
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        print(f"⚠️  Could not fetch available models: {e}")
        return []

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Proactive AI Decisions - Analyze KPIs and suggest actions using OpenRouter"
    )
    parser.add_argument("--csv", type=str, help="Path to CSV file with KPI data")
    parser.add_argument(
        "--goal", 
        type=str, 
        default="increase revenue by 20%", 
        help="Business goal to achieve"
    )
    parser.add_argument(
        "--sample", 
        action="store_true", 
        help="Generate sample KPI data"
    )
    parser.add_argument(
        "--api-key", 
        type=str, 
        help="OpenRouter API key (or set OPENROUTER_API_KEY environment variable)",
        default=os.getenv("OPENROUTER_API_KEY")
    )
    parser.add_argument(
        "--model",
        type=str,
        default="openai/gpt-3.5-turbo",  # Default to free tier model
        help="Model to use (e.g., 'openai/gpt-3.5-turbo', 'meta-llama/llama-2-70b-chat')"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit"
    )
    
    args = parser.parse_args()
    
    # List available models if requested
    if args.list_models:
        if not args.api_key:
            print("Error: API key required to list models")
            return 1
            
        print("\n🔍 Available Models:")
        print("-" * 50)
        models = get_available_models(args.api_key)
        
        # Group by provider
        providers = {}
        for model in models:
            provider = model["id"].split("/")[0]
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(model)
        
        # Print by provider
        for provider, models in providers.items():
            print(f"\n{provider.upper()}:")
            for model in models:
                pricing = ""
                if model.get("pricing"):
                    pricing = f" (${model['pricing']['prompt'] * 1000}/1K input, ${model['pricing']['completion'] * 1000}/1K output)"
                print(f"- {model['id']}{pricing}")
        return 0
    
    # Handle sample data generation
    if args.sample:
        csv_path = generate_sample_data()
        print(f"\n📊 Sample data generated at: {csv_path}")
        print("\nYou can now run the script with:")
        print(f"python proactive_decisions.py --csv {csv_path} --model {args.model}")
        return 0
    
    # Validate required arguments
    if not args.csv:
        print("❌ Error: Please provide a CSV file with --csv or use --sample to generate sample data")
        parser.print_help()
        return 1
    
    if not args.api_key:
        print("❌ Error: No API key provided. Set OPENROUTER_API_KEY environment variable or use --api-key")
        return 1
    
    try:
        # Analyze KPIs and get actions
        print("\n🤖 Analyzing your KPIs...")
        actions = rank_actions(args.csv, args.goal, args.api_key, args.model)
        
        if not actions:
            print("❌ No actionable insights could be generated. Please check your input data and try again.")
            return 1
            
        # Print results
        print("\n🚀 Top Recommended Actions:")
        print("-" * 50)
        
        for i, action in enumerate(actions, 1):
            print(f"\n{i}. {action['action']}")
            print(f"   Impact: {action['impact']:.1f}/10 | "
                  f"Effort: {action['effort']:.1f}/10 | "
                  f"Priority: {action['priority']:.2f}")
        
        print("\n💡 Tip: Focus on high-impact, low-effort actions first!")
        print("\n🔗 Powered by OpenRouter (https://openrouter.ai/)")
        
    except requests.exceptions.HTTPError as e:
        error_msg = str(e)
        if e.response.status_code == 401:
            error_msg = "Invalid API key. Please check your OpenRouter API key."
        elif e.response.status_code == 429:
            error_msg = "Rate limit exceeded. Please wait before making more requests."
        
        print(f"\n❌ API Error: {error_msg}")
        if e.response.status_code == 429:
            reset_time = e.response.headers.get('x-ratelimit-reset-requests')
            if reset_time:
                print(f"⏳ Rate limit resets at: {reset_time}")
        return 1
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    main()
