import argparse
import arxiv
import datetime
import openai
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from utils.arxiv import ArxivPaperFetcherConfig, ArxivPaperFetcher
from utils.slack import SlackNotifierConfig, SlackNotifier


def parse_args() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="gpt-3.5-turbo")
    parser.add_argument("--temperature", type=int, default=0)
    parser.add_argument("--max_tokens", type=int, default=512)
    parser.add_argument("--channel", type=str, default="#dev-arxiv")
    return parser.parse_args()


def load_environment_variables() -> None:
    """Loads environment variables from a .env file into the environment."""
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    webhook_url = os.getenv("WEBHOOK_URL")
    return (openai_api_key, webhook_url)


def make_template():
    template = """
    Please translate the following English passage into Japanese.

    {english_passage}
    """
    return template


def main(args: argparse.Namespace) -> None:
    openai_api_key, webhook_url = load_environment_variables()

    # date = format(datetime.datetime.now(datetime.UTC).date(), "%Y%m%d")
    date = "20240606"
    fetcher_config = ArxivPaperFetcherConfig(date=date)
    fetcher = ArxivPaperFetcher(fetcher_config)
    summary_list = fetcher.run()

    template = make_template()
    prompt_template = PromptTemplate.from_template(template)
    model = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name=args.model_name,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )
    parser = StrOutputParser()
    chain = prompt_template | model | parser

    for summary in summary_list:
        result = chain.invoke({"english_passage": summary})
        print(result)

        notifier_config = SlackNotifierConfig(
            webhook_url=webhook_url,
            channel=args.channel
        )
        notifier = SlackNotifier(notifier_config)
        notifier.run(text=result, color="sccess")


if __name__ == "__main__":
    main(parse_args())