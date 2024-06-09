__all__ = ["ArxivPaperFetcherConfig", "ArxivPaperFetcher"]


import arxiv
import logging
from dataclasses import dataclass
from typing import List, Optional


logger = logging.getLogger(__name__)


@dataclass
class ArxivPaperFetcherConfig:
    """Configuration class for ArxivPaperFetcher.

    Attributes:
        date (str): The date in the format 'YYYYMMDD'.
        category (str): The category or subject area for the search.
        max_results (int): The maximum number of results to fetch.
    """
    date: str = "20240101"
    category: str = "quant-ph"
    max_results: int = 2


class ArxivPaperFetcher:
    """Class to fetch papers from arXiv based on configuration settings.

    Attributes:
        date (str): The date in the format 'YYYYMMDD'.
        category (str): The category or subject area for the search.
        max_results (int): The maximum number of results to fetch.
        query (str): The constructed query string based on configuration settings.
        results (list): List of fetched paper results.
    """

    def __init__(
        self,
        config: ArxivPaperFetcherConfig,
        client: Optional[arxiv.Client] = None
    ) -> None:
        """Initializes ArxivPaperFetcher with a configuration object.

        Args:
            config (ArxivPaperFetcherConfig): Configuration object with date, category, and max_results.
            client (Optional[arxiv.Client]): Optional arxiv.Client instance for dependency injection.
        """
        self.date = config.date
        self.category = config.category
        self.max_results = config.max_results
        self.client = client if client is not None else arxiv.Client()
        self.query: Optional[str] = None
        self.results: Optional[List[arxiv.Result]] = None

    def _make_query(self) -> None:
        """Constructs the query string based on the configuration settings."""
        query_category = f"cat:{self.category}"
        query_date = f"submittedDate:[{self.date + "0000"} TO {self.date + "2359"}]"
        self.query = " AND ".join((query_category, query_date))
        logging.debug(f"Constructed query: {self.query}")

    def _fetch_papers(self) -> None:
        """Fetches paper URLs from arXiv based on the query."""
        try:
            search = arxiv.Search(
                query=self.query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            self.results = list(self.client.results(search))
            logging.info(f"Fetched {sum(1 for _ in self.results)} papers.")
        except arxiv.HTTPError as e:
            logging.error(f"HTTP error occurred while fetching papers: {e}")
            self.results = []
        except arxiv.UnexpectedEmptyPageError as e:
            logging.error(f"No results were found for the specified query: {e}")
            self.results = []
        except Exception as e:
            logging.error(f"Unexpected error occurred while fetching papers: {e}")
            self.results = []

    def run(self) -> List[str]:
        """Runs the process of fetching paper URLs from arXiv and returns the results.

        Returns:
            List[str]: Summaries of fetched papers.
        """
        self._make_query()
        self._fetch_papers()
        if self.results:
            return [result.summary for result in self.results]
        else:
            logging.warning("No results fetched.")
            return []