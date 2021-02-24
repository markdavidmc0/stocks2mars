import asyncio
import logging
import pathlib
import re
import sys
import urllib.error
import urllib.parse
from abc import ABC, abstractmethod
from typing import IO

import aiofiles
import aiohttp
from aiohttp import ClientSession


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')


class AbstractScraper(ABC):
    """Base product family for all scraper types."""

    @abstractmethod
    def scrape(self) -> None:
        pass

    @abstractmethod
    def fetch_html(self) -> str:
        pass

    @abstractmethod
    def parse(self) -> set:
        pass

    @abstractmethod
    def write_one(self) -> None:
        pass

    @abstractmethod
    def bulk_crawl_and_write(self) -> None:
        pass


class AdHocScraper(AbstractScraper):
    """Concrete ad hoc scrape library wrapper."""

    def scrape(self) -> None:
        """Concrete async data fetcher."""
        assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
        here = pathlib.Path(__file__).parent

        with open(here.joinpath("urls.txt")) as infile:
            urls = set(map(str.strip, infile))

        outpath = here.joinpath("foundurls.txt")
        with open(outpath, "w") as outfile:
            outfile.write("source_url\tparsed_url\n")

        logger.info("Scraping has started.")
        asyncio.run(self.bulk_crawl_and_write(file=outpath, urls=urls))

    @staticmethod
    async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
        """GET request wrapper to fetch page HTML.

        kwargs are passed to `session.request()`.
        """

        resp = await session.request(method="GET", url=url, **kwargs)
        resp.raise_for_status()
        logger.info("Got response [%s] for URL: %s", resp.status, url)
        html = await resp.text()
        return html

    async def parse(self, url: str, session: ClientSession, **kwargs) -> set:
        """Find HREFs in the HTML of `url`."""
        found = set()
        try:
            html = await self.fetch_html(url=url, session=session, **kwargs)
        except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
        ) as e:
            logger.error(
                "aiohttp exception for %s [%s]: %s",
                url,
                getattr(e, "status", None),
                getattr(e, "message", None),
            )
            return found
        except Exception as e:
            logger.exception(
                "Non-aiohttp exception occured:  %s", getattr(
                    e, "__dict__", {})
            )
            return found
        else:
            for link in HREF_RE.findall(html):
                try:
                    abslink = urllib.parse.urljoin(url, link)
                except (urllib.error.URLError, ValueError):
                    logger.exception("Error parsing URL: %s", link)
                    pass
                else:
                    found.add(abslink)
            logger.info("Found %d links for %s", len(found), url)
            return found

    async def write_one(self, file: IO, url: str, **kwargs) -> None:
        """Write the found HREFs from `url` to `file`."""
        res = await self.parse(url=url, **kwargs)
        if not res:
            return None
        async with aiofiles.open(file, "a") as f:
            for p in res:
                await f.write(f"{url}\t{p}\n")
            logger.info("Wrote results for source URL: %s", url)

    async def bulk_crawl_and_write(self, file: IO, urls: set, **kwargs) -> None:
        """Crawl & write concurrently to `file` for multiple `urls`."""
        async with ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(
                    self.write_one(file=file, url=url,
                                   session=session, **kwargs)
                )
            await asyncio.gather(*tasks)


class AbstractFactory(ABC):
    """Base factory that supports social media product."""

    @abstractmethod
    def create_scraper(self) -> AbstractScraper:
        pass


class AdHocFactory(AbstractFactory):
    """Concrete ad hoc scraper creator."""

    def create_scraper(self) -> AdHocScraper:
        return AdHocScraper()
