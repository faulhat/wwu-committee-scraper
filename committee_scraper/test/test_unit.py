import unittest
import sys, os
from src.scraper import Scraper

# Test scraper object creation.
def test_1_assignment():
    scraper = Scraper("llama3.2:1b", 1, None)
    assert scraper.model == "llama3.2:1b"
    assert scraper.score_threshold == 1
    assert scraper.db_connection is None

# Test email and doc_link scraping functionality.
def test_2_scraper():
    scraper = Scraper("llama3.2:1b", 1, None)
    page = Scraper.PageData("https://as.wwu.edu/committees/sehome-hill-arboretum-board-of-governors/", scraper)
    page.run()
    assert len(page.emails) == 0
    assert len(page.doc_links) == 0

