"""
Proactive AI Decisions - 60s Script

Analyze KPIs and get AI-powered business recommendations in under a minute using OpenRouter's free tier.

🚀 Quick Start:
1. Install: pip install requests pandas python-dotenv
2. Get API key: https://openrouter.ai/keys
3. Run: python proactive_decisions.py --sample

📚 Full tutorial: [Your YouTube Link]
⭐ Star the repo: https://github.com/Mohammad-Emon/ai-shorts-lab
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
    """Represents a recommended action with impact and effort scores."""
    action: str
    impact: float
    effort: float

def analyze_kpis(
    csv_path: str, 
    goal: str, 
    api_key: Optional[str] = None,
    model: str = "openai/gpt-3.5-turbo"
) -> List[Dict]:
    """
    Analyze KPIs and suggest top 3 actions with impact and effort scores.
    
    Args:
        csv_path: Path to CSV file with KPI data
        goal: Business objective to achieve
        api_key: OpenRouter API key (or set OPENROUTER_API_KEY env var)
        model: AI model to use (default: openai/gpt-3.5-turbo)
        
    Returns:
        List of dicts with action details
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV: {e}")
    
    prompt = f"""Analyze these KPIs and suggest the top 3 most impactful actions 
    to achieve: {goal}

    KPI Data:
    {df.to_string()}

    For each action, provide:
    1. A specific, actionable recommendation
    2. Impact score (1-10, 10=highest)
    3. Effort score (1-10, 1=lowest)
    
    Format as a numbered list with each action on a new line."""
    
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("No API key provided. Set OPENROUTER_API_KEY or use --api-key")
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Mohammad-Emon/ai-shorts-lab"
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a data-driven business analyst."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
        )
        response.raise_for_status()
        
        # Handle rate limiting
        remaining = int(response.headers.get('x-ratelimit-remaining', 0))
        if remaining < 5:
            print(f"⚠️  Warning: {remaining} requests remaining this minute")
            
        return parse_actions(response.json()["choices"][0]["message"]["content"])
        
    except Exception as e:
        raise Exception(f"API Error: {e}")

def parse_actions(response: str) -> List[Dict]:
    """Convert AI response into structured action items."""
    import re
    actions = []
    
    for line in [l.strip() for l in response.split('\n') if l.strip()]:
        if line[0].isdigit() and '.' in line:
            try:
                action = line.split('.', 1)[1].strip()
                nums = [float(x) for x in re.findall(r'\d+\.?\d*', line)]
                impact = min(10, max(1, nums[0])) if len(nums) > 0 else 5
                effort = min(10, max(1, nums[1])) if len(nums) > 1 else 5
                
                actions.append({
                    'action': action,
                    'impact': impact,
                    'effort': effort,
                    'priority': impact / effort if effort > 0 else 0
                })
            except:
                continue
    
    return sorted(actions, key=lambda x: x['priority'], reverse=True)[:3]

def generate_sample_data(output_path: str = "sample_kpi_data.csv"):
    """Generate sample KPI data for testing."""
    data = {
        'KPI': [
            'Monthly Active Users', 'Customer Acquisition Cost',
            'Customer Lifetime Value', 'Churn Rate',
            'Conversion Rate', 'Average Order Value',
            'Monthly Recurring Revenue', 'Net Promoter Score'
        ],
        'Current': [
            8432, 125.50, 1200.00, 0.15,
            0.045, 87.99, 45000, 8.2
        ],
        'Target': [
            'Increase', 'Decrease', 'Increase', 'Decrease',
            'Increase', 'Increase', 'Increase', 'Increase'
        ]
    }
    
    pd.DataFrame(data).to_csv(output_path, index=False)
    print(f"✅ Sample data saved to {output_path}")
    return output_path

def list_available_models(api_key: str):
    """List available OpenRouter models."""
    try:
        models = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        ).json()["data"]
        print("\n".join([m["id"] for m in models]))
    except Exception as e:
        print(f"⚠️  Error fetching models: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Get AI-powered business recommendations from KPIs")
    parser.add_argument("--csv", help="Path to KPI CSV file")
    parser.add_argument("--goal", default="increase revenue by 20%", help="Business goal")
    parser.add_argument("--sample", action="store_true", help="Generate sample KPI data")
    parser.add_argument("--api-key", help="OpenRouter API key")
    parser.add_argument("--model", default="openai/gpt-3.5-turbo", help="AI model to use")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    
    args = parser.parse_args()
    
    if args.list_models:
        return list_available_models(args.api_key or os.getenv("OPENROUTER_API_KEY"))
    
    if args.sample:
        csv_path = generate_sample_data()
        print("\nAnalyzing sample data...\n")
    elif args.csv:
        csv_path = args.csv
    else:
        print("Error: Please provide --csv or --sample")
        return
    
    try:
        actions = analyze_kpis(csv_path, args.goal, args.api_key, args.model)
        
        print("🚀 Top 3 Recommended Actions:")
        for i, action in enumerate(actions, 1):
            print(f"\n{i}. {action['action']}")
            print(f"   📈 Impact: {action['impact']}/10")
            print(f"   ⚡ Effort: {action['effort']}/10")
            print(f"   🎯 Priority: {action['priority']:.1f}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Tip: Make sure you have a valid OpenRouter API key.")
        print("Get one at: https://openrouter.ai/keys")

if __name__ == "__main__":
    main()
