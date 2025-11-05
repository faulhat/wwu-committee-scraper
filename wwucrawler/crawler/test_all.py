import pytest

from bs4 import BeautifulSoup

from pages_db import PagesDB
from search import SearchRes, Trie, search, tiered_search

# Mock database
test_db = PagesDB(":memory:")
test_db.setup()


def test_add_page():
    assert test_db.count_pages() == 0

    search_null = SearchRes({}, -1, -1, 0)
    test_db.add_page("helloworld.com", "Hello World", search_null, 0, "")
    assert test_db.count_pages() == 1

    cur = test_db.con.cursor()
    cur.execute("SELECT url, title, score FROM pages")
    rows = cur.fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "helloworld.com"
    assert rows[0][1] == "Hello World"
    assert rows[0][2] == 0


def test_search():
    expected_appearances = {
        "vast": 1,
        "inhabit": 1,
        "portion": 1,
        "the": 5,
    }

    with open("testdata/sample.html", "r") as f:
        text = f.read()
        soup = BeautifulSoup(text, "html.parser")
        res = search(soup.text, expected_appearances.keys())
        for term, num in expected_appearances.items():
            assert term in res.appearances
            assert res.appearances[term] == num

        assert res.total == 8


def test_trie():
    terms = ["a", "aa", "into", "in", "hero", "heroic"]
    t = Trie(terms)
    for term in terms:
        assert t.has_term(term)

    assert not t.has_term("int")


def test_trie_search():
    expected_appearances = {
        "vast": 1,
        "inhabit": 1,
        "portion": 1,
        "the": 5,
    }

    with open("testdata/sample.html", "r") as f:
        text = f.read()
        soup = BeautifulSoup(text, "html.parser")
        t = Trie(expected_appearances.keys())
        res = t.search(soup.text)
        for term, num in expected_appearances.items():
            assert term in res.appearances
            assert res.appearances[term] == num

        assert res.total == 8


def test_tiered_search():
    keywords = [["vast", "inhabit"], ["portion"], ["the"]]
    expected_appearances = {
        "vast": 1,
        "inhabit": 1,
        "portion": 1,
        "the": 5,
    }

    with open("testdata/sample.html", "r") as f:
        text = f.read()
        soup = BeautifulSoup(text, "html.parser")
        res = tiered_search(soup.text, keywords)
        for term, num in expected_appearances.items():
            assert term in res.appearances
            assert res.appearances[term] == num

        assert res.total == 13


def test_summarize():
    keywords = [["vast", "inhabit"], ["portion"], ["the"]]
    expected_appearances = {
        "vast": 1,
        "inhabit": 1,
        "portion": 1,
        "the": 5,
    }

    fname = "testdata/sample.html"
    with open(fname, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        title = soup.title.string
        text = soup.text
        res = tiered_search(text, keywords)
        test_db.add_page(fname, title, res, res.total, text)

        cur = test_db.con.cursor()
        cur.execute(
            "SELECT summary_before, summary_keyword, summary_after FROM pages WHERE url = ?",
            (fname,),
        )
        rows = cur.fetchall()
        summary_before, summary_keyword, summary_after = rows[0]

        assert summary_keyword == "vast"
        assert summary_before.startswith("...")
        assert summary_after.endswith("...")
        assert summary_before[3:] == text[res.first - 10 : res.first]
        assert summary_after[:-3] == text[res.end : res.end + 100]
