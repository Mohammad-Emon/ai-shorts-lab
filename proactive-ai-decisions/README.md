# 🚀 Proactive AI Decisions in 60s (OpenRouter Edition)

Make data-driven business decisions in under a minute using OpenRouter's free tier. This tool analyzes your KPIs and suggests the most impactful actions to achieve your business goals using various AI models.

## ✨ Features

- **Free AI Models**: Uses OpenRouter's free tier (GPT-3.5-turbo by default)
- **Multiple Models**: Supports any model available on OpenRouter
- **Quick Analysis**: Get actionable insights from your KPI data in seconds
- **Smart Prioritization**: AI ranks actions by impact vs. effort
- **Easy Setup**: Works with any CSV file containing your KPI data
- **Sample Data**: Includes a sample dataset to get started quickly

## 🚀 Quick Start

### 1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### 2. **Get your OpenRouter API key**:
   - Visit [OpenRouter](https://openrouter.ai/keys) and sign up
   - Create an API key
   - Set it as an environment variable:
     ```bash
   export OPENROUTER_API_KEY='your-api-key-here'
   ```

### 3. **List available models** (optional):
   ```bash
   python proactive_decisions.py --list-models
   ```

### 4. **Run with sample data**:
   ```bash
   python proactive_decisions.py --sample
   ```

### 5. **Run with your own data**:
   ```bash
   python proactive_decisions.py --csv your_kpi_data.csv --goal "increase revenue by 20%"
   ```

### 6. **Try different models** (optional):
   ```bash
   python proactive_decisions.py --csv your_data.csv --model "anthropic/claude-2"
   ```


## 📊 Sample Output

```
🚀 Top Recommended Actions:
--------------------------------------------------

1. Focus on reducing churn through targeted retention campaigns
   Impact: 8.5/10 | Effort: 4.0/10 | Priority: 2.12

2. Improve onboarding process to increase activation rates
   Impact: 7.0/10 | Effort: 3.5/10 | Priority: 2.00

3. Launch referral program to lower acquisition costs
   Impact: 7.5/10 | Effort: 5.0/10 | Priority: 1.50

💡 Tip: Focus on high-impact, low-effort actions first!
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Set default model (overrides the built-in default)
# DEFAULT_MODEL=openai/gpt-3.5-turbo
```

### Command Line Arguments

```bash
python proactive_decisions.py --help

Options:
  --csv TEXT       Path to CSV file with KPI data
  --goal TEXT      Business goal to achieve  [default: increase revenue by 20%]
  --sample         Generate sample KPI data
  --api-key TEXT   OpenRouter API key (or set OPENROUTER_API_KEY env var)
  --model TEXT     Model to use (e.g., 'openai/gpt-3.5-turbo', 'anthropic/claude-2')
  --list-models    List available models and exit
  --help           Show this message and exit.
```

## 📝 Sample Data Format

Your CSV should include at least these columns:

```csv
KPI,Current,Target
Monthly Active Users,5000,Increase
Customer Acquisition Cost,150,Decrease
Churn Rate,0.15,Decrease
Conversion Rate,0.05,Increase
```

## 🤖 How It Works

1. The script reads your KPI data from a CSV file
2. It sends the data to OpenRouter's API, which routes to your chosen AI model (default: GPT-3.5-turbo)
3. The AI identifies the most impactful actions to achieve your goal
4. Results are ranked by priority (impact/effort ratio)
5. Rate limits and usage are automatically handled by OpenRouter

## ⚠️ Important Notes

- Keep your OpenRouter API key secure and never commit it to version control
- The free tier has rate limits (check [OpenRouter Pricing](https://openrouter.ai/pricing))
- For production use, consider upgrading to a paid plan for higher rate limits
- The quality of recommendations depends on the chosen model and your input data quality
- You can monitor your usage at [OpenRouter Dashboard](https://openrouter.ai/activity)

## 📄 License

MIT
