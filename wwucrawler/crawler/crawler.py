"""
Tom's wwu.edu crawler program
Can be used to search the domain to an arbitrary (or unlimited) depth for an arbitrary number of keywords
"""

import requests
from bs4 import BeautifulSoup
import sys
from queue import Queue
from urls import *
from database import *
from sqlite3 import Cursor
from search import search


class Crawler:
    def __init__(
        self,
        db_cur: Cursor,
        keywords: list[str],
        black_subdomains: list[str] = [],
        black_urls: list[str] = [],
    ):
        self.db_cur = db_cur
        self.seen = set()
        self.keywords = keywords
        self.black_subdomains = set(black_subdomains)
        self.black_urls = set(black_urls)

    def crawl(self, root: str, bounded=True, depth=0) -> dict[str, set[str]]:
        next_urls = Queue()
        next_urls.put((root, 0))

        counter = 1
        while not next_urls.empty():
            url, layer = next_urls.get()
            print(f"{counter} {layer} {url}")
            counter += 1

            try:
                res = requests.get(url, timeout=(3, 10))
            except TimeoutError:
                print("Timed out")

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                text = re.sub(r"\s+", " ", soup.text.strip())
                terms = search(text, self.keywords)
                db_add_page(self.db_cur, url, terms, terms.total, text)

                if not bounded or layer < depth:
                    new_links = [
                        a["href"] for a in soup.find_all("a") if a.has_attr("href")
                    ]

                    for link in new_links:
                        if link.startswith("https://") or link.startswith("/"):
                            if not link.endswith("/"):
                                link += "/"

                            if link.startswith("/"):
                                domain = get_domain(url)
                                link = "https://" + domain + link

                                if link not in self.seen:
                                    self.seen.add(link)
                                    next_urls.put((link, layer + 1))
                            elif not self.skip_url(link, url):
                                self.seen.add(link)
                                next_urls.put((link, layer + 1))

    def search_page(self, page_txt: str) -> set[str]:
        words = set(page_txt.split())
        return set.intersection(self.keywords, words)

    def skip_url(self, link: str, url: str) -> bool:
        domain, _ = get_domain_subdomain(url)
        link_domain, link_subdomain = get_domain_subdomain(link)
        return (
            strip_query(link) == strip_query(url)  # Some pages have recursive links
            or link_domain != domain
            or link_subdomain in self.black_subdomains
            or link in self.seen
            or link in self.black_urls
        )
