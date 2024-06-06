import os
from dotenv import load_dotenv
from utils import SlackNotifier


if __name__ == "__main__":
    load_dotenv()
    webhook_url = os.getenv("WEBHOOK_URL")
    channel = os.getenv("CHANNEL")
    username = os.getenv("USERNAME")
    icon = os.getenv("ICON")
    notifier = SlackNotifier(
        webhook_url=webhook_url,
        channel=channel,
        username=username,
        icon=icon
    )
    notifier.notify(text="This is test.", color="sccess")