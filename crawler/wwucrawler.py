#!/usr/bin/env python3

"""
Tom's wwu.edu crawler program
Can be used to search the domain to an arbitrary (or unlimited) depth for an arbitrary number of keywords
"""

import re
import requests
from bs4 import BeautifulSoup
import sys
from argparse import ArgumentParser, REMAINDER
from queue import Queue


def perr(s: str):
    print(s, file=sys.stderr)


def get_domain(url: str) -> str:
    return re.split(r"/", url, 3)[2]


def get_domain_subdomain(url: str) -> tuple[str, str]:
    full_domain = get_domain(url)
    segmented = full_domain.split(".")
    domain = ".".join(segmented[len(segmented) - 2 :])
    subdomain = segmented[len(segmented) - 3] if len(segmented) > 2 else None
    return domain, subdomain


def strip_query(url: str) -> str:
    return url.split("?")[0]


class Crawler:
    def __init__(
        self,
        keywords: list[str],
        black_subdomains: list[str] = [],
        black_urls: list[str] = [],
    ):
        self.seen = set()
        self.keywords = set(keywords)
        self.black_subdomains = set(black_subdomains)
        self.black_urls = set(black_urls)

    def crawl(self, root: str, bounded=True, depth=0) -> dict[str, set[str]]:
        found_urls = {}
        next_urls = Queue()
        next_urls.put((root, 0))

        counter = 1
        while not next_urls.empty():
            url, layer = next_urls.get()
            print(f"{counter} {layer} {url}")
            counter += 1

            try:
                res = requests.get(url, timeout=(3, 10))
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    res = self.search_page(soup.text)
                    if res:
                        found_urls[url] = res

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
                                elif self.skip_url(link, url):
                                    print(f"Skipping {link}")
                                else:
                                    self.seen.add(link)
                                    next_urls.put((link, layer + 1))

            except Exception as e:
                perr(e.__str__())

        return found_urls

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


if __name__ == "__main__":
    parser = ArgumentParser(prog="Web Crawler")
    parser.add_argument("-o", "--ofile", nargs="?", help="output file")
    parser.add_argument("-d", "--depth", default=4, type=int, help="max search depth")
    parser.add_argument("-u", "--unbounded", action="store_true", help="disable max search depth")
    parser.add_argument("keywords", nargs=REMAINDER, help="words to search for")
    args = parser.parse_args()

    ofile = sys.stdout
    if args.ofile is not None:
        try:
            ofile = open(args.ofile, "w")
        except:
            print("Could not open output file. Defaulting to stdout.")

    print(f"Searching WWU domain for keywords: {args.keywords}")
    print(f"Max depth: {'INF' if args.unbounded else args.depth}")

    crawler = Crawler(set(args.keywords), black_subdomains=["cedar", "catalog"])
    urls = crawler.crawl(
        "https://wwu.edu/", bounded=(not args.unbounded), depth=args.depth
    )

    print("URL\tKEYS", file=ofile)
    for url, keys in urls.items():
        print(f"{url}\t{','.join(keys)}", file=ofile)

    if ofile != sys.stdout:
        ofile.close()
