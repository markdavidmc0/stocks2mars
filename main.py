import asyncio
import time
from actions.scrape import AbstractScraper, AdHocScraper


def main(factory: AbstractScraper):
    factory.scrape()
    time.sleep(5)


if __name__ == '__main__':
    main(AdHocScraper())
