import unittest
from src.scraper import Scraper

class TestScraper(unittest.TestCase):

    def test1_summary_length(self):
        scraper = Scraper('llama3.8:1b', 0, None)
        pass


if __name__ == "__main__":
    unittest.main()
