import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Example event: Bot is mentioned in a channel
@app.event("app_mention")
def handle_mentions(event, say):
    user = event["user"]
    text = event["text"]
    
    # Extract the actual message (remove the bot mention)
    message = ' '.join(text.split()[1:]) if len(text.split()) > 1 else "Hello!"
    
    # Respond in a thread
    say(
        text=f"Hello <@{user}>! I'm your support bot. You said: {message}",
        thread_ts=event["thread_ts"] if "thread_ts" in event else None
    )

# Example slash command
@app.command("/support")
def support_command(ack, say, command):
    ack()
    say("Support request received! Our team will get back to you shortly.")

if __name__ == "__main__":
    # Start the bot
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
