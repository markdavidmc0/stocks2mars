from abc import ABC, abstractmethod


class AbstractScraper(ABC):
    """Base product family for all scraper types."""

    @abstractmethod
    def scrape(self) -> str:
        pass


class TwitterScraper(AbstractScraper):
    """Concrete Twitter scrape library wrapper."""

    def scrape(self) -> str:
        return "The scrape has been called."


class AbstractFactory(ABC):
    """Base scraper that supports continued scraper expansion."""

    @abstractmethod
    def create_scraper(self) -> AbstractScraper:
        pass


class TwitterFactory(AbstractFactory):
    """Concrete Twitter scraper creator."""

    def create_scraper(self) -> TwitterScraper:
        return TwitterScraper()
