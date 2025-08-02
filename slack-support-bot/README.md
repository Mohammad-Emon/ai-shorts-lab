# Slack Support Bot 🤖

A customizable Slack bot for handling support requests and automating responses.

## 🚀 Features

- Responds to mentions in channels
- Handles slash commands
- Threaded conversations
- Easy to extend with custom functionality

## 🛠️ Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Slack tokens:

   ```env
   SLACK_BOT_TOKEN=xoxb-your-token
   SLACK_APP_TOKEN=xapp-your-token
   ```

3. Run the bot:

   ```bash
   python bot.py
   ```

## 📚 Usage

- Mention the bot in any channel: `@SupportBot help`
- Use the slash command: `/support`

## 🔧 Configuration

Edit `bot.py` to customize:
- Event listeners
- Command handlers
- Response templates

## 📝 Environment Variables

| Variable | Description |
|----------|-------------|
| `SLACK_BOT_TOKEN` | Bot User OAuth Token from Slack API |
| `SLACK_APP_TOKEN` | App-level token for Socket Mode |

## 🤖 Extending the Bot

Add new event listeners or commands by following the pattern in `bot.py`.
