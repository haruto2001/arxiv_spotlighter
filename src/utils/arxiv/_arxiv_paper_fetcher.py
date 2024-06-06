__all__ = ["ArxivPaperFetcherConfig", "ArxivPaperFetcher"]


import arxiv


class ArxivPaperFetcherConfig:
    """Configuration class for ArxivPaperFetcher.

    Attributes:
        date (str): The date in the format 'YYYYMMDD'.
        category (str): The category or subject area for the search.
        max_results (int): The maximum number of results to fetch.
    """
    def __init__(
        self,
        date="20240101",
        category="quant-ph",
        max_results=2
    ):
        """Initializes ArxivPaperFetcherConfig with default values.

        Args:
            date (str): The date in the format 'YYYYMMDD'.
            category (str): The category or subject area for the search.
            max_results (int): The maximum number of results to fetch.
        """
        self.date = date
        self.category = category
        self.max_results = max_results


class ArxivPaperFetcher:
    """Class to fetch papers from arXiv based on configuration settings.

    Attributes:
        date (str): The date in the format 'YYYYMMDD'.
        category (str): The category or subject area for the search.
        max_results (int): The maximum number of results to fetch.
        results (list): List of fetched paper results.
    """

    def __init__(self, config: ArxivPaperFetcherConfig):
        """Initializes ArxivPaperFetcher with a configuration object.

        Args:
            config (ArxivPaperFetcherConfig): Configuration object with date, category, and max_results.
        """
        self.date = config.date
        self.category = config.category
        self.max_results = config.max_results
        self.results = None

    def _make_query(self):
        """Constructs the query string based on the configuration settings.
        """
        query_category = f"cat:{self.category}"
        query_date = f"submittedDate:[{self.date + "0000"} TO {self.date + "2359"}]"
        query = query_category + " AND " + query_date
        self.query = query

    def _fetch_paper_urls(self):
        """Fetches paper URLs from arXiv based on the query.
        """
        client = arxiv.Client()
        search = arxiv.Search(
            query=self.query,
            max_results = self.max_results,
            sort_by = arxiv.SortCriterion.SubmittedDate
        )
        self.results = client.results(search)

    def run(self):
        """Runs the process of fetching paper URLs from arXiv and prints the results.
        """
        self._make_query()
        self._fetch_paper_urls()
        for result in self.results:
            print(result)