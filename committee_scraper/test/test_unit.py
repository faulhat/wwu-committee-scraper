import sys, os
from src.scraper import Scraper
from src.scraper import utils
from sqlite3 import connect

# Enter the model you want to test with here.
DEFAULT_MODEL = "llama3.2:1b"
DEFAULT_DB = None

# Test scraper object creation.
def test_1_assignment():
    scraper = Scraper(DEFAULT_MODEL, 1, DEFAULT_DB)
    assert scraper.model == DEFAULT_MODEL
    assert scraper.score_threshold == 0.01
    assert scraper.db_connection is DEFAULT_DB

# Test email and doc_link scraping functionality.
def test_2_scraper():
    scraper = Scraper(DEFAULT_MODEL, 1, DEFAULT_DB)
    page = Scraper.PageData("https://as.wwu.edu/committees/sehome-hill-arboretum-board-of-governors/", scraper)
    page.run()
    assert len(page.emails) == 0
    assert len(page.doc_links) == 0

# This webpage displays a link to a charter pdf. Check the URL is sucessfully scraped.
def test_3_scraper():
    scraper = Scraper(DEFAULT_MODEL, 1, DEFAULT_DB)
    page = Scraper.PageData("https://as.wwu.edu/committees/as-election-appeals-panel/", scraper)
    page.run()
    assert len(page.emails) == 0
    assert len(page.doc_links) == 1

# This webpage displays 3 emails and 1 pdf link.
def test_4_scraper():
    scraper = Scraper(DEFAULT_MODEL, 1, DEFAULT_DB)
    page = Scraper.PageData("https://as.wwu.edu/committees/as-queer-guild-council/", scraper)
    page.run()
    assert len(page.emails) == 3
    assert len(page.doc_links) == 1

# This webpage displays 3 emails and 1 pdf link.
def test_5_scraper():
    scraper = Scraper(DEFAULT_MODEL, 1, DEFAULT_DB)
    page = Scraper.PageData("https://as.wwu.edu/committees/as-queer-guild-council/", scraper)
    page.run()
    assert len(page.page) > len(page.extract_page_contents())

# Assumes that the crawler has already been run and has created a table for pages.
def test_6_db_fetch_url():
    con = connect('../pages.db')
    scraper = Scraper(DEFAULT_MODEL, 1, con)
    try:
        scraper.fetch_urls()
        assert len(scraper.URLS) > 0
    except Exception as e:
        print('\n', e, sys.stderr)

# Test validate_request used to test response codes.
def test_7_utils():
    assert not utils.validate_request("https://thisdoesnotexist.haha")
    assert utils.validate_request("https://wwu.edu")

def test_8_utils():
    assert utils.validate_email("haha@something.org")
    assert not utils.validate_email("!#$#$@somet#!@ing.org")
    assert not utils.validate_email("")

def test_9_utils():
    assert utils.extract_list('[hello world]') == 'hello world'
    assert utils.extract_list('[]') == ''
    assert utils.extract_list('') == None
