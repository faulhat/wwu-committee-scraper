"""
Tom's wwu.edu crawler program
Can be used to search the domain to an arbitrary (or unlimited) depth for an arbitrary number of keywords
"""

import sys
from traceback import print_exc

from crawler import Crawler
from pages_db import PagesDB
from fingerprints import *
from argparse import ArgumentParser, REMAINDER


# The canonical set of committee pages
#  Candidate pages are boosted based on similarity to these.
CANON_URLS = [
    "https://as.wwu.edu/committees/as-finance-council/",
    "https://as.wwu.edu/committees/as-student-trustee-selection-committee/",
    "https://wce.wwu.edu/edc",
    "https://gradschool.wwu.edu/graduate-faculty-governance-council",
    "https://as.wwu.edu/committees/as-student-advisory-committee/",
    "https://as.wwu.edu/committees/sehome-hill-arboretum-board-of-governors/",
]

# Subdomains for the crawler to ignore
#  They have a lot of pages, none of which are relevant.
BLACK_SUBDOMAINS = ["cedar", "catalog"]


def parse_args():
    parser = ArgumentParser(prog="crawler")
    parser.add_argument("-o", "--ofile", nargs="?", help="output file")
    parser.add_argument("-d", "--depth", default=4, type=int, help="max search depth")
    parser.add_argument(
        "-w", "--workers", default=6, type=int, help="number of worker threads"
    )
    parser.add_argument(
        "-u", "--unbounded", action="store_true", help="disable max search depth"
    )
    parser.add_argument(
        "-t", "--target", nargs="?", default="../pages.db", help="target database file"
    )
    parser.add_argument("-i", "--ifile", help="keyword file")
    return parser.parse_args()


# Retrieve tiered keyword file
# Format: keywords are listed from highest to lowest priority
#  Priority tiers are separated by lines containing only '#'
# The first tier of keywords.txt contains the keywords supplied by our client.
def parse_keyword_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        keywords = [[]]
        for line in lines:
            if line == "#":
                keywords.append([])
            elif line != "":
                keywords[-1].append(line)

        return keywords


if __name__ == "__main__":
    args = parse_args()
    ofile = sys.stdout
    if args.ofile is not None:
        try:
            ofile = open(args.ofile, "w")
        except:
            print("Could not open output file. Defaulting to stdout.")

    keywords = parse_keyword_file(args.ifile)
    print(f"Searching WWU domain for keywords from file {args.ifile}")
    print(f"All keywords: {keywords}")
    print(f"Max depth: {'INF' if args.unbounded else args.depth}")

    print("Retrievng canonical URLs for comparison...")
    canon_texts = texts_from_urls(CANON_URLS)
    canon_fps, canon_w2p = gen_canonical_fingerprints(canon_texts)

    try:
        crawler = Crawler(
            args.target,
            "https://wwu.edu/",
            keywords,
            max_depth=args.depth,
            n_workers=args.workers,
            black_subdomains=BLACK_SUBDOMAINS,
            canon_fps=canon_fps,
            canon_w2p=canon_w2p,
        )
        crawler.start()

        with PagesDB(args.target) as db:
            db.dump_results(f=ofile)
    except:
        print_exc()
    finally:
        if ofile != sys.stdout:
            ofile.close()
