import sys
from traceback import print_exc
from argparse import ArgumentParser, REMAINDER

from crawler import Crawler
from pages_db import PagesDB


parser = ArgumentParser(prog="crawler")
parser.add_argument("-o", "--ofile", nargs="?", help="output file")
parser.add_argument("-d", "--depth", default=4, type=int, help="max search depth")
parser.add_argument("-w", "--workers", default=6, type=int, help="number of worker threads")
parser.add_argument(
    "-u", "--unbounded", action="store_true", help="disable max search depth"
)
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

DB_PATH = "../pages.db"
try:
    crawler = Crawler(
        DB_PATH,
        "https://wwu.edu/",
        set(args.keywords),
        max_depth=args.depth,
        n_workers=args.workers,
        black_subdomains=["cedar", "catalog"],
    )
    crawler.start()

    with PagesDB(DB_PATH) as db:
        db.dump_results(f=ofile)
except:
    print_exc()
finally:
    if ofile != sys.stdout:
        ofile.close()
