import arxiv
import os
from dotenv import load_dotenv
from utils.arxiv import ArxivPaperFetcherConfig, ArxivPaperFetcher
from utils.slack import SlackNotifier


def main():
    load_dotenv()
    webhook_url = os.getenv("WEBHOOK_URL")
    channel = os.getenv("CHANNEL")
    username = os.getenv("USERNAME")
    icon = os.getenv("ICON")
    date = "20240605"
    config = ArxivPaperFetcherConfig(date=date)
    fetcher = ArxivPaperFetcher(config)
    fetcher.run()
    notifier = SlackNotifier(
        webhook_url=webhook_url,
        channel=channel,
        username=username,
        icon=icon
    )
    notifier.notify(text="This is test.", color="sccess")


if __name__ == "__main__":
    main()