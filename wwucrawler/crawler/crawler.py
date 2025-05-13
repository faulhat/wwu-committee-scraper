"""
Tom's wwu.edu crawler program
Can be used to search the domain to an arbitrary (or unlimited) depth for an arbitrary number of keywords
"""

import requests, sys, queue, time
from bs4 import BeautifulSoup
from queue import Queue
from urls import *
from pages_db import PagesDB
from search import search
from multiprocessing import Process, JoinableQueue, Manager, Event, Value, Lock


def print_reprint_count(msg, lock, total, f=sys.stderr):
    with lock:
        print(f"\33[2K\r{msg}\nTotal scanned: {total.value}", file=f, end="\r")


class Crawler:
    def __init__(
        self,
        db_path,
        root,
        keywords,
        bounded=True,
        max_depth=0,
        black_subdomains=[],
        black_urls=[],
        n_workers=6,
    ):
        self.db_path = db_path
        self.root = root
        self.keywords = keywords
        self.bounded = bounded
        self.max_depth = max_depth
        self.black_subdomains = set(black_subdomains)
        self.black_urls = set(black_urls)
        self.n_workers = n_workers

    def start(self):
        start = time.time()
        with Manager() as manager:
            seen_lock = Lock()
            seen = manager.dict()
            seen[self.root] = 1

            print_lock = Lock()
            url_queue = JoinableQueue()
            url_queue.put((self.root, 0))
            total_scanned = Value("i", 0)

            workers = [
                Process(
                    target=self.crawl,
                    args=(
                        i,
                        seen_lock,
                        seen,
                        print_lock,
                        url_queue,
                        total_scanned,
                    ),
                )
                for i in range(self.n_workers)
            ]

            for worker in workers:
                worker.start()

            url_queue.join()
            for worker in workers:
                url_queue.put(None) # Shutdown signal

            for worker in workers:
                worker.join()
            
            elapsed = time.time() - start
            with PagesDB(self.db_path) as db:
                total = db.count_pages()
                print(f"Total scanned: {total}")
                print(f"Time elapsed (total):   {elapsed:.2f}s")
                print(f"             (per url): {elapsed/total:.2f}s")


    def crawl(
        self,
        my_id,
        seen_lock,
        seen,
        print_lock,
        url_queue,
        total_scanned,
    ):
        with PagesDB(self.db_path) as db:
            db.setup()
            while (next_url := url_queue.get()) is not None:
                url, layer = next_url
                print_reprint_count(f"[{my_id}] ({layer}) {url}", print_lock, total_scanned)

                try:
                    res = requests.get(url, timeout=(3, 10))
                except TimeoutError:
                    print_reprint_count("Timed out", print_lock, total_scanned)
                except requests.exceptions.RequestException as e:
                    print_reprint_count(f"Couldn't retrieve page: {e.__str__()}", print_lock, total_scanned)

                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    title = soup.title.string if soup.title else None

                    text = re.sub(r"\s+", " ", soup.text.strip())
                    terms = search(text, self.keywords)
                    db.add_page(url, title, terms, terms.total, text)
                    total_scanned.value = db.count_pages()
                    
                    if not self.bounded or layer < self.max_depth:
                        new_links = [
                            a["href"] for a in soup.find_all("a") if a.has_attr("href")
                        ]

                        for link in new_links:
                            if link.startswith("https://") or link.startswith("/"):
                                if not link.endswith("/"):
                                    link += "/"

                                skip = False
                                if link.startswith("/"):
                                    domain = get_domain(url)
                                    link = "https://" + domain + link
                                    skip = (
                                        strip_query(link) == strip_query(url)
                                        or link in self.black_urls
                                    )
                                else:
                                    domain, _ = get_domain_subdomain(url)
                                    link_domain, link_subdomain = get_domain_subdomain(
                                        link
                                    )
                                    skip = (
                                        strip_query(link) == strip_query(url)
                                        or link_domain != domain
                                        or link_subdomain in self.black_subdomains
                                        or link in self.black_urls
                                    )

                                if not skip:
                                    with seen_lock:
                                        if link not in seen:
                                            seen[link] = 1
                                            url_queue.put((link, layer + 1))
                
                url_queue.task_done()
            
            url_queue.task_done()
            print_reprint_count(f"[{my_id}] done!", print_lock, total_scanned)

    def search_page(self, page_txt):
        words = set(page_txt.split())
        return set.intersection(self.keywords, words)
