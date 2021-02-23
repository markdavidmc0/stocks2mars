import time

from actions.scrape import AbstractScraper, TwitterScraper


def main(factory: AbstractScraper):
    scrape = factory.scrape()
    while True:
        print(scrape)
        time.sleep(5)


if __name__ == '__main__':
    main(TwitterScraper())
