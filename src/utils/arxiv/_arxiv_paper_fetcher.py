__all__ = ["ArxivPaperFetcherConfig", "ArxivPaperFetcher"]


import arxiv
from typing import List


class ArxivPaperFetcherConfig:
    """Configuration class for ArxivPaperFetcher.

    Attributes:
        date (str): The date in the format 'YYYYMMDD'.
        category (str): The category or subject area for the search.
        max_results (int): The maximum number of results to fetch.
    """
    def __init__(
        self,
        date: str = "20240101",
        category: str = "quant-ph",
        max_results: int = 2
    ) -> None:
        """Initializes ArxivPaperFetcherConfig with default values.

        Args:
            date (str): The date in the format 'YYYYMMDD'.
            category (str): The category or subject area for the search.
            max_results (int): The maximum number of results to fetch.
        """
        self.date = date
        self.category = category
        self.max_results = max_results

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the configuration.

        Returns:
            str: String representation of the configuration.
        """
        return f"ArxivPaperFetcherConfig(date={self.date}, category={self.category}, max_results={self.max_results})"

    def __repr__(self) -> str:
        """Returns an official string representation of the configuration.

        Returns:
            str: Official string representation of the configuration.
        """
        return f"ArxivPaperFetcherConfig(date={self.date!r}, category={self.category!r}, max_results={self.max_results!r})"


class ArxivPaperFetcher:
    """Class to fetch papers from arXiv based on configuration settings.

    Attributes:
        date (str): The date in the format 'YYYYMMDD'.
        category (str): The category or subject area for the search.
        max_results (int): The maximum number of results to fetch.
        results (list): List of fetched paper results.
    """

    def __init__(self, config: ArxivPaperFetcherConfig) -> None:
        """Initializes ArxivPaperFetcher with a configuration object.

        Args:
            config (ArxivPaperFetcherConfig): Configuration object with date, category, and max_results.
        """
        self.date = config.date
        self.category = config.category
        self.max_results = config.max_results
        self.results = None

    def _make_query(self) -> None:
        """Constructs the query string based on the configuration settings."""
        query_category = f"cat:{self.category}"
        query_date = f"submittedDate:[{self.date + "0000"} TO {self.date + "2359"}]"
        query = " AND ".join((query_category, query_date))
        self.query = query

    def _fetch_papers(self) -> None:
        """Fetches paper URLs from arXiv based on the query."""
        client = arxiv.Client()
        search = arxiv.Search(
            query=self.query,
            max_results = self.max_results,
            sort_by = arxiv.SortCriterion.SubmittedDate
        )
        self.results = client.results(search)

    def run(self) -> List[str]:
        """Runs the process of fetching paper URLs from arXiv and returns the results.

        Returns:
            List[str]: Summaries of fetched papers.
        """
        self._make_query()
        self._fetch_papers()
        return [result.summary for result in self.results]