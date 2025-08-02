# Prompt Chains

A collection of reusable prompt chain templates for AI applications.

## 📚 Templates

1. **Basic Prompt Chain** (`chain-template.json`)
   - A simple template to get started with prompt chaining
   - Includes system, user, and assistant message templates
   - Customizable variables for dynamic content

## 🚀 Getting Started

1. Copy the template file:

   ```bash
   cp chain-template.json my-prompt-chain.json
   ```

2. Customize the prompts and flow in the JSON file

3. Use with your preferred LLM framework

## 🤖 Usage Example

```python
import json

# Load your prompt chain
with open('my-prompt-chain.json') as f:
    chain = json.load(f)

# Process the chain
for prompt in chain['prompts']:
    # Your LLM interaction logic here
    print(f"Processing step: {prompt['id']}")
```

## 📝 Contributing

Feel free to submit pull requests with your own prompt chain templates!
